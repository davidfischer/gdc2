import unittest

from gdc2.archiveparser import GitHubArchiveParser


class TestArchiveParser(unittest.TestCase):
    def test_flatten(self):
        arch = GitHubArchiveParser('/not/a/file')
        self.assertEqual(arch._flatten({}), {})
        self.assertEqual(
            arch._flatten({"a": 1}),
            {"a": 1})
        self.assertEqual(
            arch._flatten({"a": 1, "b": {"a": 2}}),
            {"a": 1, "b_a": 2})
        self.assertEqual(
            arch._flatten({"b": {"a": 2, "c": {"d": True}}}),
            {"b_a": 2, "b_c_d": True})