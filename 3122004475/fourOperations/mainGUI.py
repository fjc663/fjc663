import os
import random
import fractions
import re
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkinter.filedialog import asksaveasfilename


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


# 生成题目并写入 GUI
def generate_problems_gui():
    try:
        n = int(entry_number_of_problems.get())
        r = int(entry_range_limit.get())
        if r <= 1:
            messagebox.showerror("输入错误", "数值范围必须大于1")
            return

        global problems, answers, is_get_ans

        is_get_ans = False
        # 清除 Treeview 中的所有条目
        for item in problems_list.get_children():
            problems_list.delete(item)

        problems = []
        answers = []

        while len(problems) < n:
            expr = generate_expression(r)
            answer = calculate_answer(expr)
            if answer is not None and answer >= 0:
                expr = expr.replace(" * ", " × ").replace(" / ", " ÷ ")
                problems.append(expr)
                answers.append(format_number(answer))

        # 在窗口中显示题目（答案列为空）
        for i, problem in enumerate(problems):
            problems_list.insert("", "end", iid=i, values=(f"{i + 1}. {problem} =", ""))

        # 启用生成答案按钮
        btn_generate_answers.config(state=tk.NORMAL)

    except ValueError:
        messagebox.showerror("输入错误", "请确保输入正确的数字")


# 生成答案
def generate_answers_gui():
    global is_get_ans
    is_get_ans = True
    # 更新 Treeview 中的条目，显示答案
    for i, answer in enumerate(answers):
        problems_list.item(i, values=(problems_list.item(i, 'values')[0], answer))


# 保存题目
def save_problems():
    # 检查问题列表是否为空
    if not problems_list.get_children():
        messagebox.showwarning("Warning", "请先生成题目")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as f:
            for child in problems_list.get_children():
                item = problems_list.item(child)
                problem = item['values'][0]
                f.write(f"{problem}\n")

        messagebox.showinfo("Success", "题目保存成功")
    else:
        messagebox.showinfo("Fail", "题目保存失败")


# 保存答案
def save_answers():
    # 检查答案列表是否为空
    if not is_get_ans:
        messagebox.showwarning("Warning", "请先生成答案")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as f:
            for index, child in enumerate(problems_list.get_children()):
                item = problems_list.item(child)
                answer = item['values'][1]
                f.write(f"{index + 1}. {answer}\n")
        messagebox.showinfo("Success", "答案保存成功")
    else:
        messagebox.showinfo("Fail", "答案保存失败")


# 文件选择部分
def select_file(entry, file_type):
    file_path = filedialog.askopenfilename(filetypes=[(file_type, "*.txt")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path.split('/')[-1])


# 保存结果
def save_results(correct_count, wrong_count, correct_indices, wrong_indices):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as f:
            f.write(f"Correct: {correct_count} ({', '.join(map(str, correct_indices))})\n")
            f.write(f"Wrong: {wrong_count} ({', '.join(map(str, wrong_indices))})\n")
        messagebox.showinfo("Success", "结果保存成功")
    else:
        messagebox.showinfo("Fail", '保存结果失败')


# 验证答案
def validate_answers_gui():
    problem_file = problem_file_entry.get()
    answer_file = answer_file_entry.get()

    if not problem_file or not answer_file:
        messagebox.showerror("错误", "请确保选择了题目文件和答案文件。")
        return

    if not os.path.exists(problem_file):
        messagebox.showerror("错误", "题目文件不存在。")
        return

    if not os.path.exists(answer_file):
        messagebox.showerror("错误", "答案文件不存在。")
        return

    # 假设 answers 是从题目文件中读取的答案
    with open(problem_file, 'r') as f:
        problems = f.readlines()
    with open(answer_file, 'r') as f:
        answers = f.readlines()

    correct_count = 0
    wrong_count = 0
    correct_indices = []
    wrong_indices = []

    for i, (problem, answer) in enumerate(zip(problems, answers)):
        problem = problem.strip().split('. ')[1][:-2]
        answer = answer.strip().split('. ')[1]

        expr = problem.replace(" × ", " * ").replace(" ÷ ", " / ")
        expr = expr.replace("(", "( ").replace(")", " )")

        if answer == format_number(calculate_answer(expr)):
            correct_count += 1
            correct_indices.append(i + 1)
        else:
            wrong_count += 1
            wrong_indices.append(i + 1)

    result_message = f"Correct: {correct_count} ({', '.join(map(str, correct_indices))})\n" \
                     f"Wrong: {wrong_count} ({', '.join(map(str, wrong_indices))})"

    # 如果选择保存结果，执行保存操作
    if save_results_var.get():
        save_results(correct_count, wrong_count, correct_indices, wrong_indices)

    messagebox.showinfo("结果", result_message)


# 是否生成答案
is_get_ans = False

# 创建主窗口
root = tk.Tk()
root.title("四则运算生成器")

# 问题生成区域
frame_generate = tk.Frame(root)
frame_generate.pack(pady=10)

tk.Label(frame_generate, text="题目数量:").grid(row=0, column=0)
entry_number_of_problems = tk.Entry(frame_generate)
entry_number_of_problems.grid(row=0, column=1)

tk.Label(frame_generate, text="数值范围:").grid(row=1, column=0)
entry_range_limit = tk.Entry(frame_generate)
entry_range_limit.grid(row=1, column=1)

btn_generate_problems = tk.Button(frame_generate, text="生成题目", command=generate_problems_gui)
btn_generate_problems.grid(row=2, column=0, padx=(40, 5), pady=10)

btn_generate_answers = tk.Button(frame_generate, text="生成答案", command=generate_answers_gui, state=tk.DISABLED)
btn_generate_answers.grid(row=2, column=1, padx=(5, 10), pady=10)


# 创建一个框架来包含 Treeview 和滚动条
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# 创建 Treeview 组件，设置两列（题目和答案）
problems_list = ttk.Treeview(frame, columns=("Problem", "Answer"), show="headings", height=10)
problems_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 设置每一列的标题和宽度
problems_list.heading("Problem", text="题目")
problems_list.heading("Answer", text="答案")
problems_list.column("Problem", width=250)
problems_list.column("Answer", width=150)

# 创建垂直滚动条
vsb = tk.Scrollbar(frame, orient="vertical", command=problems_list.yview)
vsb.pack(side='right', fill='y')

# 将滚动条与 Treeview 关联
problems_list.configure(yscrollcommand=vsb.set)

# 创建按钮的 Frame
buttons_frame = tk.Frame(root)
buttons_frame.pack(fill=tk.X, pady=10)

# 添加按钮
save_problems_button = tk.Button(buttons_frame, text="保存题目", command=save_problems)
save_problems_button.pack(side=tk.LEFT, padx=50)

save_answers_button = tk.Button(buttons_frame, text="保存答案", command=save_answers)
save_answers_button.pack(side=tk.RIGHT, padx=50)

# 文件选择和显示标签
tk.Label(root, text="选择题目文件:").pack(pady=5)
problem_file_entry = tk.Entry(root, width=50)
problem_file_entry.pack(pady=5)
tk.Button(root, text="选择文件", command=lambda: select_file(problem_file_entry, "题目文件")).pack(pady=5)

tk.Label(root, text="选择答案文件:").pack(pady=5)
answer_file_entry = tk.Entry(root, width=50)
answer_file_entry.pack(pady=5)
tk.Button(root, text="选择文件", command=lambda: select_file(answer_file_entry, "答案文件")).pack(pady=5)

# 创建复选框变量
save_results_var = tk.BooleanVar()

# 创建按钮和复选框
validate_button_frame = tk.Frame(root)
validate_button_frame.pack(pady=10)

validate_button = tk.Button(validate_button_frame, text="验证答案", command=validate_answers_gui)
validate_button.pack(side=tk.LEFT, padx=5)

save_result_check = tk.Checkbutton(validate_button_frame, text="保存答案", variable=save_results_var)
save_result_check.pack(side=tk.LEFT, padx=5)

root.mainloop()
