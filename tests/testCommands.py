import unittest
from cvCommit import *
import os.path
from collections import namedtuple


class TestCommands(unittest.TestCase):
    def test_init(self):
        file = '.cv.yaml'
        init()
        self.assertTrue(os.path.exists(file))

        data = open_repo()
        self.assertEqual(data['branches'][0].name, 'master')

    def test_commit(self):
        Args = namedtuple('Args', 'message description')
        args = Args('Gromenauer', 'GromenauerD')
        data = open_repo()
        previous_length = len(data['commits'])
        commit_func(args)
        data = open_repo()
        new_length = len(data['commits'])
        self.assertEqual(previous_length + 1, new_length)
