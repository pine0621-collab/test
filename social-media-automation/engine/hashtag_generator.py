"""
해시태그 생성기

플랫폼별 최적화된 해시태그를 생성합니다.
"""

import json
from pathlib import Path
from typing import Optional


class HashtagGenerator:
    """해시태그 생성기"""

    # 플랫폼별 최적 해시태그 수
    OPTIMAL_COUNTS = {
        "linkedin": 5,
        "instagram": 15,
        "twitter": 3
    }

    # 인기 AI/비즈니스 해시태그 (한국어)
    TRENDING_HASHTAGS = {
        "ai": [
            "AI", "인공지능", "생성형AI", "ChatGPT", "Claude",
            "LLM", "머신러닝", "딥러닝", "AI활용", "AI트렌드"
        ],
        "business": [
            "디지털전환", "비즈니스혁신", "스타트업", "기업교육",
            "생산성", "업무효율", "스마트워크", "자동화", "DX"
        ],
        "education": [
            "교육", "AI교육", "기업연수", "해커톤", "워크숍",
            "역량개발", "리스킬링", "업스킬링"
        ],
        "linkedin_kr": [
            "링크드인", "네트워킹", "커리어", "취업", "이직",
            "자기계발", "직장인", "비즈니스"
        ],
        "instagram_kr": [
            "인스타그램", "인스타", "일상", "팔로우", "좋아요",
            "데일리", "소통", "맞팔"
        ]
    }

    def __init__(self, kb_path: str = None):
        if kb_path is None:
            kb_path = Path(__file__).parent.parent / "knowledge-base"
        self.kb_path = Path(kb_path)
        self._company_hashtags = None

    @property
    def company_hashtags(self) -> dict:
        """회사 브랜드 해시태그"""
        if self._company_hashtags is None:
            company_file = self.kb_path / "company.json"
            if company_file.exists():
                with open(company_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._company_hashtags = data.get("hashtags", {})
            else:
                self._company_hashtags = {}
        return self._company_hashtags

    def generate(
        self,
        platform: str,
        content_type: str = None,
        topic: str = None,
        include_brand: bool = True
    ) -> list[str]:
        """
        해시태그 생성

        Args:
            platform: 플랫폼 (linkedin, instagram)
            content_type: 콘텐츠 유형 (thought_leadership, case_study, etc.)
            topic: 주제 (ai, business, education)
            include_brand: 브랜드 해시태그 포함 여부

        Returns:
            해시태그 리스트
        """
        hashtags = []
        optimal_count = self.OPTIMAL_COUNTS.get(platform, 10)

        # 1. 브랜드 해시태그
        if include_brand:
            brand_tags = self.company_hashtags.get("brand", [])
            hashtags.extend(brand_tags[:2])

        # 2. 서비스 해시태그
        if content_type:
            service_tags = self.company_hashtags.get("service", [])
            hashtags.extend(service_tags[:3])

        # 3. 주제별 해시태그
        if topic and topic in self.TRENDING_HASHTAGS:
            topic_tags = self.TRENDING_HASHTAGS[topic]
            hashtags.extend(topic_tags[:5])

        # 4. 플랫폼별 해시태그
        platform_key = f"{platform}_kr"
        if platform_key in self.TRENDING_HASHTAGS:
            platform_tags = self.TRENDING_HASHTAGS[platform_key]
            hashtags.extend(platform_tags[:3])

        # 5. AI 기본 해시태그
        ai_tags = self.TRENDING_HASHTAGS.get("ai", [])
        hashtags.extend(ai_tags[:5])

        # 중복 제거 및 최적 개수로 제한
        unique_hashtags = list(dict.fromkeys(hashtags))
        return unique_hashtags[:optimal_count]

    def format_hashtags(self, hashtags: list[str], style: str = "inline") -> str:
        """
        해시태그 포맷팅

        Args:
            hashtags: 해시태그 리스트
            style: 포맷 스타일 (inline, newline, block)

        Returns:
            포맷된 해시태그 문자열
        """
        formatted = [f"#{tag}" if not tag.startswith("#") else tag for tag in hashtags]

        if style == "inline":
            return " ".join(formatted)
        elif style == "newline":
            return "\n".join(formatted)
        elif style == "block":
            return "\n\n" + " ".join(formatted)
        else:
            return " ".join(formatted)

    def analyze_hashtag_performance(self, hashtags: list[str]) -> dict:
        """
        해시태그 성과 분석 (예상 도달률)

        실제로는 API를 통해 분석해야 하지만,
        여기서는 간단한 휴리스틱 사용
        """
        analysis = {
            "total_count": len(hashtags),
            "brand_hashtags": [],
            "trending_hashtags": [],
            "niche_hashtags": [],
            "estimated_reach": "medium"
        }

        brand_tags = set(self.company_hashtags.get("brand", []))
        trending_tags = set()
        for tags in self.TRENDING_HASHTAGS.values():
            trending_tags.update(tags)

        for tag in hashtags:
            clean_tag = tag.lstrip("#")
            if clean_tag in brand_tags:
                analysis["brand_hashtags"].append(tag)
            elif clean_tag in trending_tags:
                analysis["trending_hashtags"].append(tag)
            else:
                analysis["niche_hashtags"].append(tag)

        # 도달률 추정
        trending_ratio = len(analysis["trending_hashtags"]) / max(len(hashtags), 1)
        if trending_ratio > 0.5:
            analysis["estimated_reach"] = "high"
        elif trending_ratio > 0.3:
            analysis["estimated_reach"] = "medium"
        else:
            analysis["estimated_reach"] = "low"

        return analysis


def get_linkedin_hashtags(topic: str = "ai") -> str:
    """LinkedIn용 해시태그 생성 헬퍼"""
    generator = HashtagGenerator()
    hashtags = generator.generate(
        platform="linkedin",
        topic=topic,
        include_brand=True
    )
    return generator.format_hashtags(hashtags, style="inline")


def get_instagram_hashtags(topic: str = "ai") -> str:
    """Instagram용 해시태그 생성 헬퍼"""
    generator = HashtagGenerator()
    hashtags = generator.generate(
        platform="instagram",
        topic=topic,
        include_brand=True
    )
    return generator.format_hashtags(hashtags, style="block")


if __name__ == "__main__":
    generator = HashtagGenerator()

    print("=== LinkedIn 해시태그 ===")
    linkedin_tags = generator.generate("linkedin", topic="ai")
    print(generator.format_hashtags(linkedin_tags))

    print("\n=== Instagram 해시태그 ===")
    instagram_tags = generator.generate("instagram", topic="business")
    print(generator.format_hashtags(instagram_tags, style="block"))

    print("\n=== 해시태그 분석 ===")
    analysis = generator.analyze_hashtag_performance(instagram_tags)
    print(json.dumps(analysis, ensure_ascii=False, indent=2))
