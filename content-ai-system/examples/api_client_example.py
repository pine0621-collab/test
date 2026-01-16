"""
바리온랩스 콘텐츠 생성 AI API 클라이언트 예시
"""

import httpx
import asyncio
import json
from typing import Dict, Any


# API 기본 URL
BASE_URL = "http://localhost:8000"


async def check_api_status():
    """API 상태 확인"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/")
        return response.json()


async def list_content_types():
    """콘텐츠 유형 목록 조회"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/content-types")
        return response.json()


async def generate_blog_post(topic: str, **kwargs) -> Dict[str, Any]:
    """블로그 포스트 생성 요청"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/generate/blog-post",
            json={
                "topic": topic,
                "target_audience": kwargs.get("target_audience", "기업 의사결정자"),
                "tone": kwargs.get("tone", "전문적"),
                "length": kwargs.get("length", "중간 (800-1200자)"),
                "include_points": kwargs.get("include_points", "")
            }
        )
        return response.json()


async def generate_proposal(
    client_name: str,
    industry: str,
    service_type: str,
    client_needs: str,
    **kwargs
) -> Dict[str, Any]:
    """제안서 생성 요청"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/generate/proposal",
            json={
                "client_name": client_name,
                "industry": industry,
                "service_type": service_type,
                "client_needs": client_needs,
                "budget_range": kwargs.get("budget_range", "협의 필요")
            }
        )
        return response.json()


async def generate_email(
    recipient_name: str,
    email_type: str,
    purpose: str,
    key_message: str,
    desired_action: str,
    **kwargs
) -> Dict[str, Any]:
    """이메일 생성 요청"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/generate/email",
            json={
                "recipient_name": recipient_name,
                "recipient_role": kwargs.get("recipient_role", ""),
                "email_type": email_type,
                "purpose": purpose,
                "key_message": key_message,
                "desired_action": desired_action,
                "context": kwargs.get("context", "")
            }
        )
        return response.json()


async def search_knowledge(query: str, categories: list = None) -> Dict[str, Any]:
    """지식베이스 검색"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/knowledge/search",
            json={
                "query": query,
                "categories": categories
            }
        )
        return response.json()


async def get_company_info() -> Dict[str, Any]:
    """회사 정보 조회"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/knowledge/company")
        return response.json()


async def main():
    """API 클라이언트 예시 실행"""
    print("바리온랩스 콘텐츠 생성 AI API 클라이언트 예시")
    print("=" * 60)
    print("주의: 이 예시를 실행하려면 먼저 API 서버를 시작해야 합니다.")
    print("실행 방법: uvicorn api.app:app --reload")
    print("=" * 60 + "\n")

    try:
        # API 상태 확인
        print("1. API 상태 확인")
        status = await check_api_status()
        print(f"   상태: {json.dumps(status, ensure_ascii=False)}")

        # 콘텐츠 유형 목록
        print("\n2. 콘텐츠 유형 목록")
        content_types = await list_content_types()
        for ct in content_types:
            print(f"   - {ct['id']}: {ct['name']}")

        # 블로그 포스트 생성
        print("\n3. 블로그 포스트 생성")
        blog = await generate_blog_post(
            topic="AI 교육의 미래",
            target_audience="기업 의사결정자"
        )
        print(f"   콘텐츠 유형: {blog['content_type']}")
        print(f"   사용자 프롬프트 (일부): {blog['user_prompt'][:200]}...")

        # 회사 정보 조회
        print("\n4. 회사 정보 조회")
        company = await get_company_info()
        print(f"   회사명: {company.get('company_name')}")
        print(f"   비전: {company.get('vision')}")

        # 지식베이스 검색
        print("\n5. 지식베이스 검색 ('해커톤')")
        search_results = await search_knowledge("해커톤")
        for result in search_results[:3]:
            print(f"   - {result['category']}: 관련도 {result['relevance_score']}")

        print("\n" + "=" * 60)
        print("API 클라이언트 예시 완료!")

    except httpx.ConnectError:
        print("\n[오류] API 서버에 연결할 수 없습니다.")
        print("먼저 다음 명령으로 서버를 시작하세요:")
        print("  cd content-ai-system && uvicorn api.app:app --reload")


if __name__ == "__main__":
    asyncio.run(main())
