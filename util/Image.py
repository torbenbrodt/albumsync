class Image:

    # used https://github.com/jackpal/picasawebuploader/blob/master/main.py and 
    # http://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
    def shrinkIfNeeded(path):
        imagePath = tempfile.NamedTemporaryFile(delete=False) 
        try:     
            im = Image.open(path)
            if (im.size[0] > PICASA_MAX_FREE_IMAGE_DIMENSION  or im.size[1] > PICASA_MAX_FREE_IMAGE_DIMENSION):
                print "Shrinking " + path
                im.thumbnail((PICASA_MAX_FREE_IMAGE_DIMENSION, PICASA_MAX_FREE_IMAGE_DIMENSION), Image.ANTIALIAS)
                im.save(imagePath, "JPEG")
                if (jHead is not None):
                    call (["jhead", "-q", "-te", path, imagePath.name])
                return imagePath.name
        except IOError:
            print "cannot create thumbnail for '%s' - using full size image" % path

