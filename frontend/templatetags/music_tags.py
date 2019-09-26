import os

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def basename(value):
    return os.path.basename(value)


@register.simple_tag
def audio(song_id):
    song_url = reverse("stream_song", args=[song_id])
    html = '<audio controls preload="none"><source src="%s" type="audio/mpeg">Not supported.</audio>' % song_url

    return mark_safe(html)
