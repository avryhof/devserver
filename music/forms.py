from django.forms import CharField, Form, ModelChoiceField, TextInput

from music.models import PlayList, Song


class SongSearchForm(Form):
    search = CharField(
        required=False,
        widget=TextInput(attrs={"placeholder": "Search", "class": "form-control form-control-dark w-100"}),
    )
    artist = CharField(required=False)
    album = CharField(required=False)
    song = CharField(required=False)


class AddToPlaylistForm(Form):
    playlist = ModelChoiceField(PlayList.objects.all())
    song = ModelChoiceField(Song.objects.all())


class PlaylistForm(Form):
    title = CharField(required=True)
