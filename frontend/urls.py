from django.conf.urls import url

from frontend.views import HomeView
from music.views import find_song, get_song, download_song

urlpatterns = [
    url("^$", HomeView.as_view(), name="home"),
]