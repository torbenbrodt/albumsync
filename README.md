Description
-----------
This app allows to sync different albums like Google+ (Picasa API) and Harddisk.

Consider the following scenario
* All images from the smartphone are automatically uploaded in full resolution to web album
* Running this script on a computer (or a raspberry) the images will be downloaded to a local filesystem as full resolution backup
* Images from my dslr are stored in a local folder
* all images uploaded to web albums will be resized to meet free storage plan

Contributions
-------------
Other albums like flickr, dropbox and facebook can be integrated.
Please fork this project and create pull requests if you want to help.

Usage
-----
usage: albumsync.py [-h] [--service_picasa_username user@gmail.com]
                    [--service_picasa_password ***]
                    [--service_picasa_noresize]
                    [--service_picasa_max_video_size 1073741824]
                    [--service_local_dir ~/Pictures] [--album ALBUM]
                    [--util_index_dir ~/.albumsyncindex]
                    [--util_index_ttl 86400] [--log warn]
                    [--allowdelete False] [--allowsourceupdate False]
                    [--from_index_src] [--from_index_target] [--src service]
                    [--target service] [--purge] [--sync] [--list]

Setup
-----
Needs pyexiv2 to resize images without loosing exif data
* apt-get install python-pyexiv2

Needs gdata python library version 1
* download https://code.google.com/p/gdata-python-client/downloads/detail?name=gdata-1.3.3.tar.gz&can=2&q=
* unzip and run within directory: sudo python setup.py install

Testing
-------
[![Build Status](https://travis-ci.org/torbenbrodt/albumsync.png)](https://travis-ci.org/torbenbrodt/albumsync)
* Tests should be run on an empty user
* Results can be found at https://travis-ci.org/torbenbrodt/albumsync

License
-------
Copyright 2014 Torben Brodt

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.