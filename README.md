This code is not working yet.

# albumsync
This code supports the best practice setup i discovered for my self.
* All images from the smartphone are automatically uploaded in full resolution to google plus albums (other web albums like dropbox and facebook are planned)
* Running this script the images will be downloaded to a local filesystem. I use a raspberry pi for and a harddisk raid.
* The online images which are not shared publicly will be replaced by a lower resolution (2048x2048), since this is for free.
* Images from my dslr (local folder system) are uploaded in lower resolution to google plus photos.

Needs pyexiv2 to resize images without loosing exif data
* apt-get install python-pyexiv2

Needs gdata python library version 1
* download https://code.google.com/p/gdata-python-client/downloads/detail?name=gdata-1.3.3.tar.gz&can=2&q=
* unzip and run within directory: sudo python setup.py install

Testing
[![Build Status](https://travis-ci.org/torbenbrodt/albumsync.png)](https://travis-ci.org/torbenbrodt/albumsync)
 * Results can be found at https://travis-ci.org/torbenbrodt/albumsync

# Similar Projects
https://github.com/leocrawford/picasawebsync
* i still consider pushing my changes back, but i did not like the codebase

