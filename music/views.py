import os

from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from music.api_auth import AnonymousAuthentication
from music.constants import NO_CACHE_HEADERS, ID3_SEARCH_FIELDS, API_FAILURE, API_SUCCESS
from music.forms import SongSearchForm, AddToPlaylistForm
from music.models import Song
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
        cache_file = cache_song(song_pk)

        if cache_file:
            # file_size = os.path.getsize(cache_file)
            mp3 = open(cache_file, "rb").read()

            response = HttpResponse(content=mp3, content_type="audio/mpeg")
            response["Content-Length"] = len(mp3)
            # response["Content-Length"] = file_size
            response.streaming = True
        else:
            response = HttpResponse(status=status.HTTP_404_NOT_FOUND)

    else:
        response = HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return response


def song_download(request, *args, **kwargs):
    song_pk = kwargs.get("pk")

    if song_pk:
        cache_file = cache_song(song_pk)

        if cache_file:
            # file_size = os.path.getsize(cache_file)
            mp3 = open(cache_file, "rb").read()

            file_name = os.path.split(cache_file)[-1]
            response = HttpResponse(content=mp3, content_type="audio/mpeg")
            # response["Content-Length"] = file_size
            response["Content-Disposition"] = "attachment; filename=%s" % file_name
        else:
            response = HttpResponse(status=status.HTTP_404_NOT_FOUND)
    else:
        response = HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return response


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
