from django.conf.urls import url

from music.views import find_song, get_song, download_song

urlpatterns = [
    url(r"^search/$", find_song, name="find_song"),
    url(r"^song/(?P<pk>\d+)/$", download_song, name="song"),
    url(r"^song/(?P<pk>\d+)/stream$", get_song, name="stream_song"),
    url(r"^song/(?P<pk>\d+)/download/$", download_song, name="download_song"),
]
