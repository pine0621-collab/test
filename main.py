#!/usr/bin/env python3
"""
아침 증시 알림 시스템

매일 아침 지정된 시간에 증시 현황을 Slack 채널로 전송합니다.

사용법:
    # 한 번 실행 (테스트)
    python main.py --once

    # 스케줄러로 실행 (백그라운드)
    python main.py

    # 특정 시간 설정
    python main.py --hour 9 --minute 0
"""
import os
import argparse
from datetime import datetime

import pytz
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from src.market_data import get_market_summary, format_market_message
from src.slack_notifier import SlackNotifier, create_market_blocks


def send_morning_alert():
    """아침 증시 알림을 전송합니다."""
    tz = pytz.timezone(os.getenv("TIMEZONE", "Asia/Seoul"))
    now = datetime.now(tz)
    print(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S')}] 아침 증시 알림 실행 중...")

    # 주말 체크 (토요일=5, 일요일=6)
    if now.weekday() >= 5:
        print("[정보] 주말이므로 알림을 건너뜁니다.")
        return

    try:
        # 증시 데이터 수집
        print("[정보] 증시 데이터 수집 중...")
        data = get_market_summary()

        if not data["indices"] and not data["stocks"]:
            print("[경고] 증시 데이터를 가져오지 못했습니다.")
            return

        # Slack 전송
        print("[정보] Slack 메시지 전송 중...")
        notifier = SlackNotifier()

        # Block Kit 형식으로 전송 (더 보기 좋음)
        blocks = create_market_blocks(data)
        success = notifier.send_blocks(blocks, text="오늘의 증시 현황")

        if success:
            print("[완료] 아침 증시 알림이 성공적으로 전송되었습니다.")
        else:
            # 블록 전송 실패 시 텍스트로 재시도
            print("[정보] 텍스트 형식으로 재시도 중...")
            message = format_market_message(data)
            notifier.send_message(message)

    except Exception as e:
        print(f"[오류] 알림 전송 중 오류 발생: {e}")


def main():
    """메인 함수"""
    load_dotenv()

    parser = argparse.ArgumentParser(description="아침 증시 알림 시스템")
    parser.add_argument("--once", action="store_true", help="한 번만 실행 (테스트용)")
    parser.add_argument("--hour", type=int, default=None, help="알림 시간 (시)")
    parser.add_argument("--minute", type=int, default=None, help="알림 시간 (분)")
    args = parser.parse_args()

    if args.once:
        print("=== 테스트 실행 (1회) ===")
        send_morning_alert()
        return

    # 환경변수에서 설정 로드
    hour = args.hour or int(os.getenv("ALERT_HOUR", "8"))
    minute = args.minute or int(os.getenv("ALERT_MINUTE", "30"))
    timezone = os.getenv("TIMEZONE", "Asia/Seoul")

    print("=== 아침 증시 알림 스케줄러 시작 ===")
    print(f"알림 시간: 매일 {hour:02d}:{minute:02d} ({timezone})")
    print(f"주말 제외: 예")
    print("종료하려면 Ctrl+C를 누르세요.\n")

    # 스케줄러 설정
    scheduler = BlockingScheduler(timezone=timezone)

    # 월~금 매일 아침 실행
    trigger = CronTrigger(
        day_of_week="mon-fri",
        hour=hour,
        minute=minute,
        timezone=timezone,
    )

    scheduler.add_job(
        send_morning_alert,
        trigger=trigger,
        id="morning_market_alert",
        name="아침 증시 알림",
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n스케줄러가 종료되었습니다.")


if __name__ == "__main__":
    main()
