import gdata
import gdata.photos, gdata.photos.service
from service.picasa.Config import Config


class Client:
    """
    see https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol
    see https://code.google.com/p/googlecl/source/browse/trunk/src/googlecl/picasa/service.py
    """

    def __init__(self):
        pass

    @staticmethod
    def get_client():
        """walk the web album finding albums there
        @rtype : gdata.photos.service.PhotosService
        """
        assert Config.username, "picasa username cannot be empty"
        assert Config.password, "picasa password cannot be empty"
        #todo use oauth implementation from Leo crawford
        gd_client = gdata.photos.service.PhotosService()
        gd_client.email = Config.username
        gd_client.password = Config.password
        gd_client.source = 'api-sample-google-com'
        gd_client.ProgrammaticLogin()
        return gd_client


