import argparse
import logging
from controller.Sync import Sync
from controller.List import List
from controller.Purge import Purge


class Front:
    def __init__(self):
        pass

    @staticmethod
    def run_assertions(args):
        actions = filter(bool, [args.sync, args.purge, args.list])
        if len(actions) == 0:
            raise AssertionError("No action given")
        if len(actions) > 1:
            raise AssertionError("More than one action given")

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(description='albumsync will sync your albums')

        parser.add_argument('--service_picasa_username', help='Your picasa username', metavar='user@gmail.com')
        parser.add_argument('--service_picasa_password', help='Your picasa password', metavar='***')
        parser.add_argument('--service_local_dir', help='Directory where local images are stored', metavar='~/Pictures')
        parser.add_argument('--album', help='Limit action to single album')

        # index is optional, use it to allow file deletion
        parser.add_argument('--util_index_dir', help='Directory where the index is written', metavar='~/.albumsyncindex')

        # super config
        parser.add_argument('--log', help='possible values are DEBUG, INFO, WARN', default='warn', metavar='warn')
        parser.add_argument('--allowdelete', help='is delete allowed', type=bool, metavar=False)

        # source and target
        parser.add_argument('--src', help='source service e.g. local', metavar='service')
        parser.add_argument('--target', help='source service e.g. picasa', metavar='service')

        # actions
        parser.add_argument('--purge', help='Action: drop index files', action='store_true')
        parser.add_argument('--sync', help='Action: Sync services', action='store_true')
        parser.add_argument('--list', help='Action: List', action='store_true')
        return parser

    @staticmethod
    def update_config(args):
        if args.service_local_dir:
            import service.local.Config
            service.local.Config.Config.dir = args.service_local_dir
        if args.service_picasa_username:
            import service.picasa.Config
            service.picasa.Config.Config.username = args.service_picasa_username
        if args.service_picasa_password:
            import service.picasa.Config
            service.picasa.Config.Config.password = args.service_picasa_password

        # set log level
        numeric_level = getattr(logging, args.log.upper(), None)
        if not isinstance(numeric_level, int):
            raise AssertionError('Invalid log level: %s' % args.log)
        logging.basicConfig(level=numeric_level)

    @staticmethod
    def run():
        parser = Front.get_parser()
        try:
            # parse args
            args = parser.parse_args()
            # run additional assertions
            Front.run_assertions(args)
            # setting configs
            Front.update_config(args)
            # run action
            if args.sync:
                ctrl = Sync(args.src, args.target, args.album)
                ctrl.run()
            elif args.list:
                ctrl = List(args.src, args.album)
                ctrl.run()
            elif args.list:
                ctrl = Purge(args.src, args.album)
                ctrl.run()

        except AssertionError as e:
            print parser.format_usage() + "\nAssertionError: " + e.message