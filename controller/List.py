import util.index.Album
import util.index.Media
import util.Bootstrap
import util.Superconfig


class List:
    """Controller 1: list albums or medias."""

    def __init__(self, service, album_str):
        assert service, "when using list action, src cannot be empty"
        boot = util.Bootstrap.Bootstrap()
        self.service = boot.get_service(service)
        self.album_str = album_str

    def _get_albums(self):
        if util.Superconfig.Superconfig.from_index_src:
            index = util.index.Album.Album(self.service)
            index.sync()
            return index.fetch_all_as_album()
        else:
            return self.service.Album.Album.fetch_all()

    def list_media(self, album):
        index = util.index.Media.Media(self.service, album)
        print "deleted: "
        for entry in index.fetch_all_deleted():
            print '{0:40} {1}'.format(entry.get_match_name()[0:40], entry.get_url())
        print "existing: "
        for entry in self.service.Media.Media.fetch_all(album):
            print '{0:40} {1}'.format(entry.get_match_name()[0:40], entry.get_url())

    def list_album(self):
        index = util.index.Album.Album(self.service)
        print "deleted: "
        for entry in index.fetch_all_deleted():
            print entry.get_match_name()
        print "existing: "
        for entry in self._get_albums():
            print '{0:40} {1}'.format(entry.get_match_name()[0:40], entry.get_url())

    def run(self):
        if self.album_str:
            boot = util.Bootstrap.Bootstrap()
            album = boot.get_album(self.service, self.album_str)
            self.list_media(album)
        else:
            self.list_album()