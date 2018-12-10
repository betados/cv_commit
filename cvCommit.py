import argparse
import yaml


class Commit(object):
    def __init__(self, message, parent):
        self.message = message
        self.__parent = parent

    def __repr__(self):
        return self.__class__.__name__ + f'("{self.message}", {self.__parent})'


def init(args):
    try:
        open('.cv.yaml', 'r')
        print('Already a cv repository')
        exit()
    except FileNotFoundError:
        stream = open('.cv.yaml', 'w')
        yaml.dump({
            'commits': [],
            'last': -1,
        }, stream)


def commit(args):
    try:
        open('.cv.yaml', 'r')
    except FileNotFoundError:
        print('fatal: not a cv repository')
        exit()
    stream = open('.cv.yaml', 'r')
    data = yaml.load(stream)
    try:
        data['commits'].append(Commit(args.message, data['commits'][data['last']]))
    except IndexError:
        data['commits'].append(Commit(args.message, None))
    data['last'] = -1
    stream = open('.cv.yaml', 'w')
    yaml.dump(data, stream)


def rebase(args):
    raise NotImplementedError


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
    commands[args.command](args)
