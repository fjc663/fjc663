import difflib

# 读取论文 A 和 B 的内容
with open(r"E:\study\软件工程\测试文本\orig.txt", 'r', encoding='utf-8') as file:
    paper_a_content = file.read()

with open(r"E:\study\软件工程\测试文本\orig_0.8_dis_1.txt", 'r', encoding='utf-8') as file:
    paper_b_content = file.read()

# 创建 SequenceMatcher 对象并进行比较
matcher = difflib.SequenceMatcher(None, paper_a_content, paper_b_content)
similarity_ratio = matcher.ratio()

print(f'论文 A 和 B 的相似度为：{similarity_ratio}')