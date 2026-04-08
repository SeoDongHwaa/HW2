from textblob import TextBlob

class SentimentModel:
    def __init__(self):
        # MLOps 파이프라인에서 실제 모델(Pickle, HuggingFace 등)을 로드하는 자리입니다.
        # 현재는 가벼운 분석을 위해 TextBlob을 사용합니다.
        pass
        
    def predict(self, text: str):
        # 분석 실행
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        # 극성 모델에 맞춰 긍/부정 판단 (-1.0 ~ 1.0)
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        return sentiment, polarity

# 싱글톤으로 유지하여 추론시 중복 객체 생성을 막음
sentiment_model = SentimentModel()
