from .models import SpotifyTokens
from django.utils import timezone
from datetime import timedelta
def  get_user_tokens(session_key):
    user_tokens=SpotifyTokens.objects.filter(user=session_key)
    
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None
    
    
def update_or_create_tokens(session_key,access_token, refresh_token,token_type,user_tokens,expires_in):
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