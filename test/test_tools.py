import unittest
from yltk.tools import build_cmd


class TestBuildCmd(unittest.TestCase):

    def test_list_args(self):
        actual = build_cmd(
            base_cmd='ls',
            args=[('a', 1), ('bb', None)]
        )
        expected = f'''\
ls \\
-a 1 \\
--bb'''
        self.assertEqual(actual, expected)

    def test_dict_args(self):
        actual = build_cmd(
            base_cmd='ls',
            args={'a': 1, 'bb': None, 'file': 'with blank space.txt'}
        )
        expected = f'''\
ls \\
-a 1 \\
--bb \\
--file "with blank space.txt"'''
        self.assertEqual(actual, expected)
