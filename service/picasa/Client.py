import gdata
import gdata.photos
import gdata.photos.service
from service.picasa.Config import Config


class Client:
    """
    see https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol
    see https://code.google.com/p/googlecl/source/browse/trunk/src/googlecl/picasa/service.py
    """
    SUPPORTED_VIDEO_TYPES = {
        'wmv': 'video/x-ms-wmv',
        'avi': 'video/avi',
        '3gp': 'video/3gpp',
        'mov': 'video/quicktime',
        'qt': 'video/quicktime',
        'mp4': 'video/mp4',
        'mpa': 'video/mpeg',
        'mpe': 'video/mpeg',
        'mpeg': 'video/mpeg',
        'mpg': 'video/mpeg',
        'mpv2': 'video/mpeg',
        'mpeg4': 'video/mpeg4'
    }
    MAX_VIDEO_SIZE = 1073741824
    MAX_FREE_IMAGE_DIMENSION = 2048
    _UPDATED_CONFIG = False

    def __init__(self):
        pass

    @staticmethod
    def _update_config():
        if Client._UPDATED_CONFIG:
            return

        Client._UPDATED_CONFIG = True

        # XXX gdata.photos.service contains a very strange check against (outdated)
        # allowed MIME types. This is a hack to allow videos to be uploaded.
        # We're creating a list of the allowed video types stripped of the initial
        # 'video/', eliminating duplicates via set(), then converting to tuple()
        # since that's what gdata.photos.service uses.
        gdata.photos.service.SUPPORTED_UPLOAD_TYPES += \
            tuple(set([video_type.split('/')[1] for video_type in Client.SUPPORTED_VIDEO_TYPES.values()]))

    @staticmethod
    def get_client():
        """walk the web album finding albums there
        @rtype : gdata.photos.service.PhotosService
        """
        assert Config.username, "picasa username cannot be empty"
        assert Config.password, "picasa password cannot be empty"
        Client._update_config()
        #todo use oauth implementation from Leo crawford
        gd_client = gdata.photos.service.PhotosService()
        gd_client.email = Config.username
        gd_client.password = Config.password
        gd_client.source = 'api-sample-google-com'
        gd_client.ProgrammaticLogin()
        return gd_client
