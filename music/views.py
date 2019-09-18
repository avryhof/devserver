import os
import re
import shutil

from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from music.api_auth import AnonymousAuthentication
from music.constants import NO_CACHE_HEADERS, ID3_SEARCH_FIELDS
from music.forms import SongSearchForm
from music.models import Song
from music.permissions import AnonymousPermission


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


def get_song(request, *args, **kwargs):
    song_pk = kwargs.get("pk")

    if song_pk:
        song = Song.objects.get(pk=song_pk)

        cache_path = os.path.join(settings.MEDIA_ROOT, "song_cache")
        cache_file = os.path.join(cache_path, os.path.basename(song.path))
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        if not os.path.exists(cache_file):
            shutil.copy(song.path, cache_file)

        mp3 = open(cache_file, "rb").read()

        response = HttpResponse(content=mp3, content_type="audio/mpeg")
        response.streaming = True
    else:
        response = HttpResponse(status=404)

    return response


def download_song(request, *args, **kwargs):
    song_pk = kwargs.get("pk")

    if song_pk:
        song = Song.objects.get(pk=song_pk)
        if song.artist and song.album:
            file_name = re.sub(r"[^A-Za-z0-9_\- ]", "", "%s.mp3" % str(song))
        else:
            file_name = re.sub(r"[^A-Za-z0-9_\- ]", "", os.path.split(song.path)[-1])

        cache_path = os.path.join(settings.MEDIA_ROOT, "song_cache")
        cache_file = os.path.join(cache_path, os.path.basename(song.path))
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        if not os.path.exists(cache_file):
            shutil.copy(song.path, cache_file)

        mp3 = open(cache_file, "rb").read()

        response = HttpResponse(content=mp3, content_type="audio/mpeg")
        response["Content-Disposition"] = "attachment; filename=%s" % file_name
    else:
        response = HttpResponse(status=404)

    return response
