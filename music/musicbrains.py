import pprint

import musicbrainzngs


class MusicBrains:
    app_name = "Vryhof dev Music Library"
    version = "0.1"
    contact = "amos@vryhof.net"

    client = None

    def __init__(self):
        self.client = musicbrainzngs
        self.client.set_useragent(self.app_name, self.version, contact=self.contact)

    def find_song(self, **kwargs):
        pprint.pprint(self.client.search_recordings(query='', country="us", limit=None, offset=None, strict=False,
                                      artist="metallica", recording="until it sleeps"))

mb = MusicBrains()
mb.find_song()
