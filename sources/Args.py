import argparse

def parseArgs(args):
	parser = argparse.ArgumentParser(prog="gladitek", description='Sync Epitech Intra\'s Calendar with google')
	parser.add_argument('-d', '--gladir', required=True, dest='gladir', type=str, help='Where the credentials.json and gladitek.json are located')
	parser.add_argument('-redump', '--redump', required=False, dest='redump', action='store_true', help='Flush calendars and pull everything back', default=False)
	return parser.parse_args(args)