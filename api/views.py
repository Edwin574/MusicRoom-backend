from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse


# Create your views here.

class RoomView(generics.ListAPIView):
    '''
    View all available rooms
    '''
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    '''
    Create a room if none exists and update room details if it exists.
    '''
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host_session_id = self.request.session.session_key
            queryset = Room.objects.filter(room_host=host_session_id)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip', 'created_at'])
                self.request.session['room_code'] = room.room_code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(room_host=host_session_id, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
                self.request.session['room_code'] = room.room_code

                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response({'Bad request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class GetRoom(APIView):
    '''
    Getting details of a specific room by submitting the room code
    '''
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):

        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(room_code=code)
            if len(room) > 0:
                data = self.serializer_class(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].room_host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not Found': 'Invalid Room Code'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)


class JoinRoom(APIView):
    '''
    :Functionality for joining room by submitting the given room code.
    '''
    join_code = 'code'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.join_code)
        if code != None:
            room_result = Room.objects.filter(room_code=code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session['room_code'] = code
                return Response({'message': 'Rooom Joined Successfully'}, status=status.HTTP_200_OK)
            Response({'Bad Request': 'Invalid Room code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request': 'Invalid post data, did not find the room code'},
                        status=status.HTTP_400_BAD_REQUEST)


class UserInRoom(APIView):
    '''
    :Check if a user exists in a room
    '''

    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get('room_code')
        }

        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    '''
    :Leave a particular room and if the user is the host of the room we delete
    the room from the database.
    '''

    def post(self, request, format=None):
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(room_host=host_id)
            if len(room_results) > 0:
                room = room_results[0]
                room.delete()
        return Response({'Message': 'Success'}, status=status.HTTP_200_OK)


class UpdateRoom(APIView):
    '''
    :Updating details of a specific room.
    
    '''
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')

            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({'msg': 'Room not found'}, status=status.HTTP_400_BAD_REQUEST)
            room = queryset[0]
            user_id = self.request.session.session_key
            if room.room_host != user_id:
                return Response({'msg': 'You are not the host of this room'}, status=status.HTTP_403_FORBIDDEN)

            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['votes_to_skip', 'guest_can_pause'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
  