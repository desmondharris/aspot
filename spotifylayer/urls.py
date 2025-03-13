from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.spotify_login, name="spotify_login"),
    path("callback/", views.spotify_callback, name="spotify_callback"),
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("likedsongs/", views.liked_songs, name="liked_songs"),
    path("playlist/<str:spotify_id>", views.playlist, name="playlist")
]