"""
소셜 미디어 콘텐츠 생성 엔진

LinkedIn/Instagram 콘텐츠를 자동으로 생성합니다.
"""

import json
import yaml
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class ContentRequest:
    """콘텐츠 생성 요청"""
    platform: str  # linkedin, instagram
    template_type: str  # thought_leadership, case_study, carousel, etc.
    variables: dict


@dataclass
class GeneratedContent:
    """생성된 콘텐츠"""
    platform: str
    content_type: str
    main_text: str
    hashtags: list[str]
    metadata: dict


class KnowledgeBase:
    """회사 지식베이스"""

    def __init__(self, kb_path: str = None):
        if kb_path is None:
            kb_path = Path(__file__).parent.parent / "knowledge-base"
        self.kb_path = Path(kb_path)
        self._company = None
        self._themes = None

    @property
    def company(self) -> dict:
        if self._company is None:
            with open(self.kb_path / "company.json", "r", encoding="utf-8") as f:
                self._company = json.load(f)
        return self._company

    @property
    def themes(self) -> dict:
        if self._themes is None:
            with open(self.kb_path / "content-themes.json", "r", encoding="utf-8") as f:
                self._themes = json.load(f)
        return self._themes

    def get_company_info(self) -> str:
        """회사 정보를 텍스트로 반환"""
        c = self.company["company"]
        return f"""
회사명: {c['name']} ({c['name_en']})
비전: {c['vision']}
웹사이트: {c['website']}
이메일: {c['email'][0]}
"""

    def get_services(self) -> list[dict]:
        """서비스 목록 반환"""
        return self.company["services"]

    def get_projects(self) -> list[dict]:
        """프로젝트 실적 반환"""
        return self.company["projects"]

    def get_brand_hashtags(self) -> list[str]:
        """브랜드 해시태그 반환"""
        return self.company["hashtags"]["brand"]

    def get_posting_schedule(self, platform: str) -> dict:
        """플랫폼별 포스팅 스케줄 반환"""
        return self.themes["posting_schedule"].get(platform, {})


class TemplateLoader:
    """템플릿 로더"""

    def __init__(self, templates_path: str = None):
        if templates_path is None:
            templates_path = Path(__file__).parent.parent / "templates"
        self.templates_path = Path(templates_path)

    def load_template(self, platform: str, template_type: str) -> dict:
        """템플릿 로드"""
        template_file = self.templates_path / platform / f"{template_type}.yaml"
        if not template_file.exists():
            raise ValueError(f"Template not found: {platform}/{template_type}")

        with open(template_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def list_templates(self, platform: str = None) -> list[str]:
        """사용 가능한 템플릿 목록"""
        templates = []

        if platform:
            platform_path = self.templates_path / platform
            if platform_path.exists():
                for f in platform_path.glob("*.yaml"):
                    templates.append(f"{platform}/{f.stem}")
        else:
            for platform_dir in self.templates_path.iterdir():
                if platform_dir.is_dir():
                    for f in platform_dir.glob("*.yaml"):
                        templates.append(f"{platform_dir.name}/{f.stem}")

        return templates


class SocialMediaContentGenerator:
    """소셜 미디어 콘텐츠 생성기"""

    def __init__(self, llm_client=None):
        """
        Args:
            llm_client: LLM 클라이언트 (Anthropic, OpenAI 등)
        """
        self.kb = KnowledgeBase()
        self.template_loader = TemplateLoader()
        self.llm_client = llm_client

    def generate_prompt(self, request: ContentRequest) -> str:
        """LLM 프롬프트 생성"""
        template = self.template_loader.load_template(
            request.platform,
            request.template_type
        )

        # 템플릿의 프롬프트에 변수 대입
        prompt = template.get("prompt_template", "")
        for key, value in request.variables.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))

        # 회사 정보 추가
        company_context = self.kb.get_company_info()
        full_prompt = f"""
[회사 정보]
{company_context}

[콘텐츠 생성 요청]
{prompt}
"""
        return full_prompt

    def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """콘텐츠 생성"""
        prompt = self.generate_prompt(request)

        if self.llm_client is None:
            # LLM 클라이언트가 없으면 프롬프트만 반환
            return GeneratedContent(
                platform=request.platform,
                content_type=request.template_type,
                main_text=f"[프롬프트]\n{prompt}",
                hashtags=self.kb.get_brand_hashtags(),
                metadata={"prompt": prompt}
            )

        # LLM을 사용하여 콘텐츠 생성
        response = self._call_llm(prompt)

        return GeneratedContent(
            platform=request.platform,
            content_type=request.template_type,
            main_text=response,
            hashtags=self._extract_hashtags(response),
            metadata={"prompt": prompt}
        )

    def _call_llm(self, prompt: str) -> str:
        """LLM API 호출"""
        if hasattr(self.llm_client, 'messages'):
            # Anthropic Claude
            response = self.llm_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        elif hasattr(self.llm_client, 'chat'):
            # OpenAI
            response = self.llm_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            return response.choices[0].message.content

        else:
            raise ValueError("Unsupported LLM client")

    def _extract_hashtags(self, text: str) -> list[str]:
        """텍스트에서 해시태그 추출"""
        import re
        hashtags = re.findall(r'#(\w+)', text)
        return list(set(hashtags))

    def get_content_calendar(self, weeks: int = 4) -> list[dict]:
        """콘텐츠 캘린더 생성"""
        themes = self.kb.themes["content_pillars"]
        calendar = []

        for week in range(1, weeks + 1):
            for theme in themes:
                if theme["frequency"] == "weekly":
                    calendar.append({
                        "week": week,
                        "theme": theme["name"],
                        "platforms": theme["platforms"],
                        "suggested_topics": theme["topics"]
                    })
                elif theme["frequency"] == "bi-weekly" and week % 2 == 0:
                    calendar.append({
                        "week": week,
                        "theme": theme["name"],
                        "platforms": theme["platforms"],
                        "suggested_topics": theme["topics"]
                    })

        return calendar


# LinkedIn 전용 헬퍼 함수
def create_linkedin_post(
    template_type: str,
    variables: dict,
    llm_client=None
) -> GeneratedContent:
    """LinkedIn 포스트 생성 헬퍼"""
    generator = SocialMediaContentGenerator(llm_client)
    request = ContentRequest(
        platform="linkedin",
        template_type=template_type,
        variables=variables
    )
    return generator.generate_content(request)


# Instagram 전용 헬퍼 함수
def create_instagram_post(
    template_type: str,
    variables: dict,
    llm_client=None
) -> GeneratedContent:
    """Instagram 포스트 생성 헬퍼"""
    generator = SocialMediaContentGenerator(llm_client)
    request = ContentRequest(
        platform="instagram",
        template_type=template_type,
        variables=variables
    )
    return generator.generate_content(request)


if __name__ == "__main__":
    # 테스트
    generator = SocialMediaContentGenerator()

    # 사용 가능한 템플릿 출력
    print("=== 사용 가능한 템플릿 ===")
    for t in generator.template_loader.list_templates():
        print(f"  - {t}")

    # LinkedIn 포스트 생성 테스트
    print("\n=== LinkedIn Thought Leadership 포스트 ===")
    content = create_linkedin_post(
        template_type="thought_leadership",
        variables={
            "topic": "AI 도입 실패 원인 분석",
            "key_insight": "기술보다 조직 문화가 더 중요하다",
            "supporting_points": "1. 교육 부재, 2. 명확한 목표 부재, 3. 경영진 지원 부족",
            "example": "한화생명 해커톤 사례",
            "cta_question": "여러분의 AI 도입 경험은 어떠셨나요?"
        }
    )
    print(content.main_text[:500] + "...")
