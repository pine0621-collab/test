"""
바리온랩스 지식베이스 검색 엔진
RAG (Retrieval-Augmented Generation) 시스템의 검색 컴포넌트
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class KnowledgeCategory(Enum):
    """지식베이스 카테고리"""
    COMPANY = "company"
    SERVICES = "services"
    TEAM = "team"
    PROJECTS = "projects"
    FAQ = "faq"


@dataclass
class KnowledgeItem:
    """지식 아이템"""
    category: KnowledgeCategory
    content: Dict[str, Any]
    relevance_score: float = 0.0


class KnowledgeRetriever:
    """지식베이스 검색기"""

    def __init__(self, knowledge_base_path: str = None):
        """
        Args:
            knowledge_base_path: 지식베이스 디렉토리 경로
        """
        if knowledge_base_path is None:
            # 기본 경로 설정
            self.base_path = Path(__file__).parent.parent / "knowledge-base"
        else:
            self.base_path = Path(knowledge_base_path)

        self.knowledge_data: Dict[KnowledgeCategory, Dict] = {}
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """지식베이스 로드"""
        category_files = {
            KnowledgeCategory.COMPANY: "company/profile.json",
            KnowledgeCategory.SERVICES: "services/services.json",
            KnowledgeCategory.TEAM: "team/team.json",
            KnowledgeCategory.PROJECTS: "projects/portfolio.json",
            KnowledgeCategory.FAQ: "faq/faq.json",
        }

        for category, file_path in category_files.items():
            full_path = self.base_path / file_path
            if full_path.exists():
                with open(full_path, "r", encoding="utf-8") as f:
                    self.knowledge_data[category] = json.load(f)

    def get_company_info(self) -> Dict[str, Any]:
        """회사 정보 조회"""
        return self.knowledge_data.get(KnowledgeCategory.COMPANY, {})

    def get_services(self, service_id: Optional[str] = None) -> Dict[str, Any]:
        """서비스 정보 조회"""
        services_data = self.knowledge_data.get(KnowledgeCategory.SERVICES, {})

        if service_id:
            services = services_data.get("services", [])
            for service in services:
                if service.get("id") == service_id:
                    return service
            return {}

        return services_data

    def get_team_info(self) -> Dict[str, Any]:
        """팀 정보 조회"""
        return self.knowledge_data.get(KnowledgeCategory.TEAM, {})

    def get_projects(self, project_type: Optional[str] = None) -> Dict[str, Any]:
        """프로젝트 실적 조회"""
        projects_data = self.knowledge_data.get(KnowledgeCategory.PROJECTS, {})

        if project_type:
            projects = projects_data.get("projects", [])
            filtered = [p for p in projects if p.get("type") == project_type]
            return {"projects": filtered}

        return projects_data

    def get_faqs(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """FAQ 조회"""
        faq_data = self.knowledge_data.get(KnowledgeCategory.FAQ, {})
        faqs = faq_data.get("faqs", [])

        if category:
            return [faq for faq in faqs if faq.get("category") == category]

        return faqs

    def search(self, query: str, categories: Optional[List[KnowledgeCategory]] = None) -> List[KnowledgeItem]:
        """
        지식베이스 검색

        Args:
            query: 검색 쿼리
            categories: 검색할 카테고리 목록 (None이면 전체 검색)

        Returns:
            관련 지식 아이템 목록
        """
        results = []
        query_lower = query.lower()

        search_categories = categories or list(KnowledgeCategory)

        for category in search_categories:
            if category not in self.knowledge_data:
                continue

            data = self.knowledge_data[category]
            score = self._calculate_relevance(query_lower, data)

            if score > 0:
                results.append(KnowledgeItem(
                    category=category,
                    content=data,
                    relevance_score=score
                ))

        # 관련도 순으로 정렬
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results

    def _calculate_relevance(self, query: str, data: Dict[str, Any], depth: int = 0) -> float:
        """
        관련도 점수 계산 (간단한 키워드 매칭)

        실제 프로덕션에서는 임베딩 기반 유사도 검색 사용 권장
        """
        if depth > 5:  # 재귀 깊이 제한
            return 0.0

        score = 0.0
        query_words = query.split()

        def search_in_value(value, current_depth=0):
            nonlocal score
            if current_depth > 5:
                return

            if isinstance(value, str):
                value_lower = value.lower()
                for word in query_words:
                    if word in value_lower:
                        score += 1.0
            elif isinstance(value, list):
                for item in value:
                    search_in_value(item, current_depth + 1)
            elif isinstance(value, dict):
                for v in value.values():
                    search_in_value(v, current_depth + 1)

        search_in_value(data)
        return score

    def get_context_for_content_type(self, content_type: str) -> Dict[str, Any]:
        """
        콘텐츠 유형에 따른 관련 컨텍스트 조회

        Args:
            content_type: 콘텐츠 유형 (blog_post, proposal, email 등)

        Returns:
            관련 지식베이스 정보
        """
        context = {
            "company": self.get_company_info(),
        }

        if content_type in ["proposal", "company_intro"]:
            context["team"] = self.get_team_info()
            context["projects"] = self.get_projects()
            context["services"] = self.get_services()

        elif content_type in ["blog_post", "social_media"]:
            context["services"] = self.get_services()
            context["projects"] = self.get_projects()

        elif content_type == "email":
            context["services"] = self.get_services()
            context["faq"] = self.get_faqs()

        return context

    def format_context_for_prompt(self, context: Dict[str, Any]) -> str:
        """
        프롬프트에 삽입할 컨텍스트 포맷팅
        """
        formatted_parts = []

        if "company" in context:
            company = context["company"]
            formatted_parts.append(f"""
### 회사 정보
- 회사명: {company.get('company_name', '')} ({company.get('company_name_en', '')})
- 비전: {company.get('vision', '')}
- 미션: {company.get('mission', '')}
- 연락처: {', '.join(company.get('contact', {}).get('email', []))}
""")

        if "services" in context:
            services = context["services"]
            if isinstance(services, dict) and "services" in services:
                service_list = services["services"]
                services_text = "\n".join([
                    f"- {s.get('name', '')}: {s.get('description', '')}"
                    for s in service_list
                ])
                formatted_parts.append(f"""
### 서비스
{services_text}
""")

        if "projects" in context:
            projects = context["projects"]
            if isinstance(projects, dict) and "projects" in projects:
                project_list = projects["projects"]
                projects_text = "\n".join([
                    f"- {p.get('client', '')} ({p.get('date', '')}): {p.get('title', '')}"
                    for p in project_list
                ])
                formatted_parts.append(f"""
### 프로젝트 실적
{projects_text}
""")

        if "team" in context:
            team = context["team"]
            leadership = team.get("leadership", {})
            ceo = leadership.get("ceo", {})
            if ceo:
                formatted_parts.append(f"""
### 리더십
- 대표: {ceo.get('name', '')} - {', '.join(ceo.get('expertise', []))}
""")

        return "\n".join(formatted_parts)


# 사용 예시
if __name__ == "__main__":
    retriever = KnowledgeRetriever()

    # 회사 정보 조회
    print("=== 회사 정보 ===")
    print(json.dumps(retriever.get_company_info(), ensure_ascii=False, indent=2))

    # 서비스 검색
    print("\n=== 서비스 정보 ===")
    print(json.dumps(retriever.get_services(), ensure_ascii=False, indent=2))

    # 검색 테스트
    print("\n=== '교육' 검색 결과 ===")
    results = retriever.search("교육")
    for item in results:
        print(f"- {item.category.value}: 관련도 {item.relevance_score}")
