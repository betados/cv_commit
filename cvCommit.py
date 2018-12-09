import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('commit', help='')
    parser.add_argument('rebase', help='')
    parser.add_argument('-m', help='')

    args = parser.parse_args()

    print(args)
