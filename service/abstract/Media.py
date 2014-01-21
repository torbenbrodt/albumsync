class Media:
    """Model: common public api for all medias like photos and videos"""

    @staticmethod
    def fetch_all(album):
        """walk the directories
        @rtype : list of Album
        """
        raise Exception("method needs to be implemented")

    @staticmethod
    def create(album, media_src):
        raise Exception("method needs to be implemented")

    def __init__(self, album, path):
        raise Exception("method needs to be implemented")
    
    def get_url(self):
        raise Exception("method needs to be implemented")

    def get_hash(self):
        raise Exception("method needs to be implemented")

    def get_date(self):
        raise Exception("method needs to be implemented")

    def get_size(self):
        raise Exception("method needs to be implemented")

    def delete(self):
        raise Exception("method needs to be implemented")

    def get_title(self):
        raise Exception("method needs to be implemented")

    def get_description(self):
        raise Exception("method needs to be implemented")

    def get_mime_type(self):
        raise Exception("method needs to be implemented")

    def download(self, path):
        raise Exception("method needs to be implemented")

    def get_match_name(self):
        """this method is used to match media"""
        raise Exception("method needs to be implemented")

    def is_resize_necessary(self):
        raise Exception("method needs to be implemented")

    def resize(self):
        raise Exception("method needs to be implemented")
