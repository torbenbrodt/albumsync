class Sync:
    "Controller: compares service1 (e.g. local) with service2 (e.g. picasa) and controls up- and download."

    def __init__(self):
        #todo, use servicefactory, pass config from CLI to here
        self.albums1 = service.local
        self.albums2 = service.picasa

    def run(self):
        sync_from_1_to_2=True
        sync_from_2_to_1=False

        if sync_from_1_to_2:
            syncAlbum(self.albums1.Album, self.albums2.Album)

        if sync_from_2_to_1:
            syncAlbum(self.albums2.Album, self.albums1.Album)

    def syncAlbum(self, album_src, album_target):
        targets = album_target.fetchAll()
        for album_src in album_src.fetchAll():
             if album_src.getTitle() in targets:
                 target = targets[album_src.getTitle()]
             else 
                 target = album_target.create(album1)
             self.syncMedia(album_src, target)

     def syncMedia(self, album_src, album_target):
        targets = album_target.Media.fetchAll(album_target)
        for media_src in media_src.fetchAll():
             if media_src.getTitle() in targets:
                 target = targets[media_src.getTitle()]
             else:
                 if album_target.getRestrictions():
                     if media_src.getSize() > xxx:
                         do resize
                     if media_src.getSize() > xxx:
                         do resize

                 target = media_target.create(media_src)
