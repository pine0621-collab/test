"""
LLM 연동 예시 - 실제 콘텐츠 생성

이 예시는 생성된 프롬프트를 LLM API에 전송하여 실제 콘텐츠를 생성합니다.
사용 전 해당 LLM 제공자의 API 키를 환경 변수로 설정해야 합니다.
"""

import os
import sys
from pathlib import Path
from typing import Optional

# 프로젝트 루트를 path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from engine.content_generator import ContentGenerator


def generate_with_openai(system_prompt: str, user_prompt: str) -> str:
    """OpenAI API를 사용한 콘텐츠 생성"""
    try:
        from openai import OpenAI
    except ImportError:
        return "[오류] openai 패키지가 설치되지 않았습니다. pip install openai"

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "[오류] OPENAI_API_KEY 환경 변수를 설정하세요."

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )

    return response.choices[0].message.content


def generate_with_anthropic(system_prompt: str, user_prompt: str) -> str:
    """Anthropic Claude API를 사용한 콘텐츠 생성"""
    try:
        import anthropic
    except ImportError:
        return "[오류] anthropic 패키지가 설치되지 않았습니다. pip install anthropic"

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "[오류] ANTHROPIC_API_KEY 환경 변수를 설정하세요."

    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.content[0].text


def generate_with_local_ollama(system_prompt: str, user_prompt: str, model: str = "llama3") -> str:
    """로컬 Ollama를 사용한 콘텐츠 생성"""
    import httpx

    try:
        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": f"System: {system_prompt}\n\nUser: {user_prompt}",
                "stream": False
            },
            timeout=120.0
        )
        return response.json().get("response", "[오류] 응답 없음")
    except httpx.ConnectError:
        return "[오류] Ollama 서버에 연결할 수 없습니다. Ollama가 실행 중인지 확인하세요."


def example_full_generation():
    """전체 콘텐츠 생성 예시"""
    print("=" * 60)
    print("바리온랩스 콘텐츠 생성 AI - LLM 연동 예시")
    print("=" * 60)

    # 콘텐츠 생성기 초기화
    generator = ContentGenerator()

    # 블로그 포스트 프롬프트 생성
    print("\n1. 블로그 포스트 프롬프트 생성")
    result = generator.create_blog_post(
        topic="기업의 AI 전환: 교육이 먼저다",
        target_audience="기업 의사결정자",
        include_points="""
- AI 도입의 실패 원인 분석
- 교육의 중요성
- 바리온랩스의 접근법
"""
    )

    prompts = result.get_full_prompt()

    print(f"   시스템 프롬프트 길이: {len(prompts['system'])} 자")
    print(f"   사용자 프롬프트 길이: {len(prompts['user'])} 자")

    # LLM 선택
    print("\n2. LLM 제공자 선택")
    print("   사용 가능한 제공자:")
    print("   - openai: OpenAI GPT-4")
    print("   - anthropic: Anthropic Claude")
    print("   - ollama: 로컬 Ollama")

    # 환경 변수 확인
    has_openai = bool(os.environ.get("OPENAI_API_KEY"))
    has_anthropic = bool(os.environ.get("ANTHROPIC_API_KEY"))

    print(f"\n   OPENAI_API_KEY: {'설정됨' if has_openai else '미설정'}")
    print(f"   ANTHROPIC_API_KEY: {'설정됨' if has_anthropic else '미설정'}")

    # 실제 생성 (API 키가 있는 경우에만)
    if has_anthropic:
        print("\n3. Claude를 사용하여 콘텐츠 생성 중...")
        content = generate_with_anthropic(prompts['system'], prompts['user'])
        print("\n[생성된 콘텐츠]")
        print("-" * 40)
        print(content)
    elif has_openai:
        print("\n3. OpenAI를 사용하여 콘텐츠 생성 중...")
        content = generate_with_openai(prompts['system'], prompts['user'])
        print("\n[생성된 콘텐츠]")
        print("-" * 40)
        print(content)
    else:
        print("\n[정보] API 키가 설정되지 않아 실제 생성을 건너뜁니다.")
        print("실제 콘텐츠를 생성하려면 다음 환경 변수 중 하나를 설정하세요:")
        print("  export ANTHROPIC_API_KEY=your_key")
        print("  export OPENAI_API_KEY=your_key")

        # 프롬프트만 출력
        print("\n[생성된 프롬프트 미리보기]")
        print("-" * 40)
        print("[시스템 프롬프트]")
        print(prompts['system'][:500] + "...")
        print("\n[사용자 프롬프트]")
        print(prompts['user'])


def batch_generation_example():
    """배치 콘텐츠 생성 예시"""
    print("\n" + "=" * 60)
    print("배치 콘텐츠 생성 예시")
    print("=" * 60)

    generator = ContentGenerator()

    # 여러 콘텐츠 유형 생성
    contents = [
        ("블로그", generator.create_blog_post(
            topic="AI 시대의 인재 육성 전략"
        )),
        ("LinkedIn", generator.create_social_media(
            platform="LinkedIn",
            content_type="인사이트 공유",
            topic="AI 교육의 중요성",
            key_message="실무 중심 AI 교육이 디지털 전환의 핵심"
        )),
        ("이메일", generator.create_email(
            recipient_name="담당자",
            email_type="미팅 요청",
            purpose="AI 교육 프로그램 소개",
            key_message="맞춤형 AI 교육 제안",
            desired_action="미팅 일정 조율"
        ))
    ]

    for name, result in contents:
        print(f"\n[{name}]")
        print(f"  프롬프트 길이: {len(result.user_prompt)} 자")
        print(f"  지식 컨텍스트 포함: {'예' if result.knowledge_context else '아니오'}")


if __name__ == "__main__":
    example_full_generation()
    batch_generation_example()
