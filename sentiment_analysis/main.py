from pathlib import Path
from transformers import pipeline
from typing import Dict, Any

LOCAL_MODEL_DIR = str(
    Path(__file__).with_name("models") / "roberta-base-finetuned-jd-binary-chinese"
)


class SentimentAnalyzer:
    def __init__(self):
        self.classifier = pipeline(
            "sentiment-analysis",
            model=LOCAL_MODEL_DIR,
            tokenizer=LOCAL_MODEL_DIR,
            device_map="auto",
        )

    def analyze(self, text: str) -> Dict[str, Any]:
        result = self.classifier(text)[0]
        label: str = result["label"]
        confidence: float = float(result["score"])

        sentiment_score = confidence if "positive" in label.lower() else -confidence
        return {
            "sentiment_score": float(sentiment_score),
            "label": label,
            "confidence": confidence,
        }


analyzer = SentimentAnalyzer()


def get_sentiment(text: str) -> Dict[str, Any]:
    return analyzer.analyze(text)


if __name__ == "__main__":
    print(get_sentiment("这台手机简直惊艳到我了！"))
    print(get_sentiment("原神实在太好玩了！"))
    print(get_sentiment("售后态度差到极致还骂人！"))
    print(get_sentiment("售后态度差到极致"))
