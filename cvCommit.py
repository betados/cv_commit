import argparse
import yaml


def init():
    stream = open('.cv.yaml', 'w')
    yaml.dump({}, stream)


def commit():
    pass


def rebase():
    pass


commands = {
    'init': init,
    'commit': commit,
    'rebase': rebase,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Description')
    subparsers = parser.add_subparsers(help='subparsers help', dest='command')

    parser_init = subparsers.add_parser('init', help='init help')

    parser_commit = subparsers.add_parser('commit', help='commit help')
    parser_commit.add_argument('-m', help='', dest='message')

    parser_rebase = subparsers.add_parser('rebase', help='rebase help')
    parser_rebase.add_argument('branch', help='')

    args = parser.parse_args()

    # print(args)
    commands[args.command]()
