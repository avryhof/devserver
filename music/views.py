import os

from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from devserver.settings import MUSIC_FOLDER
from music.api_auth import AnonymousAuthentication
from music.constants import NO_CACHE_HEADERS, ID3_SEARCH_FIELDS, API_FAILURE, API_SUCCESS
from music.forms import SongSearchForm, AddToPlaylistForm, PlaylistForm
from music.models import Song, PlayList
from music.permissions import AnonymousPermission
from music.utils import cache_song


@api_view(["GET", "POST"])
@authentication_classes((AnonymousAuthentication,))
@permission_classes((AnonymousPermission,))
def find_song(request, **kwargs):
    """

    :param request:
    :return:
    """

    resp = []
    form = False

    if request.method == "POST":
        form = SongSearchForm(request.POST)
    elif request.method == "GET":
        form = SongSearchForm(request.GET)

    if form.is_valid():
        search_data = dict()
        for sk in list(form.cleaned_data.keys()):
            val = form.cleaned_data.get(sk)
            if sk == "search":
                key = sk

            elif sk == "track":
                key = sk
                val = int(val)

            else:
                key = "%s__icontains" % sk

            if form.cleaned_data.get(sk):
                search_data.update({key: val})

        songs = Song.objects.annotate(search=SearchVector(*ID3_SEARCH_FIELDS)).filter(**search_data)

        for song in songs:
            resp.append(song.dict())

    return Response(resp, status=status.HTTP_200_OK, headers=NO_CACHE_HEADERS)


def song_stream(request, *args, **kwargs):
    song_pk = kwargs.get("pk")

    if song_pk:
        try:
            song = Song.objects.get(pk=song_pk)

        except Song.DoesNotExist:
            response = HttpResponse(status=status.HTTP_404_NOT_FOUND)

        else:
            file_size = os.path.getsize(song.path)
            mp3 = open(song.path, "rb").read()

            response = HttpResponse(content=mp3, content_type="audio/mpeg")
            response["Content-Length"] = file_size
            response.streaming = True

    else:
        response = HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return response


def song_download(request, *args, **kwargs):
    song_pk = kwargs.get("pk")

    if song_pk:
        try:
            song = Song.objects.get(pk=song_pk)

        except Song.DoesNotExist:
            response = HttpResponse(status=status.HTTP_404_NOT_FOUND)

        else:
            file_size = os.path.getsize(song.path)
            mp3 = open(song.path, "rb").read()

            file_name = os.path.split(song.path)[-1]
            response = HttpResponse(content=mp3, content_type="audio/mpeg")
            response["Content-Length"] = file_size
            response["Content-Disposition"] = "attachment; filename=%s" % file_name

    else:
        response = HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return response


@api_view(["GET"])
@authentication_classes((AnonymousAuthentication,))
@permission_classes((AnonymousPermission,))
def get_playlists(request):
    if request.user.is_authenticated():
        playlists = PlayList.objects.filter(user=request.user)
        resp = dict()

        for playlist in playlists:
            resp.update({str(playlist.pk): {
                "title": playlist.title,
                "count": playlist.songs.count()
            }})

    else:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return Response(resp, status=status.HTTP_200_OK, headers=NO_CACHE_HEADERS)


def get_playlist(request, **kwargs):
    playlist_pk = kwargs.get("pk")

    m3u_data = []

    try:
        playlist = PlayList.objects.get(pk=playlist_pk)

    except PlayList.DoesNotExist:
        pass

    else:
        site = Site.objects.get_current(request)
        request_proto = "https" if request.is_secure() else "http"
        request_url = "'%s://%s" % (request_proto, site.domain)

        for song in playlist.songs:

            stream_url = "%s%s" % (request_url, reverse("song_stream", args=[song.pk]))
            m3u_data.append(stream_url)

    return "\n".join(m3u_data)


@api_view(["GET", "POST"])
@authentication_classes((AnonymousAuthentication,))
@permission_classes((AnonymousPermission,))
def add_playlist(request):
    form = PlaylistForm(request.POST)

    if form.is_valid():
        title = form.cleaned_data.get("title")
        try:
            existing_playlist = PlayList.objects.get(title=title)
        except PlayList.DoesNotExist:
            try:
                PlayList.objects.create(title=title, user=request.user)
            except Exception:
                resp = dict(result=API_FAILURE)
            else:
                resp = dict(result=API_SUCCESS)
        else:
            resp = dict(result=API_FAILURE)
    else:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return Response(resp, status=status.HTTP_200_OK, headers=NO_CACHE_HEADERS)


@api_view(["GET", "POST"])
@authentication_classes((AnonymousAuthentication,))
@permission_classes((AnonymousPermission,))
def add_song_to_playlist(request):
    form = AddToPlaylistForm(request.POST)

    resp_status = API_FAILURE

    if form.is_valid():
        resp_status = API_SUCCESS
        playlist = form.cleaned_data.get("playlist")
        song = form.cleaned_data.get("song")

        playlist.add_song(song.pk)

    resp = dict(result=resp_status)

    return Response(resp, status=status.HTTP_200_OK, headers=NO_CACHE_HEADERS)
