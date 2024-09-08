import unittest
from testUtil import *


class TestPlagiarismChecker(unittest.TestCase):

    # 文本预处理测试
    def test_preprocess_text_basic(self):
        # 基本中文文本处理
        text = "这是一个简单的测试。"
        result = preprocess_text(text)
        self.assertEqual(result, "这是 一个 简单 的 测试")

    # 预处理 - 空字符串测试
    def test_preprocess_text_empty(self):
        # 测试空字符串处理
        text = ""
        result = preprocess_text(text)
        self.assertEqual(result, "")

    # 预处理 - 特殊符号测试
    def test_preprocess_text_special_characters(self):
        # 测试含有特殊符号的文本处理
        text = "测试，符号@#！"
        result = preprocess_text(text)
        self.assertEqual(result, "测试 符号")

    # 相似度计算 - 完全相同的文本
    def test_calculate_tfidf_similarity_identical(self):
        similarity = calculate_tfidf_similarity("../测试文本/orig.txt", "../测试文本/orig.txt")
        self.assertEqual(similarity, 100.0)

    # 相似度计算 - 完全不同的文本
    def test_calculate_tfidf_similarity_different(self):
        similarity = calculate_tfidf_similarity("testFile1.txt", "testFile2.txt")
        self.assertLess(similarity, 10.0)  # 假设完全不同文本的相似度应该很低

    # 相似度计算 - 一篇空文件
    def test_calculate_tfidf_similarity_one_empty(self):
        similarity = calculate_tfidf_similarity("testFile1.txt", "testFile3(模拟空文件).txt")
        self.assertEqual(similarity, 0.0)  # 一篇空文件相似度应为 0

    # 相似度计算 - 两篇空文件
    def test_calculate_tfidf_similarity_both_empty(self):
        similarity = calculate_tfidf_similarity("testFile3(模拟空文件).txt", "testFile3(模拟空文件).txt")
        self.assertEqual(similarity, 0.0)  # 两篇空文件的相似度应为 0
