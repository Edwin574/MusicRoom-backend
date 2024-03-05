from django.urls import path
from .views import AuthenticationURL



urlpatterns = [
    path('get-auth-url',AuthenticationURL.as_view())
]