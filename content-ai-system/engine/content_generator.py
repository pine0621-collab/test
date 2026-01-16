"""
바리온랩스 콘텐츠 생성 엔진
RAG 기반 콘텐츠 자동 생성
"""

import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

from .knowledge_retriever import KnowledgeRetriever
from .template_loader import TemplateLoader, PromptTemplate


class ContentType(Enum):
    """콘텐츠 유형"""
    BLOG_POST = "blog_post"
    PROPOSAL = "proposal"
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"
    COMPANY_INTRO = "company_intro"


@dataclass
class ContentRequest:
    """콘텐츠 생성 요청"""
    content_type: ContentType
    parameters: Dict[str, Any]
    include_knowledge: bool = True
    custom_context: Optional[str] = None


@dataclass
class GeneratedContent:
    """생성된 콘텐츠"""
    content_type: str
    system_prompt: str
    user_prompt: str
    knowledge_context: str
    parameters_used: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def get_full_prompt(self) -> Dict[str, str]:
        """LLM에 전달할 전체 프롬프트"""
        return {
            "system": self.system_prompt,
            "user": self.user_prompt
        }


class ContentGenerator:
    """콘텐츠 생성기"""

    def __init__(self,
                 knowledge_base_path: str = None,
                 templates_path: str = None):
        """
        Args:
            knowledge_base_path: 지식베이스 경로
            templates_path: 템플릿 경로
        """
        self.retriever = KnowledgeRetriever(knowledge_base_path)
        self.template_loader = TemplateLoader(templates_path)

    def generate(self, request: ContentRequest) -> GeneratedContent:
        """
        콘텐츠 생성 프롬프트 준비

        Args:
            request: 콘텐츠 생성 요청

        Returns:
            생성된 콘텐츠 (프롬프트)
        """
        # 템플릿 로드
        template = self.template_loader.get_template(request.content_type.value)
        if not template:
            raise ValueError(f"템플릿을 찾을 수 없습니다: {request.content_type.value}")

        # 파라미터 검증
        validation = self.template_loader.validate_parameters(
            request.content_type.value,
            request.parameters
        )
        if validation["errors"]:
            raise ValueError(f"파라미터 오류: {validation['errors']}")

        # 지식베이스 컨텍스트 준비
        knowledge_context = ""
        if request.include_knowledge:
            context_data = self.retriever.get_context_for_content_type(
                request.content_type.value
            )
            knowledge_context = self.retriever.format_context_for_prompt(context_data)

        # 사용자 제공 컨텍스트 추가
        if request.custom_context:
            knowledge_context += f"\n\n### 추가 컨텍스트\n{request.custom_context}"

        # 파라미터에 지식 컨텍스트 추가
        params = {**request.parameters, "knowledge_context": knowledge_context}

        # 사용자 프롬프트 렌더링
        user_prompt = template.render_user_prompt(**params)

        return GeneratedContent(
            content_type=request.content_type.value,
            system_prompt=template.system_prompt,
            user_prompt=user_prompt,
            knowledge_context=knowledge_context,
            parameters_used=request.parameters
        )

    def list_content_types(self) -> List[Dict[str, str]]:
        """사용 가능한 콘텐츠 유형 목록"""
        return self.template_loader.list_templates()

    def get_content_type_params(self, content_type: str) -> Dict[str, Any]:
        """콘텐츠 유형별 파라미터 정보"""
        return self.template_loader.get_template_parameters(content_type)

    # === 편의 메서드 ===

    def create_blog_post(self,
                        topic: str,
                        target_audience: str = "기업 의사결정자",
                        tone: str = "전문적",
                        length: str = "중간 (800-1200자)",
                        include_points: str = "") -> GeneratedContent:
        """블로그 포스트 생성"""
        request = ContentRequest(
            content_type=ContentType.BLOG_POST,
            parameters={
                "topic": topic,
                "target_audience": target_audience,
                "tone": tone,
                "length": length,
                "include_points": include_points
            }
        )
        return self.generate(request)

    def create_proposal(self,
                       client_name: str,
                       industry: str,
                       service_type: str,
                       client_needs: str,
                       budget_range: str = "협의 필요") -> GeneratedContent:
        """제안서 생성"""
        request = ContentRequest(
            content_type=ContentType.PROPOSAL,
            parameters={
                "client_name": client_name,
                "industry": industry,
                "service_type": service_type,
                "client_needs": client_needs,
                "budget_range": budget_range
            }
        )
        return self.generate(request)

    def create_email(self,
                    recipient_name: str,
                    email_type: str,
                    purpose: str,
                    key_message: str,
                    desired_action: str,
                    recipient_role: str = "",
                    context: str = "") -> GeneratedContent:
        """이메일 생성"""
        request = ContentRequest(
            content_type=ContentType.EMAIL,
            parameters={
                "recipient_name": recipient_name,
                "recipient_role": recipient_role,
                "email_type": email_type,
                "purpose": purpose,
                "key_message": key_message,
                "desired_action": desired_action,
                "context": context
            }
        )
        return self.generate(request)

    def create_social_media(self,
                           platform: str,
                           content_type: str,
                           topic: str,
                           key_message: str,
                           tone: str = "전문적") -> GeneratedContent:
        """소셜 미디어 콘텐츠 생성"""
        request = ContentRequest(
            content_type=ContentType.SOCIAL_MEDIA,
            parameters={
                "platform": platform,
                "content_type": content_type,
                "topic": topic,
                "key_message": key_message,
                "tone": tone
            }
        )
        return self.generate(request)

    def create_company_intro(self,
                            situation: str,
                            audience: str,
                            version: str = "standard",
                            emphasis: str = "종합",
                            tone: str = "전문적") -> GeneratedContent:
        """회사 소개 생성"""
        request = ContentRequest(
            content_type=ContentType.COMPANY_INTRO,
            parameters={
                "situation": situation,
                "audience": audience,
                "version": version,
                "emphasis": emphasis,
                "tone": tone
            }
        )
        return self.generate(request)


# 사용 예시
if __name__ == "__main__":
    generator = ContentGenerator()

    # 블로그 포스트 생성
    print("=== 블로그 포스트 프롬프트 ===")
    result = generator.create_blog_post(
        topic="기업의 AI 전환을 위한 첫 번째 단계",
        target_audience="기업 의사결정자",
        include_points="- AI 도입 필요성\n- 단계별 접근법\n- 성공 사례"
    )

    print(f"시스템 프롬프트:\n{result.system_prompt[:200]}...")
    print(f"\n사용자 프롬프트:\n{result.user_prompt[:500]}...")

    # 제안서 생성
    print("\n\n=== 제안서 프롬프트 ===")
    result = generator.create_proposal(
        client_name="ABC 기업",
        industry="금융/보험",
        service_type="AI 전환 교육",
        client_needs="전 직원 AI 역량 강화"
    )
    print(f"사용자 프롬프트:\n{result.user_prompt[:500]}...")
