# 바리온랩스 AI 지식베이스

바리온랩스 회사소개서를 기반으로 구축된 AI 지식베이스입니다.

## 구조

```
knowledge-base/
├── index.json              # 지식베이스 메타 정보
├── README.md               # 이 파일
├── company/                # 회사 정보
│   ├── company-profile.json
│   └── company-overview.md
├── services/               # 서비스 정보
│   ├── services.json
│   └── services-overview.md
├── team/                   # 팀 정보
│   ├── team.json
│   └── team-overview.md
├── projects/               # 프로젝트 실적
│   ├── projects.json
│   └── projects-portfolio.md
└── faq/                    # FAQ
    ├── faq.json
    └── faq.md
```

## 파일 형식

- **JSON 파일**: 구조화된 데이터로 AI 시스템에서 직접 파싱하여 활용
- **MD 파일**: 사람이 읽기 쉬운 형태의 문서로 컨텍스트 제공

## 활용 방법

### 1. RAG (Retrieval-Augmented Generation) 시스템
- JSON 파일을 벡터 DB에 임베딩하여 검색
- 사용자 질문에 맞는 관련 정보 검색 후 AI가 응답 생성

### 2. 챗봇 시스템
- FAQ를 우선 검색하여 빠른 응답
- 상세 정보가 필요한 경우 해당 카테고리의 JSON/MD 파일 참조

### 3. 지식 관리
- 회사 정보 업데이트 시 해당 JSON/MD 파일 수정
- 새로운 프로젝트 추가 시 projects.json 및 projects-portfolio.md 업데이트

## 데이터 소스

- 바리온랩스 회사소개서
- 공식 웹사이트: https://www.baryon.ai/
- Labs 사이트: https://labs.baryon.ai/

## 버전

- v1.0.0 (2026-01-16): 초기 지식베이스 구축
