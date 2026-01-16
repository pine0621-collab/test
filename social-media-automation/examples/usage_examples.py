"""
소셜 미디어 자동화 사용 예제
"""

import sys
from pathlib import Path

# 상위 디렉토리 추가
sys.path.insert(0, str(Path(__file__).parent.parent))


def example_linkedin_thought_leadership():
    """LinkedIn Thought Leadership 포스트 생성"""
    from engine import create_linkedin_post

    print("=" * 50)
    print("LinkedIn Thought Leadership 포스트")
    print("=" * 50)

    content = create_linkedin_post(
        template_type="thought_leadership",
        variables={
            "topic": "AI 도입 실패의 진짜 원인",
            "key_insight": "기술이 아닌 '조직 문화'가 성공을 결정한다",
            "supporting_points": """
1. 경영진의 AI에 대한 이해 부족
2. 임직원 교육 없이 도구만 도입
3. 명확한 성과 지표(KPI) 부재
4. 작은 성공 경험 없이 큰 프로젝트 시작
""",
            "example": "바리온랩스가 한화생명 해커톤에서 목격한 것: 단 이틀 만에 비개발자들이 AI 프로토타입을 완성했습니다.",
            "cta_question": "여러분 회사의 AI 도입 경험은 어떠셨나요? 가장 큰 도전은 무엇이었는지 댓글로 공유해주세요!"
        }
    )

    print(content.main_text)
    print("\n해시태그:", content.hashtags)


def example_linkedin_case_study():
    """LinkedIn Case Study 포스트 생성"""
    from engine import create_linkedin_post

    print("\n" + "=" * 50)
    print("LinkedIn Case Study 포스트")
    print("=" * 50)

    content = create_linkedin_post(
        template_type="case_study",
        variables={
            "client_name": "한화생명",
            "industry": "금융/보험",
            "challenge": "임직원들의 AI 역량 강화와 실제 업무에 적용 가능한 AI 서비스 아이디어 발굴",
            "solution": "비봇코딩 환경과 miri.dev 플랫폼을 활용한 2일간의 AI 해커톤",
            "results": "20개 팀 참가, 20개 AI 프로토타입 완성",
            "testimonial": "퀄리티 높은 결과물 도출"
        }
    )

    print(content.main_text)


def example_instagram_carousel():
    """Instagram 캐러셀 포스트 생성"""
    from engine import create_instagram_post

    print("\n" + "=" * 50)
    print("Instagram 캐러셀 포스트")
    print("=" * 50)

    content = create_instagram_post(
        template_type="carousel",
        variables={
            "topic": "AI 프롬프트 작성 5가지 핵심 원칙",
            "points": [
                "1. 구체적으로 요청하기 - '좋은 글 써줘' 대신 '500자 블로그 포스트 써줘'",
                "2. 맥락 제공하기 - 배경 정보를 주면 더 정확한 답변",
                "3. 예시 보여주기 - 원하는 결과물의 예시 제시",
                "4. 역할 부여하기 - '당신은 마케팅 전문가입니다'",
                "5. 단계별로 요청하기 - 복잡한 작업은 나눠서 진행"
            ],
            "target_audience": "AI 입문자, 직장인",
            "cta": "저장해두고 나중에 활용하세요!"
        }
    )

    print(content.main_text)


def example_instagram_reels():
    """Instagram 릴스 스크립트 생성"""
    from engine import create_instagram_post

    print("\n" + "=" * 50)
    print("Instagram 릴스 스크립트")
    print("=" * 50)

    content = create_instagram_post(
        template_type="reels",
        variables={
            "topic": "이메일 작성 시간 90% 줄이기",
            "key_message": "AI 템플릿 활용으로 30분 걸리던 이메일을 3분에 작성",
            "demonstration": "1. 역할 부여 → 2. 템플릿 요청 → 3. 상황만 입력",
            "duration": "30초"
        }
    )

    print(content.main_text)


def example_hashtag_generation():
    """해시태그 생성"""
    from engine import get_linkedin_hashtags, get_instagram_hashtags

    print("\n" + "=" * 50)
    print("해시태그 생성")
    print("=" * 50)

    print("\nLinkedIn 해시태그:")
    print(get_linkedin_hashtags(topic="ai"))

    print("\nInstagram 해시태그:")
    print(get_instagram_hashtags(topic="business"))


def example_scheduling():
    """포스팅 스케줄링"""
    from engine import PostingScheduler

    print("\n" + "=" * 50)
    print("포스팅 스케줄링")
    print("=" * 50)

    scheduler = PostingScheduler()

    # 주간 스케줄 생성
    print("\n주간 포스팅 스케줄:")
    weekly = scheduler.generate_weekly_schedule()

    for platform, times in weekly.items():
        print(f"\n{platform.upper()}:")
        for slot in times:
            print(f"  {slot['day']} {slot['date']} {slot['time']}")


def example_content_calendar():
    """콘텐츠 캘린더"""
    from engine import SocialMediaContentGenerator

    print("\n" + "=" * 50)
    print("콘텐츠 캘린더 (4주)")
    print("=" * 50)

    generator = SocialMediaContentGenerator()
    calendar = generator.get_content_calendar(weeks=4)

    for item in calendar[:10]:  # 처음 10개만 출력
        print(f"\n주차 {item['week']}: {item['theme']}")
        print(f"  플랫폼: {', '.join(item['platforms'])}")
        print(f"  추천 주제: {item['suggested_topics'][0]}")


if __name__ == "__main__":
    print("소셜 미디어 자동화 사용 예제")
    print("=" * 60)

    # LinkedIn 예제
    example_linkedin_thought_leadership()
    example_linkedin_case_study()

    # Instagram 예제
    example_instagram_carousel()
    example_instagram_reels()

    # 해시태그
    example_hashtag_generation()

    # 스케줄링
    example_scheduling()

    # 캘린더
    example_content_calendar()

    print("\n" + "=" * 60)
    print("예제 실행 완료!")
