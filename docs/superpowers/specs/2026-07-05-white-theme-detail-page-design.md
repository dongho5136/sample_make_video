# 화이트 톤 + 템플릿 상세 페이지 + 테이블 UI — 설계 문서

작성일: 2026-07-05

## 1. 목적

기존 다크 대시보드를 **화이트(라이트) 톤**으로 바꾸고, 템플릿 상세를 모달이
아닌 **별도 페이지**로 분리해 거기서 하위 값(카테고리/풀 항목)을 등록하며,
목록과 상세를 **테이블**로 깔끔하게 표시한다.

## 2. 결정 사항 (브레인스토밍 확정)

- 테이블 적용 범위: **템플릿 목록 + 상세 모두**
- 광고 생성 화면: 기능(카테고리 동적 드롭다운/랜덤) **유지**, 라이트 테마만 자동 적용
- 상세: 모달 → **별도 페이지 `/templates/<id>`** 로 이동

## 3. 화이트 톤 디자인

`static/css/main.css`의 `:root` CSS 변수만 라이트 팔레트로 교체한다. 클래스
구조는 그대로이므로 전 화면에 자동 적용된다.

```css
:root{
  --bg:#f6f7fb; --surface:#ffffff; --surface-2:#f0f2f7;
  --accent:#6366f1; --accent-2:#3b82f6;
  --text:#1a1d26; --muted:#6b7280; --border:#e5e7eb;
  --ok:#16a34a; --warn:#d97706; --err:#dc2626; --info:#2563eb;
  --radius:14px;
}
```

- 사이드바: 흰 배경 + 옅은 경계선. 로고 그라데이션 유지.
- 헤더 blur 배경: `rgba(246,247,251,.85)` 로 라이트화.
- 카드 그림자: 은은하게 `0 1px 3px rgba(0,0,0,.08)`.
- `components.css`의 배지 배경 투명도는 라이트 배경에서도 가독성 있으므로 유지
  (필요 시 미세 조정). 점선 썸네일/폼 필드는 변수 기반이라 자동 반영.

## 4. 템플릿 상세 페이지

### 라우트
- `GET /templates/<int:tid>` → `template_detail.html` 렌더. 없는 id면
  `404.html`, 404. app.py의 기존 `/<slug>` 라우트보다 **먼저** 등록해 충돌 방지
  (Flask는 정적 규칙을 우선하지만, `<int:tid>` 컨버터가 명확히 구분됨).

### 화면 구성 (template_detail.html)
- 상단: "← 목록으로"(→ `/templates`) + 템플릿명, 메타(스타일/톤/추천 길이·모델/사용 여부 배지)
- **카테고리별 섹션** (JS가 렌더):
  - 섹션 헤더: 카테고리명 + type 배지(asset/prompt) + "항목 N"
  - **풀 항목 테이블**: 컬럼 = 항목명 · 프롬프트 · (asset면) 이미지
  - 하단 인라인 "항목 추가" 폼 (항목명·프롬프트, asset이면 이미지URL)
- 페이지 맨 아래: "카테고리 추가" 폼 (이름 + type 선택)
- 추가는 JS 로컬 상태 + 더미 POST → 재렌더 + 토스트 (기존 패턴 유지)

### 데이터
- `GET /api/templates/<id>` (기존) 로 상세 데이터 로드. 신규 API 불필요.
- 카테고리/항목 추가 API도 기존(`POST /api/templates/<id>/categories`,
  `.../categories/<cid>/items`) 재사용.

## 5. 테이블 UI

### 템플릿 목록 (templates.html)
카드 그리드 → **테이블**:
| 템플릿명 | 스타일 | 카테고리 | 항목 | 추천 모델 | 사용 여부 |

- 행 클릭 → `window.location = "/templates/<id>"` 로 상세 페이지 이동
- "+ 신규 등록" 버튼 + 등록 모달은 유지 (목록에서 새 템플릿 생성)
- 상세 **모달 제거** (detail-modal 및 관련 JS 삭제)

### 상세 페이지 풀 항목
카테고리별 테이블 (아코디언 아님, 펼쳐진 상태):
| 항목명 | 프롬프트 | 이미지(asset만) |

## 6. 영향 범위

- 수정:
  - `static/css/main.css` — 라이트 팔레트 + 사이드바/헤더/카드 조정
  - `app.py` — `/templates/<int:tid>` 라우트 추가
  - `templates/templates.html` — 목록 테이블화, 상세 모달 제거
  - `static/js/templates.js` — 모달 로직 제거, 행 클릭 이동, 테이블 렌더
  - `scripts/smoke.py` — `/templates/1` 200, `/templates/999999` 404 확인
- 신규:
  - `templates/template_detail.html`
  - `static/js/template_detail.js`
- 광고 생성/대시보드/작업목록/결과/설정 화면: 코드 변경 없음, 라이트 테마 자동 적용

## 7. 에러 처리

- `/templates/<잘못된 id>` → 404 페이지
- 목록/상세 fetch 실패 → 기존 `UI.showError` 재시도 패턴
- 카테고리/항목 추가 폼: 이름 미입력 시 무시(제출 차단), 기존과 동일

## 8. 검증

- `scripts/smoke.py`: `/templates/1`(200), `/templates/999999`(404) 추가
- Playwright 육안:
  - 라이트 테마 렌더(대시보드·목록)
  - 템플릿 목록 테이블 → 행 클릭 → `/templates/1` 이동
  - 상세 페이지에서 카테고리 테이블 + 항목 추가 + 카테고리 추가 동작
- 프로덕션 curl 스모크 후 Vercel 재배포

## 9. 배포

구현·검증 완료 후 GitHub push → `vercel deploy --prod`.
