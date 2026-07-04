# AI 광고영상 관리자 대시보드 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 더미데이터 기반 AI 광고영상 제작 관리자 대시보드(7화면)를 Flask + Vanilla JS로 구현하고 Vercel 배포 가능한 상태로 만든다.

**Architecture:** Flask가 `/`(페이지) 라우트로 Jinja2 뼈대 HTML을 렌더하고, `/api/*` 라우트로 더미 JSON을 반환한다. Vanilla JS가 페이지 로드 시 fetch로 데이터를 받아 카드/테이블/배지를 렌더하고, 모달·진행바 애니메이션 등 상호작용을 담당한다. 실 연동 시 `data/dummy.py`와 API 핸들러만 교체한다.

**Tech Stack:** Python Flask, Jinja2, Vanilla HTML/CSS/JS, Vercel(`@vercel/python`)

## Global Constraints

- 프론트: Vanilla HTML/CSS/JS만 사용 (프레임워크·빌드툴 없음)
- 백엔드: Python Flask, 외부 의존성은 Flask만 (`requirements.txt`)
- 디자인: 모던 다크 테마 — 진한 배경, 퍼플/블루 액센트, 카드 그림자
- 더미데이터 단일 소스: `data/dummy.py`
- 상태: in-memory. 신규 등록/생성 항목은 프론트 세션(JS 로컬 배열)에서만 유지, 새로고침 시 초기화
- 구간 시나리오 순서 고정: 후킹 → 문제상황 → 제품소개 → 사용장면 → 혜택강조 → CTA
- 페이지 라우트: `/dashboard /generate /templates /assets /jobs /results /settings`, `/` → `/dashboard` 리다이렉트
- 검증: pytest 스위트 없음. 각 태스크는 스모크 스크립트(라우트 200) + 육안/Playwright 확인으로 검증

---

### Task 1: Flask 앱 뼈대 + 더미데이터 + 라우트

**Files:**
- Create: `app.py`
- Create: `data/__init__.py` (빈 파일)
- Create: `data/dummy.py`
- Create: `requirements.txt`
- Create: `templates/base.html` (최소 뼈대 — Task 2에서 확장)
- Create: `templates/dashboard.html` (플레이스홀더 — "대시보드")
- Create: `scripts/smoke.py`

**Interfaces:**
- Produces:
  - `data.dummy` 모듈: `TEMPLATES: list[dict]`, `ASSETS: list[dict]`, `JOBS: list[dict]`, `RESULTS: list[dict]`, `get_stats() -> dict`, `SETTINGS: dict`
  - Flask app `app` in `app.py`
  - 페이지 라우트 7개 + `/`, API 라우트: `GET /api/dashboard/stats`, `GET/POST /api/templates`, `GET/POST /api/assets`, `GET/POST /api/jobs`, `GET /api/results`, `GET /api/settings`
  - `PAGES: list[dict]` (사이드바 메뉴 정의: `{"slug","label","icon"}`) — base.html에 주입

- [ ] **Step 1: requirements.txt 작성**

```
Flask==3.0.3
```

- [ ] **Step 2: data/dummy.py 작성 (더미데이터 단일 소스)**

각 리스트에 3~7개 항목을 채운다. 아래는 구조와 최소 샘플.

```python
SEGMENT_SCENARIO = ["후킹", "문제상황", "제품소개", "사용장면", "혜택강조", "CTA"]

TEMPLATES = [
    {"id": 1, "name": "뼈순이 D-30일 스타일", "style": "캐릭터 챌린지",
     "base_prompt": "귀여운 캐릭터가 30일 변화를 기록하는 톤",
     "subtitle_prompt": "굵은 노란 자막, 카운트다운 강조",
     "scene_prompt": "일자별 비포/애프터 컷 전환",
     "narration_tone": "발랄하고 친근한", "rec_length": 30,
     "rec_model": "Veo", "active": True},
    {"id": 2, "name": "실사 인터뷰 스타일", "style": "다큐/인터뷰",
     "base_prompt": "실제 사용자 인터뷰 형식의 신뢰감 있는 톤",
     "subtitle_prompt": "하단 자막바, 이름/직함 표기",
     "scene_prompt": "정면 인터뷰 + 제품 클로즈업 인서트",
     "narration_tone": "차분하고 진솔한", "rec_length": 30,
     "rec_model": "Google Flow", "active": True},
    {"id": 3, "name": "숏폼 바이럴 스타일", "style": "숏폼",
     "base_prompt": "3초 안에 시선을 잡는 빠른 컷 편집",
     "subtitle_prompt": "화면 중앙 큰 텍스트, 임팩트 효과",
     "scene_prompt": "빠른 장면 전환, 트렌디 BGM 싱크",
     "narration_tone": "에너지 넘치는", "rec_length": 15,
     "rec_model": "Seedance", "active": True},
    {"id": 4, "name": "후기형 광고 스타일", "style": "리뷰",
     "base_prompt": "구매 후기를 읽어주는 형식",
     "subtitle_prompt": "별점/후기 인용 자막",
     "scene_prompt": "제품 언박싱 + 사용 장면",
     "narration_tone": "친근한 수다체", "rec_length": 30,
     "rec_model": "Veo", "active": True},
    {"id": 5, "name": "Before & After 스타일", "style": "비교",
     "base_prompt": "사용 전후를 극적으로 대비",
     "subtitle_prompt": "'BEFORE'/'AFTER' 대비 자막",
     "scene_prompt": "분할 화면 비교 연출",
     "narration_tone": "설득력 있는", "rec_length": 15,
     "rec_model": "Higgsfield", "active": True},
    {"id": 6, "name": "프리미엄 브랜드 스타일", "style": "브랜딩",
     "base_prompt": "고급스럽고 미니멀한 브랜드 무드",
     "subtitle_prompt": "얇은 세리프 자막, 절제된 사용",
     "scene_prompt": "슬로우 모션, 제품 디테일 강조",
     "narration_tone": "고급스럽고 절제된", "rec_length": 60,
     "rec_model": "Google Flow", "active": False},
    {"id": 7, "name": "애니메이션 광고 스타일", "style": "애니메이션",
     "base_prompt": "일러스트/모션그래픽 기반 설명형",
     "subtitle_prompt": "말풍선/키네틱 타이포",
     "scene_prompt": "캐릭터 애니메이션 + 아이콘 모션",
     "narration_tone": "경쾌하고 명료한", "rec_length": 30,
     "rec_model": "Figma Weave", "active": True},
]

ASSETS = [
    {"id": 1, "name": "뼈순이 캐릭터", "type": "캐릭터", "image_url": "",
     "description": "다이어트 챌린지 마스코트, 흰색 캐릭터",
     "ref_prompt": "cute white bone character, energetic pose", "active": True},
    {"id": 2, "name": "메인 제품컷", "type": "제품 이미지", "image_url": "",
     "description": "제품 정면 누끼 이미지",
     "ref_prompt": "product front shot, clean background", "active": True},
    {"id": 3, "name": "브랜드 로고", "type": "브랜드 로고", "image_url": "",
     "description": "1:1 정사각 로고",
     "ref_prompt": "brand logo, transparent bg", "active": True},
    {"id": 4, "name": "스튜디오 배경", "type": "배경 이미지", "image_url": "",
     "description": "밝은 스튜디오 배경",
     "ref_prompt": "bright studio backdrop", "active": True},
    {"id": 5, "name": "경쟁사 참고영상", "type": "참고 영상", "image_url": "",
     "description": "톤 참고용 레퍼런스",
     "ref_prompt": "reference footage", "active": False},
]

# 상태값: 대기 중 / 생성 중 / 구간 생성 완료 / 합본 생성 중 / 완료 / 실패
JOBS = [
    {"id": 101, "name": "여름 다이어트 챌린지", "template": "뼈순이 D-30일 스타일",
     "model": "Veo", "length": 30, "status": "완료",
     "requested_at": "2026-07-01 10:12", "completed_at": "2026-07-01 10:41",
     "segments": [{"name": n, "status": "완료"} for n in SEGMENT_SCENARIO[:4]]},
    {"id": 102, "name": "신제품 런칭 티저", "template": "숏폼 바이럴 스타일",
     "model": "Seedance", "length": 15, "status": "생성 중",
     "requested_at": "2026-07-04 09:30", "completed_at": "",
     "segments": [{"name": "후킹", "status": "완료"}, {"name": "문제상황", "status": "생성 중"}]},
    {"id": 103, "name": "브랜드 무드 필름", "template": "프리미엄 브랜드 스타일",
     "model": "Google Flow", "length": 60, "status": "실패",
     "requested_at": "2026-07-03 15:00", "completed_at": "2026-07-03 15:22",
     "segments": [{"name": n, "status": "실패" if i == 2 else "완료"}
                  for i, n in enumerate(SEGMENT_SCENARIO[:5])]},
    {"id": 104, "name": "고객 후기 모음", "template": "후기형 광고 스타일",
     "model": "Veo", "length": 30, "status": "대기 중",
     "requested_at": "2026-07-04 11:00", "completed_at": "",
     "segments": [{"name": n, "status": "대기 중"} for n in SEGMENT_SCENARIO[:4]]},
]

RESULTS = [
    {"id": 201, "name": "여름 다이어트 챌린지", "final_video": "",
     "template": "뼈순이 D-30일 스타일", "assets": ["뼈순이 캐릭터", "메인 제품컷"],
     "model": "Veo", "created_at": "2026-07-01 10:41",
     "segments": [{"name": n, "video": "", "thumbnail": ""} for n in SEGMENT_SCENARIO[:4]]},
    {"id": 202, "name": "가을 시즌 프로모션", "final_video": "",
     "template": "Before & After 스타일", "assets": ["메인 제품컷", "브랜드 로고"],
     "model": "Higgsfield", "created_at": "2026-06-28 14:05",
     "segments": [{"name": n, "video": "", "thumbnail": ""} for n in SEGMENT_SCENARIO[:6]]},
]

SETTINGS = {
    "ip_restrict_enabled": True,
    "allowed_ips": ["203.0.113.10", "203.0.113.11"],
    "last_access_ip": "203.0.113.10",
    "access_logs": [
        {"ip": "203.0.113.10", "time": "2026-07-04 11:02", "result": "허용"},
        {"ip": "198.51.100.7", "time": "2026-07-04 08:41", "result": "차단"},
    ],
    "admin_account": "admin@company.com",
    "default_ratio": "9:16",
    "default_model": "Veo",
    "save_path": "/videos/output",
}

MODELS = ["Veo", "Google Flow", "Seedance", "Grok", "Higgsfield", "Figma Weave"]
RATIOS = ["16:9", "9:16", "1:1", "4:5"]

def get_stats():
    return {
        "total": len(JOBS),
        "completed": sum(1 for j in JOBS if j["status"] == "완료"),
        "generating": sum(1 for j in JOBS if j["status"] in ("생성 중", "합본 생성 중", "구간 생성 완료")),
        "failed": sum(1 for j in JOBS if j["status"] == "실패"),
        "templates": len(TEMPLATES),
        "assets": len(ASSETS),
        "recent_jobs": JOBS[:5],
    }
```

- [ ] **Step 3: app.py 작성 (라우트 전체)**

```python
from flask import Flask, render_template, redirect, jsonify, request
from data import dummy

app = Flask(__name__)

PAGES = [
    {"slug": "dashboard", "label": "대시보드", "icon": "📊"},
    {"slug": "generate", "label": "광고 생성", "icon": "🎬"},
    {"slug": "templates", "label": "템플릿 관리", "icon": "🧩"},
    {"slug": "assets", "label": "에셋 관리", "icon": "🖼️"},
    {"slug": "jobs", "label": "생성 작업 목록", "icon": "⏳"},
    {"slug": "results", "label": "생성 결과 관리", "icon": "✅"},
    {"slug": "settings", "label": "설정", "icon": "⚙️"},
]
_LABELS = {p["slug"]: p["label"] for p in PAGES}


def render_page(slug):
    return render_template(f"{slug}.html", pages=PAGES,
                           active=slug, title=_LABELS[slug])


@app.route("/")
def index():
    return redirect("/dashboard")


@app.route("/<slug>")
def page(slug):
    if slug not in _LABELS:
        return render_template("404.html", pages=PAGES, active="", title="404"), 404
    return render_page(slug)


@app.route("/api/dashboard/stats")
def api_stats():
    return jsonify(dummy.get_stats())


@app.route("/api/templates", methods=["GET", "POST"])
def api_templates():
    if request.method == "POST":
        return jsonify({"ok": True, "item": request.get_json()}), 201
    return jsonify(dummy.TEMPLATES)


@app.route("/api/assets", methods=["GET", "POST"])
def api_assets():
    if request.method == "POST":
        return jsonify({"ok": True, "item": request.get_json()}), 201
    return jsonify(dummy.ASSETS)


@app.route("/api/jobs", methods=["GET", "POST"])
def api_jobs():
    if request.method == "POST":
        return jsonify({"ok": True, "item": request.get_json()}), 201
    return jsonify(dummy.JOBS)


@app.route("/api/results")
def api_results():
    return jsonify(dummy.RESULTS)


@app.route("/api/settings")
def api_settings():
    return jsonify(dummy.SETTINGS)


@app.route("/api/meta")
def api_meta():
    return jsonify({"models": dummy.MODELS, "ratios": dummy.RATIOS,
                    "scenario": dummy.SEGMENT_SCENARIO})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

- [ ] **Step 4: templates/base.html 최소 뼈대 작성**

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title }} | AI 광고 대시보드</title>
</head>
<body>
  <main>{% block content %}{% endblock %}</main>
</body>
</html>
```

- [ ] **Step 5: templates/dashboard.html 플레이스홀더**

```html
{% extends "base.html" %}
{% block content %}<h1>대시보드</h1>{% endblock %}
```

나머지 6개 페이지(`generate/templates/assets/jobs/results/settings`)도 동일 패턴으로
`<h1>{{ title }}</h1>` 플레이스홀더 생성. `404.html`도 `<h1>404</h1>`로 생성.

- [ ] **Step 6: scripts/smoke.py 작성 (라우트 200 스모크 체크)**

```python
import sys
sys.path.insert(0, ".")
from app import app, PAGES

FAIL = []
with app.test_client() as c:
    for p in PAGES:
        r = c.get(f"/{p['slug']}")
        if r.status_code != 200:
            FAIL.append(f"/{p['slug']} -> {r.status_code}")
    if c.get("/").status_code not in (301, 302):
        FAIL.append("/ redirect missing")
    for path in ["/api/dashboard/stats", "/api/templates", "/api/assets",
                 "/api/jobs", "/api/results", "/api/settings", "/api/meta"]:
        r = c.get(path)
        if r.status_code != 200:
            FAIL.append(f"{path} -> {r.status_code}")
    if c.get("/nonexistent").status_code != 404:
        FAIL.append("404 handler missing")

if FAIL:
    print("SMOKE FAIL:", *FAIL, sep="\n  ")
    sys.exit(1)
print("SMOKE OK: all routes green")
```

- [ ] **Step 7: 스모크 실행 (검증)**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && python scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 8: Commit**

```bash
git add app.py data/ requirements.txt templates/ scripts/smoke.py
git commit -m "feat: Flask 앱 뼈대 + 더미데이터 + 라우트/API"
```

---

### Task 2: 공통 레이아웃 & 다크 테마 CSS

**Files:**
- Modify: `templates/base.html` (사이드바 + 헤더 완성)
- Create: `static/css/main.css`
- Create: `static/css/components.css`
- Create: `static/js/components.js`
- Create: `static/js/api.js`

**Interfaces:**
- Consumes: `PAGES`, `active`, `title` (Task 1의 render_page가 주입)
- Produces:
  - `static/js/api.js`: `window.API = { get(path), post(path, body) }` — fetch 래퍼, 실패 시 throw
  - `static/js/components.js`: `window.UI = { openModal(id), closeModal(id), toast(msg), badge(status), showError(container, retryFn), skeleton(container) }`
  - CSS 변수: `--bg`, `--surface`, `--surface-2`, `--accent`, `--accent-2`, `--text`, `--muted`, `--border`, `--radius`, 상태색(`--ok --warn --err --info`)
  - `.sidebar .header .content .card .table .badge .modal .btn .form-field .progress` 클래스

- [ ] **Step 1: static/css/main.css — 다크 테마 변수 + 레이아웃**

```css
:root{
  --bg:#0f1117; --surface:#171a21; --surface-2:#1e222c;
  --accent:#7c5cff; --accent-2:#4c7dff;
  --text:#e6e8ee; --muted:#8b90a0; --border:#262b36;
  --ok:#3ecf8e; --warn:#f5a524; --err:#f26d6d; --info:#4c7dff;
  --radius:14px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);
  font-family:'Pretendard','Segoe UI',system-ui,sans-serif;font-size:14px}
.layout{display:grid;grid-template-columns:240px 1fr;min-height:100vh}
.sidebar{background:var(--surface);border-right:1px solid var(--border);
  padding:20px 12px;position:sticky;top:0;height:100vh}
.sidebar .logo{font-weight:700;font-size:18px;padding:8px 12px 20px;
  background:linear-gradient(90deg,var(--accent),var(--accent-2));
  -webkit-background-clip:text;background-clip:text;color:transparent}
.sidebar nav a{display:flex;gap:10px;align-items:center;padding:11px 12px;
  border-radius:10px;color:var(--muted);text-decoration:none;margin-bottom:4px}
.sidebar nav a:hover{background:var(--surface-2);color:var(--text)}
.sidebar nav a.active{background:linear-gradient(90deg,
  rgba(124,92,255,.18),rgba(76,125,255,.10));color:var(--text)}
.main{display:flex;flex-direction:column;min-width:0}
.header{display:flex;justify-content:space-between;align-items:center;
  padding:18px 28px;border-bottom:1px solid var(--border);
  position:sticky;top:0;background:rgba(15,17,23,.85);backdrop-filter:blur(8px);z-index:5}
.header h1{font-size:20px}
.header .profile{display:flex;gap:10px;align-items:center;color:var(--muted)}
.content{padding:28px;max-width:1200px;width:100%}
.menu-toggle{display:none;background:none;border:none;color:var(--text);
  font-size:22px;cursor:pointer}
@media(max-width:768px){
  .layout{grid-template-columns:1fr}
  .sidebar{position:fixed;left:0;top:0;z-index:20;width:240px;
    transform:translateX(-100%);transition:transform .2s}
  .sidebar.open{transform:translateX(0)}
  .menu-toggle{display:block}
}
```

- [ ] **Step 2: static/css/components.css — 카드/테이블/배지/모달/폼/버튼/진행바**

```css
.grid{display:grid;gap:16px}
.grid.stats{grid-template-columns:repeat(auto-fill,minmax(180px,1fr))}
.grid.cards{grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}
.card{background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:18px;box-shadow:0 4px 18px rgba(0,0,0,.25)}
.card h3{font-size:13px;color:var(--muted);font-weight:500;margin-bottom:8px}
.card .stat-num{font-size:30px;font-weight:700}
.section-head{display:flex;justify-content:space-between;align-items:center;margin:26px 0 14px}
.section-head h2{font-size:16px}
.table{width:100%;border-collapse:collapse;background:var(--surface);
  border:1px solid var(--border);border-radius:var(--radius);overflow:hidden}
.table th,.table td{text-align:left;padding:12px 14px;border-bottom:1px solid var(--border)}
.table th{color:var(--muted);font-weight:500;background:var(--surface-2)}
.table tr:last-child td{border-bottom:none}
.badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:12px;font-weight:500}
.badge.ok{background:rgba(62,207,142,.15);color:var(--ok)}
.badge.warn{background:rgba(245,165,36,.15);color:var(--warn)}
.badge.err{background:rgba(242,109,109,.15);color:var(--err)}
.badge.info{background:rgba(76,125,255,.15);color:var(--info)}
.badge.muted{background:var(--surface-2);color:var(--muted)}
.btn{background:linear-gradient(90deg,var(--accent),var(--accent-2));
  color:#fff;border:none;padding:10px 16px;border-radius:10px;cursor:pointer;font-size:13px}
.btn.ghost{background:var(--surface-2);color:var(--text);border:1px solid var(--border)}
.btn.sm{padding:6px 12px;font-size:12px}
.form-field{margin-bottom:14px;display:flex;flex-direction:column;gap:6px}
.form-field label{color:var(--muted);font-size:12px}
.form-field input,.form-field select,.form-field textarea{
  background:var(--surface-2);border:1px solid var(--border);color:var(--text);
  padding:10px 12px;border-radius:8px;font-size:13px;font-family:inherit}
.form-field.error input,.form-field.error select{border-color:var(--err)}
.form-field .err-msg{color:var(--err);font-size:11px;display:none}
.form-field.error .err-msg{display:block}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 16px}
.modal-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.6);
  display:none;align-items:center;justify-content:center;z-index:50}
.modal-backdrop.open{display:flex}
.modal{background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:24px;width:560px;max-width:92vw;
  max-height:88vh;overflow:auto}
.modal .modal-head{display:flex;justify-content:space-between;margin-bottom:18px}
.progress-row{display:flex;align-items:center;gap:12px;padding:10px 0}
.progress-row .bar{flex:1;height:8px;background:var(--surface-2);border-radius:999px;overflow:hidden}
.progress-row .bar > i{display:block;height:100%;width:0;
  background:linear-gradient(90deg,var(--accent),var(--accent-2));transition:width .4s}
.toast{position:fixed;bottom:24px;right:24px;background:var(--surface-2);
  border:1px solid var(--border);padding:14px 18px;border-radius:10px;
  box-shadow:0 6px 24px rgba(0,0,0,.4);opacity:0;transform:translateY(10px);
  transition:.25s;z-index:60}
.toast.show{opacity:1;transform:translateY(0)}
.empty,.error-box{text-align:center;color:var(--muted);padding:40px}
.filter-bar{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap}
.chip{padding:7px 14px;border-radius:999px;background:var(--surface-2);
  border:1px solid var(--border);color:var(--muted);cursor:pointer;font-size:12px}
.chip.active{background:rgba(124,92,255,.18);color:var(--text);border-color:var(--accent)}
.thumb{aspect-ratio:16/9;background:var(--surface-2);border:1px dashed var(--border);
  border-radius:8px;display:flex;align-items:center;justify-content:center;color:var(--muted)}
```

- [ ] **Step 3: templates/base.html 완성 (사이드바 + 헤더 + CSS/JS 링크)**

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title }} | AI 광고 대시보드</title>
  <link rel="stylesheet" href="/static/css/main.css">
  <link rel="stylesheet" href="/static/css/components.css">
</head>
<body>
  <div class="layout">
    <aside class="sidebar" id="sidebar">
      <div class="logo">AI AD STUDIO</div>
      <nav>
        {% for p in pages %}
        <a href="/{{ p.slug }}" class="{{ 'active' if p.slug == active else '' }}">
          <span>{{ p.icon }}</span><span>{{ p.label }}</span>
        </a>
        {% endfor %}
      </nav>
    </aside>
    <div class="main">
      <header class="header">
        <div style="display:flex;gap:12px;align-items:center">
          <button class="menu-toggle" onclick="document.getElementById('sidebar').classList.toggle('open')">☰</button>
          <h1>{{ title }}</h1>
        </div>
        <div class="profile"><span>👤</span><span>관리자</span></div>
      </header>
      <div class="content">{% block content %}{% endblock %}</div>
    </div>
  </div>
  <div class="toast" id="toast"></div>
  <script src="/static/js/api.js"></script>
  <script src="/static/js/components.js"></script>
  {% block scripts %}{% endblock %}
</body>
</html>
```

- [ ] **Step 4: static/js/api.js**

```javascript
window.API = {
  async get(path) {
    const r = await fetch(path);
    if (!r.ok) throw new Error(`GET ${path} -> ${r.status}`);
    return r.json();
  },
  async post(path, body) {
    const r = await fetch(path, {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify(body)
    });
    if (!r.ok) throw new Error(`POST ${path} -> ${r.status}`);
    return r.json();
  }
};
```

- [ ] **Step 5: static/js/components.js**

```javascript
const STATUS_CLASS = {
  "완료": "ok", "생성 중": "info", "합본 생성 중": "info",
  "구간 생성 완료": "info", "대기 중": "muted", "실패": "err",
  "사용": "ok", "미사용": "muted"
};
window.UI = {
  openModal(id){ document.getElementById(id).classList.add("open"); },
  closeModal(id){ document.getElementById(id).classList.remove("open"); },
  badge(status){
    const cls = STATUS_CLASS[status] || "muted";
    return `<span class="badge ${cls}">${status}</span>`;
  },
  toast(msg){
    const t = document.getElementById("toast");
    t.textContent = msg; t.classList.add("show");
    clearTimeout(this._tt);
    this._tt = setTimeout(() => t.classList.remove("show"), 2500);
  },
  showError(container, retryFn){
    container.innerHTML = `<div class="error-box">데이터를 불러오지 못했습니다.
      <br><button class="btn sm ghost" style="margin-top:12px">재시도</button></div>`;
    container.querySelector("button").onclick = retryFn;
  },
  skeleton(container){ container.innerHTML = `<div class="empty">불러오는 중…</div>`; }
};
```

- [ ] **Step 6: 스모크 재실행 + 육안 확인**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && python scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

수동: `python app.py` 후 브라우저에서 `http://localhost:5000/dashboard` 열어 사이드바/헤더/다크테마가 보이는지 확인.

- [ ] **Step 7: Commit**

```bash
git add templates/base.html static/css static/js/api.js static/js/components.js
git commit -m "feat: 공통 레이아웃 + 다크 테마 + 공통 JS 유틸"
```

---

### Task 3: 대시보드 화면

**Files:**
- Modify: `templates/dashboard.html`
- Create: `static/js/dashboard.js`

**Interfaces:**
- Consumes: `GET /api/dashboard/stats` → `{total, completed, generating, failed, templates, assets, recent_jobs}`, `window.API`, `window.UI`

- [ ] **Step 1: templates/dashboard.html**

```html
{% extends "base.html" %}
{% block content %}
<div class="grid stats" id="stats"></div>
<div class="section-head"><h2>최근 생성 광고</h2></div>
<div id="recent"></div>
{% endblock %}
{% block scripts %}<script src="/static/js/dashboard.js"></script>{% endblock %}
```

- [ ] **Step 2: static/js/dashboard.js**

```javascript
const STAT_DEFS = [
  ["total", "전체 생성 광고"], ["completed", "생성 완료"],
  ["generating", "생성 중"], ["failed", "실패"],
  ["templates", "등록 템플릿"], ["assets", "등록 에셋"]
];
async function load(){
  const statsEl = document.getElementById("stats");
  const recentEl = document.getElementById("recent");
  UI.skeleton(statsEl);
  try {
    const d = await API.get("/api/dashboard/stats");
    statsEl.innerHTML = STAT_DEFS.map(([k, label]) =>
      `<div class="card"><h3>${label}</h3><div class="stat-num">${d[k]}</div></div>`
    ).join("");
    recentEl.innerHTML = `<table class="table"><thead><tr>
      <th>광고명</th><th>템플릿</th><th>모델</th><th>상태</th><th>요청일</th>
      </tr></thead><tbody>${
        d.recent_jobs.map(j => `<tr><td>${j.name}</td><td>${j.template}</td>
        <td>${j.model}</td><td>${UI.badge(j.status)}</td><td>${j.requested_at}</td></tr>`).join("")
      }</tbody></table>`;
  } catch(e){ UI.showError(statsEl, load); recentEl.innerHTML = ""; }
}
load();
```

- [ ] **Step 3: 검증**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && python scripts/smoke.py`
Expected: `SMOKE OK`

수동: `/dashboard`에서 통계 카드 6개 + 최근 광고 테이블(상태 배지 색상 포함)이 렌더되는지 확인.

- [ ] **Step 4: Commit**

```bash
git add templates/dashboard.html static/js/dashboard.js
git commit -m "feat: 대시보드 화면 (통계 카드 + 최근 광고)"
```

---

### Task 4: 템플릿 관리 화면 (모달 등록 포함)

**Files:**
- Modify: `templates/templates.html`
- Create: `static/js/templates.js`

**Interfaces:**
- Consumes: `GET /api/templates`, `POST /api/templates`, `GET /api/meta` → `{models, ratios, scenario}`, `window.UI`
- 신규 등록 항목은 JS 로컬 배열(`items`)에 push 후 재렌더 (세션 유지)

- [ ] **Step 1: templates/templates.html**

```html
{% extends "base.html" %}
{% block content %}
<div class="section-head"><h2>광고 스타일 템플릿</h2>
  <button class="btn" onclick="UI.openModal('tpl-modal')">+ 신규 등록</button></div>
<div class="grid cards" id="tpl-list"></div>

<div class="modal-backdrop" id="tpl-modal">
  <div class="modal">
    <div class="modal-head"><h2>템플릿 등록</h2>
      <button class="btn ghost sm" onclick="UI.closeModal('tpl-modal')">✕</button></div>
    <form id="tpl-form">
      <div class="form-field" id="f-name"><label>템플릿명 *</label>
        <input name="name"><span class="err-msg">필수 항목입니다</span></div>
      <div class="form-field"><label>광고 스타일</label><input name="style"></div>
      <div class="form-field"><label>기본 프롬프트</label><textarea name="base_prompt" rows="2"></textarea></div>
      <div class="form-field"><label>자막 효과 프롬프트</label><textarea name="subtitle_prompt" rows="2"></textarea></div>
      <div class="form-field"><label>장면 구성 프롬프트</label><textarea name="scene_prompt" rows="2"></textarea></div>
      <div class="form-field"><label>나레이션 톤</label><input name="narration_tone"></div>
      <div class="form-grid">
        <div class="form-field"><label>추천 영상 길이(초)</label>
          <select name="rec_length"><option>15</option><option>30</option><option>60</option></select></div>
        <div class="form-field"><label>추천 AI 모델</label><select name="rec_model" id="tpl-model"></select></div>
      </div>
      <div class="form-field"><label>사용 여부</label>
        <select name="active"><option value="true">사용</option><option value="false">미사용</option></select></div>
      <button class="btn" type="submit">저장</button>
    </form>
  </div>
</div>
{% endblock %}
{% block scripts %}<script src="/static/js/templates.js"></script>{% endblock %}
```

- [ ] **Step 2: static/js/templates.js**

```javascript
let items = [];
function render(){
  document.getElementById("tpl-list").innerHTML = items.map(t => `
    <div class="card">
      <div style="display:flex;justify-content:space-between">
        <h3 style="color:var(--text);font-size:15px">${t.name}</h3>
        ${UI.badge(t.active ? "사용" : "미사용")}</div>
      <p style="color:var(--muted);margin:8px 0">${t.style}</p>
      <div style="display:flex;gap:8px;color:var(--muted);font-size:12px">
        <span>⏱ ${t.rec_length}초</span><span>🤖 ${t.rec_model}</span></div>
    </div>`).join("");
}
async function load(){
  const el = document.getElementById("tpl-list"); UI.skeleton(el);
  try {
    items = await API.get("/api/templates");
    const meta = await API.get("/api/meta");
    document.getElementById("tpl-model").innerHTML =
      meta.models.map(m => `<option>${m}</option>`).join("");
    render();
  } catch(e){ UI.showError(el, load); }
}
document.getElementById("tpl-form").addEventListener("submit", async e => {
  e.preventDefault();
  const f = e.target, name = f.name.value.trim();
  const nf = document.getElementById("f-name");
  if(!name){ nf.classList.add("error"); return; }
  nf.classList.remove("error");
  const item = Object.fromEntries(new FormData(f).entries());
  item.active = item.active === "true";
  item.rec_length = Number(item.rec_length);
  try { await API.post("/api/templates", item); } catch(_){}
  items.push({id: Date.now(), ...item}); render();
  f.reset(); UI.closeModal("tpl-modal"); UI.toast("템플릿이 등록되었습니다");
});
load();
```

- [ ] **Step 3: 검증**

Run: `python scripts/smoke.py` → `SMOKE OK`
수동: `/templates`에서 카드 7개 표시 → "신규 등록" 모달 열기 → 템플릿명 비우고 저장 시 에러 표시 → 채우고 저장 시 카드 추가 + 토스트 확인.

- [ ] **Step 4: Commit**

```bash
git add templates/templates.html static/js/templates.js
git commit -m "feat: 템플릿 관리 화면 (카드 목록 + 모달 등록 + 검증)"
```

---

### Task 5: 에셋 관리 화면 (유형 필터 + 모달)

**Files:**
- Modify: `templates/assets.html`
- Create: `static/js/assets.js`

**Interfaces:**
- Consumes: `GET /api/assets`, `POST /api/assets`, `window.UI`
- 에셋 유형: 캐릭터 / 제품 이미지 / 브랜드 로고 / 배경 이미지 / 참고 이미지 / 참고 영상

- [ ] **Step 1: templates/assets.html**

```html
{% extends "base.html" %}
{% block content %}
<div class="section-head"><h2>에셋 관리</h2>
  <button class="btn" onclick="UI.openModal('asset-modal')">+ 등록</button></div>
<div class="filter-bar" id="asset-filter"></div>
<div class="grid cards" id="asset-list"></div>

<div class="modal-backdrop" id="asset-modal">
  <div class="modal">
    <div class="modal-head"><h2>에셋 등록</h2>
      <button class="btn ghost sm" onclick="UI.closeModal('asset-modal')">✕</button></div>
    <form id="asset-form">
      <div class="form-field" id="af-name"><label>에셋명 *</label>
        <input name="name"><span class="err-msg">필수 항목입니다</span></div>
      <div class="form-field"><label>에셋 유형</label>
        <select name="type"><option>캐릭터</option><option>제품 이미지</option>
        <option>브랜드 로고</option><option>배경 이미지</option>
        <option>참고 이미지</option><option>참고 영상</option></select></div>
      <div class="form-field"><label>설명</label><textarea name="description" rows="2"></textarea></div>
      <div class="form-field"><label>참조용 프롬프트</label><textarea name="ref_prompt" rows="2"></textarea></div>
      <div class="form-field"><label>사용 여부</label>
        <select name="active"><option value="true">사용</option><option value="false">미사용</option></select></div>
      <button class="btn" type="submit">저장</button>
    </form>
  </div>
</div>
{% endblock %}
{% block scripts %}<script src="/static/js/assets.js"></script>{% endblock %}
```

- [ ] **Step 2: static/js/assets.js**

```javascript
let items = [], filter = "전체";
const TYPES = ["전체","캐릭터","제품 이미지","브랜드 로고","배경 이미지","참고 이미지","참고 영상"];
function renderFilter(){
  document.getElementById("asset-filter").innerHTML = TYPES.map(t =>
    `<span class="chip ${t===filter?'active':''}" data-t="${t}">${t}</span>`).join("");
  document.querySelectorAll("#asset-filter .chip").forEach(c =>
    c.onclick = () => { filter = c.dataset.t; renderFilter(); render(); });
}
function render(){
  const list = filter==="전체" ? items : items.filter(a => a.type===filter);
  document.getElementById("asset-list").innerHTML = list.length ? list.map(a => `
    <div class="card"><div class="thumb">🖼 미리보기</div>
      <div style="display:flex;justify-content:space-between;margin-top:10px">
        <h3 style="color:var(--text);font-size:14px">${a.name}</h3>
        ${UI.badge(a.active ? "사용":"미사용")}</div>
      <p style="color:var(--muted);font-size:12px;margin-top:6px">${UI.badge(a.type)}</p>
      <p style="color:var(--muted);font-size:12px;margin-top:8px">${a.description||""}</p>
    </div>`).join("") : `<div class="empty">해당 유형의 에셋이 없습니다</div>`;
}
async function load(){
  const el = document.getElementById("asset-list"); UI.skeleton(el);
  try { items = await API.get("/api/assets"); renderFilter(); render(); }
  catch(e){ UI.showError(el, load); }
}
document.getElementById("asset-form").addEventListener("submit", async e => {
  e.preventDefault();
  const f = e.target, name = f.name.value.trim();
  const nf = document.getElementById("af-name");
  if(!name){ nf.classList.add("error"); return; }
  nf.classList.remove("error");
  const item = Object.fromEntries(new FormData(f).entries());
  item.active = item.active === "true";
  try { await API.post("/api/assets", item); } catch(_){}
  items.push({id: Date.now(), image_url:"", ...item}); render();
  f.reset(); UI.closeModal("asset-modal"); UI.toast("에셋이 등록되었습니다");
});
load();
```

- [ ] **Step 3: 검증**

Run: `python scripts/smoke.py` → `SMOKE OK`
수동: `/assets`에서 카드 5개 + 유형 칩 필터 동작 확인, 모달 등록 + 검증 확인.

- [ ] **Step 4: Commit**

```bash
git add templates/assets.html static/js/assets.js
git commit -m "feat: 에셋 관리 화면 (유형 필터 + 모달 등록)"
```

---

### Task 6: 광고 생성 화면 (폼 + 구간별 진행 애니메이션)

**Files:**
- Modify: `templates/generate.html`
- Create: `static/js/generate.js`

**Interfaces:**
- Consumes: `GET /api/templates`, `GET /api/assets`, `GET /api/meta` → `{models, ratios, scenario}`, `POST /api/jobs`, `window.UI`
- 구간 수 규칙: 15초→2, 30초→4, 60초→6 (scenario 앞에서부터 슬라이스)
- 진행 애니메이션: 각 구간 `대기 중 → 생성 중 → 완료` 순차 전환 → 전체 완료 시 `합본 생성 중 → 완료`

- [ ] **Step 1: templates/generate.html**

```html
{% extends "base.html" %}
{% block content %}
<div class="grid" style="grid-template-columns:1fr 1fr;gap:24px">
  <form id="gen-form" class="card">
    <h2 style="margin-bottom:16px">광고 정보 입력</h2>
    <div class="form-field" id="g-name"><label>광고명 *</label>
      <input name="name"><span class="err-msg">필수</span></div>
    <div class="form-grid">
      <div class="form-field" id="g-product"><label>제품명 *</label>
        <input name="product"><span class="err-msg">필수</span></div>
      <div class="form-field"><label>브랜드명</label><input name="brand"></div>
    </div>
    <div class="form-field"><label>광고 목적</label><input name="purpose"></div>
    <div class="form-grid">
      <div class="form-field"><label>광고 길이</label>
        <select name="length"><option value="15">15초</option>
        <option value="30" selected>30초</option><option value="60">60초</option></select></div>
      <div class="form-field"><label>영상 비율</label><select name="ratio" id="g-ratio"></select></div>
    </div>
    <div class="form-grid">
      <div class="form-field"><label>AI 모델</label><select name="model" id="g-model"></select></div>
      <div class="form-field" id="g-tpl"><label>스타일 템플릿 *</label>
        <select name="template" id="g-template"></select><span class="err-msg">필수</span></div>
    </div>
    <div class="form-field"><label>캐릭터/제품 에셋</label><select name="asset" id="g-asset"></select></div>
    <div class="form-field"><label>추가 요청사항</label><textarea name="note" rows="2"></textarea></div>
    <button class="btn" type="submit">🎬 생성 요청</button>
  </form>
  <div class="card">
    <h2 style="margin-bottom:16px">생성 진행 상태</h2>
    <div id="gen-progress"><div class="empty">생성 요청 시 구간별 진행 상태가 표시됩니다</div></div>
  </div>
</div>
{% endblock %}
{% block scripts %}<script src="/static/js/generate.js"></script>{% endblock %}
```

- [ ] **Step 2: static/js/generate.js**

```javascript
let scenario = [];
const SEG_COUNT = {15: 2, 30: 4, 60: 6};

async function init(){
  const [tpls, assets, meta] = await Promise.all([
    API.get("/api/templates"), API.get("/api/assets"), API.get("/api/meta")]);
  scenario = meta.scenario;
  document.getElementById("g-model").innerHTML = meta.models.map(m=>`<option>${m}</option>`).join("");
  document.getElementById("g-ratio").innerHTML = meta.ratios.map(r=>`<option>${r}</option>`).join("");
  document.getElementById("g-template").innerHTML =
    `<option value="">선택</option>` + tpls.map(t=>`<option>${t.name}</option>`).join("");
  document.getElementById("g-asset").innerHTML =
    `<option value="">선택 안 함</option>` + assets.map(a=>`<option>${a.name}</option>`).join("");
}

function segmentsFor(length){
  return scenario.slice(0, SEG_COUNT[length] || 4);
}

function runAnimation(container, segs){
  container.innerHTML = segs.map((s,i) =>
    `<div class="progress-row"><span style="width:74px">${i+1}. ${s}</span>
     <span class="bar"><i></i></span>
     <span id="st-${i}" style="width:60px;text-align:right">${UI.badge("대기 중")}</span></div>`).join("")
    + `<div class="progress-row" style="margin-top:8px;border-top:1px solid var(--border);padding-top:14px">
       <span style="width:74px">최종 합본</span><span class="bar"><i id="final-bar"></i></span>
       <span id="final-st" style="width:60px;text-align:right">${UI.badge("대기 중")}</span></div>`;
  let i = 0;
  const tick = () => {
    if(i >= segs.length){
      document.getElementById("final-st").innerHTML = UI.badge("합본 생성 중");
      document.getElementById("final-bar").style.width = "60%";
      setTimeout(() => {
        document.getElementById("final-bar").style.width = "100%";
        document.getElementById("final-st").innerHTML = UI.badge("완료");
        UI.toast("광고 생성이 완료되었습니다");
      }, 900);
      return;
    }
    const bar = container.querySelectorAll(".progress-row .bar > i")[i];
    document.getElementById(`st-${i}`).innerHTML = UI.badge("생성 중");
    bar.style.width = "100%";
    setTimeout(() => {
      document.getElementById(`st-${i}`).innerHTML = UI.badge("완료");
      i++; tick();
    }, 800);
  };
  tick();
}

document.getElementById("gen-form").addEventListener("submit", async e => {
  e.preventDefault();
  const f = e.target;
  let ok = true;
  [["g-name", f.name.value], ["g-product", f.product.value], ["g-tpl", f.template.value]]
    .forEach(([id, v]) => {
      const el = document.getElementById(id);
      if(!v.trim()){ el.classList.add("error"); ok = false; }
      else el.classList.remove("error");
    });
  if(!ok) return;
  const length = Number(f.length.value);
  const segs = segmentsFor(length);
  try {
    await API.post("/api/jobs", {name: f.name.value, template: f.template.value,
      model: f.model.value, length, status: "생성 중"});
  } catch(_){}
  runAnimation(document.getElementById("gen-progress"), segs);
});
init();
```

- [ ] **Step 3: 검증**

Run: `python scripts/smoke.py` → `SMOKE OK`
수동: `/generate`에서 셀렉트들이 채워지는지 확인 → 필수 필드 비우고 제출 시 에러 → 채우고 제출 시 구간이 순차적으로 완료→최종 합본→완료 애니메이션 + 토스트 확인. 길이 15/30/60초 변경 시 구간 수(2/4/6) 반영 확인.

- [ ] **Step 4: Commit**

```bash
git add templates/generate.html static/js/generate.js
git commit -m "feat: 광고 생성 화면 (폼 검증 + 구간별 진행 애니메이션)"
```

---

### Task 7: 생성 작업 목록 화면

**Files:**
- Modify: `templates/jobs.html`
- Create: `static/js/jobs.js`

**Interfaces:**
- Consumes: `GET /api/jobs`, `window.UI`

- [ ] **Step 1: templates/jobs.html**

```html
{% extends "base.html" %}
{% block content %}
<div class="section-head"><h2>생성 작업 목록</h2></div>
<div id="jobs-list"></div>
{% endblock %}
{% block scripts %}<script src="/static/js/jobs.js"></script>{% endblock %}
```

- [ ] **Step 2: static/js/jobs.js**

```javascript
async function load(){
  const el = document.getElementById("jobs-list"); UI.skeleton(el);
  try {
    const jobs = await API.get("/api/jobs");
    el.innerHTML = `<table class="table"><thead><tr>
      <th>작업명</th><th>템플릿</th><th>모델</th><th>길이</th><th>상태</th>
      <th>요청일</th><th>완료일</th><th></th></tr></thead><tbody>${
      jobs.map(j => `<tr><td>${j.name}</td><td>${j.template}</td><td>${j.model}</td>
        <td>${j.length}초</td><td>${UI.badge(j.status)}</td>
        <td>${j.requested_at}</td><td>${j.completed_at || "-"}</td>
        <td><button class="btn sm ghost" data-name="${j.name}">재생성</button></td></tr>`).join("")
    }</tbody></table>`;
    el.querySelectorAll("button[data-name]").forEach(b =>
      b.onclick = () => UI.toast(`'${b.dataset.name}' 재생성 요청됨`));
  } catch(e){ UI.showError(el, load); }
}
load();
```

- [ ] **Step 3: 검증**

Run: `python scripts/smoke.py` → `SMOKE OK`
수동: `/jobs`에서 작업 4건 테이블 + 상태 배지(완료/생성중/실패/대기) 색상 + 재생성 버튼 클릭 시 토스트 확인.

- [ ] **Step 4: Commit**

```bash
git add templates/jobs.html static/js/jobs.js
git commit -m "feat: 생성 작업 목록 화면"
```

---

### Task 8: 생성 결과 관리 화면 (목록 + 상세)

**Files:**
- Modify: `templates/results.html`
- Create: `static/js/results.js`

**Interfaces:**
- Consumes: `GET /api/results`, `window.UI`
- 카드 클릭 → 상세 모달에 최종 영상 플레이어(플레이스홀더) + 구간 썸네일 표시

- [ ] **Step 1: templates/results.html**

```html
{% extends "base.html" %}
{% block content %}
<div class="section-head"><h2>생성 결과 관리</h2></div>
<div class="grid cards" id="results-list"></div>

<div class="modal-backdrop" id="result-modal">
  <div class="modal" style="width:720px">
    <div class="modal-head"><h2 id="rm-title"></h2>
      <button class="btn ghost sm" onclick="UI.closeModal('result-modal')">✕</button></div>
    <div id="rm-body"></div>
  </div>
</div>
{% endblock %}
{% block scripts %}<script src="/static/js/results.js"></script>{% endblock %}
```

- [ ] **Step 2: static/js/results.js**

```javascript
let items = [];
function openDetail(r){
  document.getElementById("rm-title").textContent = r.name;
  document.getElementById("rm-body").innerHTML = `
    <div class="thumb" style="aspect-ratio:16/9;margin-bottom:16px">▶ 최종 영상 미리보기</div>
    <div style="display:flex;gap:8px;color:var(--muted);font-size:12px;margin-bottom:16px;flex-wrap:wrap">
      <span>🧩 ${r.template}</span><span>🤖 ${r.model}</span>
      <span>🖼 ${r.assets.join(", ")}</span><span>📅 ${r.created_at}</span></div>
    <h3 style="color:var(--muted);font-size:13px;margin-bottom:10px">구간별 영상</h3>
    <div class="grid" style="grid-template-columns:repeat(3,1fr)">${
      r.segments.map((s,i) => `<div><div class="thumb">${i+1}. ${s.name}</div></div>`).join("")}</div>
    <div style="display:flex;gap:8px;margin-top:20px">
      <button class="btn" onclick="UI.toast('다운로드를 시작합니다')">⬇ 다운로드</button>
      <button class="btn ghost" onclick="UI.toast('재생성 요청됨')">🔄 재생성</button></div>`;
  UI.openModal("result-modal");
}
async function load(){
  const el = document.getElementById("results-list"); UI.skeleton(el);
  try {
    items = await API.get("/api/results");
    el.innerHTML = items.map((r,i) => `
      <div class="card" data-i="${i}" style="cursor:pointer">
        <div class="thumb">▶ 미리보기</div>
        <h3 style="color:var(--text);font-size:15px;margin-top:10px">${r.name}</h3>
        <p style="color:var(--muted);font-size:12px;margin-top:6px">
          ${r.template} · ${r.segments.length}구간 · ${r.created_at}</p></div>`).join("");
    el.querySelectorAll(".card").forEach(c =>
      c.onclick = () => openDetail(items[c.dataset.i]));
  } catch(e){ UI.showError(el, load); }
}
load();
```

- [ ] **Step 3: 검증**

Run: `python scripts/smoke.py` → `SMOKE OK`
수동: `/results`에서 결과 카드 2개 → 카드 클릭 시 상세 모달(최종 영상 플레이스홀더 + 구간 썸네일 + 다운로드/재생성) 확인.

- [ ] **Step 4: Commit**

```bash
git add templates/results.html static/js/results.js
git commit -m "feat: 생성 결과 관리 화면 (목록 + 상세 모달)"
```

---

### Task 9: 설정 화면

**Files:**
- Modify: `templates/settings.html`
- Create: `static/js/settings.js`

**Interfaces:**
- Consumes: `GET /api/settings`, `window.UI` — UI만, 저장 시 토스트만

- [ ] **Step 1: templates/settings.html**

```html
{% extends "base.html" %}
{% block content %}
<div id="settings-body"></div>
{% endblock %}
{% block scripts %}<script src="/static/js/settings.js"></script>{% endblock %}
```

- [ ] **Step 2: static/js/settings.js**

```javascript
async function load(){
  const el = document.getElementById("settings-body"); UI.skeleton(el);
  try {
    const s = await API.get("/api/settings");
    el.innerHTML = `
      <div class="card" style="margin-bottom:20px">
        <h2 style="margin-bottom:16px">회사 IP 제한</h2>
        <div class="form-field"><label>IP 제한 사용</label>
          <select><option ${s.ip_restrict_enabled?'selected':''}>사용</option>
          <option ${!s.ip_restrict_enabled?'selected':''}>미사용</option></select></div>
        <div class="form-field"><label>허용 IP 목록</label>
          <textarea rows="2">${s.allowed_ips.join("\\n")}</textarea></div>
        <p style="color:var(--muted);font-size:12px">마지막 접속 IP: ${s.last_access_ip}</p>
        <h3 style="color:var(--muted);font-size:13px;margin:16px 0 8px">접속 로그</h3>
        <table class="table"><thead><tr><th>IP</th><th>시간</th><th>결과</th></tr></thead>
          <tbody>${s.access_logs.map(l=>`<tr><td>${l.ip}</td><td>${l.time}</td>
          <td>${UI.badge(l.result==="허용"?"사용":"실패")}</td></tr>`).join("")}</tbody></table>
      </div>
      <div class="card">
        <h2 style="margin-bottom:16px">기본 설정</h2>
        <div class="form-grid">
          <div class="form-field"><label>관리자 계정</label><input value="${s.admin_account}"></div>
          <div class="form-field"><label>기본 영상 비율</label><input value="${s.default_ratio}"></div>
          <div class="form-field"><label>기본 생성 모델</label><input value="${s.default_model}"></div>
          <div class="form-field"><label>기본 저장 경로</label><input value="${s.save_path}"></div>
        </div>
        <div class="form-field"><label>API 연동 설정</label><input placeholder="API Key (미설정)"></div>
        <div class="form-field"><label>광고 매체 연동</label><input placeholder="Meta / Google Ads (미설정)"></div>
        <button class="btn" onclick="UI.toast('설정이 저장되었습니다')">저장</button>
      </div>`;
  } catch(e){ UI.showError(el, load); }
}
load();
```

- [ ] **Step 3: 검증**

Run: `python scripts/smoke.py` → `SMOKE OK`
수동: `/settings`에서 IP 제한 섹션(허용 IP/접속 로그 배지) + 기본 설정 폼 + 저장 토스트 확인.

- [ ] **Step 4: Commit**

```bash
git add templates/settings.html static/js/settings.js
git commit -m "feat: 설정 화면 (IP 제한 + 기본 설정 UI)"
```

---

### Task 10: Vercel 배포 설정 + README

**Files:**
- Create: `vercel.json`
- Create: `README.md`

**Interfaces:**
- Consumes: `app.py`의 `app` 객체 (WSGI)

- [ ] **Step 1: vercel.json**

```json
{
  "version": 2,
  "builds": [
    { "src": "app.py", "use": "@vercel/python" },
    { "src": "static/**", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/static/(.*)", "dest": "/static/$1" },
    { "src": "/(.*)", "dest": "/app.py" }
  ]
}
```

- [ ] **Step 2: README.md**

```markdown
# AI 광고영상 제작 관리자 대시보드

Flask + Vanilla JS 기반 더미데이터 관리자 대시보드 (데모).

## 로컬 실행
```
pip install -r requirements.txt
python app.py
# http://localhost:5000
```

## 화면
대시보드 · 광고 생성 · 템플릿 관리 · 에셋 관리 · 생성 작업 목록 · 생성 결과 관리 · 설정

## 배포
Vercel 연동 후 자동 배포 (`vercel.json`).

## 구조
- `app.py` — 라우트 + `/api/*` 더미 JSON
- `data/dummy.py` — 더미데이터 단일 소스 (실 연동 시 이 파일 + API 핸들러만 교체)
- `templates/` — Jinja2 화면, `static/` — CSS/JS

> 상태(신규 등록/생성)는 프론트 세션에서만 유지되며 새로고침 시 초기화됩니다.
```

- [ ] **Step 3: 전체 스모크 최종 확인**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && python scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 4: Commit**

```bash
git add vercel.json README.md
git commit -m "chore: Vercel 배포 설정 + README"
```

---

## Self-Review

**1. Spec coverage:**
- 7개 화면 → Task 3~9 ✅
- Flask API + JS fetch → Task 1(API) + Task 2(api.js) ✅
- 멀티페이지 라우팅 → Task 1 ✅
- 다크 테마 → Task 2 ✅
- 모달/토스트/배지 공통 → Task 2 (`UI`) ✅
- 구간별 진행 애니메이션 + 구간 수 규칙(15→2/30→4/60→6) → Task 6 ✅
- 폼 검증(필수 필드) → Task 4/5/6 ✅
- 에셋 유형 필터 → Task 5 ✅
- 상태 배지(6종) → Task 2 STATUS_CLASS + 전 화면 ✅
- IP 제한 UI → Task 9 ✅
- 반응형 사이드바 토글 → Task 2 ✅
- 에러 처리(fetch 실패 재시도, 404) → Task 2 `showError` + Task 1 404 ✅
- Vercel 배포 → Task 10 ✅
- 검증(스모크 + 육안) → 각 태스크 ✅

**2. Placeholder scan:** 모든 코드 스텝에 실제 코드 포함, "TODO/TBD" 없음 ✅

**3. Type consistency:**
- `window.API.get/post`, `window.UI.openModal/closeModal/toast/badge/showError/skeleton` — Task 2에서 정의, Task 3~9에서 동일 시그니처 사용 ✅
- `get_stats()` 반환 키(total/completed/generating/failed/templates/assets/recent_jobs) — Task 1 정의, Task 3 소비 일치 ✅
- `/api/meta` → `{models, ratios, scenario}` — Task 1 정의, Task 4/6 소비 일치 ✅
- 구간 수 `SEG_COUNT = {15:2, 30:4, 60:6}` — Task 6 내부 일관 ✅

이슈 없음.
