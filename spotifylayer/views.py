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
from .parsers import parse_user, parse_user_playlists, parse_playlist_items, parse_playlist
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
        liked_songs_json = sp.current_user_saved_tracks(limit=50)
        tracks = parse_playlist_items(liked_songs_json)
        total = liked_songs_json["total"]

        offset = 50
        while offset-50 < total:
            liked_songs_json = sp.current_user_saved_tracks(limit=50, offset=offset)
            tracks.extend(parse_playlist_items(liked_songs_json))
            offset += 50

        return render(request, "spotifylayer/playlist.html", {"tracks": tracks})

    except spotipy.SpotifyException as e:
        if e.http_status == 401:
            return redirect("spotify_login")
        print(f"Error: {e}")
        return HttpResponse("Error fetching liked songs.")


def playlist(request, spotify_id):
    sp = get_spotify_client(request.user)
    playlist_id = spotify_id #sp.playlist(request.GET.get('spotify_id', ''))
    if playlist_id:
        items_json = sp.playlist_items(playlist_id)
        tracks = parse_playlist_items(items_json)
        playlist_json = sp.playlist(playlist_id)
        playlist_obj = parse_playlist(playlist_json)
        # TODO: create a playlist object for liked songs and pass to playlist view
        return render(request, "spotifylayer/playlist.html", {"playlist": playlist_obj,
                                                              "tracks": tracks})


    else:
        return HttpResponse("Playlist does not exist")


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
    code = request.GET.get("code")  # parse the code from url

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

