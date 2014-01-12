class SyncAlbum:
    """ ... """

    def __init__(self, service_src, service_target, album_src, album_target):
        self.service_src = service_src
        self.service_target = service_target
        self.album_src = album_src
        self.album_target = album_target

    def run(self):
        medias_target = self.service_target.Media.Media.fetch_all(self.album_target)
        media_target_match_names = lambda x: x.get_matching_name, medias_target
        for media_src in self.service_src.Media.Media.fetch_all(self.album_src):
            print "matching media ", media_src.get_match_name()
            if media_src.get_match_name() in media_target_match_names:
                print "match media found"
                self.sync()
            else:
                print "no match media found"
                self.sync()

    def sync(self):
        #todo call SyncMedia.run
        pass
