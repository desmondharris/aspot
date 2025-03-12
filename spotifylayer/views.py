from os import getenv

import spotipy
from django.http import HttpResponse
from django.shortcuts import render

from constants import *

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .spotify_helper import get_spotify_auth, update_or_create_token, get_spotify_client
from .helper_types import TrimmedTrack
from .parsers import parse_user, parse_user_playlists
import logging

logger = logging.getLogger(__name__)

@login_required
def index(request):
    sp = get_spotify_client(request.user)
    if not sp:
        return redirect("spotify_login")

    playlists = []
    for n in range(3):
        playlists.extend(parse_user_playlists(sp.current_user_playlists(limit=50, offset=n*50)))
    return render(request, "spotifylayer/index.html", context={"playlists": playlists})


@login_required
def liked_songs(request):
    sp = get_spotify_client(request.user)
    if not sp:
        return redirect("spotify_login")
    try:
        results = sp.current_user_saved_tracks(offset=0, limit=50)
        trimmed_tracks = []
        for idx, item in enumerate(results['items']):
            track = item['track']
            track['album'].pop('available_markets')
            trimmed_track = TrimmedTrack(
                name=track['name'],
                artists=[artist['name'] for artist in track['artists']],
                album=track['album']['name'],
                release_date=track['album']['release_date'],
            )
            trimmed_tracks.append(trimmed_track)
        return render(request, "spotifylayer/likedsongs.html", {"liked_songs": trimmed_tracks})

    except spotipy.SpotifyException as e:
        if e.http_status == 401:
            return redirect("spotify_login")
        print(f"Error: {e}")
        return HttpResponse("Error fetching liked songs.")


@login_required
def spotify_login(request):
    """
    Redirects the user to the Spotify authentication page.
    """
    auth_manager = get_spotify_auth()
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)


@login_required
def spotify_callback(request):
    """
    Callback view for Spotify authentication. Spotify redirects here with an auth code as a parameter.
    This view exchanges the code for an access token and refresh token, and stores them in the database.
    :param request:
    :return:
    """
    auth_manager = get_spotify_auth()
    code = request.GET.get("code") # parse the code from url

    if code:
        token_info = auth_manager.get_access_token(code)
        update_or_create_token(request.user,
                               token_info["access_token"],
                               token_info["refresh_token"],
                               token_info["token_type"],
                               token_info["expires_in"])

        sp = get_spotify_client(request.user)
        spotify_user, created = SpotifyUser.objects.update_or_create(user=request.user,
                                                                     defaults=parse_user(sp.current_user()))
        if created:
            logger.info(f"New SpotifyUser created: {spotify_user} for user {request.user}")
        else:
            logger.debug(f"{request.user} logged in.")

    else:
        logger.error(f"Auth code note found in callback for user {request.user}")
        return HttpResponse("Server-side authentication error")



    return redirect("/")

