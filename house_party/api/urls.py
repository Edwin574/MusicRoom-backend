from django.urls import path

from .views import RoomView,CreateRoomView,GetRoom,JoinRoom

urlpatterns = [
    path('rooms',RoomView.as_view()),
    path('createroom',CreateRoomView.as_view()),
    path('get-room',GetRoom.as_view()),
    path('join-room',JoinRoom.as_view())
]
