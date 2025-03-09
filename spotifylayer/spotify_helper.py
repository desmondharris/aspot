import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.utils.timezone import now, timedelta
from .models import SpotifyToken
from django.conf import settings
from os import getenv
from dotenv import load_dotenv
load_dotenv()

SPOTIPY_CLIENT_ID = getenv('CLIENT_ID')
SPOTIPY_CLIENT_SECRET = getenv('CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = getenv('REDIRECT_URI')

SCOPES = "user-read-playback-state user-modify-playback-state playlist-modify-private playlist-modify-public"


def get_spotify_auth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPES
    )


def get_user_token(user):
    try:
        return SpotifyToken.objects.get(user=user)
    except SpotifyToken.DoesNotExist:
        return None


def update_or_create_token(user, access_token, refresh_token, token_type, expires_in):
    expires_at = now() + timedelta(seconds=expires_in)
    token, created = SpotifyToken.objects.update_or_create(
        user=user,
        defaults={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": token_type,
            "expires_in": expires_at,
        },
    )
    return token


def is_token_expired(token):
    return now() >= token.expires_in


def get_spotify_client(user):
    token = get_user_token(user)

    if not token:
        return None

    if is_token_expired(token):
        auth_manager = get_spotify_auth()
        new_token_info = auth_manager.refresh_access_token(token.refresh_token)
        update_or_create_token(user,
                               new_token_info["access_token"],
                               token.refresh_token,
                               new_token_info["token_type"],
                               new_token_info["expires_in"])
        token = get_user_token(user)  # Retrieve updated token

    return spotipy.Spotify(auth=token.access_token)
