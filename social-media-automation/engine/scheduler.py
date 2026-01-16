"""
소셜 미디어 포스팅 스케줄러

최적의 포스팅 시간을 계산하고 스케줄을 관리합니다.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict


@dataclass
class ScheduledPost:
    """스케줄된 포스트"""
    id: str
    platform: str
    content: str
    hashtags: list[str]
    scheduled_time: datetime
    status: str = "pending"  # pending, published, failed
    metadata: dict = None

    def to_dict(self) -> dict:
        """딕셔너리 변환"""
        d = asdict(self)
        d["scheduled_time"] = self.scheduled_time.isoformat()
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "ScheduledPost":
        """딕셔너리에서 생성"""
        data["scheduled_time"] = datetime.fromisoformat(data["scheduled_time"])
        return cls(**data)


class PostingScheduler:
    """포스팅 스케줄러"""

    # 플랫폼별 최적 포스팅 시간 (한국 시간 기준)
    OPTIMAL_TIMES = {
        "linkedin": {
            "best_hours": [9, 12, 17],  # 오전 9시, 점심, 퇴근 전
            "best_days": [1, 2, 3],  # 화, 수, 목 (0=월요일)
            "avoid_hours": [0, 1, 2, 3, 4, 5, 22, 23],
            "posts_per_week": 4
        },
        "instagram": {
            "best_hours": [12, 18, 21],  # 점심, 퇴근 후, 저녁
            "best_days": [0, 2, 4],  # 월, 수, 금
            "avoid_hours": [0, 1, 2, 3, 4, 5],
            "posts_per_week": 5
        }
    }

    def __init__(self, storage_path: str = None):
        if storage_path is None:
            storage_path = Path(__file__).parent.parent / "data" / "schedule.json"
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._schedule = None

    @property
    def schedule(self) -> list[ScheduledPost]:
        """스케줄 로드"""
        if self._schedule is None:
            if self.storage_path.exists():
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._schedule = [ScheduledPost.from_dict(p) for p in data]
            else:
                self._schedule = []
        return self._schedule

    def save_schedule(self):
        """스케줄 저장"""
        with open(self.storage_path, "w", encoding="utf-8") as f:
            data = [p.to_dict() for p in self.schedule]
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_next_optimal_time(
        self,
        platform: str,
        after: datetime = None
    ) -> datetime:
        """
        다음 최적 포스팅 시간 계산

        Args:
            platform: 플랫폼
            after: 이 시간 이후로 계산 (기본: 현재)

        Returns:
            최적 포스팅 시간
        """
        if after is None:
            after = datetime.now()

        settings = self.OPTIMAL_TIMES.get(platform, self.OPTIMAL_TIMES["linkedin"])
        best_hours = settings["best_hours"]
        best_days = settings["best_days"]
        avoid_hours = settings["avoid_hours"]

        # 현재 시간부터 7일간 탐색
        candidate = after + timedelta(minutes=5)

        for _ in range(7 * 24):  # 최대 7일 탐색
            hour = candidate.hour
            weekday = candidate.weekday()

            # 피해야 할 시간 건너뛰기
            if hour in avoid_hours:
                candidate = candidate.replace(
                    hour=(hour + 1) % 24,
                    minute=0,
                    second=0
                )
                if hour + 1 >= 24:
                    candidate += timedelta(days=1)
                continue

            # 최적 시간과 요일인지 확인
            if hour in best_hours and weekday in best_days:
                # 이미 스케줄된 포스트가 있는지 확인
                existing = self._get_posts_at_time(platform, candidate)
                if not existing:
                    return candidate.replace(minute=0, second=0)

            # 1시간 후로 이동
            candidate += timedelta(hours=1)

        # 찾지 못하면 다음 날 오전 9시
        next_day = after + timedelta(days=1)
        return next_day.replace(hour=9, minute=0, second=0)

    def _get_posts_at_time(
        self,
        platform: str,
        time: datetime
    ) -> list[ScheduledPost]:
        """특정 시간에 스케줄된 포스트 조회"""
        return [
            p for p in self.schedule
            if p.platform == platform
            and p.scheduled_time.date() == time.date()
            and p.scheduled_time.hour == time.hour
            and p.status == "pending"
        ]

    def add_post(
        self,
        platform: str,
        content: str,
        hashtags: list[str] = None,
        scheduled_time: datetime = None,
        metadata: dict = None
    ) -> ScheduledPost:
        """
        포스트 스케줄 추가

        Args:
            platform: 플랫폼
            content: 콘텐츠
            hashtags: 해시태그
            scheduled_time: 스케줄 시간 (없으면 자동 계산)
            metadata: 메타데이터

        Returns:
            스케줄된 포스트
        """
        if scheduled_time is None:
            scheduled_time = self.get_next_optimal_time(platform)

        post_id = f"{platform}_{scheduled_time.strftime('%Y%m%d%H%M')}_{len(self.schedule)}"

        post = ScheduledPost(
            id=post_id,
            platform=platform,
            content=content,
            hashtags=hashtags or [],
            scheduled_time=scheduled_time,
            status="pending",
            metadata=metadata or {}
        )

        self.schedule.append(post)
        self.save_schedule()

        return post

    def get_pending_posts(
        self,
        platform: str = None,
        before: datetime = None
    ) -> list[ScheduledPost]:
        """대기 중인 포스트 조회"""
        posts = [p for p in self.schedule if p.status == "pending"]

        if platform:
            posts = [p for p in posts if p.platform == platform]

        if before:
            posts = [p for p in posts if p.scheduled_time <= before]

        return sorted(posts, key=lambda p: p.scheduled_time)

    def mark_as_published(self, post_id: str) -> bool:
        """포스트 발행 완료 처리"""
        for post in self.schedule:
            if post.id == post_id:
                post.status = "published"
                self.save_schedule()
                return True
        return False

    def mark_as_failed(self, post_id: str, error: str = None) -> bool:
        """포스트 발행 실패 처리"""
        for post in self.schedule:
            if post.id == post_id:
                post.status = "failed"
                if error:
                    post.metadata = post.metadata or {}
                    post.metadata["error"] = error
                self.save_schedule()
                return True
        return False

    def generate_weekly_schedule(
        self,
        start_date: datetime = None
    ) -> dict:
        """
        주간 포스팅 스케줄 생성

        Returns:
            플랫폼별 추천 스케줄
        """
        if start_date is None:
            start_date = datetime.now()

        schedule = {}

        for platform, settings in self.OPTIMAL_TIMES.items():
            schedule[platform] = []
            posts_needed = settings["posts_per_week"]

            current_time = start_date
            for _ in range(posts_needed):
                optimal_time = self.get_next_optimal_time(platform, current_time)
                schedule[platform].append({
                    "day": optimal_time.strftime("%A"),
                    "date": optimal_time.strftime("%Y-%m-%d"),
                    "time": optimal_time.strftime("%H:%M"),
                    "datetime": optimal_time.isoformat()
                })
                current_time = optimal_time + timedelta(hours=1)

        return schedule

    def get_schedule_summary(self) -> dict:
        """스케줄 요약"""
        total = len(self.schedule)
        pending = len([p for p in self.schedule if p.status == "pending"])
        published = len([p for p in self.schedule if p.status == "published"])
        failed = len([p for p in self.schedule if p.status == "failed"])

        by_platform = {}
        for post in self.schedule:
            if post.platform not in by_platform:
                by_platform[post.platform] = {"pending": 0, "published": 0, "failed": 0}
            by_platform[post.platform][post.status] += 1

        return {
            "total": total,
            "pending": pending,
            "published": published,
            "failed": failed,
            "by_platform": by_platform
        }


if __name__ == "__main__":
    scheduler = PostingScheduler()

    print("=== 주간 스케줄 생성 ===")
    weekly = scheduler.generate_weekly_schedule()

    for platform, times in weekly.items():
        print(f"\n{platform.upper()}:")
        for slot in times:
            print(f"  {slot['day']} {slot['date']} {slot['time']}")

    print("\n=== 포스트 스케줄 추가 테스트 ===")
    post = scheduler.add_post(
        platform="linkedin",
        content="테스트 포스트입니다.",
        hashtags=["AI", "바리온랩스"]
    )
    print(f"스케줄됨: {post.id} at {post.scheduled_time}")

    print("\n=== 스케줄 요약 ===")
    summary = scheduler.get_schedule_summary()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
