import os
import re

from mp3_tagger import MP3File

from getlyrics import findlyrics


class PathInfo:
    path = None
    path_parts = []
    dirname = None
    basename = None
    extension = None
    filename = None

    def __init__(self, path):
        self.path = path
        self.path_parts = re.split(r"/|\\", self.path)
        self.dirname = os.path.dirname(self.path)
        self.basename = os.path.basename(self.path)
        if os.path.isfile(self.path):
            self.extension = os.path.splitext(self.path)[-1].replace(".", "")
            self.filename = self.path_parts[-1]

    def __str__(self):
        return self.path


class Mp3Info(PathInfo):
    id3 = None

    attrib_list = [
        "path",
        "artist",
        "album",
        "song",
        "track",
        "year",
        "genre",
        "band",
        "composer",
        "copyright",
        "publisher",
    ]

    artist = None
    album = None
    song = None
    track = None
    year = None
    genre = None
    band = None
    composer = None
    copyright = None
    publisher = None

    def __init__(self, path):
        super(Mp3Info, self).__init__(path)

        mp3 = MP3File(self.path)
        tags = mp3.get_tags()

        for tag_version, tag_dict in tags.items():
            for attr_name in self.attrib_list:
                if not getattr(self, attr_name):
                    setattr(self, attr_name, tag_dict.get(attr_name, None))

    def dict(self):
        retn = dict()
        for attr_name in self.attrib_list:
            retn[attr_name] = getattr(self, attr_name)

        return retn

    @property
    def lyrics(self):
        return findlyrics(self.artist, self.song)
