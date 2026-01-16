# 소셜 미디어 자동화 시스템

바리온랩스 LinkedIn/Instagram 콘텐츠 자동 생성 및 포스팅 시스템

## 구조

```
social-media-automation/
├── knowledge-base/           # 회사 지식베이스
│   ├── company.json          # 회사 정보
│   └── content-themes.json   # 콘텐츠 테마 및 전략
├── templates/                # 콘텐츠 템플릿
│   ├── linkedin/
│   │   ├── thought_leadership.yaml
│   │   ├── case_study.yaml
│   │   └── announcement.yaml
│   └── instagram/
│       ├── carousel.yaml
│       ├── reels.yaml
│       └── story.yaml
├── engine/                   # 자동화 엔진
│   ├── content_generator.py  # 콘텐츠 생성
│   ├── hashtag_generator.py  # 해시태그 생성
│   └── scheduler.py          # 스케줄링
├── n8n-workflows/            # n8n 워크플로우
│   ├── linkedin_auto_post.json
│   └── instagram_auto_post.json
├── api/                      # REST API
│   └── app.py
└── config/
    └── settings.yaml
```

## 빠른 시작

### 1. 설치

```bash
cd social-media-automation
pip install -r requirements.txt
```

### 2. 환경변수 설정

```bash
# LLM API (선택)
export ANTHROPIC_API_KEY=your_key
# 또는
export OPENAI_API_KEY=your_key

# Instagram (Meta Graph API)
export INSTAGRAM_ACCESS_TOKEN=your_token
export INSTAGRAM_BUSINESS_ACCOUNT_ID=your_id
```

### 3. API 서버 실행

```bash
uvicorn api.app:app --reload
```

### 4. API 문서 확인

```
http://localhost:8000/docs
```

## 사용 방법

### Python으로 직접 사용

```python
from engine import create_linkedin_post, create_instagram_post

# LinkedIn Thought Leadership 포스트 생성
content = create_linkedin_post(
    template_type="thought_leadership",
    variables={
        "topic": "AI 도입 실패 원인",
        "key_insight": "기술보다 조직 문화가 중요",
        "supporting_points": "1. 교육 부재, 2. 목표 부재, 3. 지원 부족",
        "example": "한화생명 해커톤 사례",
        "cta_question": "여러분의 경험은 어떠셨나요?"
    }
)
print(content.main_text)

# Instagram 캐러셀 포스트 생성
content = create_instagram_post(
    template_type="carousel",
    variables={
        "topic": "AI 프롬프트 작성법",
        "points": ["구체적으로 요청", "맥락 제공", "예시 포함", "역할 부여", "단계별 진행"],
        "target_audience": "AI 초보자",
        "cta": "저장하고 나중에 활용하기"
    }
)
print(content.main_text)
```

### API 사용

```bash
# 콘텐츠 생성
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "linkedin",
    "template_type": "thought_leadership",
    "variables": {
      "topic": "AI 트렌드",
      "key_insight": "2024년 AI 도입 가속화",
      "supporting_points": "1. 비용 절감, 2. 생산성 향상",
      "cta_question": "어떤 AI를 사용하고 계신가요?"
    }
  }'

# 해시태그 생성
curl -X POST http://localhost:8000/api/hashtags \
  -H "Content-Type: application/json" \
  -d '{"platform": "instagram", "topic": "ai"}'

# 주간 스케줄 조회
curl http://localhost:8000/api/schedule/weekly
```

## n8n 워크플로우 설정

### LinkedIn 자동 포스팅

1. n8n에서 `n8n-workflows/linkedin_auto_post.json` 임포트
2. LinkedIn OAuth2 자격 증명 설정
3. 환경변수 설정:
   - `CONTENT_API_URL`: API 서버 URL
4. 워크플로우 활성화

### Instagram 자동 포스팅

1. n8n에서 `n8n-workflows/instagram_auto_post.json` 임포트
2. Meta Graph API 토큰 설정:
   - Instagram Business Account 필요
   - Facebook Page 연결 필요
3. 환경변수 설정:
   - `INSTAGRAM_ACCESS_TOKEN`
   - `INSTAGRAM_BUSINESS_ACCOUNT_ID`
4. 워크플로우 활성화

## API 연동 가이드

### LinkedIn API

LinkedIn은 공식 API 접근이 제한적입니다. 권장 방법:

1. **LinkedIn Marketing API** (파트너 전용)
   - 광고 계정 필요
   - 승인 과정 필요

2. **n8n LinkedIn 노드** (권장)
   - OAuth2 인증
   - 기본 포스팅 기능 제공

3. **Buffer/Hootsuite 연동**
   - 중간 서비스를 통한 포스팅
   - API 제한 회피

### Instagram API (Meta Graph API)

Instagram Business Account가 필요합니다.

```bash
# 1. 미디어 컨테이너 생성
curl -X POST \
  "https://graph.facebook.com/v18.0/{ig-user-id}/media" \
  -d "image_url={image-url}" \
  -d "caption={caption}" \
  -d "access_token={access-token}"

# 2. 미디어 발행
curl -X POST \
  "https://graph.facebook.com/v18.0/{ig-user-id}/media_publish" \
  -d "creation_id={creation-id}" \
  -d "access_token={access-token}"
```

## 콘텐츠 전략

### LinkedIn (B2B 전문가 타겟)

| 콘텐츠 유형 | 빈도 | 최적 시간 |
|------------|------|----------|
| Thought Leadership | 주 2회 | 화/목 09:00 |
| Case Study | 격주 | 수 12:00 |
| Announcement | 필요시 | 평일 오전 |

### Instagram (일반 대중 타겟)

| 콘텐츠 유형 | 빈도 | 최적 시간 |
|------------|------|----------|
| Carousel | 주 2회 | 월/금 18:00 |
| Reels | 주 2회 | 수/토 21:00 |
| Story | 매일 | 12:00, 18:00 |

## 해시태그 전략

### LinkedIn (3-5개)
- 브랜드: #바리온랩스 #BaryonLabs
- 주제: #AI #디지털전환 #AI교육

### Instagram (10-15개)
- 브랜드: #바리온랩스 #AI혁신
- 주제: #AI #인공지능 #ChatGPT #생성형AI
- 트렌드: #AI팁 #업무자동화 #스마트워크

## 문의

- 이메일: ceo@baryon.ai
- 웹사이트: https://labs.baryon.ai/
