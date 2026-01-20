# 아침 대기목록 알림 설정 가이드

매일 오전 9시(KST)에 슬랙으로 대기목록 알림을 받을 수 있습니다.
이 가이드는 처음 설정하는 분도 쉽게 따라할 수 있도록 상세하게 작성되었습니다.

---

## 목차

1. [사전 준비](#1-사전-준비)
2. [Slack 앱 생성하기](#2-slack-앱-생성하기)
3. [Webhook URL 생성하기](#3-webhook-url-생성하기)
4. [GitHub Secrets 설정하기](#4-github-secrets-설정하기)
5. [알림 테스트하기](#5-알림-테스트하기)
6. [대기목록 관리하기](#6-대기목록-관리하기)
7. [문제 해결 (트러블슈팅)](#7-문제-해결-트러블슈팅)
8. [자주 묻는 질문 (FAQ)](#8-자주-묻는-질문-faq)

---

## 1. 사전 준비

시작하기 전에 다음 사항을 확인하세요:

| 항목 | 필수 여부 | 설명 |
|------|----------|------|
| Slack 워크스페이스 관리자 권한 | ✅ 필수 | 앱을 설치하려면 관리자이거나 관리자 승인이 필요합니다 |
| GitHub 저장소 관리자 권한 | ✅ 필수 | Secrets 설정을 위해 필요합니다 |
| 웹 브라우저 | ✅ 필수 | Chrome, Firefox, Safari 등 |

---

## 2. Slack 앱 생성하기

### 2.1. Slack API 페이지 접속

1. 웹 브라우저를 열고 **[https://api.slack.com/apps](https://api.slack.com/apps)** 에 접속합니다
2. 우측 상단의 **"Sign in"** 버튼을 클릭합니다
3. Slack 워크스페이스 계정으로 로그인합니다

### 2.2. 새 앱 만들기

1. **"Create New App"** 버튼을 클릭합니다 (녹색 버튼)

2. 팝업창에서 **"From scratch"** 를 선택합니다
   > ⚠️ "From an app manifest"가 아닌 **"From scratch"**를 선택해야 합니다

3. 앱 정보를 입력합니다:
   ```
   App Name: 바리온랩스 알림봇
   Pick a workspace to develop your app in: [본인의 워크스페이스 선택]
   ```
   > 💡 앱 이름은 원하는 대로 변경 가능합니다 (예: "아침 알림봇", "대기목록 알리미")

4. **"Create App"** 버튼을 클릭합니다

---

## 3. Webhook URL 생성하기

### 3.1. Incoming Webhooks 활성화

1. 앱이 생성되면 **"Basic Information"** 페이지가 표시됩니다

2. 좌측 사이드바에서 **"Features"** 섹션 아래의 **"Incoming Webhooks"** 를 클릭합니다
   ```
   📍 위치: 좌측 메뉴 > Features > Incoming Webhooks
   ```

3. 화면 상단의 **"Activate Incoming Webhooks"** 토글을 **"On"** 으로 변경합니다
   - Off (회색) → **On (녹색)**

### 3.2. Webhook URL 추가

1. 페이지 하단의 **"Add New Webhook to Workspace"** 버튼을 클릭합니다

2. 권한 요청 페이지가 나타납니다:
   ```
   [앱 이름]이(가) [워크스페이스]에 액세스하도록 허용하시겠습니까?

   [앱 이름]이(가) 다음 작업을 수행할 수 있습니다:
   ✓ 채널에 메시지 게시
   ```

3. **"알림을 받을 채널"** 을 선택합니다:
   - 드롭다운에서 원하는 채널 선택 (예: `#general`, `#알림`, 또는 개인 DM)

   > 💡 **채널 선택 팁:**
   > - 팀 전체 알림: `#general` 또는 `#공지사항`
   > - 개인 알림: **"Direct Messages"** 에서 본인 선택
   > - 특정 프로젝트: 해당 프로젝트 채널 선택

4. **"허용(Allow)"** 버튼을 클릭합니다

### 3.3. Webhook URL 복사

1. **"Incoming Webhooks"** 페이지로 돌아오면 새로운 Webhook URL이 생성되어 있습니다

2. **"Webhook URL"** 섹션에서 생성된 URL을 찾습니다:
   ```
   [여기에 Webhook URL이 표시됩니다 - 복사하세요]
   형식: https://hooks.slack.com/services/T.../B.../...
   ```

3. **"Copy"** 버튼을 클릭하여 URL을 복사합니다
   > ⚠️ **중요:** 이 URL은 절대 외부에 공개하지 마세요!
   > URL을 알면 누구나 해당 채널에 메시지를 보낼 수 있습니다.

4. 복사한 URL을 메모장 등에 임시 저장해 둡니다

---

## 4. GitHub Secrets 설정하기

### 4.1. 저장소 Settings 접속

1. GitHub에서 **해당 저장소**로 이동합니다
   ```
   예: https://github.com/pine0621-collab/test
   ```

2. 상단 탭에서 **"Settings"** 를 클릭합니다
   ```
   📍 위치: Code | Issues | Pull requests | Actions | Projects | Wiki | Security | Insights | Settings
                                                                                              ^^^^^^^^
   ```
   > ⚠️ Settings가 보이지 않으면 저장소 관리자 권한이 없는 것입니다

### 4.2. Secrets and Variables 메뉴 진입

1. 좌측 사이드바에서 **"Security"** 섹션을 찾습니다

2. **"Secrets and variables"** 를 클릭하면 하위 메뉴가 펼쳐집니다

3. **"Actions"** 를 클릭합니다
   ```
   📍 위치: 좌측 메뉴 > Security > Secrets and variables > Actions
   ```

### 4.3. SLACK_WEBHOOK_URL 시크릿 추가

1. **"New repository secret"** 버튼을 클릭합니다 (녹색 버튼)

2. 다음과 같이 입력합니다:

   | 필드 | 값 |
   |------|-----|
   | **Name** | `SLACK_WEBHOOK_URL` |
   | **Secret** | 아까 복사한 Webhook URL 붙여넣기 |

   > ⚠️ **주의사항:**
   > - Name은 반드시 `SLACK_WEBHOOK_URL` 이어야 합니다 (대소문자 정확히)
   > - Secret에 앞뒤 공백이 없는지 확인하세요

3. **"Add secret"** 버튼을 클릭합니다

### 4.4. (선택사항) SLACK_CHANNEL 시크릿 추가

특정 채널을 지정하고 싶다면:

1. 다시 **"New repository secret"** 버튼을 클릭합니다

2. 다음과 같이 입력합니다:

   | 필드 | 값 |
   |------|-----|
   | **Name** | `SLACK_CHANNEL` |
   | **Secret** | `#채널이름` (예: `#general`) |

3. **"Add secret"** 버튼을 클릭합니다

### 4.5. 설정 확인

Secrets 목록에서 다음과 같이 표시되면 성공입니다:

```
Repository secrets
──────────────────────────────────────
Name                    Updated
SLACK_WEBHOOK_URL       now
SLACK_CHANNEL           now        (선택사항)
```

---

## 5. 알림 테스트하기

### 5.1. 수동으로 워크플로우 실행

1. GitHub 저장소에서 **"Actions"** 탭을 클릭합니다

2. 좌측에서 **"Morning Todo Notification"** 워크플로우를 선택합니다

3. **"Run workflow"** 버튼을 클릭합니다

4. 드롭다운에서 브랜치를 선택하고 **"Run workflow"** (녹색 버튼)을 클릭합니다

### 5.2. 실행 결과 확인

1. 워크플로우 실행이 완료될 때까지 기다립니다 (약 30초~1분)

2. 상태가 ✅ (녹색 체크)로 표시되면 성공입니다

3. Slack에서 알림 메시지가 도착했는지 확인합니다

### 5.3. 알림 예시

정상적으로 설정되면 다음과 같은 메시지가 Slack에 도착합니다:

```
🌅 오늘의 대기목록 (2026-01-21)

오늘 처리해야 할 업무 2건

🔴 [콘텐츠] 오늘 만든 영상콘텐츠 - 국민성장펀드 ABQ - 업로드
🔴 [콘텐츠] GSC영상검수 & 재촬영

💡 대기목록을 완료하면 슬랙에서 업데이트해 주세요!
```

---

## 6. 대기목록 관리하기

### 6.1. 대기목록 파일 위치

대기목록은 `data/todo.json` 파일에서 관리됩니다.

### 6.2. 파일 형식

```json
{
  "pending_tasks": [
    {
      "id": 1,
      "task": "업무 내용을 여기에 작성",
      "category": "카테고리",
      "priority": "high",
      "due_date": "2026-01-21",
      "created_at": "2026-01-20"
    },
    {
      "id": 2,
      "task": "두 번째 업무",
      "category": "미팅",
      "priority": "medium",
      "due_date": "2026-01-21",
      "created_at": "2026-01-20"
    }
  ]
}
```

### 6.3. 필드 설명

| 필드 | 필수 | 설명 | 예시 |
|------|------|------|------|
| `id` | ✅ | 고유 식별자 (숫자) | `1`, `2`, `3` |
| `task` | ✅ | 업무 내용 | `"영상 편집 완료하기"` |
| `category` | ❌ | 업무 분류 | `"콘텐츠"`, `"미팅"`, `"개발"` |
| `priority` | ❌ | 우선순위 | `"high"`, `"medium"`, `"low"` |
| `due_date` | ❌ | 마감일 | `"2026-01-21"` |
| `created_at` | ❌ | 생성일 | `"2026-01-20"` |

### 6.4. 우선순위 표시

알림에서 우선순위는 다음과 같이 표시됩니다:

| 우선순위 | 표시 | 의미 |
|---------|------|------|
| `high` | 🔴 | 긴급/중요 |
| `medium` | 🟡 | 보통 |
| `low` | 🟢 | 여유 있음 |

### 6.5. 새 업무 추가하기

1. `data/todo.json` 파일을 엽니다

2. `pending_tasks` 배열에 새 항목을 추가합니다:
   ```json
   {
     "id": 3,
     "task": "새로운 업무 내용",
     "category": "기타",
     "priority": "medium",
     "due_date": "2026-01-22",
     "created_at": "2026-01-21"
   }
   ```

3. 파일을 저장하고 커밋합니다

---

## 7. 문제 해결 (트러블슈팅)

### 문제 1: Slack에 알림이 오지 않아요

**확인사항:**

1. **Webhook URL이 올바른지 확인**
   - GitHub Secrets에서 `SLACK_WEBHOOK_URL` 값이 정확한지 확인
   - URL이 `https://hooks.slack.com/services/`로 시작하는지 확인

2. **워크플로우 실행 상태 확인**
   - Actions 탭에서 워크플로우가 ✅ 성공인지 확인
   - ❌ 실패라면 로그를 클릭해서 에러 메시지 확인

3. **채널 권한 확인**
   - 선택한 채널이 비공개인 경우 앱이 해당 채널에 초대되어 있는지 확인

### 문제 2: 워크플로우가 실패해요

**에러 메시지별 해결방법:**

| 에러 메시지 | 원인 | 해결방법 |
|------------|------|---------|
| `secret not found` | Secrets 설정 안됨 | 4단계 다시 수행 |
| `invalid_token` | Webhook URL 오류 | URL 다시 복사/붙여넣기 |
| `channel_not_found` | 채널이 없음 | 채널 이름 확인 |
| `rate_limited` | 요청 너무 많음 | 잠시 후 다시 시도 |

### 문제 3: 알림 시간이 이상해요

- GitHub Actions의 cron은 UTC 기준입니다
- `0 0 * * *` = UTC 0시 = **한국시간 오전 9시**
- 서버 부하에 따라 최대 15분 정도 지연될 수 있습니다

### 문제 4: 대기목록이 안 보여요

1. `data/todo.json` 파일이 존재하는지 확인
2. JSON 형식이 올바른지 확인 (쉼표, 중괄호 등)
3. `pending_tasks` 배열에 항목이 있는지 확인

---

## 8. 자주 묻는 질문 (FAQ)

### Q1. 알림 시간을 변경할 수 있나요?

**A:** 네, `.github/workflows/morning-notification.yml` 파일에서 cron 표현식을 수정하면 됩니다.

```yaml
# 예시: 오후 6시(KST)에 알림 받기
schedule:
  - cron: '0 9 * * *'  # UTC 9시 = KST 18시
```

| 원하는 시간 (KST) | cron 설정 (UTC) |
|------------------|-----------------|
| 오전 8시 | `0 23 * * *` (전날 UTC 23시) |
| 오전 9시 | `0 0 * * *` |
| 오전 10시 | `0 1 * * *` |
| 오후 6시 | `0 9 * * *` |

### Q2. 주말에는 알림을 받고 싶지 않아요

**A:** cron 표현식에 요일 조건을 추가하세요.

```yaml
# 월~금요일만 알림
schedule:
  - cron: '0 0 * * 1-5'  # 1=월요일, 5=금요일
```

### Q3. 여러 채널에 알림을 보낼 수 있나요?

**A:** 각 채널별로 별도의 Webhook URL을 생성하고, 워크플로우를 복제하여 설정하면 됩니다.

### Q4. Webhook URL이 노출되면 어떻게 하나요?

**A:**
1. Slack API 페이지에서 해당 Webhook을 즉시 삭제합니다
2. 새 Webhook URL을 생성합니다
3. GitHub Secrets에서 `SLACK_WEBHOOK_URL` 값을 업데이트합니다

### Q5. 대기목록을 Slack에서 직접 수정할 수 있나요?

**A:** 현재는 `data/todo.json` 파일을 직접 수정해야 합니다. 향후 Slack 명령어 연동 기능 추가를 검토 중입니다.

---

## 파일 구조

```
📁 저장소 루트
├── 📁 .github
│   └── 📁 workflows
│       └── 📄 morning-notification.yml  ← GitHub Actions 워크플로우
├── 📁 scripts
│   └── 📄 send_morning_notification.py  ← 알림 전송 스크립트
├── 📁 data
│   └── 📄 todo.json                     ← 대기목록 데이터
└── 📄 MORNING_NOTIFICATION_SETUP.md     ← 이 가이드 문서
```

---

## 도움이 필요하신가요?

설정 중 문제가 발생하면 Slack에서 바리온랩스팀에게 문의하세요!

---

*마지막 업데이트: 2026-01-20*
