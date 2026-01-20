#!/usr/bin/env python3
"""
아침 대기목록 알림 스크립트
매일 오전 9시에 실행되어 슬랙으로 대기목록을 전송합니다.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# 환경 변수에서 슬랙 웹훅 URL 가져오기
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '#general')

def load_todo_data(file_path: str) -> dict:
    """대기목록 JSON 파일 로드"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} 파일을 찾을 수 없습니다.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: JSON 파싱 오류 - {e}")
        sys.exit(1)

def format_slack_message(todo_data: dict) -> dict:
    """슬랙 메시지 포맷 생성"""
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    pending_tasks = todo_data.get('pending_tasks', [])

    if not pending_tasks:
        task_list = "등록된 대기목록이 없습니다."
    else:
        task_lines = []
        for i, task in enumerate(pending_tasks, 1):
            priority_emoji = "🔴" if task.get('priority') == 'high' else "🟡" if task.get('priority') == 'medium' else "🟢"
            category = task.get('category', '기타')
            task_lines.append(f"{priority_emoji} [{category}] {task['task']}")
        task_list = "\n".join(task_lines)

    # 슬랙 Block Kit 메시지 포맷
    message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🌅 오늘의 대기목록 ({today})",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*오늘 처리해야 할 업무 {len(pending_tasks)}건*\n\n{task_list}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "💡 대기목록을 완료하면 슬랙에서 업데이트해 주세요!"
                    }
                ]
            }
        ]
    }

    return message

def send_slack_notification(message: dict) -> bool:
    """슬랙으로 알림 전송"""
    if not SLACK_WEBHOOK_URL:
        print("Error: SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return False

    try:
        data = json.dumps(message).encode('utf-8')
        req = Request(SLACK_WEBHOOK_URL, data=data, headers={'Content-Type': 'application/json'})

        with urlopen(req) as response:
            if response.status == 200:
                print("✅ 슬랙 알림이 성공적으로 전송되었습니다.")
                return True
            else:
                print(f"❌ 슬랙 알림 전송 실패: {response.status}")
                return False

    except HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        return False
    except URLError as e:
        print(f"❌ URL Error: {e.reason}")
        return False

def main():
    """메인 함수"""
    # 스크립트 디렉토리 기준으로 todo.json 경로 설정
    script_dir = os.path.dirname(os.path.abspath(__file__))
    todo_file = os.path.join(script_dir, '..', 'data', 'todo.json')

    print(f"📋 대기목록 파일 로드 중: {todo_file}")
    todo_data = load_todo_data(todo_file)

    print("📝 슬랙 메시지 생성 중...")
    message = format_slack_message(todo_data)

    print("📤 슬랙으로 알림 전송 중...")
    success = send_slack_notification(message)

    if success:
        print("🎉 아침 알림 완료!")
        sys.exit(0)
    else:
        print("⚠️ 알림 전송에 실패했습니다.")
        sys.exit(1)

if __name__ == '__main__':
    main()
