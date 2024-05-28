from django.urls import path
from .views import *



urlpatterns = [
    path('get-auth-url',AuthenticationURL.as_view()),
    path('redirect',spotify_callback),
    path('is-authenticated',UserIsAuthenticated.as_view()),
    path('current-song',CurrentSong.as_view())
]