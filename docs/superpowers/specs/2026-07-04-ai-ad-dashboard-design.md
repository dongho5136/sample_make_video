# AI 광고영상 제작 관리자 대시보드 — 설계 문서

작성일: 2026-07-04

## 1. 목적 & 범위

AI 광고영상 자동 제작 시스템의 **초기 관리자 대시보드**. 1차 개발은 실제 AI
영상 생성 없이, **더미데이터 기반 프론트엔드 화면**으로 다음 흐름을 구현한다:

> 템플릿 등록 → 광고 생성 요청 → 구간별 생성 상태 확인 → 최종 결과 확인

클라이언트가 전체 서비스 구조와 사용 흐름을 웹에서 직접 눈으로 확인하는 것이
목표인 **인터랙티브 데모**다.

### 포함 범위
- 좌측 사이드바 대시보드 UI (7개 화면)
- 더미데이터 기반 리스트/카드/상태값 표시
- 모달 입력 폼, 구간별 생성 진행 애니메이션
- 기본 반응형 레이아웃
- Vercel 배포

### 제외 범위
실제 AI 영상 생성 API, 실제 영상 업로드/저장, 실제 DB, 실제 로그인, 실제 IP
차단, 광고 매체 연동, 성과 데이터 수집, 학습/자동 최적화.

## 2. 기술 스택 & 결정사항

| 항목 | 결정 |
|------|------|
| 프론트 렌더링 | **Flask API + Vanilla JS fetch** — Flask가 `/api/*` JSON 제공, JS가 fetch로 렌더링 |
| 페이지 구조 | **멀티페이지** — 메뉴별 개별 URL (Flask 라우팅) |
| 디자인 톤 | **모던 다크 대시보드** — 진한 배경, 퍼플/블루 액센트, 카드 그림자 |
| 상호작용 | **인터랙티브 데모** — 모달, 진행바 애니메이션, 상태 전환 포함 |
| 백엔드 | Python Flask |
| 프론트 | Vanilla HTML / CSS / JS |
| 배포 | Vercel (`@vercel/python`) |
| 데이터 | DB 없이 in-memory 더미데이터, 추후 DB 연동 가능 구조 |

**설계 원칙**: 실제 DB/AI API로 전환 시 `data/dummy.py`와 `/api/*` 핸들러만
교체하면 되고, 프론트엔드 코드는 그대로 유지되도록 경계를 분리한다.

## 3. 아키텍처

```
app.py
├── 페이지 라우트  → Jinja2로 뼈대 HTML 렌더 (base.html 상속)
│   /dashboard /generate /templates /assets /jobs /results /settings
│   / → /dashboard 리다이렉트
├── API 라우트 (/api/*) → 더미데이터 JSON 반환
│   GET  /api/dashboard/stats
│   GET  /api/templates      POST /api/templates
│   GET  /api/assets         POST /api/assets
│   GET  /api/jobs           POST /api/jobs
│   GET  /api/results
│   GET  /api/settings
└── 404 핸들러

data/
└── dummy.py   → 모든 더미데이터의 단일 소스 (모듈 전역 리스트/딕셔너리)

templates/
├── base.html          → 사이드바 + 헤더 공통 레이아웃
├── dashboard.html  generate.html  templates.html
├── assets.html  jobs.html  results.html  settings.html
└── 404.html

static/
├── css/
│   ├── main.css        → 다크 테마 변수, 레이아웃, 사이드바, 헤더
│   └── components.css  → 카드, 테이블, 배지, 모달, 버튼, 폼, 진행바
└── js/
    ├── api.js          → fetch 래퍼 (에러 처리 공통)
    ├── components.js   → 모달 open/close, 토스트, 상태배지 헬퍼
    ├── dashboard.js  generate.js  templates.js
    └── assets.js  jobs.js  results.js  settings.js
```

**데이터 흐름**: Flask가 화면 뼈대만 렌더 → JS가 로드 시 `/api/*` fetch →
카드/테이블/배지 렌더. 폼 제출/등록은 `POST /api/*`로 보내되, Vercel
serverless는 요청 간 in-memory 상태가 유지되지 않으므로 **새로 추가된 항목은
프론트 세션 내(JS 로컬 배열)에서만 유지**한다(새로고침 시 초기화).

## 4. 화면별 상세

### 공통 레이아웃 (base.html)
- 좌측 사이드바: 로고 + 7개 메뉴, 현재 페이지 하이라이트, 좁은 화면에서 토글 접힘
- 상단 헤더: 페이지 타이틀 + 관리자 프로필(더미)
- 메인 콘텐츠 영역: `{% block content %}`

### 1) 대시보드 `/dashboard`
- 통계 카드 6~8개: 전체 생성 광고 수, 완료, 생성 중, 실패, 등록 템플릿 수, 등록 에셋 수
- 최근 생성 광고 목록 테이블 (상태 배지 포함)
- API: `GET /api/dashboard/stats`

### 2) 광고 생성 `/generate`
- 입력 폼: 광고명, 제품명, 브랜드명, 광고 목적, 광고 길이, 영상 비율, AI 모델,
  스타일 템플릿, 캐릭터 에셋, 제품 이미지, 로고 이미지, 추가 요청사항
- 필수 필드(광고명/제품명/템플릿) 인라인 검증, 미충족 시 제출 차단
- "생성 요청" 클릭 → **구간별 진행 애니메이션**:
  `setInterval`로 각 구간을 `대기중 → 생성중 → 완료`로 순차 전환 → 전체 완료 시
  `합본중 → 완료` → 결과 요약 표시
- API: `POST /api/jobs`

### 3) 템플릿 관리 `/templates`
- 카드 그리드로 템플릿 목록 (예: 뼈순이 D-30일, 실사 인터뷰, 숏폼 바이럴,
  후기형, Before&After, 프리미엄 브랜드, 애니메이션 — 7종)
- 카드 표시: 템플릿명, 스타일, 추천 길이/모델, 사용 여부 배지
- "신규 등록" → 모달 폼 (템플릿명/스타일/기본·자막·장면 프롬프트/나레이션 톤/
  추천 길이/추천 모델/사용 여부)
- API: `GET /api/templates`, `POST /api/templates`

### 4) 에셋 관리 `/assets`
- 유형 필터(캐릭터/제품/로고/배경/참고 이미지/참고 영상) + 카드 그리드
- 카드: 이미지 미리보기(플레이스홀더), 에셋명, 유형 배지, 설명, 사용 여부
- "등록" → 모달 폼
- API: `GET /api/assets`, `POST /api/assets`

### 5) 생성 작업 목록 `/jobs`
- 테이블: 작업명, 사용 템플릿, 사용 모델, 영상 길이, 생성 상태(배지), 요청일, 완료일, 재생성 버튼
- 상태값: 대기 중 / 생성 중 / 구간 생성 완료 / 합본 생성 중 / 완료 / 실패
- API: `GET /api/jobs`

### 6) 생성 결과 관리 `/results`
- 카드 목록 → 선택 시 상세: 최종 영상 플레이어(플레이스홀더), 6구간 영상 썸네일
  (1.후킹 2.문제상황 3.제품소개 4.사용장면 5.혜택강조 6.CTA), 사용 템플릿/에셋/
  모델, 생성일, 다운로드/재생성 버튼
- API: `GET /api/results`

### 7) 설정 `/settings`
- IP 제한(허용 IP 목록/사용 여부/마지막 접속 IP/접속 로그), 관리자 계정,
  기본 영상 비율, 기본 생성 모델, 기본 저장 경로, API 연동, 광고 매체 연동
- UI만 구성, 저장 시 토스트만 표시 (실제 동작 없음)
- API: `GET /api/settings`

## 5. 데이터 모델 (data/dummy.py)

```python
TEMPLATES = [{
  "id", "name", "style", "base_prompt", "subtitle_prompt",
  "scene_prompt", "narration_tone", "rec_length", "rec_model", "active"
}]
ASSETS = [{
  "id", "name", "type", "image_url", "description", "ref_prompt", "active"
}]
JOBS = [{
  "id", "name", "template", "model", "length", "status",
  "requested_at", "completed_at",
  "segments": [{"name", "status"}]
}]
RESULTS = [{
  "id", "name", "final_video", "template", "assets", "model", "created_at",
  "segments": [{"name", "video", "thumbnail"}]
}]
STATS = {"total", "completed", "generating", "failed", "templates", "assets"}
```

## 6. 구간(segment) 로직

광고 길이에 따라 구간 수 결정 (PRD 규칙):
- 15초 → 1~2구간, 30초 → 3~5구간, 60초 → 5~8구간

구간 시나리오(순서 고정): `후킹 → 문제상황 → 제품소개 → 사용장면 → 혜택강조 → CTA`.
길이에 해당하는 구간 수만큼 앞에서부터 슬라이스한다. 생성 화면의 진행
애니메이션은 이 구간 배열을 순차적으로 상태 전환한다.

## 7. 에러 처리

- **API fetch 실패**: 각 화면에 "데이터를 불러오지 못했습니다" 안내 + 재시도 버튼
- **폼 검증**: 필수 필드 미입력 시 인라인 에러, 제출 차단
- **404**: 없는 경로 접근 시 전용 404 페이지

## 8. 반응형

CSS Grid/Flex 기반. 사이드바는 데스크톱 고정, 좁은 화면(<= 768px)에서 상단
햄버거 토글로 접힘. 카드 그리드는 화면 폭에 따라 열 수 자동 조정.

## 9. 테스트 & 검증

더미 UI 데모이므로 무거운 테스트 프레임워크는 도입하지 않는다(YAGNI). 대신:
- Flask 앱 기동 + 7개 페이지 라우트가 200 반환하는지 스모크 체크
- Playwright로 각 페이지 로드 및 핵심 상호작용(모달 열기, 생성 진행바 동작)
  육안/스크린샷 검증

정식 unit test는 실제 API 연동 단계에서 추가한다.

## 10. 배포 (Vercel)

- `vercel.json`: Flask를 `@vercel/python` serverless로 라우팅, static 서빙
- `requirements.txt`: Flask
- serverless 특성상 in-memory 상태는 요청 간 유지되지 않음 → 데모 상태는 프론트
  세션(JS 로컬 배열)이 담당

## 11. 추후 확장 (참고, 이번 범위 아님)

실제 AI 영상 생성 API 연동(Veo/Flow/Seedance/Grok/Higgsfield/Figma Weave),
광고 매체 자동 등록(Meta/Google/TikTok/YouTube Ads), 성과 데이터 수집, 성과
기반 자동 제작.
