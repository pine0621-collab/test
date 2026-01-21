# 아침 증시 알림 시스템

매일 아침 지정된 시간에 코스피, 코스닥, 주요 종목 현황을 Slack 채널로 알려주는 시스템입니다.

## 기능

- **주요 지수**: 코스피, 코스닥, 다우존스, 나스닥, S&P 500
- **국내 종목**: 삼성전자, SK하이닉스, 현대차, NAVER, 카카오
- **자동 실행**: 평일 아침 지정 시간에 자동 전송
- **주말 제외**: 토/일요일은 자동 건너뜀

## 설치

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일에서 SLACK_BOT_TOKEN 및 SLACK_CHANNEL_ID 설정
```

## 환경변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `SLACK_BOT_TOKEN` | Slack Bot 토큰 | `xoxb-...` |
| `SLACK_CHANNEL_ID` | 알림 받을 채널 ID | `C05THCPQ9T9` |
| `ALERT_HOUR` | 알림 시간 (시) | `8` |
| `ALERT_MINUTE` | 알림 시간 (분) | `30` |
| `TIMEZONE` | 타임존 | `Asia/Seoul` |

## 사용법

```bash
# 테스트 실행 (즉시 1회 전송)
python main.py --once

# 스케줄러 실행 (백그라운드)
python main.py

# 특정 시간으로 실행
python main.py --hour 9 --minute 0
```

## 프로젝트 구조

```
.
├── main.py              # 메인 실행 파일
├── requirements.txt     # 의존성 목록
├── .env.example         # 환경변수 예시
└── src/
    ├── market_data.py   # 증시 데이터 수집
    └── slack_notifier.py # Slack 알림 전송
```

## Slack Bot 설정

1. [Slack API](https://api.slack.com/apps)에서 새 앱 생성
2. OAuth & Permissions에서 Bot Token Scopes 추가:
   - `chat:write`
   - `chat:write.public`
3. 앱을 워크스페이스에 설치
4. Bot User OAuth Token을 `.env`에 설정
