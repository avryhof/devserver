import os
import re
import shutil

from django.conf import settings

from music.models import Song


def fn_slug(filename):
    return re.sub(r"[^A-Za-z0-9_\- ]", "", filename)


def get_song_filename(song):
    if song.artist and song.album:
        file_name = fn_slug("%s.mp3" % str(song))
    else:
        file_name = fn_slug(os.path.split(song.path)[-1])

    return file_name


def cache_song(song_pk):
    was_cached = True

    try:
        song = Song.objects.get(pk=song_pk)

    except Song.DoesNotExist:
        was_cached = False

    else:
        file_name = get_song_filename(song)

        if file_name:
            cache_path = getattr(settings, "SONG_CACHE_PATH")
            cache_file = os.path.join(cache_path, file_name)
            if not os.path.exists(cache_path):
                os.makedirs(cache_path)

            if not os.path.exists(cache_file) or not os.path.getsize(song.path) == os.path.getsize(cache_file):
                shutil.copy(song.path, cache_file)

    return was_cached
