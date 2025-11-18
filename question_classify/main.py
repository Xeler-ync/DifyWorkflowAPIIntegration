import json
import numpy as np
import pandas as pd
import jieba
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib  # 用于加载模型


# 加载模型和向量化器
def load_model_and_vectorizer(model_path, vectorizer_path):
    clf = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return clf, vectorizer


# 使用 jieba 进行分词
def preprocess_text(text):
    return " ".join(jieba.cut(text))


# 预测函数
def predict_text(text, clf, vectorizer):
    text = preprocess_text(text)
    text_tfidf = vectorizer.transform([text])
    return clf.predict_proba(text_tfidf)


# 格式化预测结果
def format_prediction(text, probabilities, actual_label, clf):
    # 获取标签列表
    labels = clf.classes_

    # 将概率和标签组合并排序
    label_probabilities = sorted(
        zip(labels, probabilities[0]), key=lambda x: x[1], reverse=True
    )

    # 格式化输出
    result = f"文本: {text}\n"
    result += f"实际标签: -> {actual_label} <-\n"  # 添加箭头突出显示实际标签
    for label, prob in label_probabilities:
        result += f"{label}: {prob:.4f}\n"
    return result


def get_top_n_predictions(
    text: str, clf: RandomForestClassifier, vectorizer: TfidfVectorizer, n: int = 3
) -> List[str]:
    """
    获取预测概率最高的前n个标签名称

    Args:
        text: 输入文本
        clf: 分类器模型
        vectorizer: TF-IDF向量化器
        n: 返回前n个预测结果，默认为3

    Returns:
        list: 包含前n个最可能的标签名称的列表
    """
    text = preprocess_text(text)
    text_tfidf = vectorizer.transform([text])
    probabilities = clf.predict_proba(text_tfidf)

    # 获取标签列表
    labels = clf.classes_

    # 将概率和标签组合并排序
    label_probabilities = sorted(
        zip(labels, probabilities[0]), key=lambda x: x[1], reverse=True
    )

    with open("question_classify\data\labels.json", "r", encoding="utf-8") as f:
        s = f.read()
        print(s)
        d = json.loads(s)

    # 返回前n个标签名称
    return [d[label] for label, _ in label_probabilities[:n]]


# 加载模型和向量化器
clf, vectorizer = load_model_and_vectorizer(
    "question_classify/models/random_forest_model.pkl",
    "question_classify/models/tfidf_vectorizer.pkl",
)
