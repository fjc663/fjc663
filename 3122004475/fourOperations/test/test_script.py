import fractions
import re
import unittest
from util import generate_problems, validate_answers, calculate_answer

class TestMathProblems(unittest.TestCase):

    def test_generate_problems(self):
        # 测试生成 10 个题目，数值范围为 10
        problems, answers = generate_problems(10, 10)
        self.assertEqual(len(problems), 10)
        self.assertEqual(len(answers), 10)

    def test_generate_problems_with_range(self):
        # 测试生成题目中的数值是否在范围内
        problems, answers = generate_problems(5, 100)
        for problem in problems:
            for num in re.findall(r'\d+', problem):
                self.assertTrue(1 <= int(num) <= 100)

    def test_validate_correct_answers(self):
        # 测试答案验证是否正确
        exercise_data = [
            "1. 3 + 2 =",
            "2. 6 × 4 =",
        ]
        answer_data = [
            "1. 5",
            "2. 24",
        ]
        correct_count, wrong_count, correct_indices, wrong_indices = validate_answers(exercise_data, answer_data)
        self.assertEqual(correct_count, 2)
        self.assertEqual(wrong_count, 0)

    def test_validate_wrong_answers(self):
        # 测试错误答案的验证
        exercise_data = [
            "1. 3 + 2 =",
            "2. 6 ÷ 2 =",
        ]
        answer_data = [
            "1. 6",
            "2. 3",
        ]
        correct_count, wrong_count, correct_indices, wrong_indices = validate_answers(exercise_data, answer_data)
        self.assertEqual(correct_count, 1)
        self.assertEqual(wrong_count, 1)
        self.assertEqual(wrong_indices, [1])

    def test_fraction_handling(self):
        # 测试带分数的验证
        exercise_data = [
            "1. 1'1/2 + 1/2 =",
        ]
        answer_data = [
            "1. 2",
        ]
        correct_count, wrong_count, correct_indices, wrong_indices = validate_answers(exercise_data, answer_data)
        self.assertEqual(correct_count, 1)
        self.assertEqual(wrong_count, 0)

    def test_calculate_answer(self):
        # 测试分数计算结果
        self.assertEqual(calculate_answer("1'1/2 + 1/2"), fractions.Fraction(2))
        self.assertEqual(calculate_answer("3 ÷ 2".replace(' ÷ ', '/')), fractions.Fraction(3, 2))


if __name__ == "__main__":
    unittest.main()
