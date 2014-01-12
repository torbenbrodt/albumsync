import gdata
from service.picasa.Config import Config


class Client:
    """see https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol"""

    def __init__(self):
        pass

    @staticmethod
    def get_client():
        """walk the web album finding albums there
        @rtype : gdata.photos.service.PhotosService
        """
        gd_client = gdata.photos.service.PhotosService()
        gd_client.email = Config.username # Set your Picasaweb e-mail address...
        gd_client.password = Config.password
        gd_client.source = 'api-sample-google-com'
        gd_client.ProgrammaticLogin()

        #todo use oauth implementation from Leo crawford


