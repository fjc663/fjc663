import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba


# 预处理文本数据
def preprocess_text(text):
    # 中文分词，并去除停用词、标点符号等
    tokens = jieba.lcut(text)
    return ' '.join(tokens)


# 计算两篇论文的余弦相似度
def calculate_tfidf_similarity(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
        # 读取文本数据
        text1 = file1.read().strip()
        text2 = file2.read().strip()

    # 文本预处理
    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)

    # 使用 TF-IDF 计算文本向量
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # 计算余弦相似度
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    # 重复率是相似度的百分比
    return round(similarity * 100, 2)


def main():
    # 判断输入参数是否正确
    if len(sys.argv) != 4:
        print(
            "Usage: python main.py <original_file_path> <plagiarized_file_path> <ans_file_path>")
        return

    # 命令行后三个参数的输入
    original_file_path = sys.argv[1]
    plagiarized_file_path = sys.argv[2]
    output_file_path = sys.argv[3]

    # 计算输入论文的余弦相似度
    similarity_rate = calculate_tfidf_similarity(original_file_path, plagiarized_file_path)

    # 将查重结果写入.txt文件
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"{similarity_rate:.2f}")


if __name__ == "__main__":
    # 程序启动入口
    main()
