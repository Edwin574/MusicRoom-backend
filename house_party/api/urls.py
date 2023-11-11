from django.urls import path

from .views import RoomView

urlpatterns = [
    path('rooms',RoomView.as_view()),
]
