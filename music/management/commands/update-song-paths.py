import glob
import os

from django.conf import settings
from django.core.management import BaseCommand
from mp3_tagger import MP3File

from music.constants import ID3_FIELDS
from music.models import Song


class Command(BaseCommand):
    help = "Update weather station data from the Ambient Weather API."
    verbosity = 0
    current_file = None
    log_file_name = None
    log_file = False

    def handle(self, *args, **options):
        self.verbosity = int(options["verbosity"])

        songs = Song.objects.all()

        for song in songs:
            file_name = song.path
            new_path = song.path.replace(settings.OLD_MUSIC_FOLDER, "")

            print(file_name, new_path)
            exit()
