from os import getenv

from django.http import HttpResponse
from django.shortcuts import render

from constants import *

from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth
from django.contrib.auth.decorators import login_required
import spotipy
from .spotify_helper import get_spotify_auth, update_or_create_token, get_spotify_client

from dotenv import load_dotenv



def index(request):
    return HttpResponse("Hello, world. You're at the spotifylayer index.")

@login_required
def likedsongs(request):
    sp = get_spotify_client(request.user)
    if not sp:
        return redirect("spotify_login")

    results = sp.current_user_saved_tracks(offset=0, limit=50)
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])
    return HttpResponse("Liked songs will go here.")


@login_required
def spotify_login(request):
    auth_manager = get_spotify_auth()
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)


@login_required
def spotify_callback(request):
    auth_manager = get_spotify_auth()
    code = request.GET.get("code")

    if code:
        token_info = auth_manager.get_access_token(code)
        update_or_create_token(request.user,
                               token_info["access_token"],
                               token_info["refresh_token"],
                               token_info["token_type"],
                               token_info["expires_in"])

    return redirect("likedsongs")

