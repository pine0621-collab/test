# Slack 몰입 업무 리마인더 봇

매일 오후 5시(KST)에 Slack 채널로 몰입 업무 체크인 리마인더를 보내는 봇입니다.

## 리마인더 메시지

> :dart: **오늘의 몰입 업무 체크인**
>
> 오늘 몰입한 업무와 몰입에 방해되는 업무는 무엇이셨나요?
>
> - :fire: **몰입한 업무:**
> - :no_entry_sign: **몰입을 방해한 업무:**

## 설정

### 1. Slack App 생성

1. [Slack API](https://api.slack.com/apps)에서 새 앱 생성
2. **OAuth & Permissions**에서 Bot Token Scopes 추가:
   - `chat:write` — 메시지 전송
3. 워크스페이스에 앱 설치 후 Bot User OAuth Token 복사

### 2. 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 편집하여 값을 채웁니다:

| 변수 | 설명 | 예시 |
|------|------|------|
| `SLACK_BOT_TOKEN` | Slack Bot OAuth Token | `xoxb-...` |
| `SLACK_CHANNEL_ID` | 대상 채널 ID | `C05THCPQ9T9` |
| `TZ` | 타임존 | `Asia/Seoul` |
| `CRON_SCHEDULE` | 크론 표현식 (선택) | `0 17 * * 1-5` |

### 3. 실행

```bash
npm install
npm start
```

## 크론 스케줄

기본값은 `0 17 * * 1-5` (평일 오후 5시)입니다.

| 표현식 | 설명 |
|--------|------|
| `0 17 * * 1-5` | 평일 오후 5시 |
| `0 17 * * *` | 매일 오후 5시 |
| `0 9,17 * * 1-5` | 평일 오전 9시, 오후 5시 |
