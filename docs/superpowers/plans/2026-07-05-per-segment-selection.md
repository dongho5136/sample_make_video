# 광고 생성: 구간별 카테고리 선택 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 광고 생성 화면에서 템플릿 선택 시 구간(길이 자동) 카드를 생성하고, 각 구간에서 템플릿의 모든 카테고리를 개별 선택(수동/구간랜덤/전체랜덤)해 광고를 구성한다.

**Architecture:** generate.html의 단일 카테고리 영역을 구간 컨테이너로 바꾸고, generate.js가 템플릿의 categories × 구간 수만큼 드롭다운을 렌더한다. 데이터/API는 기존(`/api/templates`, `/api/meta`, `/api/jobs`)을 재사용한다.

**Tech Stack:** Python Flask, Jinja2, Vanilla HTML/CSS/JS, Vercel

## Global Constraints

- 프론트: Vanilla HTML/CSS/JS만 (프레임워크·빌드툴 없음)
- 상태: in-memory, 프론트 세션 유지, 새로고침 초기화
- 구간 수: `SEG_COUNT = {15:2, 30:4, 60:6}`, 기본 4
- 구간 이름: `SEGMENT_SCENARIO` (후킹/문제상황/제품소개/사용장면/혜택강조/CTA)에서 앞에서부터 슬라이스 — `/api/meta`의 `scenario`
- 카테고리 선택: 선택사항(비워도 생성 가능)
- 필수 검증(유지): 광고명·제품명·템플릿
- 데이터/API 변경 없음
- 검증: `venv/Scripts/python.exe scripts/smoke.py` → `SMOKE OK` + Playwright 육안

---

### Task 1: 구간별 카테고리 선택 UI 구현

**Files:**
- Modify: `templates/generate.html`
- Modify: `static/js/generate.js`

**Interfaces:**
- Consumes: `GET /api/templates`(categories 포함), `GET /api/meta`(models/ratios/scenario), `POST /api/jobs`, `window.UI`
- 생성 payload: `{name, template, model, length, status:"생성 중", segments:[{name, selections:{카테고리명:항목명}}]}`

- [ ] **Step 1: generate.html의 카테고리 영역을 구간 컨테이너로 교체**

`templates/generate.html`에서 아래 블록:

```html
    <div style="display:flex;justify-content:space-between;align-items:center;margin:6px 0 4px">
      <label style="color:var(--muted);font-size:12px">카테고리 선택</label>
      <button type="button" class="btn sm ghost" id="rand-all">🎲 전체 랜덤</button></div>
    <div id="g-categories"><p class="empty" style="padding:16px">템플릿을 먼저 선택하세요</p></div>
```

를 아래로 교체:

```html
    <div style="display:flex;justify-content:space-between;align-items:center;margin:6px 0 4px">
      <label style="color:var(--muted);font-size:12px">구간별 요소 선택</label>
      <button type="button" class="btn sm ghost" id="rand-all">🎲 전체 랜덤</button></div>
    <div id="g-segments"><p class="empty" style="padding:16px">템플릿을 먼저 선택하세요</p></div>
```

- [ ] **Step 2: generate.js를 구간별 렌더/랜덤/수집으로 재작성**

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
function currentLength(){ return Number(document.getElementById("gen-form").length.value); }
function segmentNames(length){ return scenario.slice(0, SEG_COUNT[length] || 4); }

function renderSegments(){
  const t = currentTemplate();
  const box = document.getElementById("g-segments");
  if(!t){ box.innerHTML = `<p class="empty" style="padding:16px">템플릿을 먼저 선택하세요</p>`; return; }
  const segs = segmentNames(currentLength());
  box.innerHTML = segs.map((name, si) => {
    const cats = t.categories.length ? t.categories.map(c => `
      <div class="form-field" style="margin-bottom:8px">
        <label>${c.name} ${UI.badge(c.type)}</label>
        <select data-seg="${si}" data-cat="${c.id}" style="width:100%;background:var(--surface-2);
          border:1px solid var(--border);color:var(--text);padding:9px;border-radius:8px;font-size:13px">
          <option value="">선택 안 함</option>
          ${c.items.map(it=>`<option>${it.name}</option>`).join("")}</select>
      </div>`).join("")
      : `<p style="color:var(--muted);font-size:12px">선택할 요소가 없습니다</p>`;
    return `<div class="card" style="margin-bottom:12px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
        <b style="font-size:14px">${si+1}. ${name}</b>
        <button type="button" class="btn sm ghost" data-seg-rand="${si}">🎲</button></div>
      ${cats}</div>`;
  }).join("");
  box.querySelectorAll("button[data-seg-rand]").forEach(b =>
    b.onclick = () => randomizeSegment(b.dataset.segRand));
}

function randomizeSelect(sel){
  const opts = [...sel.options].filter(o => o.value !== "");
  if(opts.length) sel.value = opts[Math.floor(Math.random()*opts.length)].text;
}
function randomizeSegment(si){
  document.querySelectorAll(`#g-segments select[data-seg="${si}"]`).forEach(randomizeSelect);
}
function randomizeAll(){
  document.querySelectorAll("#g-segments select[data-seg]").forEach(randomizeSelect);
}

function collectSegments(){
  const t = currentTemplate();
  const segs = segmentNames(currentLength());
  return segs.map((name, si) => {
    const selections = {};
    document.querySelectorAll(`#g-segments select[data-seg="${si}"]`).forEach(sel => {
      if(sel.value){
        const cat = t.categories.find(c => String(c.id) === sel.dataset.cat);
        selections[cat.name] = sel.value;
      }
    });
    return {name, selections};
  });
}

function runAnimation(container, segs){
  container.innerHTML = segs.map((s,i) =>
    `<div class="progress-row"><span style="width:74px">${i+1}. ${s.name}</span>
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

document.getElementById("g-template").addEventListener("change", renderSegments);
document.getElementById("gen-form").length.addEventListener("change", renderSegments);
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
  const t = currentTemplate();
  const segments = collectSegments();
  try {
    await API.post("/api/jobs", {name: f.name.value, template: t ? t.name : "",
      model: f.model.value, length: currentLength(), status: "생성 중", segments});
  } catch(_){}
  runAnimation(document.getElementById("gen-progress"), segments);
});
init();
```

- [ ] **Step 3: 스모크 실행**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 4: Commit**

```bash
git add templates/generate.html static/js/generate.js
git commit -m "feat: 광고 생성 구간별 카테고리 개별 선택 + 구간/전체 랜덤"
```

---

### Task 2: 육안 검증 + Vercel 재배포

**Files:** (없음)

**Interfaces:**
- Consumes: 로컬 Flask, Playwright, vercel CLI

- [ ] **Step 1: 로컬 서버 기동**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe app.py` (백그라운드)
확인: `curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/generate` → `200`

- [ ] **Step 2: Playwright 육안 검증**

- `/generate` → 템플릿(뼈순이, id=1) 선택 → 구간 카드 4개(30초) 생성, 각 카드에 캐릭터/후킹문구/장면구성 드롭다운 확인, 스크린샷
- 광고 길이 15초로 변경 → 구간 카드 2개로 줄어드는지 확인
- "전체 랜덤" 클릭 → 모든 드롭다운 값 채워짐 확인
- 광고명/제품명 입력 후 생성 요청 → 우측 진행 애니메이션(구간 순차 완료 + 합본 완료 토스트), 스크린샷

- [ ] **Step 3: 서버 종료 + 임시파일 정리**

Run: `pkill -f app.py; rm -rf .playwright-mcp *.png`

- [ ] **Step 4: master 병합 + push**

```bash
git checkout master
git merge --no-ff feature/per-segment-selection -m "Merge: 광고 생성 구간별 카테고리 선택"
venv/Scripts/python.exe scripts/smoke.py   # SMOKE OK
git push origin master
```

- [ ] **Step 5: Vercel 프로덕션 재배포**

```bash
vercel deploy --prod --yes
```

- [ ] **Step 6: 프로덕션 스모크 (curl)**

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://samplemakevideo.vercel.app/generate  # 200
```
Expected: 200

- [ ] **Step 7: 플랜 문서 커밋**

```bash
git add docs/superpowers/plans/2026-07-05-per-segment-selection.md
git commit -m "docs: 구간별 카테고리 선택 구현 플랜"
git push origin master
```

---

## Self-Review

**1. Spec coverage:**
- 구간마다 모든 카테고리 선택 → Task 1 renderSegments (구간 × categories) ✅
- 구간 수 길이 자동(15/30/60→2/4/6) → Task 1 SEG_COUNT + segmentNames ✅
- 구간 이름 시나리오 슬라이스 → Task 1 scenario.slice ✅
- 구간별 카드 세로 나열 → Task 1 카드 렌더 ✅
- 구간별 🎲 + 전체 랜덤 → Task 1 randomizeSegment/randomizeAll ✅
- 카테고리 선택사항(비워도 생성) → collectSegments가 빈 값 제외, 검증은 이름/제품/템플릿만 ✅
- 길이 변경 시 구간 재생성 → Task 1 length change 리스너 ✅
- payload segments 구조 → Task 1 collectSegments + POST ✅
- 진행 애니메이션(segs[].name) → Task 1 runAnimation ✅
- 데이터/API/스모크 무변경 → Task 1 파일 범위 ✅
- 육안 검증 + 재배포 → Task 2 ✅

**2. Placeholder scan:** 모든 코드 스텝에 실제 코드, TODO/TBD 없음 ✅

**3. Type consistency:**
- `currentTemplate/currentLength/segmentNames/renderSegments/randomizeSelect/randomizeSegment/randomizeAll/collectSegments/runAnimation` — Task 1 내부 정의·호출 일관 ✅
- `segments: [{name, selections}]` — collectSegments 생성, runAnimation은 `s.name` 소비 일치 ✅
- 드롭다운 data 속성 `data-seg`/`data-cat`/`data-seg-rand` — 렌더·수집·랜덤에서 동일 사용 ✅
- `document.getElementById("gen-form").length` — generate.html의 `<select name="length">`와 정합(폼의 named element 접근) ✅

이슈 없음.
