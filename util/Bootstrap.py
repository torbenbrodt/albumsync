class Bootstrap:
    def __init__(self):
        # todo, disable imports and load automatically from Sync class
        # module = __import__('service.local', fromlist=['Album'])
        # getattr(module, 'Album')
        import service.local
        import service.picasa
        import service.picasa.Album
        import service.local.Album
        import service.picasa.Media
        import service.local.Media

    def get_service(self, name):
        """
        @param name: e.g. picasa
        @return:
        """
        return getattr(__import__('service.' + name), name)

    def get_album(self, service, album_str):
        module = getattr(service, 'Album')
        return module.Album(album_str)

