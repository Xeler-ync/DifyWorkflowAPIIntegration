import json
import os
import numpy as np
import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib  # 用于保存模型


# 加载 labels.json 文件
def load_labels(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        labels = json.load(f)
    return labels


# 加载文本数据
def load_texts(labels):
    texts = []
    labels_list = []
    for label, file_name in labels.items():
        file_path = os.path.join(
            "data", file_name + ".txt"
        )  # 假设文本文件在 texts 文件夹中
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                texts.append(line.strip())
                labels_list.append(label)
    return texts, labels_list


# 使用 jieba 进行分词
def preprocess_text(texts):
    return [" ".join(jieba.cut(text)) for text in texts]


# 主函数
def main():
    # 加载标签和文本数据
    labels = load_labels("data/labels.json")
    texts, labels_list = load_texts(labels)

    # 对文本进行分词处理
    texts = preprocess_text(texts)

    # 将数据转换为 DataFrame
    data = pd.DataFrame({"text": texts, "label": labels_list})

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        data["text"], data["label"], test_size=0.2, random_state=42
    )

    # 文本向量化
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # 训练随机森林模型
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_tfidf, y_train)

    # 评估模型
    y_pred = clf.predict(X_test_tfidf)
    print("模型评估报告：")
    print(classification_report(y_test, y_pred))

    # 保存模型和向量化器
    joblib.dump(clf, "models/random_forest_model.pkl")
    joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")


if __name__ == "__main__":
    main()
