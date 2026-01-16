# 바리온랩스 콘텐츠 생성 AI 활용 가이드

## 빠른 시작

### 1. 환경 설정

```bash
cd content-ai-system
pip install -r requirements.txt

# LLM API 키 설정 (둘 중 하나 선택)
export ANTHROPIC_API_KEY=your_anthropic_key
# 또는
export OPENAI_API_KEY=your_openai_key
```

### 2. API 서버 실행

```bash
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

---

## 실무 활용 시나리오

### 시나리오 1: 영업 제안서 자동 생성

잠재 고객과 미팅 후 맞춤형 제안서가 필요할 때:

```python
from engine.content_generator import ContentGenerator

generator = ContentGenerator()

# 제안서 생성
result = generator.create_proposal(
    client_name="현대자동차",
    industry="제조/자동차",
    service_type="AI 전환 교육 + 해커톤",
    client_needs="생산라인 최적화를 위한 AI 역량 내재화",
    budget_range="1억원 이상"
)

# 프롬프트를 LLM에 전달하여 실제 제안서 생성
prompts = result.get_full_prompt()
# → Claude/GPT API 호출
```

**활용 효과**: 제안서 작성 시간 2시간 → 10분으로 단축

---

### 시나리오 2: 주간 블로그 콘텐츠 생성

마케팅용 블로그 포스트를 정기적으로 발행할 때:

```python
# 이번 주 블로그 주제
topics = [
    "기업 AI 전환, 왜 교육이 먼저인가",
    "해커톤으로 시작하는 AI 혁신",
    "비봇코딩으로 AI 서비스 만들기"
]

for topic in topics:
    result = generator.create_blog_post(
        topic=topic,
        target_audience="기업 의사결정자",
        tone="전문적",
        include_points="""
        - 바리온랩스의 차별화된 접근법
        - 실제 고객 성공 사례 포함
        """
    )
    # LLM으로 콘텐츠 생성 후 검토
```

**활용 효과**: 월 4개 블로그 포스트 자동화

---

### 시나리오 3: 콜드 이메일 캠페인

신규 고객 발굴을 위한 이메일 작성:

```python
# 타겟 기업 목록
prospects = [
    {"name": "김철수", "role": "DT추진팀장", "company": "롯데"},
    {"name": "이영희", "role": "인재개발본부장", "company": "SK"},
]

for prospect in prospects:
    result = generator.create_email(
        recipient_name=prospect["name"],
        recipient_role=prospect["role"],
        email_type="첫 접촉",
        purpose=f"{prospect['company']}의 AI 역량 강화 협력 제안",
        key_message="실무 중심 AI 교육으로 즉시 적용 가능한 역량 확보",
        desired_action="15분 줌미팅 요청",
        context="AI 전환에 관심 있는 기업 대상"
    )
```

**활용 효과**: 개인화된 영업 이메일 대량 생성

---

### 시나리오 4: 소셜 미디어 운영

LinkedIn, Instagram 콘텐츠 자동화:

```python
# 프로젝트 완료 후 LinkedIn 포스트
result = generator.create_social_media(
    platform="LinkedIn",
    content_type="프로젝트 완료",
    topic="한화생명 AI 해커톤 성공 완료",
    key_message="48시간 만에 10개의 AI 프로토타입 탄생",
    tone="전문적"
)

# Instagram용 짧은 콘텐츠
result_ig = generator.create_social_media(
    platform="Instagram",
    content_type="인사이트 공유",
    topic="AI 시대 생존 전략",
    key_message="배우는 조직만이 살아남는다",
    tone="친근함"
)
```

**활용 효과**: 일관된 브랜드 메시지로 주 3회 포스팅

---

### 시나리오 5: 네트워킹 행사 대비

컨퍼런스, 행사에서 회사 소개할 때:

```python
# 30초 엘리베이터 피치
pitch = generator.create_company_intro(
    situation="네트워킹 행사",
    audience="기업 의사결정자",
    version="elevator_pitch",
    emphasis="AI 교육 역량"
)

# 5분 상세 소개
detailed = generator.create_company_intro(
    situation="고객 미팅",
    audience="인사/교육 담당자",
    version="detailed",
    emphasis="종합"
)
```

---

## REST API 활용

### n8n/Zapier 연동

외부 자동화 도구와 연동하여 워크플로우 자동화:

```bash
# 제안서 생성 API
curl -X POST http://localhost:8000/generate/proposal \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "ABC기업",
    "industry": "금융",
    "service_type": "AI 컨설팅",
    "client_needs": "업무 자동화"
  }'
```

### Slack 봇 연동

Slack에서 직접 콘텐츠 생성:

```
/baryon 블로그 "AI 교육의 중요성"
→ 블로그 포스트 초안 자동 생성

/baryon 제안서 "삼성전자" "제조" "해커톤"
→ 맞춤 제안서 자동 생성
```

---

## 지식베이스 업데이트

새로운 프로젝트 완료 시 지식베이스 업데이트:

### 프로젝트 추가

```json
// knowledge-base/projects/portfolio.json 에 추가
{
  "id": "project_new",
  "client": "새 고객사",
  "period": "2026.01",
  "service": "AI 해커톤",
  "description": "프로젝트 설명",
  "results": ["성과 1", "성과 2"],
  "testimonial": "고객 후기"
}
```

### 서비스 업데이트

```json
// knowledge-base/services/services.json 수정
// 새로운 서비스나 가격 정보 추가
```

---

## 추천 워크플로우

### 월간 콘텐츠 캘린더

| 주차 | 콘텐츠 유형 | 자동화 대상 |
|------|------------|------------|
| 1주 | 블로그 포스트 | `create_blog_post()` |
| 2주 | LinkedIn 3회 | `create_social_media()` |
| 3주 | 뉴스레터 | `create_email(email_type="뉴스레터")` |
| 4주 | 사례 연구 | `create_blog_post()` + 프로젝트 데이터 |

### 영업 파이프라인

```
리드 발굴 → 콜드 이메일 (자동) → 미팅 확정 → 제안서 (자동) → 계약
```

---

## 비용 절감 효과 (예상)

| 콘텐츠 유형 | 기존 소요시간 | 자동화 후 | 절감률 |
|------------|--------------|----------|--------|
| 제안서 | 2시간 | 15분 | 87% |
| 블로그 포스트 | 3시간 | 30분 | 83% |
| 영업 이메일 | 30분/건 | 3분/건 | 90% |
| 소셜 미디어 | 1시간 | 10분 | 83% |

**월간 총 절감**: 약 40시간 (주 10시간)

---

## 다음 단계

1. **즉시 시작**: API 서버 실행 후 블로그/이메일 생성 테스트
2. **워크플로우 구축**: n8n으로 주간 콘텐츠 자동 생성 파이프라인 구축
3. **지식베이스 확장**: 새 프로젝트/서비스 정보 지속 업데이트
4. **Slack 연동**: 팀원 누구나 쉽게 콘텐츠 생성 가능하도록

---

## 문의

- **이메일**: ceo@baryon.ai
- **전화**: 010-9020-7775
- **웹사이트**: https://labs.baryon.ai/

---

*작성일: 2026-01-16*
