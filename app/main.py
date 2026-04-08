from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import SentimentRequest, SentimentResponse
from app.model import sentiment_model

app = FastAPI(
    title="Sentiment Analysis API",
    description="MLOps 파이프라인 구축을 위한 간단한 텍스트 감성 분석 API 서버입니다.",
    version="1.0.0"
)

# CORS 설정 (프론트엔드 연동이 필요할 경우를 대비)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API 서버가 정상적으로 실행 중입니다. /docs 로 이동하여 Swagger UI를 확인하세요."}

@app.get("/health")
def health_check():
    """헬스 체크를 위한 엔드포인트입니다. 배포 시 정상 동작 여부를 확인합니다."""
    return {"status": "ok"}

@app.post("/predict", response_model=SentimentResponse)
def predict_sentiment(request: SentimentRequest):
    """
    텍스트를 입력받아 긍정적(positive), 부정적(negative), 중립적(neutral)인지 예측합니다.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="텍스트가 비어있습니다. 입력값을 확인해주세요.")
        
    try:
        sentiment, polarity = sentiment_model.predict(request.text)
        return SentimentResponse(
            text=request.text,
            sentiment=sentiment,
            polarity=polarity
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"예측 중 오류가 발생했습니다: {str(e)}")
