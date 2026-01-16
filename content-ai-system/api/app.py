"""
바리온랩스 콘텐츠 생성 AI API
FastAPI 기반 REST API 서버
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager

# 프로젝트 루트를 path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from engine.content_generator import ContentGenerator, ContentType, ContentRequest
from engine.knowledge_retriever import KnowledgeRetriever


# === Pydantic 모델 ===

class ContentGenerationRequest(BaseModel):
    """콘텐츠 생성 요청 모델"""
    content_type: str = Field(..., description="콘텐츠 유형 (blog_post, proposal, email, social_media, company_intro)")
    parameters: Dict[str, Any] = Field(..., description="콘텐츠 생성 파라미터")
    include_knowledge: bool = Field(True, description="지식베이스 포함 여부")
    custom_context: Optional[str] = Field(None, description="추가 컨텍스트")


class BlogPostRequest(BaseModel):
    """블로그 포스트 요청"""
    topic: str = Field(..., description="블로그 주제")
    target_audience: str = Field("기업 의사결정자", description="타겟 독자")
    tone: str = Field("전문적", description="톤")
    length: str = Field("중간 (800-1200자)", description="길이")
    include_points: str = Field("", description="포함할 내용")


class ProposalRequest(BaseModel):
    """제안서 요청"""
    client_name: str = Field(..., description="고객사명")
    industry: str = Field(..., description="산업")
    service_type: str = Field(..., description="서비스 유형")
    client_needs: str = Field(..., description="고객 니즈")
    budget_range: str = Field("협의 필요", description="예산 범위")


class EmailRequest(BaseModel):
    """이메일 요청"""
    recipient_name: str = Field(..., description="수신자명")
    recipient_role: str = Field("", description="수신자 직책")
    email_type: str = Field(..., description="이메일 유형")
    purpose: str = Field(..., description="목적")
    key_message: str = Field(..., description="핵심 메시지")
    desired_action: str = Field(..., description="요청 액션")
    context: str = Field("", description="추가 맥락")


class SocialMediaRequest(BaseModel):
    """소셜 미디어 요청"""
    platform: str = Field(..., description="플랫폼")
    content_type: str = Field(..., description="콘텐츠 유형")
    topic: str = Field(..., description="주제")
    key_message: str = Field(..., description="핵심 메시지")
    tone: str = Field("전문적", description="톤")


class CompanyIntroRequest(BaseModel):
    """회사 소개 요청"""
    situation: str = Field(..., description="상황")
    audience: str = Field(..., description="대상")
    version: str = Field("standard", description="버전")
    emphasis: str = Field("종합", description="강조점")
    tone: str = Field("전문적", description="톤")


class KnowledgeSearchRequest(BaseModel):
    """지식베이스 검색 요청"""
    query: str = Field(..., description="검색어")
    categories: Optional[List[str]] = Field(None, description="검색 카테고리")


# === 앱 설정 ===

@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 생명주기 관리"""
    # 시작 시
    app.state.generator = ContentGenerator()
    app.state.retriever = KnowledgeRetriever()
    yield
    # 종료 시
    pass


app = FastAPI(
    title="바리온랩스 콘텐츠 생성 AI API",
    description="RAG 기반 콘텐츠 자동 생성 서비스",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === API 엔드포인트 ===

@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "service": "바리온랩스 콘텐츠 생성 AI",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/content-types")
async def list_content_types():
    """사용 가능한 콘텐츠 유형 목록"""
    return app.state.generator.list_content_types()


@app.get("/content-types/{content_type}/parameters")
async def get_content_type_params(content_type: str):
    """콘텐츠 유형별 파라미터 정보"""
    params = app.state.generator.get_content_type_params(content_type)
    if not params:
        raise HTTPException(status_code=404, detail=f"콘텐츠 유형을 찾을 수 없습니다: {content_type}")
    return params


@app.post("/generate")
async def generate_content(request: ContentGenerationRequest):
    """범용 콘텐츠 생성"""
    try:
        content_type = ContentType(request.content_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 콘텐츠 유형: {request.content_type}"
        )

    try:
        content_request = ContentRequest(
            content_type=content_type,
            parameters=request.parameters,
            include_knowledge=request.include_knowledge,
            custom_context=request.custom_context
        )
        result = app.state.generator.generate(content_request)
        return result.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/generate/blog-post")
async def generate_blog_post(request: BlogPostRequest):
    """블로그 포스트 생성"""
    result = app.state.generator.create_blog_post(
        topic=request.topic,
        target_audience=request.target_audience,
        tone=request.tone,
        length=request.length,
        include_points=request.include_points
    )
    return result.to_dict()


@app.post("/generate/proposal")
async def generate_proposal(request: ProposalRequest):
    """제안서 생성"""
    result = app.state.generator.create_proposal(
        client_name=request.client_name,
        industry=request.industry,
        service_type=request.service_type,
        client_needs=request.client_needs,
        budget_range=request.budget_range
    )
    return result.to_dict()


@app.post("/generate/email")
async def generate_email(request: EmailRequest):
    """이메일 생성"""
    result = app.state.generator.create_email(
        recipient_name=request.recipient_name,
        recipient_role=request.recipient_role,
        email_type=request.email_type,
        purpose=request.purpose,
        key_message=request.key_message,
        desired_action=request.desired_action,
        context=request.context
    )
    return result.to_dict()


@app.post("/generate/social-media")
async def generate_social_media(request: SocialMediaRequest):
    """소셜 미디어 콘텐츠 생성"""
    result = app.state.generator.create_social_media(
        platform=request.platform,
        content_type=request.content_type,
        topic=request.topic,
        key_message=request.key_message,
        tone=request.tone
    )
    return result.to_dict()


@app.post("/generate/company-intro")
async def generate_company_intro(request: CompanyIntroRequest):
    """회사 소개 생성"""
    result = app.state.generator.create_company_intro(
        situation=request.situation,
        audience=request.audience,
        version=request.version,
        emphasis=request.emphasis,
        tone=request.tone
    )
    return result.to_dict()


# === 지식베이스 API ===

@app.get("/knowledge/company")
async def get_company_info():
    """회사 정보 조회"""
    return app.state.retriever.get_company_info()


@app.get("/knowledge/services")
async def get_services(service_id: Optional[str] = Query(None)):
    """서비스 정보 조회"""
    return app.state.retriever.get_services(service_id)


@app.get("/knowledge/team")
async def get_team_info():
    """팀 정보 조회"""
    return app.state.retriever.get_team_info()


@app.get("/knowledge/projects")
async def get_projects(project_type: Optional[str] = Query(None)):
    """프로젝트 실적 조회"""
    return app.state.retriever.get_projects(project_type)


@app.get("/knowledge/faq")
async def get_faq(category: Optional[str] = Query(None)):
    """FAQ 조회"""
    return app.state.retriever.get_faqs(category)


@app.post("/knowledge/search")
async def search_knowledge(request: KnowledgeSearchRequest):
    """지식베이스 검색"""
    from engine.knowledge_retriever import KnowledgeCategory

    categories = None
    if request.categories:
        try:
            categories = [KnowledgeCategory(c) for c in request.categories]
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"잘못된 카테고리: {e}")

    results = app.state.retriever.search(request.query, categories)
    return [
        {
            "category": item.category.value,
            "relevance_score": item.relevance_score,
            "content": item.content
        }
        for item in results
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
