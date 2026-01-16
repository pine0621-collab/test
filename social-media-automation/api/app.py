"""
소셜 미디어 자동화 API

FastAPI 기반 REST API 서버
"""

import os
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

# 엔진 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(
    title="바리온랩스 소셜 미디어 자동화 API",
    description="LinkedIn/Instagram 콘텐츠 자동 생성 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Request/Response 모델 ===

class GenerateRequest(BaseModel):
    platform: str  # linkedin, instagram
    template_type: str  # thought_leadership, case_study, carousel, etc.
    variables: dict
    use_llm: bool = False


class GenerateResponse(BaseModel):
    success: bool
    platform: str
    content_type: str
    main_text: str
    hashtags: list[str]
    prompt: Optional[str] = None


class ScheduleRequest(BaseModel):
    platform: str
    content: str
    hashtags: list[str] = []
    scheduled_time: Optional[str] = None


class ScheduleResponse(BaseModel):
    success: bool
    post_id: str
    platform: str
    scheduled_time: str


class HashtagRequest(BaseModel):
    platform: str
    topic: str = "ai"
    include_brand: bool = True


class HashtagResponse(BaseModel):
    hashtags: list[str]
    formatted: str
    count: int


# === API 엔드포인트 ===

@app.get("/")
def root():
    """API 상태 확인"""
    return {
        "status": "running",
        "service": "소셜 미디어 자동화 API",
        "version": "1.0.0"
    }


@app.get("/api/templates")
def list_templates():
    """사용 가능한 템플릿 목록"""
    from engine import TemplateLoader

    loader = TemplateLoader()
    templates = loader.list_templates()

    return {
        "templates": templates,
        "platforms": {
            "linkedin": [t.split("/")[1] for t in templates if t.startswith("linkedin/")],
            "instagram": [t.split("/")[1] for t in templates if t.startswith("instagram/")]
        }
    }


@app.post("/api/generate", response_model=GenerateResponse)
def generate_content(request: GenerateRequest):
    """콘텐츠 생성"""
    from engine import SocialMediaContentGenerator, ContentRequest

    try:
        # LLM 클라이언트 설정 (옵션)
        llm_client = None
        if request.use_llm:
            api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY")
            if api_key:
                if os.environ.get("ANTHROPIC_API_KEY"):
                    import anthropic
                    llm_client = anthropic.Anthropic()
                elif os.environ.get("OPENAI_API_KEY"):
                    import openai
                    llm_client = openai.OpenAI()

        generator = SocialMediaContentGenerator(llm_client)

        content_request = ContentRequest(
            platform=request.platform,
            template_type=request.template_type,
            variables=request.variables
        )

        result = generator.generate_content(content_request)

        return GenerateResponse(
            success=True,
            platform=result.platform,
            content_type=result.content_type,
            main_text=result.main_text,
            hashtags=result.hashtags,
            prompt=result.metadata.get("prompt") if not request.use_llm else None
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/schedule", response_model=ScheduleResponse)
def schedule_post(request: ScheduleRequest):
    """포스트 스케줄"""
    from engine import PostingScheduler

    try:
        scheduler = PostingScheduler()

        scheduled_time = None
        if request.scheduled_time:
            scheduled_time = datetime.fromisoformat(request.scheduled_time)

        post = scheduler.add_post(
            platform=request.platform,
            content=request.content,
            hashtags=request.hashtags,
            scheduled_time=scheduled_time
        )

        return ScheduleResponse(
            success=True,
            post_id=post.id,
            platform=post.platform,
            scheduled_time=post.scheduled_time.isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/schedule")
def get_schedule(platform: str = None):
    """스케줄 조회"""
    from engine import PostingScheduler

    scheduler = PostingScheduler()
    posts = scheduler.get_pending_posts(platform=platform)

    return {
        "pending_posts": [p.to_dict() for p in posts],
        "summary": scheduler.get_schedule_summary()
    }


@app.get("/api/schedule/weekly")
def get_weekly_schedule():
    """주간 스케줄 생성"""
    from engine import PostingScheduler

    scheduler = PostingScheduler()
    return scheduler.generate_weekly_schedule()


@app.post("/api/hashtags", response_model=HashtagResponse)
def generate_hashtags(request: HashtagRequest):
    """해시태그 생성"""
    from engine import HashtagGenerator

    generator = HashtagGenerator()
    hashtags = generator.generate(
        platform=request.platform,
        topic=request.topic,
        include_brand=request.include_brand
    )

    return HashtagResponse(
        hashtags=hashtags,
        formatted=generator.format_hashtags(hashtags),
        count=len(hashtags)
    )


@app.get("/api/company")
def get_company_info():
    """회사 정보"""
    from engine import KnowledgeBase

    kb = KnowledgeBase()
    return {
        "company": kb.company["company"],
        "services": kb.get_services(),
        "projects": kb.get_projects()
    }


@app.get("/api/calendar")
def get_content_calendar(weeks: int = 4):
    """콘텐츠 캘린더"""
    from engine import SocialMediaContentGenerator

    generator = SocialMediaContentGenerator()
    return generator.get_content_calendar(weeks=weeks)


# === 건강 체크 ===

@app.get("/health")
def health_check():
    """헬스 체크"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
