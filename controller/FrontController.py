import argparse

class FrontController:

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-u","--username", help="Your picassaweb username")
        parser.add_argument("-p","--password", help="Your picassaweb password", default=False)

	# parse
	args = parser.parse_args()

	# usage
	verbose = args.verbose
