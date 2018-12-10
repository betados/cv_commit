import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Description')
	subparsers = parser.add_subparsers(help='sub-command help')

	parser_commit = subparsers.add_parser('commit', help='commit help')
	parser_commit.add_argument('-m', help='', dest='message')

	parser_r = subparsers.add_parser('rebase', help='rebase help')
	parser_r.add_argument('-m', help='', dest='message')

	args = parser.parse_args()
	args_c = parser_commit.parse_args()

	print(args)
	print(args_c)
