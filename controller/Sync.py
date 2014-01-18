
class Sync:
    """Controller: compares service1 (e.g. local) with service2 (e.g. picasa) and controls up- and download."""

    def __init__(self, service_src, service_target):
        self.service_src = service_src
        self.service_target = service_target

    def run(self):
        albums_targets = self.service_target.Album.Album.fetch_all()
        album_target_match_names = map(lambda x: x.get_match_name(), albums_targets)
        for album_src in self.service_src.Album.Album.fetch_all():
            print album_src.get_match_name()
            if album_src.get_match_name() in album_target_match_names:
                print "\tMATCH ALBUM FOUND, use ref"
                # todo how to find ref
                self.sync()
            else:
                print "\tno match album found, create()"
                album_target = self.service_target.Album.Album.create(album_src)
                self.sync()

    def sync(self):
        #todo call SyncAlbum.run
        pass
