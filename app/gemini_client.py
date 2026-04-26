# Google Gemini AI API를 사용해 리뷰를 분석하는 클라이언트 모듈입니다.
import logging
import os
import json
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


# Gemini가 반환할 JSON 응답의 스키마 정의
REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "sentiment": {"type" : "string"},
        "category": {"type" : "string"},
        "summary": {"type" : "string"},
        "confidence": {"type" : "number"}
    },
    "required": ["sentiment", "category", "summary", "confidence"]
}

class ReviewAnalyzer:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API KEY가 설정되지 않습니다.")
        # Google Generative AI 클라이언트 인스턴스를 생성하는 부분입니다. 
        # 이후 이 self.client를 통해 Gemini 모델에 요청을 보냅니다.
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        logger.info("리뷰 분석기 초기화 완료")
        

    def analyze(self, review_text:str) -> dict:
        prompt = f"""주어진 리뷰 텍스트를 분석해주세요.

                리뷰 : {review_text}

                다음 기준으로 분석하세요:
                - sentiment : '긍정', '부정', '중립' 중 하나
                - category : '배송', '품질', '가격', '고객서비스', '기타' 중 하나
                - summary : 리뷰 핵심을 1~2문장으로 요약
                - confidence : 0.0 ~ 1.0 사이의 신뢰도
                """
        
        # Gemini API에 콘텐츠 생성 요청을 보내는 핵심 코드입니다.
        response = self.client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt,
            config = types.GenerateContentConfig( # 응답 형식 설정
                response_mime_type="application/json",
                response_schema=REVIEW_SCHEMA # 반환받을 JSON의 구조를 REVIEW_SCHEMA로 강제
            )
        )

        result = json.loads(response.text) #  JSON 형식의 문자열(str) 을 Python 딕셔너리(dict) 로 파싱
        
        logger.info(f"result : {result}")

        return result