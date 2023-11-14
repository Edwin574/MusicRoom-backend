from .models import Room
from .serializers import RoomSerializer,CreateRoomSerializer
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class RoomView(generics.ListAPIView):
    queryset=Room.objects.all()
    serializer_class=RoomSerializer

class CreateRoomView(APIView):

    serializer_class=CreateRoomSerializer

    def post(self,request,format=None):

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid():
            guest_can_pause=serializer.data.get('guest_can_pause')
            votes_to_skip=serializer.data.get('votes_to_skip')
            host_session_id=self.request.session.session_key 
            queryset=Room.objects.filter(room_host=host_session_id)
            if queryset.exists():
                room=queryset[0]
                room.guest_can_pause=guest_can_pause
                room.votes_to_skip=votes_to_skip
                room.save(update_fields=['guest_can_pause','votes_to_skip','created_at'])
                self.request.session['room_code']=room.room_code
                return Response(RoomSerializer(room).data,status=status.HTTP_200_OK)
            else:
                room=Room(room_host=host_session_id,guest_can_pause=guest_can_pause,votes_to_skip=votes_to_skip)
                room.save()
                self.request.session['room_code']=room.room_code

                return Response(RoomSerializer(room).data,status=status.HTTP_201_CREATED)
        return Response({'Bad request':'Invalid data...'},status=status.HTTP_400_BAD_REQUEST)
    
class GetRoom(APIView):
    serializer_class=RoomSerializer
    lookup_url_kwarg='code'

    def get(self,request,format=None):

        code=request.GET.get(self.lookup_url_kwarg)
        if code!=None:
            room=Room.objects.filter(room_code=code)
            if len(room)>0:
                data=self.serializer_class(room[0]).data
                data['is_host']=self.request.session.session_key==room[0].room_host
                return Response(data,status=status.HTTP_200_OK)
            return Response({'Room Not Found':'Invalid Room Code'},status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request':'Code parameter not found in request'},status=status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):
    join_code='code'
    def post(self,request,format=None):
        if not self.request.session.exist(self.request.sessions.session_key):
            self.request.session.create()
        
        code=request.data.get(self.join_code)
        if code!=None:
            room_result=Room.objects.filter(room_code=code)
            if len(room_result)>0:
                room=room_result[0]
                self.request.session['room_code']=code
                return Response({'message':'Rooom Joined Successfully'},status=status.HTTP_200_OK)
            Response({'Bad Request':'Invalid Room code'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request':'Invalid post data, did not find the room code'},status=status.HTTP_400_BAD_REQUEST)