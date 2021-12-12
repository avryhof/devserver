from django.urls import path

from music.views import find_song, song_stream, song_download, add_song_to_playlist, get_playlists, get_playlist

urlpatterns = [
    path("search/", find_song, name="find_song"),
    path("song/<str:pk>/", song_download, name="song"),
    path("song/<str:pk>/stream/", song_stream, name="song_stream"),
    path("song/<str:pk>/download/", song_download, name="song_download"),
    path("playlists/", get_playlists, name="playlists"),
    path("playlist/<str:pk>/", get_playlist, name="playlist"),
    path("playlist/add/", add_song_to_playlist, name="playlist_add"),
]
