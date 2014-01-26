import argparse
import logging
from controller.Sync import Sync


class Front:
    def __init__(self):
        pass

    @staticmethod
    def run():
        # example
        # albumsync.py --service.picasa.user albumsync.test@googlemail.com --service.picasa.password xxx
        # --service.local.dir ~/Pictures --util.index.dir ~/.albumsync
        # --sync --service_src picasa --service_target local

        parser = argparse.ArgumentParser()

        parser.add_argument('--service.picasa.user', help='Your picasa username')
        parser.add_argument('--service.picasa.password', help='Your picasa password')

        parser.add_argument('--service.local.dir', help='Directory where local images are stored')

        # index is optional, use it to allow file deletion
        parser.add_argument('--util.index.dir', help='Directory where the index is written')

        # super config
        parser.add_argument('--log', help='possible values are DEBUG, INFO, WARN')
        parser.add_argument('--allowdelete', help='are deletion commando', type=bool)

        # actions
        parser.add_argument('--purge', help='Drop all index files after run', type=bool)
        parser.add_argument('--sync', help='Drop all index files')

        # parse
        args = parser.parse_args()

        # set log level
        numeric_level = getattr(logging, args.log.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.log)
        logging.basicConfig(level=numeric_level)

        # todo load modules
        sync = Sync()
        sync.run()

