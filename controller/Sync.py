import util


class Sync:
    "Controller: compares service1 (e.g. local) with service2 (e.g. picasa) and controls up- and download."

    def __init__(self):
        #todo, use servicefactory, pass config from CLI to here
        self.albums1 = service.local
        self.albums2 = service.picasa

    def run(self):
        sync_from_1_to_2 = True
        sync_from_2_to_1 = False

        if sync_from_1_to_2:
            self.syncAlbum(self.albums1.Album, self.albums2.Album)

        if sync_from_2_to_1:
            self.syncAlbum(self.albums2.Album, self.albums1.Album)

    def syncAlbum(self, album_src, album_target):
        """
        @param album_src:
        @param album_target:
        """
        targets = album_target.fetchAll()
        for album_src in album_src.fetchAll():
             if album_src.getMatchName() in targets:
                 target = targets[album_src.getMatchName()]
             else 
                 target = album_target.create(album1)

             self.syncMedia(album_src, target)

     def syncMedia(self, album_src, album_target):
        targets = album_target.Media.fetchAll(album_target)
        for media_src in album_src.Media.fetchAll(album_src):
             if media_src.getMatchName() in targets:
                 media_target = targets[media_src.getMatchName()]
             else:
                 if album_target.getRestrictions():
                     if media_src.getSize() > album_src.getConfig().getMaxWidth():
                         util.Image.resize(media_src)
                     if media_src.getSize() > album_target.getConfig().getMaxWidth():
                         util.Image.resize(media_src)

                 media_target = album_target.Media.create(album_target, media_src)

            #todo Do local backups if files are overriden
            #todo Update meta data (including version?)
            #todo think about etag usage, https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol
            media_target.compare()
