from controller.SyncAlbum import SyncAlbum


class Sync:
    """Controller: compares service1 (e.g. local) with service2 (e.g. picasa) and controls up- and download."""

    def __init__(self, service_src, service_target):
        self.service_src = service_src
        self.service_target = service_target

    def run(self):
        albums_target = self.service_target.Album.Album.fetch_all()
        album_target_match_names = lambda x: x.get_matching_name, albums_target
        for album_src in self.service_src.Album.Album.fetch_all():
            print "matching album ", album_src.get_match_name()
            if album_src.get_match_name() in album_target_match_names:
                print "match album found"
                self.sync()
            else:
                print "no match album found"
                self.sync()

    def sync(self):
        #todo call SyncAlbum.run
        pass
