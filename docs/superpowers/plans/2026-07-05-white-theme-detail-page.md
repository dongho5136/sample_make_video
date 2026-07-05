# 화이트 톤 + 템플릿 상세 페이지 + 테이블 UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 다크 테마를 화이트 톤으로 바꾸고, 템플릿 상세를 별도 페이지(`/templates/<id>`)로 분리해 하위 값을 등록하며, 목록·상세를 테이블로 표시한다.

**Architecture:** main.css의 CSS 변수만 라이트 팔레트로 교체해 전 화면에 자동 적용한다. app.py에 `/templates/<int:tid>` 라우트를 추가하고, 템플릿 목록을 테이블화하며 기존 상세 모달을 제거한다. 신규 template_detail 페이지가 카테고리별 풀 항목 테이블과 추가 폼을 렌더한다.

**Tech Stack:** Python Flask, Jinja2, Vanilla HTML/CSS/JS, Vercel

## Global Constraints

- 프론트: Vanilla HTML/CSS/JS만 (프레임워크·빌드툴 없음)
- 백엔드: Flask만
- 더미데이터 단일 소스: `data/dummy.py`
- 상태: in-memory. 신규 추가는 프론트 세션(JS 로컬)에서만 유지, 새로고침 초기화
- 라이트 팔레트: `--bg:#f6f7fb --surface:#ffffff --surface-2:#f0f2f7 --text:#1a1d26 --muted:#6b7280 --border:#e5e7eb --accent:#6366f1 --accent-2:#3b82f6`
- 상태색: `--ok:#16a34a --warn:#d97706 --err:#dc2626 --info:#2563eb`
- 상세 라우트: `GET /templates/<int:tid>` (없으면 404)
- 기존 API 재사용: `GET /api/templates/<id>`, `POST /api/templates/<id>/categories`, `POST /api/templates/<id>/categories/<cid>/items`
- 검증: `venv/Scripts/python.exe scripts/smoke.py` → `SMOKE OK` + Playwright 육안

---

### Task 1: 라이트 팔레트 적용 (main.css)

**Files:**
- Modify: `static/css/main.css`

**Interfaces:**
- Produces: `:root` CSS 변수 라이트화, 사이드바/헤더/카드 라이트 대비 조정 (클래스명 불변 → 전 화면 자동 반영)

- [ ] **Step 1: main.css의 :root 변수와 사이드바/헤더 라이트화**

`static/css/main.css`에서 `:root { ... }` 블록과 `.sidebar`, `.header` 규칙을 아래로 교체 (나머지 규칙은 변수 기반이라 유지):

```css
:root{
  --bg:#f6f7fb; --surface:#ffffff; --surface-2:#f0f2f7;
  --accent:#6366f1; --accent-2:#3b82f6;
  --text:#1a1d26; --muted:#6b7280; --border:#e5e7eb;
  --ok:#16a34a; --warn:#d97706; --err:#dc2626; --info:#2563eb;
  --radius:14px;
}
```

그리고 `.header` 규칙의 배경을 라이트로:

```css
.header{display:flex;justify-content:space-between;align-items:center;
  padding:18px 28px;border-bottom:1px solid var(--border);
  position:sticky;top:0;background:rgba(246,247,251,.85);backdrop-filter:blur(8px);z-index:5}
```

- [ ] **Step 2: components.css 카드 그림자 은은하게**

`static/css/components.css`의 `.card` 규칙에서 box-shadow를 교체:

```css
.card{background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:18px;box-shadow:0 1px 3px rgba(0,0,0,.08)}
```

- [ ] **Step 3: 스모크 실행 (회귀 확인)**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 4: Commit**

```bash
git add static/css/main.css static/css/components.css
git commit -m "feat: 화이트 톤 라이트 팔레트 적용"
```

---

### Task 2: 템플릿 상세 페이지 라우트 (app.py)

**Files:**
- Modify: `app.py`
- Modify: `scripts/smoke.py`

**Interfaces:**
- Consumes: `data.dummy.TEMPLATES`, `PAGES`
- Produces: `GET /templates/<int:tid>` → `template_detail.html` 렌더(존재 시) 또는 404. 템플릿 dict를 `template`으로 주입.

- [ ] **Step 1: 상세 라우트 추가**

`app.py`의 `page(slug)` 함수 바로 위(또는 아래)에 추가. `<int:tid>` 컨버터라 `/<slug>`와 충돌하지 않는다:

```python
@app.route("/templates/<int:tid>")
def template_detail_page(tid):
    for t in dummy.TEMPLATES:
        if t["id"] == tid:
            return render_template("template_detail.html", pages=PAGES,
                                   active="templates", title=t["name"], template=t)
    return render_template("404.html", pages=PAGES, active="", title="404"), 404
```

- [ ] **Step 2: smoke.py에 상세 페이지 검증 추가**

`scripts/smoke.py`의 `# 신규: 템플릿 상세` 주석 블록 바로 아래에 추가:

```python
    if c.get("/templates/1").status_code != 200:
        FAIL.append("/templates/1 page -> not 200")
    if c.get("/templates/999999").status_code != 404:
        FAIL.append("/templates/<bad> page not 404")
```

- [ ] **Step 3: template_detail.html 임시 뼈대 생성 (라우트 검증용)**

`templates/template_detail.html` 생성:

```html
{% extends "base.html" %}
{% block content %}<h1>{{ template.name }}</h1>{% endblock %}
```

- [ ] **Step 4: 스모크 실행**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 5: Commit**

```bash
git add app.py scripts/smoke.py templates/template_detail.html
git commit -m "feat: 템플릿 상세 페이지 라우트 추가"
```

---

### Task 3: 템플릿 목록 테이블화 + 모달 제거 (templates)

**Files:**
- Modify: `templates/templates.html`
- Modify: `static/js/templates.js`

**Interfaces:**
- Consumes: `GET /api/templates`, `GET /api/meta`, `window.UI`
- 행 클릭 → `window.location.href = "/templates/<id>"`. 상세 모달 제거. 등록 모달은 유지.

- [ ] **Step 1: templates.html에서 상세 모달 제거 + 테이블 컨테이너**

`templates/templates.html` 전체를 아래로 교체 (등록 모달 유지, detail-modal 삭제, grid → 테이블 컨테이너):

```html
{% extends "base.html" %}
{% block content %}
<div class="section-head"><h2>광고 스타일 템플릿</h2>
  <button class="btn" onclick="UI.openModal('tpl-modal')">+ 신규 등록</button></div>
<div id="tpl-list"></div>

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
{% endblock %}
{% block scripts %}<script src="/static/js/templates.js"></script>{% endblock %}
```

- [ ] **Step 2: templates.js를 테이블 렌더 + 행 이동으로 교체**

`static/js/templates.js` 전체를 아래로 교체 (상세 모달/아코디언 로직 전부 제거):

```javascript
let items = [];

function catCount(t){ return (t.categories || []).length; }
function itemCount(t){ return (t.categories || []).reduce((s,c)=>s+c.items.length,0); }

function renderList(){
  const el = document.getElementById("tpl-list");
  el.innerHTML = `<table class="table"><thead><tr>
    <th>템플릿명</th><th>스타일</th><th>카테고리</th><th>항목</th>
    <th>추천 모델</th><th>사용 여부</th></tr></thead><tbody>${
    items.map(t => `<tr data-id="${t.id}" style="cursor:pointer">
      <td><b>${t.name}</b></td><td>${t.style}</td>
      <td>${catCount(t)}</td><td>${itemCount(t)}</td>
      <td>${t.rec_model}</td><td>${UI.badge(t.active ? "사용" : "미사용")}</td></tr>`).join("")
  }</tbody></table>`;
  el.querySelectorAll("tr[data-id]").forEach(r =>
    r.onclick = () => { window.location.href = `/templates/${r.dataset.id}`; });
}

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
git commit -m "feat: 템플릿 목록 테이블화 + 상세 모달 제거, 행 클릭 페이지 이동"
```

---

### Task 4: 템플릿 상세 페이지 — 카테고리 테이블 + 추가 폼

**Files:**
- Modify: `templates/template_detail.html`
- Create: `static/js/template_detail.js`

**Interfaces:**
- Consumes: `GET /api/templates/<id>`, `POST /api/templates/<id>/categories`, `POST /api/templates/<id>/categories/<cid>/items`, `window.UI`
- 페이지 URL에서 tid 추출: `location.pathname.split("/").pop()`

- [ ] **Step 1: template_detail.html 완성 (헤더 + 컨테이너)**

`templates/template_detail.html` 전체를 아래로 교체:

```html
{% extends "base.html" %}
{% block content %}
<a href="/templates" class="btn ghost sm" style="margin-bottom:16px;display:inline-block">← 목록으로</a>
<div class="card" id="tpl-meta"></div>
<div class="section-head"><h2>카테고리 & 풀 항목</h2></div>
<div id="cat-sections"></div>
<div class="card" style="margin-top:16px">
  <form id="add-cat-form" style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
    <b style="font-size:13px;margin-right:8px">카테고리 추가</b>
    <input name="name" placeholder="새 카테고리명" style="flex:1;min-width:140px;background:var(--surface-2);
      border:1px solid var(--border);color:var(--text);padding:9px;border-radius:8px;font-size:13px">
    <select name="type" style="background:var(--surface-2);border:1px solid var(--border);
      color:var(--text);padding:9px;border-radius:8px;font-size:13px">
      <option value="prompt">prompt</option><option value="asset">asset</option></select>
    <button class="btn sm" type="submit">+ 추가</button>
  </form>
</div>
{% endblock %}
{% block scripts %}<script src="/static/js/template_detail.js"></script>{% endblock %}
```

- [ ] **Step 2: template_detail.js 작성**

`static/js/template_detail.js` 생성:

```javascript
const TID = location.pathname.split("/").pop();
let tpl = null;

function renderMeta(){
  document.getElementById("tpl-meta").innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h2>${tpl.name}</h2>${UI.badge(tpl.active ? "사용" : "미사용")}</div>
    <div style="display:flex;gap:14px;color:var(--muted);font-size:13px;margin-top:10px;flex-wrap:wrap">
      <span>🎨 ${tpl.style}</span><span>🎙 ${tpl.narration_tone}</span>
      <span>⏱ ${tpl.rec_length}초</span><span>🤖 ${tpl.rec_model}</span></div>`;
}

function renderCategories(){
  const box = document.getElementById("cat-sections");
  if(!tpl.categories.length){ box.innerHTML = `<p class="empty">카테고리가 없습니다. 아래에서 추가하세요.</p>`; return; }
  box.innerHTML = tpl.categories.map(c => `
    <div class="card" style="margin-bottom:16px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
        <div><b style="font-size:15px">${c.name}</b> ${UI.badge(c.type)}
          <span style="color:var(--muted);font-size:12px">· 항목 ${c.items.length}</span></div></div>
      <table class="table"><thead><tr><th>항목명</th><th>프롬프트</th>
        ${c.type === "asset" ? "<th>이미지</th>" : ""}</tr></thead><tbody>${
        c.items.map(it => `<tr><td><b>${it.name}</b></td><td>${it.prompt}</td>
          ${c.type === "asset" ? `<td>${it.image_url ? "🖼" : "-"}</td>` : ""}</tr>`).join("")
          || `<tr><td colspan="3" style="color:var(--muted)">항목이 없습니다</td></tr>`
      }</tbody></table>
      <form class="add-item-form" data-cid="${c.id}" data-type="${c.type}"
            style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
        <input name="name" placeholder="항목명" style="flex:1;min-width:120px;background:var(--surface-2);
          border:1px solid var(--border);color:var(--text);padding:8px;border-radius:8px;font-size:12px">
        <input name="prompt" placeholder="프롬프트" style="flex:2;min-width:160px;background:var(--surface-2);
          border:1px solid var(--border);color:var(--text);padding:8px;border-radius:8px;font-size:12px">
        ${c.type === "asset" ? `<input name="image_url" placeholder="이미지 URL" style="flex:1;min-width:120px;
          background:var(--surface-2);border:1px solid var(--border);color:var(--text);padding:8px;
          border-radius:8px;font-size:12px">` : ""}
        <button class="btn sm" type="submit">+ 항목</button>
      </form>
    </div>`).join("");
  box.querySelectorAll(".add-item-form").forEach(f =>
    f.addEventListener("submit", e => {
      e.preventDefault();
      const name = f.name.value.trim();
      if(!name) return;
      const cat = tpl.categories.find(c => String(c.id) === f.dataset.cid);
      const img = f.image_url ? f.image_url.value : "";
      cat.items.push({id: Date.now(), name, prompt: f.prompt.value, image_url: img});
      try { API.post(`/api/templates/${TID}/categories/${cat.id}/items`,
        {name, prompt: f.prompt.value, image_url: img}); } catch(_){}
      renderCategories(); UI.toast("항목이 추가되었습니다");
    }));
}

document.getElementById("add-cat-form").addEventListener("submit", e => {
  e.preventDefault();
  const f = e.target, name = f.name.value.trim();
  if(!name) return;
  tpl.categories.push({id: Date.now(), name, type: f.type.value, items: []});
  try { API.post(`/api/templates/${TID}/categories`, {name, type: f.type.value}); } catch(_){}
  renderCategories(); f.reset(); UI.toast("카테고리가 추가되었습니다");
});

async function load(){
  const box = document.getElementById("cat-sections"); UI.skeleton(box);
  try {
    tpl = await API.get(`/api/templates/${TID}`);
    renderMeta(); renderCategories();
  } catch(e){ UI.showError(box, load); }
}
load();
```

- [ ] **Step 3: 스모크 실행**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 4: Commit**

```bash
git add templates/template_detail.html static/js/template_detail.js
git commit -m "feat: 템플릿 상세 페이지 카테고리 테이블 + 항목/카테고리 추가"
```

---

### Task 5: 육안 검증 + Vercel 재배포

**Files:** (없음 — 검증/배포)

**Interfaces:**
- Consumes: 로컬 Flask, Playwright, vercel CLI

- [ ] **Step 1: 로컬 서버 기동**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe app.py` (백그라운드)
확인: `curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/templates/1` → `200`

- [ ] **Step 2: Playwright 육안 검증**

- `/dashboard` → 라이트 테마(흰 배경/사이드바) 렌더 확인, 스크린샷
- `/templates` → 테이블 렌더 확인 → 첫 행 클릭 → `/templates/1` 이동 확인
- `/templates/1` → 메타 카드 + 카테고리별 테이블 + 항목 추가 폼 → 항목 추가 동작 + 토스트, 스크린샷
- 카테고리 추가 폼 동작 확인

- [ ] **Step 3: 서버 종료 + 임시파일 정리**

Run: `pkill -f app.py; rm -rf .playwright-mcp *.png`

- [ ] **Step 4: master 병합 + push**

```bash
git checkout master
git merge --no-ff feature/white-theme-detail -m "Merge: 화이트 톤 + 템플릿 상세 페이지 + 테이블 UI"
venv/Scripts/python.exe scripts/smoke.py   # SMOKE OK
git push origin master
```

- [ ] **Step 5: Vercel 프로덕션 재배포**

```bash
vercel deploy --prod --yes
```

- [ ] **Step 6: 프로덕션 스모크 (curl)**

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://samplemakevideo.vercel.app/templates       # 200
curl -s -o /dev/null -w "%{http_code}\n" https://samplemakevideo.vercel.app/templates/1     # 200
curl -s -o /dev/null -w "%{http_code}\n" https://samplemakevideo.vercel.app/templates/99999 # 404
```
Expected: 200 / 200 / 404

- [ ] **Step 7: 플랜 문서 커밋**

```bash
git add docs/superpowers/plans/2026-07-05-white-theme-detail-page.md
git commit -m "docs: 화이트 톤 + 상세 페이지 구현 플랜"
git push origin master
```

---

## Self-Review

**1. Spec coverage:**
- 화이트 톤 팔레트 → Task 1 ✅
- 카드 그림자/헤더 라이트 조정 → Task 1 ✅
- 상세 페이지 라우트 `/templates/<int:tid>` (없으면 404) → Task 2 ✅
- 목록 테이블화 + 행 클릭 이동 → Task 3 ✅
- 상세 모달 제거 → Task 3 ✅
- 상세 페이지 카테고리별 풀 항목 테이블 + 추가 폼 → Task 4 ✅
- 카테고리 추가 폼 → Task 4 ✅
- 기존 API 재사용(상세/카테고리/항목) → Task 4 ✅
- 광고 생성/기타 화면 무변경 + 자동 라이트 → Task 1(자동) ✅
- smoke 갱신(/templates/1 200, 999999 404) → Task 2 ✅
- Playwright 육안 + 프로덕션 스모크 + 재배포 → Task 5 ✅

**2. Placeholder scan:** 모든 코드 스텝에 실제 코드, TODO/TBD 없음 ✅

**3. Type consistency:**
- `catCount/itemCount` — Task 3 정의·사용 일관 ✅
- 상세 데이터 `tpl.categories[].{id,name,type,items[].{name,prompt,image_url}}` — 기존 데이터 구조(이전 기능)와 일치, Task 4 소비 일치 ✅
- `TID = location.pathname.split("/").pop()` — Task 4 내부 일관, 라우트 `/templates/<int:tid>`(Task 2)와 정합 ✅
- `UI.badge`(asset/prompt 포함) — 기존 components.js STATUS_CLASS에 이미 매핑됨(이전 기능) ✅

이슈 없음.
