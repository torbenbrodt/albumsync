class Client:
    def getInstance(self):
        gd_client = gdata.photos.service.PhotosService()
        gd_client.email = args.username # Set your Picasaweb e-mail address...
        gd_client.password = args.password 
        gd_client.source = 'api-sample-google-com'
        gd_client.ProgrammaticLogin()


