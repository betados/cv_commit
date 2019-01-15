import argparse
from collections import namedtuple

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


class Branch(object):
    def __init__(self, name, commit):
        self.name = name
        self.commit = commit


file = '.cv.yaml'


def init(args):
    try:
        open(file, 'r')
        print('Already a cv repository')
    except FileNotFoundError:
        stream = open(file, 'w')
        # TODO create by default a master branch
        yaml.dump({
            'commits': [],
            'branches': [Branch('master', None),],
            'last': None,
            'checked_out_branch': 0,
        }, stream)


def commit(args):
    data = open_repo()
    if not args.message:
        message = input('Please, give a message for the commit:')
    else:
        message = args.message
    data['commits'].append(Commit(message, data['last']))
    data['last'] = len(data['commits']) - 1
    data['branches'][data['checked_out_branch']].commit = data['last']
    stream = open(file, 'w')
    yaml.dump(data, stream)


def rebase(args):
    raise NotImplementedError


def checkout(args):
    data = open_repo()
    if args.branch_name:
        print(args.branch_name)
        # TODO check if already exists
        data['branches'].append(Branch(args.branch_name, data['last']))
        data['checked_out_branch'] = -1
    else:
        try:
            if int(args.index) >= len(data['commits']):
                print('fatal: not a commit index')
                exit()
            data['last'] = int(args.index)
            data['branches'][data['checked_out_branch']].commit = int(args.index)
        except ValueError:
            for i, branch in enumerate(data['branches']):
                if branch.name == args.index:
                    data['last'] = branch.commit
                    data['checked_out_branch'] = i
                    save_repo(data)
                    return
            print(f'fatal: {args.index} is not a branch name')
            exit()
    save_repo(data)


def export(args):
    data = open_repo()
    # commits_dict = {str(i): {"message": c.message, "parent": c.parent, "branch": } for i, c in
    #                 enumerate(data['commits'])}
    commits_dict = {}
    for i, c in enumerate(data['commits']):
        branch = None
        for b in data['branches']:
            if b.commit == i:
                if not branch:
                    branch = [b.name, ]
                else:
                    branch.append(b.name)
        commits_dict[str(i)] = {"message": c.message, "parent": c.parent, "branch": branch}
    name = args.name
    if not name:
        name = 'commits.json'
    elif name[-5:] != '.json':
        name += '.json'
    import json
    with open(f'front-end/static/{name}', 'w') as fp:
        json.dump(commits_dict, fp)


def open_repo():
    try:
        open(file, 'r')
    except FileNotFoundError:
        print('fatal: not a cv repository')
        exit()
    stream = open(file, 'r')
    return yaml.load(stream)


def save_repo(data):
    stream = open(file, 'w')
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

    parser_init = subparsers.add_parser('init', help='Creates a new CV repository')

    parser_commit = subparsers.add_parser('commit', help='Creates a new node')
    parser_commit.add_argument('-m', help='', dest='message')

    parser_rebase = subparsers.add_parser('rebase', help='rebase help')
    parser_rebase.add_argument('branch', help='')

    parser_checkout = subparsers.add_parser('checkout', help='Changes the pointer to the given index')
    pcg = parser_checkout.add_mutually_exclusive_group(required=True)
    pcg.add_argument('index', help='', nargs='?')
    pcg.add_argument('-b', '--branch', dest='branch_name')

    parser_export = subparsers.add_parser('export', help='Export the nodes to a JSON for the viewer to render it')
    parser_export.add_argument('-n', help='destination name', dest='name')

    args = parser.parse_args()

    # print(args)
    commands[args.command](args)
