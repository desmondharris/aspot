from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("likedsongs/", views.liked_songs, name="liked_songs"),
    path("login/", views.spotify_login, name="spotify_login"),
    path("callback/", views.spotify_callback, name="spotify_callback"),
]