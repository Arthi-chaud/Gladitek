import argparse

def parseArgs(args):
	parser = argparse.ArgumentParser(prog="gladitek", description='Sync Epitech Intra\'s Calendar with google')
	parser.add_argument('-d', '--gladir', required=True, dest='gladir', type=str, help='Where the credentials.json and gladitek.json are located')
	parser.add_argument('--clear', required=False, dest='clear', action='store_true', help='Flush calendars', default=False)
	parser.add_argument('--full', required=False, dest='full', action='store_true', help='Fetch Events, even before today', default=False)
	return parser.parse_args(args)