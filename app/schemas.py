from pydantic import BaseModel, Field

class SentimentRequest(BaseModel):
    text: str = Field(..., description="감성을 분석할 텍스트", example="This API is really fast and awesome!")

class SentimentResponse(BaseModel):
    text: str
    sentiment: str = Field(..., description="positive, negative, neutral 중 하나")
    polarity: float = Field(..., description="-1.0 (부정적) 부터 1.0 (긍정적) 사이의 점수")
