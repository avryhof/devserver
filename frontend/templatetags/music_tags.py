import os

from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe

from music.utils import get_song_path

register = template.Library()


@register.filter
def basename(value):
    return os.path.basename(value)


@register.simple_tag
def audio(song_id):
    song_url = reverse("song_stream", args=[song_id])
    html = '<audio controls preload="none"><source src="%s" type="audio/mpeg">Not supported.</audio>' % song_url

    return mark_safe(html)
