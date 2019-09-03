from django.conf import settings
from django.db import models
from django.db.models import DO_NOTHING
from django.db.models import Model, TextField, CharField, IntegerField, URLField

from music.constants import ID3_FIELDS


class AuthorizedAgent(models.Model):
    authorized = models.BooleanField(default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=None, blank=True, null=True, on_delete=DO_NOTHING)
    app_name = models.CharField(max_length=200, blank=True, null=True)
    app_key = models.TextField(blank=True, null=True)


class Song(Model):
    path = TextField()
    artist = CharField(max_length=255, blank=True, null=True)
    album = CharField(max_length=255, blank=True, null=True)
    song = CharField(max_length=255, blank=True, null=True)
    track = IntegerField(blank=True, null=True)
    comment = TextField(blank=True, null=True)
    year = CharField(max_length=255, blank=True, null=True)
    genre = CharField(max_length=255, blank=True, null=True)
    band = CharField(max_length=255, blank=True, null=True)
    composer = CharField(max_length=255, blank=True, null=True)
    copyright = CharField(max_length=255, blank=True, null=True)
    url = URLField(blank=True, null=True)
    publisher = TextField(blank=True, null=True)

    class Meta:
        db_table = "song"
        verbose_name = "Song"
        verbose_name_plural = "Songs"

    def __str__(self):
        if self.track:
            retn = "%s - %s - %s - %s" % (self.artist, self.album, self.track, self.song)

        elif self.album:
            retn = "%s - %s - %s" % (self.artist, self.album, self.song)

        elif self.artist:
            retn = "%s - %s" % (self.artist, self.song)

        elif self.song:
            retn = self.song

        else:
            retn = self.path

        return retn

    def dict(self):
        retn = dict(pk=self.pk)

        for sk in ID3_FIELDS:
            val = getattr(self, sk)
            if isinstance(val, str):
                val = val.strip()
            retn.update({sk: val})

        return retn
