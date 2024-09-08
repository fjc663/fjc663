import unittest
from testUtil import *


class TestGeneralException(unittest.TestCase):

    def test_general_exception(self):
        result = calculate_tfidf_similarity('../测试文本/orig.txt', 'file_not_found.txt')
        self.assertIsNone(result, "Expected None for general Exception")


if __name__ == '__main__':
    unittest.main()
