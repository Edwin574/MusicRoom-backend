from django.urls import path
from .views import AuthenticationURL,spotify_callback,UserIsAuthenticated



urlpatterns = [
    path('get-auth-url',AuthenticationURL.as_view()),
    path('redirect',spotify_callback),
    path('is-authenticated',UserIsAuthenticated.as_view())
]