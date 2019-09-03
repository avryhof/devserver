# -*- coding: utf-8 -*-
from django.contrib import admin
from mp3_tagger import MP3File, VERSION_2, VERSION_1

from music.constants import ID3_FIELDS, ID3_SEARCH_FIELDS
from .models import AuthorizedAgent, Song


@admin.register(AuthorizedAgent)
class AuthorizedAgentAdmin(admin.ModelAdmin):
    list_display = ("app_name", "user", "authorized")
    list_filter = ("authorized", "user")


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("artist", "album", "track", "song")
    list_display_links = ("artist", "album", "track", "song")
    list_filter = ("artist", "album")
    search_fields = tuple(ID3_SEARCH_FIELDS)

    def save_model(self, request, obj, form, change):
        super(SongAdmin, self).save_model(request, obj, form, change)

        mp3 = MP3File(obj.path)

        for tag_version in [VERSION_2, VERSION_1]:
            mp3.set_version(tag_version)

            for id3_key in ID3_FIELDS:
                if id3_key != "genre":
                    field_val = getattr(obj, id3_key)
                    if field_val:
                        setattr(mp3, id3_key, str(field_val))

            mp3.save()
