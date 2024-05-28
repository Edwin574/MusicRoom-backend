from django.shortcuts import render,redirect
from api.models import Room


from .credentials import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI

from rest_framework.views import APIView 
# from rest_famework.requests import Request,post
# from rest_framework.request import Request,post
from requests import Request,post
from rest_framework import status
from rest_framework.response import Response
from .utility import *


class AuthenticationURL(APIView):
    
    def get(self, request,format=None):
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
    
    if not request.session.exists(request.session.session_key):
        request.session.create()
    
    update_or_create_tokens(session_key=request.session.session_key ,access_token=access_token,refresh_token=refresh_token,token_type=token_type,expires_in=expires_in)
    
    return redirect('https://open.spotify.com/') #the url you want to redirect to

class UserIsAuthenticated(APIView):
    def get(self,request,format=None):
        is_authenticated=is_user_authenticated(request.session.session_key)
        
        return Response({"status":is_authenticated},status=status.HTTP_200_OK)
        
class CurrentSong(APIView):
    def get(self,request,format=None):
        room_code=self.request.session.get('room_code')
        room=Room.objects.filter(room_code=room_code)
        if room.exists():
            room=room[0]
        else:
            return Response({},status=status.HTTP_404_NOT_FOUND)
        room_host=room.room_host
        endpoint="player/currently-playing"
        response=handle_api_request(session_key=room_host,endpoint=endpoint)
        
        if 'error' in response or 'item' not in response:
            return Response({},status=status.HTTP_204_NO_CONTENT)
        
        item=response.get('item')
        duration=item.get('duration_ms')
        progress=response.get('progress_ms')
        album_cover=item.get('album').get('images')[0].get('url')
        is_playing=response.get('is_playing')
        song_id=item.get('id')
        
        arstist_names_string=""
        
        for i,artist in enumerate(item.get('artists')):
            if i>0:
                arstist_names_string+=","
            name=artist.get('name')
            arstist_names_string += name
        song={
            'title':item.get('name'),
            'artist':arstist_names_string,
            'duration':duration,
            'time':progress,
            'image_url':album_cover,
            'is_playing':is_playing,
            'votes':0,
            'id':song_id
        }
        
        return Response(song,status=status.HTTP_200_OK)
    
class PauseSong(APIView):
    def put(self,response,format=None):
        room_code=self.request.session.get('room_code')
        room=Room.objects.filter(room_code=room_code)[0]
        if self.request.session_key==room.room_host or room.guest_can_pause:
            pause_song(room.room_host)
            return Response({},status=status.HTTP_204_NO_CONTENT)
        return Response({},status=status.HTTP_403_FORBIDDEN)
class PlaySong(APIView):
    def put(self,response,format=None):
        room_code=self.request.session.get('room_code')
        room=Room.objects.filter(room_code=room_code)[0]
        if self.request.session_key==room.room_host or room.guest_can_pause:
            play_song(room.room_host)
            return Response({},status=status.HTTP_204_NO_CONTENT)
        return Response({},status=status.HTTP_403_FORBIDDEN)         
        
        


    