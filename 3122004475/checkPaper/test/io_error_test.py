import unittest
from testUtil import *


class TestIOError(unittest.TestCase):

    def test_io_error(self):
        result = calculate_tfidf_similarity('../测试文本/orig.txt', 'file_not_found.txt')
        self.assertIsNone(result, "Expected None for IOError")
