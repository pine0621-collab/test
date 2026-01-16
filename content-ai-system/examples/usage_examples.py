"""
바리온랩스 콘텐츠 생성 AI 사용 예시
"""

import json
import sys
from pathlib import Path

# 프로젝트 루트를 path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from engine.content_generator import ContentGenerator


def example_blog_post():
    """블로그 포스트 생성 예시"""
    print("=" * 60)
    print("예시 1: 블로그 포스트 생성")
    print("=" * 60)

    generator = ContentGenerator()

    result = generator.create_blog_post(
        topic="기업 AI 도입의 첫 걸음: 임직원 교육의 중요성",
        target_audience="기업 의사결정자",
        tone="전문적",
        length="중간 (800-1200자)",
        include_points="""
- AI 리터러시의 정의와 중요성
- 교육 없이 AI 도입 시 발생하는 문제점
- 바리온랩스의 교육 접근법
- 성공 사례 (한화생명 해커톤)
"""
    )

    print("\n[시스템 프롬프트 미리보기]")
    print(result.system_prompt[:300] + "...")

    print("\n[사용자 프롬프트]")
    print(result.user_prompt)

    print("\n[사용된 파라미터]")
    print(json.dumps(result.parameters_used, ensure_ascii=False, indent=2))


def example_proposal():
    """제안서 생성 예시"""
    print("\n" + "=" * 60)
    print("예시 2: 제안서 생성")
    print("=" * 60)

    generator = ContentGenerator()

    result = generator.create_proposal(
        client_name="삼성SDS",
        industry="IT/테크",
        service_type="AI 전환 교육",
        client_needs="전사 임직원 대상 AI 역량 강화 및 실무 적용 교육",
        budget_range="5천만원 ~ 1억원"
    )

    print("\n[시스템 프롬프트 미리보기]")
    print(result.system_prompt[:300] + "...")

    print("\n[사용자 프롬프트]")
    print(result.user_prompt)


def example_email():
    """이메일 생성 예시"""
    print("\n" + "=" * 60)
    print("예시 3: 비즈니스 이메일 생성")
    print("=" * 60)

    generator = ContentGenerator()

    result = generator.create_email(
        recipient_name="김철수",
        recipient_role="인재개발팀장",
        email_type="첫 접촉",
        purpose="AI 교육 프로그램 소개 및 미팅 제안",
        key_message="바리온랩스의 실무 중심 AI 교육으로 귀사의 디지털 전환을 가속화할 수 있습니다",
        desired_action="다음 주 중 30분 미팅 요청",
        context="지난 AI 컨퍼런스에서 명함 교환"
    )

    print("\n[사용자 프롬프트]")
    print(result.user_prompt)


def example_social_media():
    """소셜 미디어 콘텐츠 생성 예시"""
    print("\n" + "=" * 60)
    print("예시 4: LinkedIn 포스트 생성")
    print("=" * 60)

    generator = ContentGenerator()

    result = generator.create_social_media(
        platform="LinkedIn",
        content_type="프로젝트 완료",
        topic="한화생명 AI 해커톤 성공 사례",
        key_message="비봇코딩을 활용한 AI 서비스 프로토타입으로 실질적인 업무 혁신 달성",
        tone="전문적"
    )

    print("\n[사용자 프롬프트]")
    print(result.user_prompt)


def example_company_intro():
    """회사 소개 생성 예시"""
    print("\n" + "=" * 60)
    print("예시 5: 회사 소개 (네트워킹용)")
    print("=" * 60)

    generator = ContentGenerator()

    # 엘리베이터 피치 버전
    result = generator.create_company_intro(
        situation="네트워킹 행사",
        audience="기업 의사결정자",
        version="elevator_pitch",
        emphasis="AI 교육 역량",
        tone="전문적"
    )

    print("\n[엘리베이터 피치 프롬프트]")
    print(result.user_prompt)

    # 상세 버전
    result_detailed = generator.create_company_intro(
        situation="고객 미팅",
        audience="기업 의사결정자",
        version="detailed",
        emphasis="종합",
        tone="전문적"
    )

    print("\n[상세 소개 프롬프트]")
    print(result_detailed.user_prompt)


def example_knowledge_search():
    """지식베이스 검색 예시"""
    print("\n" + "=" * 60)
    print("예시 6: 지식베이스 검색")
    print("=" * 60)

    from engine.knowledge_retriever import KnowledgeRetriever

    retriever = KnowledgeRetriever()

    # 검색
    print("\n['해커톤' 검색 결과]")
    results = retriever.search("해커톤")
    for item in results[:3]:
        print(f"- {item.category.value}: 관련도 {item.relevance_score}")

    print("\n['교육' 검색 결과]")
    results = retriever.search("교육")
    for item in results[:3]:
        print(f"- {item.category.value}: 관련도 {item.relevance_score}")

    # 특정 정보 조회
    print("\n[회사 정보]")
    company = retriever.get_company_info()
    print(f"- 회사명: {company.get('company_name')}")
    print(f"- 비전: {company.get('vision')}")

    print("\n[서비스 목록]")
    services = retriever.get_services()
    for service in services.get('services', []):
        print(f"- {service.get('name')}: {service.get('description')[:50]}...")


def main():
    """모든 예시 실행"""
    print("바리온랩스 콘텐츠 생성 AI 사용 예시")
    print("이 예시들은 LLM에 전달할 프롬프트를 생성합니다.")
    print("실제 콘텐츠 생성은 LLM API 호출이 필요합니다.\n")

    example_blog_post()
    example_proposal()
    example_email()
    example_social_media()
    example_company_intro()
    example_knowledge_search()

    print("\n" + "=" * 60)
    print("모든 예시 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()
