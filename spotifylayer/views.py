from django.http import HttpResponse
from django.shortcuts import render

from constants import *

import spotipy
from spotipy.oauth2 import SpotifyOAuth



def index(request):
    return HttpResponse("Hello, world. You're at the spotifylayer index.")

def likedsongs(request):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE))
    return HttpResponse("Liked songs will go here.")