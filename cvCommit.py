import argparse
import yaml


class Commit(object):
    def __init__(self, message, parent):
        self.message = message
        self.__parent = parent

    @property
    def parent(self):
        return self.__parent

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
            'last': None,
        }, stream)


def commit(args):
    data = open_repo()
    data['commits'].append(Commit(args.message, data['last']))
    data['last'] = len(data['commits'])-1
    stream = open('.cv.yaml', 'w')
    yaml.dump(data, stream)


def rebase(args):
    raise NotImplementedError


def checkout(args):
    data = open_repo()
    data['last'] = int(args.index)
    save_repo(data)


def export(args):
    data = open_repo()
    print(data['commits'])
    commits_dict = {str(i): {"message": c.message, "parent": c.parent} for i, c in enumerate(data['commits'])}
    print(commits_dict)
    import json
    with open('result.json', 'w') as fp:
        json.dump(commits_dict, fp)


def open_repo():
    try:
        open('.cv.yaml', 'r')
    except FileNotFoundError:
        print('fatal: not a cv repository')
        exit()
    stream = open('.cv.yaml', 'r')
    return yaml.load(stream)


def save_repo(data):
    stream = open('.cv.yaml', 'w')
    yaml.dump(data, stream)


commands = {
    'init': init,
    'commit': commit,
    'rebase': rebase,
    'checkout': checkout,
    'export': export,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Description')
    subparsers = parser.add_subparsers(help='subparsers help', dest='command')

    parser_init = subparsers.add_parser('init', help='init help')

    parser_commit = subparsers.add_parser('commit', help='commit help')
    parser_commit.add_argument('-m', help='', dest='message')

    parser_rebase = subparsers.add_parser('rebase', help='rebase help')
    parser_rebase.add_argument('branch', help='')

    parser_checkout = subparsers.add_parser('checkout', help='checkout help')
    parser_checkout.add_argument('index', help='')

    parser_export = subparsers.add_parser('export', help='export help')

    args = parser.parse_args()

    # print(args)
    commands[args.command](args)
