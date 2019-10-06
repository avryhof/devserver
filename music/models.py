from django.contrib.auth import get_user_model
from django.db.models import DO_NOTHING, ForeignKey, ManyToManyField, DateTimeField
from django.db.models import Model, TextField, CharField, IntegerField, URLField

from music.constants import ID3_FIELDS


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


class PlayList(Model):
    user = ForeignKey(get_user_model(), on_delete=DO_NOTHING)
    title = CharField(max_length=255, blank=True, null=True)
    songs = ManyToManyField(Song, blank=True)
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else "Playlist %s" % str(self.pk)

    def add_song(self, song_id):
        added = True

        try:
            new_song = Song.objects.get(pk=song_id)

        except Song.DoesNotExist:
            added = False

        else:
            self.songs.add(new_song)
            self.save()

        return added
