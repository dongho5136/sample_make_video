# 템플릿 계층화 (카테고리 + 풀) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 템플릿을 최상위 카테고리로 만들고, 그 안에 자유 정의 세부 카테고리(에셋 포함)와 풀 항목을 두어, 광고 생성 시 카테고리별로 수동/랜덤 선택해 조합하는 구조로 전환한다.

**Architecture:** `data/dummy.py`의 TEMPLATES에 `categories[].items[]` 중첩 구조를 추가하고 최상위 ASSETS를 제거한다. app.py에 템플릿 상세/카테고리/항목 API를 추가하고 에셋 API·페이지를 제거한다. 템플릿 관리 화면에 카테고리 아코디언 상세 모달을, 광고 생성 화면에 카테고리별 동적 드롭다운(개별/전체 랜덤)을 구현한다.

**Tech Stack:** Python Flask, Jinja2, Vanilla HTML/CSS/JS, Vercel

## Global Constraints

- 프론트: Vanilla HTML/CSS/JS만 (프레임워크·빌드툴 없음)
- 백엔드: Flask만
- 더미데이터 단일 소스: `data/dummy.py`
- 상태: in-memory. 신규 등록/추가는 프론트 세션(JS 로컬 배열)에서만 유지, 새로고침 시 초기화
- 카테고리 타입: `"asset"`(이미지 첨부 가능) 또는 `"prompt"`(텍스트만)
- 풀 항목 스키마: `{ "id", "name", "prompt", "image_url" }` (image_url은 asset에서만 의미)
- 사이드바 메뉴 6개(에셋 제거): dashboard, generate, templates, jobs, results, settings
- 대시보드 통계 키: `assets` → `pool_items` ("총 풀 항목")
- 검증: `venv/Scripts/python.exe scripts/smoke.py` → `SMOKE OK` + Playwright 육안

---

### Task 1: 데이터 구조 전환 (categories/items, ASSETS 제거, get_stats)

**Files:**
- Modify: `data/dummy.py`

**Interfaces:**
- Produces:
  - `TEMPLATES: list[dict]` — 각 원소에 `categories: list[{id,name,type,items}]`, `items: list[{id,name,prompt,image_url}]`
  - `get_stats() -> dict` — 키: `total, completed, generating, failed, templates, pool_items, recent_jobs`
  - `SEGMENT_SCENARIO, JOBS, RESULTS, SETTINGS, MODELS, RATIOS` 유지
  - 최상위 `ASSETS` 삭제됨

- [ ] **Step 1: TEMPLATES를 categories 구조로 재작성**

`data/dummy.py`의 기존 `TEMPLATES` 리스트 전체를 아래로 교체(앞의 3개는 카테고리 포함, 나머지 4개는 간결하게):

```python
TEMPLATES = [
    {"id": 1, "name": "뼈순이 D-30일 스타일", "style": "캐릭터 챌린지",
     "narration_tone": "발랄하고 친근한", "rec_length": 30, "rec_model": "Veo", "active": True,
     "categories": [
        {"id": 11, "name": "캐릭터", "type": "asset", "items": [
            {"id": 111, "name": "뼈순이", "prompt": "cute white bone character, energetic", "image_url": ""},
            {"id": 112, "name": "근육이", "prompt": "muscular mascot, confident pose", "image_url": ""},
        ]},
        {"id": 12, "name": "후킹 문구", "type": "prompt", "items": [
            {"id": 121, "name": "D-30 시작", "prompt": "오늘부터 D-30, 함께 시작해요", "image_url": ""},
            {"id": 122, "name": "변화 예고", "prompt": "30일 뒤 달라진 나를 만나보세요", "image_url": ""},
        ]},
        {"id": 13, "name": "장면 구성", "type": "prompt", "items": [
            {"id": 131, "name": "비포애프터", "prompt": "일자별 비포/애프터 컷 전환", "image_url": ""},
            {"id": 132, "name": "일기형", "prompt": "매일 기록하는 일기 형식 구성", "image_url": ""},
        ]},
     ]},
    {"id": 2, "name": "실사 인터뷰 스타일", "style": "다큐/인터뷰",
     "narration_tone": "차분하고 진솔한", "rec_length": 30, "rec_model": "Google Flow", "active": True,
     "categories": [
        {"id": 21, "name": "인터뷰이", "type": "asset", "items": [
            {"id": 211, "name": "20대 여성", "prompt": "young woman interview, natural light", "image_url": ""},
            {"id": 212, "name": "30대 남성", "prompt": "man interview, office backdrop", "image_url": ""},
        ]},
        {"id": 22, "name": "질문 스크립트", "type": "prompt", "items": [
            {"id": 221, "name": "첫인상", "prompt": "처음 써봤을 때 느낌은 어땠나요?", "image_url": ""},
            {"id": 222, "name": "재구매", "prompt": "다시 구매할 의향이 있나요? 이유는?", "image_url": ""},
        ]},
     ]},
    {"id": 3, "name": "숏폼 바이럴 스타일", "style": "숏폼",
     "narration_tone": "에너지 넘치는", "rec_length": 15, "rec_model": "Seedance", "active": True,
     "categories": [
        {"id": 31, "name": "훅 문구", "type": "prompt", "items": [
            {"id": 311, "name": "3초 훅", "prompt": "3초 안에 시선을 잡는 강한 첫 문장", "image_url": ""},
            {"id": 312, "name": "궁금증", "prompt": "이거 모르면 손해예요", "image_url": ""},
        ]},
        {"id": 32, "name": "BGM 무드", "type": "prompt", "items": [
            {"id": 321, "name": "트렌디", "prompt": "trendy upbeat short-form bgm", "image_url": ""},
            {"id": 322, "name": "긴장감", "prompt": "tension build-up beat", "image_url": ""},
        ]},
     ]},
    {"id": 4, "name": "후기형 광고 스타일", "style": "리뷰",
     "narration_tone": "친근한 수다체", "rec_length": 30, "rec_model": "Veo", "active": True,
     "categories": [
        {"id": 41, "name": "후기 문구", "type": "prompt", "items": [
            {"id": 411, "name": "별점 5점", "prompt": "★★★★★ 인생템 찾았어요", "image_url": ""},
        ]},
     ]},
    {"id": 5, "name": "Before & After 스타일", "style": "비교",
     "narration_tone": "설득력 있는", "rec_length": 15, "rec_model": "Higgsfield", "active": True,
     "categories": [
        {"id": 51, "name": "비교 대상", "type": "asset", "items": [
            {"id": 511, "name": "제품컷", "prompt": "product front shot, clean bg", "image_url": ""},
        ]},
     ]},
    {"id": 6, "name": "프리미엄 브랜드 스타일", "style": "브랜딩",
     "narration_tone": "고급스럽고 절제된", "rec_length": 60, "rec_model": "Google Flow", "active": False,
     "categories": []},
    {"id": 7, "name": "애니메이션 광고 스타일", "style": "애니메이션",
     "narration_tone": "경쾌하고 명료한", "rec_length": 30, "rec_model": "Figma Weave", "active": True,
     "categories": [
        {"id": 71, "name": "캐릭터", "type": "asset", "items": [
            {"id": 711, "name": "마스코트", "prompt": "brand mascot, flat illustration", "image_url": ""},
        ]},
     ]},
]
```

- [ ] **Step 2: 최상위 ASSETS 리스트 삭제**

`data/dummy.py`에서 `ASSETS = [ ... ]` 블록 전체를 삭제한다. (JOBS/RESULTS/SETTINGS/MODELS/RATIOS/SEGMENT_SCENARIO는 그대로 유지)

- [ ] **Step 3: get_stats() 갱신 (assets → pool_items)**

기존 `get_stats()`를 아래로 교체:

```python
def get_stats():
    total_items = sum(len(c["items"]) for t in TEMPLATES for c in t["categories"])
    return {
        "total": len(JOBS),
        "completed": sum(1 for j in JOBS if j["status"] == "완료"),
        "generating": sum(1 for j in JOBS if j["status"] in ("생성 중", "합본 생성 중", "구간 생성 완료")),
        "failed": sum(1 for j in JOBS if j["status"] == "실패"),
        "templates": len(TEMPLATES),
        "pool_items": total_items,
        "recent_jobs": JOBS[:5],
    }
```

- [ ] **Step 4: import 검증**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe -c "from data import dummy; print('templates', len(dummy.dummy.TEMPLATES) if hasattr(dummy,'dummy') else len(dummy.TEMPLATES)); print('stats', dummy.get_stats()['pool_items']); print('has ASSETS', hasattr(dummy,'ASSETS'))"`
Expected: `templates 7` / `stats <정수>` / `has ASSETS False`

- [ ] **Step 5: Commit**

```bash
git add data/dummy.py
git commit -m "feat: 템플릿 데이터를 카테고리/풀 구조로 전환, ASSETS 제거"
```

---

### Task 2: API 라우트 전환 (템플릿 상세/카테고리/항목 추가, 에셋 API·페이지 제거)

**Files:**
- Modify: `app.py`
- Modify: `scripts/smoke.py`

**Interfaces:**
- Consumes: `data.dummy` (Task 1의 TEMPLATES/get_stats)
- Produces:
  - `PAGES`에서 `assets` 제거 (6개)
  - `GET /api/templates/<int:tid>` → 템플릿 dict 또는 404 JSON
  - `POST /api/templates/<int:tid>/categories` → `{"ok": True, "item": <json>}`, 201
  - `POST /api/templates/<int:tid>/categories/<int:cid>/items` → `{"ok": True, "item": <json>}`, 201
  - `/api/assets` (GET/POST) 및 `/assets` 페이지 제거 → 존재 시 404

- [ ] **Step 1: PAGES에서 assets 항목 제거**

`app.py`의 `PAGES` 리스트에서 아래 한 줄을 삭제:

```python
    {"slug": "assets", "label": "에셋 관리", "icon": "🖼️"},
```

- [ ] **Step 2: api_assets 핸들러 삭제**

`app.py`에서 아래 블록 전체 삭제:

```python
@app.route("/api/assets", methods=["GET", "POST"])
def api_assets():
    if request.method == "POST":
        return jsonify({"ok": True, "item": request.get_json()}), 201
    return jsonify(dummy.ASSETS)
```

- [ ] **Step 3: 템플릿 상세/카테고리/항목 API 추가**

`app.py`의 기존 `api_templates` 함수 바로 아래에 추가:

```python
@app.route("/api/templates/<int:tid>")
def api_template_detail(tid):
    for t in dummy.TEMPLATES:
        if t["id"] == tid:
            return jsonify(t)
    return jsonify({"error": "not found"}), 404


@app.route("/api/templates/<int:tid>/categories", methods=["POST"])
def api_add_category(tid):
    return jsonify({"ok": True, "item": request.get_json()}), 201


@app.route("/api/templates/<int:tid>/categories/<int:cid>/items", methods=["POST"])
def api_add_item(tid, cid):
    return jsonify({"ok": True, "item": request.get_json()}), 201
```

- [ ] **Step 4: smoke.py 갱신**

`scripts/smoke.py`의 API 경로 리스트에서 `/api/assets`를 제거하고, 신규 검증을 추가한다. 파일 전체를 아래로 교체:

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
    for path in ["/api/dashboard/stats", "/api/templates",
                 "/api/jobs", "/api/results", "/api/settings", "/api/meta"]:
        r = c.get(path)
        if r.status_code != 200:
            FAIL.append(f"{path} -> {r.status_code}")
    # 신규: 템플릿 상세
    if c.get("/api/templates/1").status_code != 200:
        FAIL.append("/api/templates/1 -> not 200")
    if c.get("/api/templates/999999").status_code != 404:
        FAIL.append("/api/templates/<bad> not 404")
    # 신규: 카테고리/항목 추가 (더미 201)
    if c.post("/api/templates/1/categories", json={"name": "x", "type": "prompt"}).status_code != 201:
        FAIL.append("POST categories not 201")
    if c.post("/api/templates/1/categories/11/items", json={"name": "x", "prompt": "y"}).status_code != 201:
        FAIL.append("POST items not 201")
    # 제거 확인: 에셋 페이지/API 404
    if c.get("/assets").status_code != 404:
        FAIL.append("/assets page should be 404")
    if c.get("/api/assets").status_code != 404:
        FAIL.append("/api/assets should be 404")
    # 404 핸들러
    if c.get("/nonexistent").status_code != 404:
        FAIL.append("404 handler missing")

if FAIL:
    print("SMOKE FAIL:", *FAIL, sep="\n  ")
    sys.exit(1)
print("SMOKE OK: all routes green")
```

- [ ] **Step 5: 스모크 실행**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 6: Commit**

```bash
git add app.py scripts/smoke.py
git commit -m "feat: 템플릿 상세/카테고리/항목 API 추가, 에셋 API·페이지 제거"
```

---

### Task 3: 에셋 화면 파일 삭제 + 컴포넌트 배지 매핑 추가

**Files:**
- Delete: `templates/assets.html`
- Delete: `static/js/assets.js`
- Modify: `static/js/components.js`

**Interfaces:**
- Consumes: `window.UI` (기존)
- Produces: `STATUS_CLASS`에 `"asset"→"info"`, `"prompt"→"muted"` 매핑 추가 (카테고리 타입 배지용)

- [ ] **Step 1: 에셋 화면 파일 삭제**

```bash
git rm templates/assets.html static/js/assets.js
```

- [ ] **Step 2: components.js STATUS_CLASS에 타입 배지 추가**

`static/js/components.js`의 `STATUS_CLASS` 객체를 아래로 교체:

```javascript
const STATUS_CLASS = {
  "완료": "ok", "생성 중": "info", "합본 생성 중": "info",
  "구간 생성 완료": "info", "대기 중": "muted", "실패": "err",
  "사용": "ok", "미사용": "muted",
  "asset": "info", "prompt": "muted"
};
```

- [ ] **Step 3: 스모크 실행 (에셋 페이지 제거 반영 확인)**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 4: Commit**

```bash
git add static/js/components.js
git commit -m "feat: 에셋 화면 제거 + 카테고리 타입 배지 매핑 추가"
```

---

### Task 4: 템플릿 관리 화면 — 카테고리 아코디언 상세 모달

**Files:**
- Modify: `templates/templates.html`
- Modify: `static/js/templates.js`

**Interfaces:**
- Consumes: `GET /api/templates`, `GET /api/meta`, `window.UI`, `STATUS_CLASS`(asset/prompt)
- 카드에 "카테고리 N · 항목 M" 요약. 카드 클릭 → 상세 모달(아코디언). 카테고리/항목 추가는 JS 로컬 상태 반영.

- [ ] **Step 1: templates.html에 상세 모달 컨테이너 추가**

`templates/templates.html` 전체를 아래로 교체(기존 등록 모달 유지 + 상세 모달 추가):

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

<div class="modal-backdrop" id="detail-modal">
  <div class="modal" style="width:640px">
    <div class="modal-head"><h2 id="dm-title"></h2>
      <button class="btn ghost sm" onclick="UI.closeModal('detail-modal')">✕</button></div>
    <div id="dm-body"></div>
  </div>
</div>
{% endblock %}
{% block scripts %}<script src="/static/js/templates.js"></script>{% endblock %}
```

- [ ] **Step 2: templates.js를 상세 아코디언 지원으로 교체**

`static/js/templates.js` 전체를 아래로 교체:

```javascript
let items = [];        // 템플릿 목록 (categories 포함)
let current = null;    // 상세 모달에 열린 템플릿

function catCount(t){ return (t.categories || []).length; }
function itemCount(t){ return (t.categories || []).reduce((s,c)=>s+c.items.length,0); }

function renderList(){
  document.getElementById("tpl-list").innerHTML = items.map((t,i) => `
    <div class="card" data-i="${i}" style="cursor:pointer">
      <div style="display:flex;justify-content:space-between">
        <h3 style="color:var(--text);font-size:15px">${t.name}</h3>
        ${UI.badge(t.active ? "사용" : "미사용")}</div>
      <p style="color:var(--muted);margin:8px 0">${t.style}</p>
      <div style="display:flex;gap:8px;color:var(--muted);font-size:12px">
        <span>🗂 카테고리 ${catCount(t)}</span><span>📦 항목 ${itemCount(t)}</span></div>
    </div>`).join("");
  document.querySelectorAll("#tpl-list .card").forEach(c =>
    c.onclick = () => openDetail(items[c.dataset.i]));
}

function renderDetail(){
  const t = current;
  document.getElementById("dm-title").textContent = t.name;
  const cats = (t.categories || []).map((c) => `
    <div class="card" style="margin-bottom:12px">
      <div style="display:flex;justify-content:space-between;align-items:center;cursor:pointer"
           data-cid="${c.id}">
        <div><b>${c.name}</b> ${UI.badge(c.type)}
          <span style="color:var(--muted);font-size:12px">· 항목 ${c.items.length}</span></div>
        <span class="chev" style="color:var(--muted)">▾</span></div>
      <div class="cat-body" data-body="${c.id}" style="display:none;margin-top:12px">
        ${c.items.map(it => `<div style="padding:8px 0;border-top:1px solid var(--border)">
          <b style="font-size:13px">${it.name}</b>
          <p style="color:var(--muted);font-size:12px;margin-top:4px">${it.prompt}</p></div>`).join("")
          || `<p style="color:var(--muted);font-size:12px">항목이 없습니다</p>`}
        <form class="add-item-form" data-cid="${c.id}" style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
          <input name="name" placeholder="항목명" style="flex:1;min-width:120px;background:var(--surface-2);
            border:1px solid var(--border);color:var(--text);padding:8px;border-radius:8px;font-size:12px">
          <input name="prompt" placeholder="프롬프트" style="flex:2;min-width:160px;background:var(--surface-2);
            border:1px solid var(--border);color:var(--text);padding:8px;border-radius:8px;font-size:12px">
          <button class="btn sm" type="submit">+ 항목</button>
        </form>
      </div>
    </div>`).join("");
  document.getElementById("dm-body").innerHTML = cats + `
    <form id="add-cat-form" style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">
      <input name="name" placeholder="새 카테고리명" style="flex:1;min-width:120px;background:var(--surface-2);
        border:1px solid var(--border);color:var(--text);padding:8px;border-radius:8px;font-size:12px">
      <select name="type" style="background:var(--surface-2);border:1px solid var(--border);
        color:var(--text);padding:8px;border-radius:8px;font-size:12px">
        <option value="prompt">prompt</option><option value="asset">asset</option></select>
      <button class="btn sm ghost" type="submit">+ 카테고리</button>
    </form>`;

  // 아코디언 토글
  document.querySelectorAll("#dm-body [data-cid]").forEach(h => {
    if(h.tagName === "DIV") h.onclick = () => {
      const body = document.querySelector(`#dm-body [data-body="${h.dataset.cid}"]`);
      body.style.display = body.style.display === "none" ? "block" : "none";
    };
  });
  // 항목 추가
  document.querySelectorAll("#dm-body .add-item-form").forEach(f =>
    f.addEventListener("submit", e => {
      e.preventDefault();
      const name = f.name.value.trim();
      if(!name) return;
      const cat = current.categories.find(c => c.id == f.dataset.cid);
      cat.items.push({id: Date.now(), name, prompt: f.prompt.value, image_url: ""});
      try { API.post(`/api/templates/${current.id}/categories/${cat.id}/items`,
        {name, prompt: f.prompt.value}); } catch(_){}
      renderDetail(); UI.toast("항목이 추가되었습니다");
    }));
  // 카테고리 추가
  document.getElementById("add-cat-form").addEventListener("submit", e => {
    e.preventDefault();
    const f = e.target, name = f.name.value.trim();
    if(!name) return;
    current.categories.push({id: Date.now(), name, type: f.type.value, items: []});
    try { API.post(`/api/templates/${current.id}/categories`, {name, type: f.type.value}); } catch(_){}
    renderDetail(); renderList(); UI.toast("카테고리가 추가되었습니다");
  });
}

function openDetail(t){ current = t; renderDetail(); UI.openModal("detail-modal"); }

async function load(){
  const el = document.getElementById("tpl-list"); UI.skeleton(el);
  try {
    items = await API.get("/api/templates");
    const meta = await API.get("/api/meta");
    document.getElementById("tpl-model").innerHTML =
      meta.models.map(m => `<option>${m}</option>`).join("");
    renderList();
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
  item.categories = [];
  try { await API.post("/api/templates", item); } catch(_){}
  items.push({id: Date.now(), ...item}); renderList();
  f.reset(); UI.closeModal("tpl-modal"); UI.toast("템플릿이 등록되었습니다");
});
load();
```

- [ ] **Step 3: 스모크 실행**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 4: Commit**

```bash
git add templates/templates.html static/js/templates.js
git commit -m "feat: 템플릿 상세 카테고리 아코디언 + 카테고리/항목 추가 UI"
```

---

### Task 5: 광고 생성 화면 — 카테고리별 동적 드롭다운 + 랜덤

**Files:**
- Modify: `templates/generate.html`
- Modify: `static/js/generate.js`

**Interfaces:**
- Consumes: `GET /api/templates`(categories 포함), `GET /api/meta`, `POST /api/jobs`, `window.UI`
- 템플릿 선택 시 그 템플릿의 categories로 드롭다운 동적 렌더. 줄별 🎲 + 상단 "전체 랜덤".

- [ ] **Step 1: generate.html에서 단일 에셋 필드 제거 + 카테고리 컨테이너 추가**

`templates/generate.html` 전체를 아래로 교체(기존 asset 드롭다운 줄 삭제, 카테고리 선택 영역 추가):

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
    <div style="display:flex;justify-content:space-between;align-items:center;margin:6px 0 4px">
      <label style="color:var(--muted);font-size:12px">카테고리 선택</label>
      <button type="button" class="btn sm ghost" id="rand-all">🎲 전체 랜덤</button></div>
    <div id="g-categories"><p class="empty" style="padding:16px">템플릿을 먼저 선택하세요</p></div>
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

- [ ] **Step 2: generate.js에 템플릿 categories 기반 동적 선택 + 랜덤 로직 추가**

`static/js/generate.js` 전체를 아래로 교체:

```javascript
let scenario = [];
let templates = [];
const SEG_COUNT = {15: 2, 30: 4, 60: 6};

async function init(){
  const [tpls, meta] = await Promise.all([
    API.get("/api/templates"), API.get("/api/meta")]);
  templates = tpls;
  scenario = meta.scenario;
  document.getElementById("g-model").innerHTML = meta.models.map(m=>`<option>${m}</option>`).join("");
  document.getElementById("g-ratio").innerHTML = meta.ratios.map(r=>`<option>${r}</option>`).join("");
  document.getElementById("g-template").innerHTML =
    `<option value="">선택</option>` + tpls.map(t=>`<option value="${t.id}">${t.name}</option>`).join("");
}

function currentTemplate(){
  const id = document.getElementById("g-template").value;
  return templates.find(t => String(t.id) === id) || null;
}

function renderCategories(){
  const t = currentTemplate();
  const box = document.getElementById("g-categories");
  if(!t){ box.innerHTML = `<p class="empty" style="padding:16px">템플릿을 먼저 선택하세요</p>`; return; }
  if(!t.categories.length){ box.innerHTML = `<p class="empty" style="padding:16px">이 템플릿에는 카테고리가 없습니다</p>`; return; }
  box.innerHTML = t.categories.map(c => `
    <div class="form-field" style="margin-bottom:10px">
      <label>${c.name} ${UI.badge(c.type)}</label>
      <div style="display:flex;gap:8px">
        <select data-cat="${c.id}" style="flex:1;background:var(--surface-2);border:1px solid var(--border);
          color:var(--text);padding:10px;border-radius:8px;font-size:13px">
          <option value="">선택 안 함</option>
          ${c.items.map(it=>`<option>${it.name}</option>`).join("")}</select>
        <button type="button" class="btn sm ghost" data-rand="${c.id}">🎲</button>
      </div>
    </div>`).join("");
  box.querySelectorAll("button[data-rand]").forEach(b =>
    b.onclick = () => randomizeOne(b.dataset.rand));
}

function randomizeOne(cid){
  const sel = document.querySelector(`#g-categories select[data-cat="${cid}"]`);
  const opts = [...sel.options].filter(o => o.value !== "");
  if(opts.length) sel.value = opts[Math.floor(Math.random()*opts.length)].text;
}
function randomizeAll(){
  document.querySelectorAll("#g-categories select[data-cat]").forEach(sel =>
    randomizeOne(sel.dataset.cat));
}
function collectSelections(){
  const t = currentTemplate();
  const out = {};
  document.querySelectorAll("#g-categories select[data-cat]").forEach(sel => {
    if(sel.value){
      const cat = t.categories.find(c => String(c.id) === sel.dataset.cat);
      out[cat.name] = sel.value;
    }
  });
  return out;
}

function segmentsFor(length){ return scenario.slice(0, SEG_COUNT[length] || 4); }

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

document.getElementById("g-template").addEventListener("change", renderCategories);
document.getElementById("rand-all").addEventListener("click", randomizeAll);

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
  const t = currentTemplate();
  try {
    await API.post("/api/jobs", {name: f.name.value, template: t ? t.name : "",
      model: f.model.value, length, status: "생성 중", selections: collectSelections()});
  } catch(_){}
  runAnimation(document.getElementById("gen-progress"), segs);
});
init();
```

- [ ] **Step 3: 스모크 실행**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 4: Commit**

```bash
git add templates/generate.html static/js/generate.js
git commit -m "feat: 광고 생성 화면 카테고리별 동적 드롭다운 + 개별/전체 랜덤"
```

---

### Task 6: 대시보드 통계 라벨 변경 (등록 에셋 → 총 풀 항목)

**Files:**
- Modify: `static/js/dashboard.js`

**Interfaces:**
- Consumes: `GET /api/dashboard/stats` → 이제 `pool_items` 키 포함(`assets` 없음)

- [ ] **Step 1: STAT_DEFS에서 assets → pool_items 교체**

`static/js/dashboard.js`의 `STAT_DEFS` 배열을 아래로 교체:

```javascript
const STAT_DEFS = [
  ["total", "전체 생성 광고"], ["completed", "생성 완료"],
  ["generating", "생성 중"], ["failed", "실패"],
  ["templates", "등록 템플릿"], ["pool_items", "총 풀 항목"]
];
```

- [ ] **Step 2: 스모크 실행**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 3: Commit**

```bash
git add static/js/dashboard.js
git commit -m "feat: 대시보드 통계 '등록 에셋' → '총 풀 항목'"
```

---

### Task 7: 브라우저 육안 검증 + Vercel 재배포

**Files:** (없음 — 검증/배포 태스크)

**Interfaces:**
- Consumes: 로컬 Flask 서버, Playwright, vercel CLI

- [ ] **Step 1: 로컬 서버 기동**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe app.py` (백그라운드)
확인: `curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/templates` → `200`

- [ ] **Step 2: Playwright 육안 검증**

- `/templates` → 카드에 "카테고리 N · 항목 M" 표시 → 카드 클릭 → 상세 모달 아코디언 펼침 → 항목/카테고리 추가 폼 확인, 스크린샷
- `/generate` → 템플릿 선택 시 카테고리 드롭다운 동적 생성 → "전체 랜덤" 클릭 시 값 채워짐 → 제출 시 진행 애니메이션, 스크린샷
- `/dashboard` → 통계 카드 "총 풀 항목" 표시 확인
- 사이드바에 "에셋 관리" 없음 확인

- [ ] **Step 3: 서버 종료 + 스크린샷/임시파일 정리**

Run: `pkill -f app.py; rm -rf .playwright-mcp *.png`

- [ ] **Step 4: master 병합 + push**

```bash
git checkout master
git merge --no-ff feature/template-hierarchy -m "Merge: 템플릿 계층화(카테고리+풀) 구현"
venv/Scripts/python.exe scripts/smoke.py   # SMOKE OK 확인
git push origin master
```

- [ ] **Step 5: Vercel 프로덕션 재배포**

```bash
vercel deploy --prod --yes
```

- [ ] **Step 6: 프로덕션 스모크 (curl)**

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://samplemakevideo.vercel.app/templates      # 200
curl -s -o /dev/null -w "%{http_code}\n" https://samplemakevideo.vercel.app/api/templates/1 # 200
curl -s -o /dev/null -w "%{http_code}\n" https://samplemakevideo.vercel.app/assets          # 404
```
Expected: 200 / 200 / 404

- [ ] **Step 7: 문서 커밋 (플랜 반영)**

```bash
git add docs/superpowers/plans/2026-07-05-template-hierarchy.md
git commit -m "docs: 템플릿 계층화 구현 플랜"
git push origin master
```

---

## Self-Review

**1. Spec coverage:**
- 개념 모델(템플릿>카테고리>풀항목) → Task 1 데이터 구조 ✅
- 자유 정의 카테고리 + 타입(asset/prompt) → Task 1, Task 4 카테고리 추가 UI ✅
- 풀 항목 스키마 {name,prompt,image_url} → Task 1 ✅
- ASSETS 제거 + 에셋 API/페이지 제거 → Task 1(데이터), Task 2(API/페이지), Task 3(파일) ✅
- 템플릿 상세/카테고리/항목 API → Task 2 ✅
- 에셋 메뉴 제거(사이드바) → Task 2 PAGES ✅
- 템플릿 관리 아코디언 상세 + 추가 → Task 4 ✅
- 생성 화면 동적 드롭다운 + 수동/개별랜덤/전체랜덤 → Task 5 ✅
- 대시보드 pool_items → Task 1(stats) + Task 6(라벨) ✅
- 컴포넌트 배지(asset/prompt) → Task 3 ✅
- 검증(스모크 갱신 + Playwright) → Task 2(스모크), Task 7(육안) ✅
- Vercel 재배포 → Task 7 ✅

**2. Placeholder scan:** 모든 코드 스텝에 실제 코드, TODO/TBD 없음 ✅

**3. Type consistency:**
- `pool_items` — Task 1 get_stats 정의, Task 6 소비 일치 ✅
- 카테고리 스키마 `{id,name,type,items}` / 항목 `{id,name,prompt,image_url}` — Task 1 정의, Task 4/5 소비 일치 ✅
- `GET /api/templates/<int:tid>` — Task 2 정의, Task 7 검증 일치 ✅
- `collectSelections/currentTemplate/renderCategories` — Task 5 내부 일관 ✅
- STATUS_CLASS의 `asset/prompt` — Task 3 정의, Task 4/5의 `UI.badge(c.type)` 소비 일치 ✅

이슈 없음.
