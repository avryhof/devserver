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

    def import_song(self, path):
        ext = os.path.splitext(path)[-1].lower()
        if ext == ".mp3":
            try:
                mp3 = MP3File(path)
                try:
                    tags = mp3.get_tags()
                except Exception:
                    pass
                else:
                    song_dict = dict(path=path)
                    try:
                        Song.objects.get(**song_dict)
                    except Song.DoesNotExist:

                        for tag_key, tag_dict in tags.items():
                            for song_key in ID3_FIELDS:
                                if not song_dict.get(song_key):
                                    song_dict.update({song_key: tag_dict.get(song_key)})
                        try:
                            Song.objects.create(**song_dict)

                        except Exception:
                            pass

            except Exception:
                pass

    def handle(self, *args, **options):
        self.verbosity = int(options["verbosity"])

        for folder in glob.glob(os.path.join(settings.MUSIC_FOLDER, "**")):
            if os.path.isdir(folder):
                print("Processing %s" % folder)
                all_files = glob.glob(os.path.join(folder, "**"), recursive=True)
                for all_file in all_files:
                    self.import_song(all_file)

            else:
                print("Processing %s" % folder)
                self.import_song(folder)
