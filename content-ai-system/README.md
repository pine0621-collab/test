# 바리온랩스 콘텐츠 생성 AI 시스템

RAG (Retrieval-Augmented Generation) 기반의 바리온랩스 전용 콘텐츠 자동 생성 시스템입니다.

## 주요 기능

- **지식베이스 기반 콘텐츠 생성**: 회사 정보, 서비스, 프로젝트 실적 등을 활용한 맥락 있는 콘텐츠 생성
- **다양한 콘텐츠 유형 지원**: 블로그, 제안서, 이메일, 소셜 미디어, 회사 소개
- **프롬프트 템플릿 시스템**: 일관된 품질의 콘텐츠 생성을 위한 구조화된 템플릿
- **REST API 제공**: 외부 시스템과 쉬운 연동

## 시스템 구조

```
content-ai-system/
├── knowledge-base/           # 지식베이스
│   ├── company/             # 회사 정보
│   ├── services/            # 서비스 정보
│   ├── projects/            # 프로젝트 실적
│   ├── team/                # 팀 정보
│   └── faq/                 # FAQ
├── prompts/                  # 콘텐츠 생성 프롬프트 템플릿
│   ├── blog_post.yaml
│   ├── proposal.yaml
│   ├── email.yaml
│   ├── social_media.yaml
│   └── company_intro.yaml
├── engine/                   # 콘텐츠 생성 엔진
│   ├── knowledge_retriever.py
│   ├── template_loader.py
│   └── content_generator.py
├── api/                      # REST API
│   └── app.py
├── config/                   # 설정
│   └── config.yaml
├── examples/                 # 사용 예시
└── requirements.txt          # 의존성
```

## 빠른 시작

### 1. 설치

```bash
cd content-ai-system
pip install -r requirements.txt
```

### 2. API 서버 실행

```bash
uvicorn api.app:app --reload
```

서버가 `http://localhost:8000`에서 실행됩니다.

### 3. API 문서 확인

브라우저에서 `http://localhost:8000/docs` 열기 (Swagger UI)

## 사용 방법

### Python 라이브러리로 사용

```python
from engine.content_generator import ContentGenerator

generator = ContentGenerator()

# 블로그 포스트 프롬프트 생성
result = generator.create_blog_post(
    topic="기업의 AI 전환 전략",
    target_audience="기업 의사결정자",
    tone="전문적"
)

# LLM에 전달할 프롬프트
prompts = result.get_full_prompt()
print(prompts["system"])  # 시스템 프롬프트
print(prompts["user"])    # 사용자 프롬프트
```

### REST API로 사용

```bash
# 블로그 포스트 생성
curl -X POST http://localhost:8000/generate/blog-post \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI 교육의 중요성",
    "target_audience": "기업 의사결정자"
  }'

# 제안서 생성
curl -X POST http://localhost:8000/generate/proposal \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "ABC 기업",
    "industry": "금융/보험",
    "service_type": "AI 전환 교육",
    "client_needs": "전사 AI 역량 강화"
  }'

# 지식베이스 검색
curl -X POST http://localhost:8000/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{"query": "해커톤"}'
```

## 콘텐츠 유형

| 유형 | ID | 설명 |
|------|-----|------|
| 블로그 포스트 | `blog_post` | SEO 최적화된 블로그 콘텐츠 |
| 제안서 | `proposal` | 맞춤형 서비스 제안서 |
| 이메일 | `email` | 비즈니스 이메일 (첫 접촉, 후속, 미팅 요청 등) |
| 소셜 미디어 | `social_media` | LinkedIn, Twitter, Instagram 콘텐츠 |
| 회사 소개 | `company_intro` | 상황별 회사 소개 (엘리베이터 피치 ~ 상세) |

## LLM 연동

생성된 프롬프트를 다양한 LLM과 연동할 수 있습니다:

### OpenAI

```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": result.system_prompt},
        {"role": "user", "content": result.user_prompt}
    ]
)
```

### Anthropic Claude

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-opus-20240229",
    system=result.system_prompt,
    messages=[{"role": "user", "content": result.user_prompt}]
)
```

### 로컬 Ollama

```python
import httpx

response = httpx.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": f"System: {result.system_prompt}\n\nUser: {result.user_prompt}"
    }
)
```

## 지식베이스 업데이트

지식베이스 파일(JSON)을 직접 수정하여 정보를 업데이트할 수 있습니다:

- `knowledge-base/company/profile.json` - 회사 정보
- `knowledge-base/services/services.json` - 서비스 정보
- `knowledge-base/projects/portfolio.json` - 프로젝트 실적
- `knowledge-base/team/team.json` - 팀 정보
- `knowledge-base/faq/faq.json` - FAQ

## 프롬프트 템플릿 커스터마이징

`prompts/` 디렉토리의 YAML 파일을 수정하여 프롬프트를 커스터마이징할 수 있습니다.

```yaml
# prompts/blog_post.yaml
system_prompt: |
  당신은 바리온랩스의 콘텐츠 작성자입니다.
  # 여기에 커스텀 지침 추가

user_prompt_template: |
  다음 주제로 블로그 포스트를 작성해주세요:
  **주제**: {topic}
  # 템플릿 수정
```

## 프로덕션 배포

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 환경 변수

```bash
# LLM API 키 (선택)
export OPENAI_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key

# 서버 설정
export API_HOST=0.0.0.0
export API_PORT=8000
```

## 확장 계획

- [ ] 벡터 DB 기반 시맨틱 검색 (ChromaDB, Pinecone)
- [ ] 다국어 지원 (영어, 일본어)
- [ ] 콘텐츠 버전 관리
- [ ] A/B 테스트 기능
- [ ] 분석 대시보드

## 연락처

- **이메일**: ceo@baryon.ai, admin@baryon.ai
- **전화**: 010-9020-7775
- **웹사이트**: https://labs.baryon.ai/

---

© 2025 바리온랩스 (BaryonLABs). All rights reserved.
