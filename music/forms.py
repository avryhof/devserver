from django.forms import CharField, Form


class SongSearchForm(Form):
    search = CharField(required=False)
    artist = CharField(required=False)
    album = CharField(required=False)
    song = CharField(required=False)
