from django.forms import CharField, Form, ModelChoiceField

from music.models import PlayList, Song


class SongSearchForm(Form):
    search = CharField(required=False)
    artist = CharField(required=False)
    album = CharField(required=False)
    song = CharField(required=False)


class AddToPlaylistForm(Form):
    playlist = ModelChoiceField(PlayList.objects.all())
    song = ModelChoiceField(Song.objects.all())
