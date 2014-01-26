class Bootstrap:
    def __init__(self):
        # todo, disable imports and load automatically from Sync class
        # module = __import__('service.local', fromlist=['Album'])
        # getattr(module, 'Album')
        import service.picasa.Album
        import service.local.Album
        import service.picasa.Media
        import service.local.Media