# 템플릿 계층화 (카테고리 + 풀) — 설계 문서

작성일: 2026-07-05

## 1. 목적

기존 대시보드에서 **템플릿**과 **에셋**은 별개의 독립 메뉴였다. 이를 바꿔
**템플릿을 최상위 카테고리**로 두고, 그 안에 **자유 정의 세부 카테고리**를
넣는다. 에셋(캐릭터/제품 등)도 그 카테고리 중 하나다.

각 카테고리는 **풀(pool) 항목**을 가지며, 광고 생성 시 카테고리별로 항목을
하나씩(수동 또는 랜덤) 골라 조합한다. 매 생성마다 다른 조합이 나오는 구조를
데모로 표현한다.

## 2. 개념 모델

```
템플릿 (최상위)
├── 메타: 이름, 스타일, 나레이션 톤, 추천 길이/모델, 사용 여부
└── 카테고리[] (자유 추가/삭제)
    ├── "캐릭터"      type: asset  (이미지 첨부 허용)
    │   └── 풀 항목[]: { 이름, 프롬프트, 이미지(선택) }
    ├── "후킹 문구"   type: prompt (텍스트만)
    │   └── 풀 항목[]: { 이름, 프롬프트 }
    └── "장면 구성"   type: prompt
        └── 풀 항목[]: { 이름, 프롬프트 }
```

**결정 사항 (브레인스토밍 확정):**
- 카테고리 종류: **자유 정의** (템플릿마다 다르게 구성)
- 카테고리 타입: `asset`(이미지 첨부 가능) 또는 `prompt`(텍스트만)
- 풀 항목 스키마: 공통 `{ name, prompt, image_url? }` — image_url은 asset 타입에서만 노출
- 생성 시 선택: **수동 + 랜덤 둘 다** (카테고리별 드롭다운 + 개별/전체 랜덤 버튼)
- 기존 독립 "에셋 관리" 메뉴: **제거**, 에셋은 asset 타입 카테고리로 흡수
- 대시보드 통계: "등록 에셋 수" → **"총 풀 항목 수"**

## 3. 데이터 구조 (data/dummy.py)

```python
TEMPLATES = [{
  "id", "name", "style", "narration_tone", "rec_length", "rec_model", "active",
  "categories": [{
     "id", "name",           # 예: "캐릭터", "후킹 문구"
     "type",                 # "asset" | "prompt"
     "items": [{ "id", "name", "prompt", "image_url" }]  # image_url은 asset일 때만 의미
  }]
}]
```

- 최상위 `ASSETS` 리스트 **제거**. 기존 에셋(캐릭터/제품컷/로고 등)은 관련
  템플릿의 `type:"asset"` 카테고리 items로 이동.
- 기존 템플릿의 낱개 프롬프트 필드(`base_prompt`/`subtitle_prompt`/
  `scene_prompt`)는 각각 카테고리로 재구성한 더미데이터로 대체.
- `SEGMENT_SCENARIO`, `JOBS`, `RESULTS`, `SETTINGS`, `MODELS`, `RATIOS`는 유지.

### get_stats() 변경

```python
def get_stats():
    total_items = sum(len(c["items"]) for t in TEMPLATES for c in t["categories"])
    return {
        "total": ..., "completed": ..., "generating": ..., "failed": ...,
        "templates": len(TEMPLATES),
        "pool_items": total_items,     # 기존 "assets" 대체
        "recent_jobs": JOBS[:5],
    }
```

## 4. API 변경

| 메서드/경로 | 상태 | 내용 |
|-------------|------|------|
| `GET /api/templates` | 변경 | `categories`(및 items)까지 포함해 반환 |
| `GET /api/templates/<id>` | 신규 | 단일 템플릿 상세 (없으면 404) |
| `POST /api/templates/<id>/categories` | 신규 | 카테고리 추가 (더미 성공 응답) |
| `POST /api/templates/<id>/categories/<cid>/items` | 신규 | 풀 항목 추가 (더미 성공 응답) |
| `GET /api/assets`, `POST /api/assets` | 제거 | 에셋 독립 API 삭제 |
| `POST /api/templates` | 유지 | 템플릿 신규 등록 (더미) |
| `GET /api/jobs` `POST /api/jobs` `GET /api/results` `GET /api/settings` `GET /api/meta` | 유지 | 변경 없음 |

- POST 계열은 기존과 동일하게 더미(성공 응답만). 실제 상태 변화는 프론트
  세션(JS 로컬 배열)에서만 유지, 새로고침 시 초기화.

## 5. 화면 변경

### 사이드바 (PAGES)
`assets` 항목 제거 → 6개 메뉴:
대시보드 · 광고 생성 · 템플릿 관리 · 생성 작업 목록 · 생성 결과 관리 · 설정

### 템플릿 관리 화면 (`templates.html` + `templates.js`)
- 템플릿 카드 그리드는 유지. 카드에 "카테고리 N · 항목 M" 요약 추가.
- 카드 클릭 → **상세 모달**:
  - 상단: 템플릿 메타
  - 본문: **카테고리 아코디언**
    - 각 카테고리: 이름 + type 배지(asset/prompt) + "항목 N개", 클릭 시 펼침
    - 펼치면 풀 항목 리스트: 이름 / 프롬프트 미리보기 / (asset면) 썸네일
    - "+ 항목 추가" (카테고리별 인라인 폼: 이름·프롬프트·(asset면)이미지URL)
    - "+ 카테고리 추가" (이름 입력 + type 선택 prompt/asset)
- 신규 등록/추가는 JS 로컬 상태에 반영 후 재렌더 + 토스트.

### 광고 생성 화면 (`generate.html` + `generate.js`)
- 기존 "단일 템플릿 + 단일 에셋 드롭다운" → **동적 카테고리 선택 UI**:
  ```
  [스타일 템플릿 ▾]                🎲 전체 랜덤
  캐릭터     [드롭다운 ▾] 🎲
  후킹 문구  [드롭다운 ▾] 🎲
  장면 구성  [드롭다운 ▾] 🎲
  ```
  - 템플릿 선택 시, 그 템플릿의 `categories`로 드롭다운을 동적 렌더
  - 각 드롭다운 = 해당 카테고리의 items (option value = item.name)
  - 줄별 🎲(개별 랜덤), 상단 "전체 랜덤"(모든 카테고리 무작위 선택)
  - 필수 검증: 광고명·제품명·템플릿 (기존 유지). 카테고리 선택은 선택사항.
  - 생성 요청 시 선택 조합을 payload에 포함 → 구간별 진행 애니메이션(기존 유지)

### 대시보드 (`dashboard.js`)
- 통계 카드 라벨 "등록 에셋" → "총 풀 항목", 키 `assets` → `pool_items`

## 6. 마이그레이션 / 영향 범위

- 삭제: `templates/assets.html`, `static/js/assets.js`
- 수정: `app.py`(라우트), `data/dummy.py`(구조), `templates/templates.html`,
  `static/js/templates.js`, `templates/generate.html`, `static/js/generate.js`,
  `static/js/dashboard.js`, `scripts/smoke.py`
- `static/js/components.js`의 STATUS_CLASS에 `asset`/`prompt` 배지 클래스 매핑 추가

## 7. 에러 처리

- `GET /api/templates/<id>` 없는 id → 404 JSON
- 카테고리/항목 추가 폼: 이름 미입력 시 인라인 에러, 제출 차단
- 생성 화면에서 템플릿 미선택 시 카테고리 영역은 안내 문구 표시

## 8. 검증

- `scripts/smoke.py` 갱신: `/assets` 페이지 라우트 제거 반영(404 확인),
  신규 API(`/api/templates/<id>`, 카테고리/항목 POST) 200/201 확인,
  `/api/assets` 제거 확인(404)
- Playwright 육안: 템플릿 상세 아코디언 펼침 + 카테고리/항목 추가,
  생성 화면 동적 드롭다운 + 개별/전체 랜덤 동작
- 배포 후 프로덕션 URL에서 페이지/신규 API 스모크(curl)

## 9. 배포

구현·검증 완료 후 GitHub push → `vercel deploy --prod`로 재배포.
