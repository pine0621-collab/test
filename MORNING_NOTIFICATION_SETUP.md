# 아침 대기목록 알림 설정 가이드

매일 오전 9시(KST)에 슬랙으로 대기목록 알림을 받을 수 있습니다.

## 설정 방법

### 1. Slack Webhook URL 생성

1. [Slack API](https://api.slack.com/apps)에 접속
2. "Create New App" > "From scratch" 선택
3. 앱 이름 입력 (예: "바리온랩스 알림봇")
4. 워크스페이스 선택 후 "Create App"
5. 좌측 메뉴에서 "Incoming Webhooks" 클릭
6. "Activate Incoming Webhooks"를 On으로 변경
7. "Add New Webhook to Workspace" 클릭
8. 알림받을 채널 선택 (예: #general)
9. 생성된 Webhook URL 복사

### 2. GitHub Secrets 설정

1. GitHub 저장소 > Settings > Secrets and variables > Actions
2. "New repository secret" 클릭
3. 다음 시크릿 추가:
   - `SLACK_WEBHOOK_URL`: 위에서 복사한 Webhook URL
   - `SLACK_CHANNEL`: 알림받을 채널 (선택사항)

### 3. 대기목록 관리

대기목록은 `data/todo.json` 파일에서 관리됩니다.

```json
{
  "pending_tasks": [
    {
      "id": 1,
      "task": "업무 내용",
      "category": "콘텐츠",
      "priority": "high",
      "due_date": "2026-01-21",
      "created_at": "2026-01-20"
    }
  ]
}
```

**우선순위 표시:**
- `high`: 🔴 빨간색
- `medium`: 🟡 노란색
- `low`: 🟢 초록색

## 알림 시간

- **한국 시간 오전 9시**에 자동 실행
- GitHub Actions의 cron은 UTC 기준이므로 `0 0 * * *` (UTC 0시 = KST 9시)

## 수동 실행

GitHub Actions 탭에서 "Morning Todo Notification" 워크플로우를 선택하고 "Run workflow"를 클릭하면 수동으로 실행할 수 있습니다.

## 파일 구조

```
.github/
  workflows/
    morning-notification.yml  # GitHub Actions 워크플로우
scripts/
  send_morning_notification.py  # 알림 전송 스크립트
data/
  todo.json  # 대기목록 데이터
```

## 알림 예시

```
🌅 오늘의 대기목록 (2026-01-21)

오늘 처리해야 할 업무 2건

🔴 [콘텐츠] 오늘 만든 영상콘텐츠 - 국민성장펀드 ABQ - 업로드
🔴 [콘텐츠] GSC영상검수 & 재촬영

💡 대기목록을 완료하면 슬랙에서 업데이트해 주세요!
```
