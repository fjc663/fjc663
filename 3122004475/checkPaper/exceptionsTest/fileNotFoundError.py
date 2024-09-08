import unittest
from testUtil import *


class TestFileNotFoundError(unittest.TestCase):

    def test_file_not_found(self):
        result = calculate_tfidf_similarity('../测试文本/orig.txt', 'file_not_found.txt')
        self.assertIsNone(result, "Expected None for FileNotFoundError")


if __name__ == '__main__':
    unittest.main()
