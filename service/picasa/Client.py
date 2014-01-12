class Client:
    # see https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol

    def getInstance(self):
        gd_client = gdata.photos.service.PhotosService()
        gd_client.email = args.username # Set your Picasaweb e-mail address...
        gd_client.password = args.password 
        gd_client.source = 'api-sample-google-com'
        gd_client.ProgrammaticLogin()

        #todo use oauth implementation from Leo crawford


