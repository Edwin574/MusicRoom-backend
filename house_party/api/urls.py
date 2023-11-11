from django.urls import path

from .views import RoomView,CreateRoomView

urlpatterns = [
    path('rooms',RoomView.as_view()),
    path('createroom',CreateRoomView.as_view())
]
