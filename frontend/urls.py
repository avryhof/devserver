from django.conf.urls import url

from frontend.views import HomeView
from music.views import find_song, song_stream, song_download

urlpatterns = [
    url("^$", HomeView.as_view(), name="home"),
]