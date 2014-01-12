import gdata
import gdata.photos, gdata.photos.service
import time
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

        #todo use oauth implementation from Leo crawford
        gd_client = gdata.photos.service.PhotosService()
        gd_client.email = Config.username
        gd_client.password = Config.password
        gd_client.source = 'api-sample-google-com'
        gd_client.ProgrammaticLogin()

        return gd_client

    def repeat(function,  description, onFailRethrow):
        exc_info = None
        for attempt in range(3):
            try:
                if Config.verbose and (attempt > 0):
                    print ("Trying %s attempt %s" % (description, attempt) )
                return function()
            except Exception,  e:
                if exc_info == None:
                        exc_info = e
                # FIXME - to try and stop 403 token expired
                time.sleep(6)
                Client.get_client().ProgrammaticLogin()
                continue
            else:
                break
        else:
            print ("WARNING: Failed to %s. This was due to %s" % (description, exc_info))
            if onFailRethrow:
                raise exc_info


