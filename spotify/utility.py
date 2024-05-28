from .models import SpotifyTokens
from django.utils import timezone
from datetime import timedelta
from requests import post,put,get
from .credentials import *


BASE_URL="https://api.spotify.com/v1/me/"
def  get_user_tokens(session_key):
    user_tokens=SpotifyTokens.objects.filter(user=session_key)
    
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None
    
    
def update_or_create_tokens(session_key,access_token, refresh_token,token_type,expires_in):
    tokens=get_user_tokens(session_key)
    expires_in=timezone.now() +timedelta(seconds=expires_in)
    
    if tokens:
        tokens.access_token=access_token
        tokens.refresh_token=refresh_token
        tokens.token_type=token_type
        tokens.expires_in=expires_in
        tokens.save(update_fields=[
            'access_token','expires_in','refresh_token','token_type'
        ])
    else:
        tokens=SpotifyTokens(user=session_key,access_token=access_token,expires_in=expires_in,token_type=token_type)
        tokens.save()
        
def is_user_authenticated(session_key):
    tokens=get_user_tokens(session_key)
    if tokens:
        expiry=tokens.expires_in
        if expiry<=timezone.now():
            refresh_spotify_token(session_key)
        return True
    return False

def refresh_spotify_token(session_key):
    refresh_token=get_user_tokens(session_key).refresh_token
    response=post("https://accounts.spotify.com/api/token",data={
        'grant-type':'refresh_token',
        'refresh_token':refresh_token,
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET
    
    }).json()
    
    access_token=response.get('access_token')
    token_type=response.get('token_type')
    expires_in=response.get('expires_in')
    
    
    update_or_create_tokens(session_key,access_token,token_type,expires_in,refresh_token)
    
 
def handle_api_request(session_key,endpoint,post_=False,put_=False):
     tokens=get_user_tokens(session_key=session_key)
     headers={
         'Content-Type':'application/json',
         'Authorization':'Bearer ' + tokens.access_token
     }
     if post_:
         post(BASE_URL + endpoint,headers=headers)
     if put:
         put(BASE_URL + endpoint,headers=headers)
         
     response=get(BASE_URL + endpoint,{},headers=headers)
     try:
         return response.json()
     except:
         return{"Error":"Error occured while making request"}
    
def play_song(session_key):
    
    return handle_api_request(session_key=session_key,endpoint="player/play",put_=True)
    


def pause_song(session_key):
        return handle_api_request(session_key=session_key,endpoint="player/pause",put_=True)

         
         
        
    
    