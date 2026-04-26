
from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    review_text: str = Field(
        ..., 
        description="분석할 고객 리뷰 텍스트", min_length=1, max_length=5000, 
        examples="배송이 너무 느려요. 제품은 괜찮았지만 배송이 정말 실망스러웠습니다."
    )


class ReviewResponse(BaseModel):
    sentiment: str = Field(..., description="감성 분석 결과", examples=["긍정", "부정", "중립"])
    category: str = Field(..., description="리뷰 카테고리", examples=["배송", "품질", "가격", "서비스", "기타" ])
    summary: str = Field(..., description="리뷰 요약")
    confidence: float = Field(..., description="분석 신뢰도 (0.0~1.0)", ge=0.0, le= 1.0)

                               


    

    




