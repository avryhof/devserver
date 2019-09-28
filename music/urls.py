from django.urls import path, re_path

from music.views import find_song, song_stream, song_download, add_song_to_playlist

urlpatterns = [
    path("^search/", find_song, name="find_song"),
    re_path(r"^song/(?P<pk>\d+)/$", song_download, name="song"),
    re_path(r"^song/(?P<pk>\d+)/stream$", song_stream, name="song_stream"),
    re_path(r"^song/(?P<pk>\d+)/download/$", song_download, name="song_download"),
    path("playlist/add/", add_song_to_playlist, name="playlist_add")
]
