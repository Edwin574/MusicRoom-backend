# from rest_framework import serializers
from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    """
    handles outgoing response by representing the data in a better format.
    """

    class Meta:
        model = Room
        fields = '__all__'


class CreateRoomSerializer(serializers.ModelSerializer):
    """
    -handles incoming request and makes sure the posted payload is the same as what we expect
    """

    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')


class UpdateRoomSerializer(serializers.ModelSerializer):
    """
    -handles incoming request and makes sure the posted payload is the same as what we expect
    """
    # code = serializers.CharField(validtors=[])

    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip', 'room_code')
