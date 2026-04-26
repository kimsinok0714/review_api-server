from contextlib import asynccontextmanager
import logging
from dotenv import load_dotenv
from app.gemini_client import ReviewAnalyzer
from app.schemas import ReviewRequest, ReviewResponse
from pathlib import Path
from fastapi import FastAPI, HTTPException


logger = logging.getLogger(__name__)

env_path = Path(__file__).resolve().parent.parent / ".env"
logging.info(f"env_path : {env_path}")
load_dotenv(dotenv_path=env_path, override=False)


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        app.state.analyzer = ReviewAnalyzer()
        logger.info("고객 리뷰 분석기 초기화 완료")
    except ValueError as e:
        logger.info("고객 리뷰 분석기 초기화 실패")
        raise

    yield

    logger.info("고객 리뷰 분석 서비스 종료 중 ...")



app = FastAPI(
    title="고객 리뷰 분석 API",
    description="Gemini LLM 기반 고객 리뷰 감성 분석 API",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
def health_check():
    return {"status": "health"}


@app.post("/anlayze", response_model=ReviewResponse)
def analyze_review(request: ReviewRequest):
    try:
        result = app.state.analyzer.analyze(request.review_text)
        # dict를 언패킹(**)해서 ReviewResponse Pydantic 모델로 변환
        return ReviewResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))