import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba
import os

# 设置结巴分词的日志级别
jieba.setLogLevel(jieba.logging.INFO)


# 预处理文本数据
def preprocess_text(text):
    try:
        # 中文分词，并去除停用词、标点符号等
        tokens = jieba.lcut(text)
        return ' '.join(tokens)
    except Exception as e:
        print(f"Error in preprocess_text: {e}")
        return ""


# 计算两篇论文的余弦相似度
def calculate_tfidf_similarity(file1_path, file2_path):
    try:
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

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None
    except IOError as e:
        print(f"I/O error: {e}")
        return None
    except Exception as e:
        print(f"Error in calculate_tfidf_similarity: {e}")
        return None


def main():
    # 判断输入参数是否正确
    if len(sys.argv) != 4:
        print("Usage: python main.py <original_file_path> <plagiarized_file_path> <ans_file_path>")
        return

    # 命令行后三个参数的输入
    original_file_path = sys.argv[1]
    plagiarized_file_path = sys.argv[2]
    output_file_path = sys.argv[3]

    # 检查文件路径是否存在
    if not os.path.isfile(original_file_path):
        print(f"Original file not found: {original_file_path}")
        return

    if not os.path.isfile(plagiarized_file_path):
        print(f"Plagiarized file not found: {plagiarized_file_path}")
        return

    # 计算输入论文的余弦相似度
    similarity_rate = calculate_tfidf_similarity(original_file_path, plagiarized_file_path)

    if similarity_rate is not None:
        try:
            # 将查重结果写入.txt文件
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(f"{similarity_rate:.2f}")
            print(f"论文查重完毕，查重结果保存在：{output_file_path}")
        except IOError as e:
            print(f"Error writing to file: {e}")
    else:
        print("Failed to calculate similarity.")


if __name__ == "__main__":
    # 程序启动入口
    main()
