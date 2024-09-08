# 预处理文本数据
import re
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 设置结巴分词的日志级别
jieba.setLogLevel(jieba.logging.INFO)

def preprocess_text(text):
    try:
        # 使用正则表达式去除标点符号和特殊字符
        text = re.sub(r'[^\w\s]', '', text)

        # 中文分词
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

        if text1 == '' or text2 == '':
            return 0.00

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
