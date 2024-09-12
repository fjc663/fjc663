import random
import fractions
import argparse
import os
import re


# 生成随机运算符
def generate_operator():
    return random.choice(['+', '-', '*', '/'])


# 将真分数格式化为指定格式
def format_fraction(frac):
    if frac.numerator == 0:
        return '0'
    if frac.numerator >= frac.denominator:  # 分子大于分母，是带分数
        integer_part = frac.numerator // frac.denominator  # 整数部分
        fraction_part = frac.numerator % frac.denominator  # 真分数部分
        if fraction_part == 0:
            return str(integer_part)  # 如果分子刚好被分母整除，返回整数部分
        else:
            return f"{integer_part}'{fraction_part}/{frac.denominator}"  # 带分数格式
    else:
        return f"{frac.numerator}/{frac.denominator}"  # 真分数格式


# 生成随机数或真分数
def generate_number(range_limit):
    is_fraction = random.choice([True, False])
    if is_fraction:
        numerator = random.randint(1, range_limit - 1)
        denominator = random.randint(1, range_limit - 1)
        return fractions.Fraction(numerator, denominator)
    else:
        return random.randint(1, range_limit - 1)


# 将自然数或真分数格式化为输出形式
def format_number(num):
    if isinstance(num, fractions.Fraction):
        return format_fraction(num)
    else:
        return str(num)


# 随机加括号
def insert_random_parentheses(expr):
    numbers_operators = expr.split(' ')

    # 只有两个数字运算或随机为不插入时，不插入括号
    if len(numbers_operators) <= 3 or not random.choice([True, False]):
        return expr

    # 插入左括号位置
    insert_left_parentheses = random.choice(list(range(0, len(numbers_operators) - 2 - 1, 2)))
    # 插入右括号位置
    insert_right_parentheses = random.choice(list(range(insert_left_parentheses + 3, len(numbers_operators) - 1, 2)))

    new_numbers_operators = []

    for index, number_operator in enumerate(numbers_operators):
        if index == insert_left_parentheses:
            new_numbers_operators.append('(')
        elif index == insert_right_parentheses:
            new_numbers_operators.append(')')

        new_numbers_operators.append(number_operator)

    return ' '.join(new_numbers_operators)


# 生成单个四则运算题目
def generate_expression(range_limit):
    operator_count = random.randint(1, 3)  # 运算符数量限制为 1 到 3 个
    numbers = [generate_number(range_limit) for _ in range(operator_count + 1)]
    operators = [generate_operator() for _ in range(operator_count)]

    expression = format_number(numbers[0])
    for i in range(operator_count):
        expression += f" {operators[i]} {format_number(numbers[i + 1])}"

    expression = insert_random_parentheses(expression)  # 随机插入括号

    return expression


# 处理带分数或真分数字符串，将其转换为 fractions.Fraction 对象
def fractionize_expression(expression):
    # 查找带分数，例如 1'1/4 的格式，转换为 "1 + 1/4"
    expression = re.sub(r"(\d+)'(\d+)/(\d+)", r"(\1 + \2/\3)", expression)

    # 查找真分数，例如 3/5，转换为 Fraction(3, 5)
    expression = re.sub(r"(\d+)/(\d+)", r"fractions.Fraction(\1, \2)", expression)

    # 查找自然数，转换为 Fraction，自然数也可以被认为是分母为 1 的分数
    expression = re.sub(r"\b(\d+)\b", r"fractions.Fraction(\1)", expression)

    return expression


# 计算表达式结果
def calculate_answer(expression):
    try:
        # 将带分数和真分数都转换为标准的分数形式
        expression_for_eval = fractionize_expression(expression)

        # 使用 eval 进行分数计算
        result = eval(expression_for_eval, {"__builtins__": None}, {"fractions": fractions})

        return result  # 返回分数形式的结果
    except ZeroDivisionError:
        return None  # 防止除以 0 的情况


# 生成题目并写入文件
def generate_problems(n, range_limit):
    problems = []
    answers = []

    while len(problems) < n:
        expr = generate_expression(range_limit)
        answer = calculate_answer(expr)

        if answer is not None and answer >= 0:  # 过滤负数或无效的答案
            if expr not in problems:  # 防止重复题目
                # 替换运算符
                expr = expr.replace(" * ", " × ").replace(" / ", " ÷ ")
                expr = expr.replace("( ", "(").replace(" )", ")")

                problems.append(expr)
                formatted_answer = format_number(answer)  # 格式化答案
                answers.append(formatted_answer)

    return problems, answers


# 验证用户答案并输出评分结果
def validate_answers(exercise_data, answer_data):
    correct_count = 0
    wrong_count = 0
    correct_indices = []
    wrong_indices = []

    for i in range(len(exercise_data)):
        exercise = exercise_data[i].strip().split('. ')[1][:-2]
        answer = answer_data[i].strip().split('. ')[1]

        expr = exercise.replace(" × ", " * ").replace(" ÷ ", " / ")
        expr = expr.replace("(", "( ").replace(")", " )")

        if answer == format_number(calculate_answer(expr)):
            correct_count += 1
            correct_indices.append(i + 1)
        else:
            wrong_count += 1
            wrong_indices.append(i + 1)

    return correct_count, wrong_count, correct_indices, wrong_indices