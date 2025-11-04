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
    probabilities = clf.predict_proba(text_tfidf)
    return probabilities


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

    # 返回前n个标签名称
    return [label for label, _ in label_probabilities[:n]]


# 加载模型和向量化器
clf, vectorizer = load_model_and_vectorizer(
    "models/random_forest_model.pkl", "models/tfidf_vectorizer.pkl"
)


# 主函数
def main():

    # 示例文本预测
    print(
        format_prediction(
            "酒店官方联系电话",
            predict_text("酒店官方联系电话", clf, vectorizer),
            "酒店概览与核心身份",
            clf,
        )
    )
    print(
        format_prediction(
            "酒店设计风格",
            predict_text("酒店设计风格", clf, vectorizer),
            "建筑与设计风格",
            clf,
        )
    )
    print(
        format_prediction(
            "酒店的历史",
            predict_text("酒店的历史", clf, vectorizer),
            "历史与背景故事",
            clf,
        )
    )
    print(
        format_prediction(
            "酒店开房多少钱",
            predict_text("酒店开房多少钱", clf, vectorizer),
            "客房与套房类型",
            clf,
        )
    )
    print(
        format_prediction(
            "酒店有没有私人司机服务",
            predict_text("酒店有没有私人司机服务", clf, vectorizer),
            "服务与特色体验",
            clf,
        )
    )
    print(
        format_prediction(
            "酒店有没有泳池",
            predict_text("酒店有没有泳池", clf, vectorizer),
            "餐饮与娱乐设施",
            clf,
        )
    )
    print(
        format_prediction(
            "酒店附近有没有地铁站",
            predict_text("酒店附近有没有地铁站", clf, vectorizer),
            "交通与地理位置",
            clf,
        )
    )


if __name__ == "__main__":
    main()
