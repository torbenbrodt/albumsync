import util.index.Album
import util.index.Media
import util.Bootstrap


class Purge:
    """Controller 1: list albums or medias."""

    def __init__(self, service, album_str):
        assert service, "when using list action, src cannot be empty"
        self.service = service
        self.album_str = album_str

    def purge_media(self, album):
        index = util.index.Media.Media(self.service, album)
        for entry in index.fetch_all_deleted():
            entry.purge()

    def purge_album(self):
        index = util.index.Album.Album(self.service)
        index.purge()

    def run(self):
        if self.album_str:
            boot = util.Bootstrap.Bootstrap()
            album = boot.get_album(self.service, self.album_str)
            self.purge_media(album)
        else:
            self.purge_album()