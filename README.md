# review_api-server

Gemini LLM을 사용해 고객 리뷰를 분석하는 FastAPI 서버입니다.

## 주요 기능

- 리뷰 텍스트 감성 분석: `긍정`, `부정`, `중립`
- 리뷰 카테고리 분류: `배송`, `품질`, `가격`, `고객서비스`, `기타`
- 리뷰 요약 생성
- 분석 신뢰도(`0.0 ~ 1.0`) 반환

## 프로젝트 구조

```
review_api-server/
├── app/
│   ├── gemini_client.py
│   ├── main.py
│   └── schemas.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## 요구 사항

- Python 3.10+
- Gemini API Key

## 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 아래 값을 설정합니다.

```env
GEMINI_API_KEY=여기에_실제_API_KEY
```

## 로컬 실행

### 1) 의존성 설치

```bash
pip install -r requirements.txt
```

### 2) 서버 실행

```bash
uvicorn app.main:app --reload
```

기본 실행 주소: `http://127.0.0.1:8000`

## Docker 실행

### 1) 이미지 빌드

```bash
docker build -t review-api .
```

### 2) 컨테이너 실행

```bash
docker run -d --name review-api --env-file .env -p 8005:8005 review-api
```

### 3) 로그 확인

```bash
docker logs -f review-api
```

컨테이너 실행 주소: `http://127.0.0.1:8005`

## API 명세

### Health Check

- Method: `GET`
- Path: `/health`

응답 예시:

```json
{
  "status": "health"
}
```

### 리뷰 분석

- Method: `POST`
- Path: `/anlayze`

참고: 현재 코드 기준 경로는 `/anlayze`(오탈자 포함)입니다.

요청 본문 예시:

```json
{
  "review_text": "배송이 너무 느려요. 제품은 괜찮았지만 배송이 정말 실망스러웠습니다."
}
```

응답 예시:

```json
{
  "sentiment": "부정",
  "category": "배송",
  "summary": "배송 속도에 대한 불만이 크지만 제품 자체 품질은 괜찮다고 평가했습니다.",
  "confidence": 0.92
}
```

## 빠른 테스트

### 로컬 서버(8000) 테스트

```bash
curl -X POST "http://127.0.0.1:8000/anlayze" \
	-H "Content-Type: application/json" \
	-d '{"review_text":"가격은 좋은데 고객센터 응대가 아쉬웠어요."}'
```

### Docker 서버(8005) 테스트

```bash
curl -X POST "http://127.0.0.1:8005/anlayze" \
	-H "Content-Type: application/json" \
	-d '{"review_text":"배송이 빠르고 포장도 깔끔했어요."}'
```

## 트러블슈팅

### 1) `[Errno 98] Address already in use`

이미 같은 포트(예: 8000)를 다른 프로세스가 사용 중인 상태입니다.

```bash
fuser -k 8000/tcp
```

또는 다른 포트로 실행합니다.

```bash
uvicorn app.main:app --reload --port 8001
```

### 2) `API KEY가 설정되지 않습니다.`

`.env` 파일에 `GEMINI_API_KEY`가 없거나 컨테이너에 전달되지 않은 경우입니다.

- 로컬: `.env`에 키 설정
- Docker: `--env-file .env` 또는 `-e GEMINI_API_KEY=...` 옵션 사용

### 3) `403 PERMISSION_DENIED ... API key was reported as leaked`

현재 API 키가 유출로 감지되어 차단된 상태입니다.

- 새 Gemini API 키를 발급
- `.env`의 `GEMINI_API_KEY` 교체
- 서버/컨테이너 재시작
