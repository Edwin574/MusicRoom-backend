from django.shortcuts import render

# Create your views here.

from  .credentials import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI

from rest_framework.views import APIView 
from requests import Request,post
from rest_framework import status
from rest_framework.response import Response


class AuthenticationURL(APIView):
    
    def get(self,request,format=None):
        scopes="user-read-currently-playing user-modify-playback-state user-read-playback-state"
        
        url=Request('GET','https://accounts.spotify.com/authorize?',params={
            "scope":scopes,
            "response_type":"code",
            "redirect_uri":REDIRECT_URI,
            "client_id":CLIENT_ID       
        }).prepare().url
        
        return Response({'url':url},status=status.HTTP_200_OK)
    
    
def spotify_callback(request,format=None):
    code=request.GET.get('code')
    error=request.GET.get('error')
    
    if not code:
        return Response({'error':error},status=status.HTTP_400_BAD_REQUEST)
    else:
        token=post("https://accounts.spotify.com/api/token",data={
            "grant_type":"authorization_code",
            "code":code,
            "redirect_uri":REDIRECT_URI,
            "client_id":CLIENT_ID,
            "client_secret":CLIENT_SECRET
        }).json()
        
    access_token=token.get('access_token')
    token_type=token.get('token_type')
    refresh_token=token.get('refresh_token')
    expires_in=token.get('expires_in')
    error=token.get('error')