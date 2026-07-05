# 광고 생성: 구간 수동 추가/삭제 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 광고 생성 화면에서 구간을 "+ 구간 추가" 버튼으로 하나씩 추가/삭제하고, 각 구간에서 카테고리 요소를 고르게 한다. 템플릿 선택 시 1구간 자동 생성.

**Architecture:** generate.js에 `segmentList` 상태 배열을 두고 추가/삭제/렌더를 관리한다. 광고 길이 기반 자동 구간 생성을 제거하고, 구간 이름은 시나리오 순서로 자동 부여한다. 데이터/API는 기존 것을 재사용한다.

**Tech Stack:** Python Flask, Jinja2, Vanilla HTML/CSS/JS, Vercel

## Global Constraints

- 프론트: Vanilla HTML/CSS/JS만
- 상태: in-memory, 프론트 세션, 새로고침 초기화
- 구간 이름: `SEGMENT_SCENARIO`(후킹/문제상황/제품소개/사용장면/혜택강조/CTA)에서 index로, 없으면 `"구간"+(index+1)` — `/api/meta`의 `scenario`
- 템플릿 최초 선택 시 1구간 자동 생성
- 광고 길이는 메타 정보로만(구간 수와 무관)
- 필수 검증(유지): 광고명·제품명·템플릿. 카테고리/구간은 선택사항
- 데이터/API/스모크 변경 없음
- 검증: `venv/Scripts/python.exe scripts/smoke.py` → `SMOKE OK` + Playwright 육안

---

### Task 1: 구간 수동 추가/삭제 구현

**Files:**
- Modify: `templates/generate.html`
- Modify: `static/js/generate.js`

**Interfaces:**
- Consumes: `GET /api/templates`, `GET /api/meta`(scenario/models/ratios), `POST /api/jobs`, `window.UI`
- payload: `{name, template, model, length, status:"생성 중", segments:[{name, selections:{카테고리명:항목명}}]}`

- [ ] **Step 1: generate.html 구간 헤더에 "+ 구간 추가" 버튼 추가**

`templates/generate.html`에서 아래 블록:

```html
    <div style="display:flex;justify-content:space-between;align-items:center;margin:6px 0 4px">
      <label style="color:var(--muted);font-size:12px">구간별 요소 선택</label>
      <button type="button" class="btn sm ghost" id="rand-all">🎲 전체 랜덤</button></div>
    <div id="g-segments"><p class="empty" style="padding:16px">템플릿을 먼저 선택하세요</p></div>
```

를 아래로 교체:

```html
    <div style="display:flex;justify-content:space-between;align-items:center;margin:6px 0 4px">
      <label style="color:var(--muted);font-size:12px">구간별 요소 선택</label>
      <div style="display:flex;gap:8px">
        <button type="button" class="btn sm ghost" id="rand-all">🎲 전체 랜덤</button>
        <button type="button" class="btn sm" id="add-seg">+ 구간 추가</button></div></div>
    <div id="g-segments"><p class="empty" style="padding:16px">템플릿을 먼저 선택하세요</p></div>
```

- [ ] **Step 2: generate.js를 segmentList 상태 기반으로 재작성**

`static/js/generate.js` 전체를 아래로 교체:

```javascript
let scenario = [];
let templates = [];
let segmentList = [];   // [{name}]

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
function scenarioName(i){ return scenario[i] || ("구간" + (i + 1)); }

function renderSegments(){
  const t = currentTemplate();
  const box = document.getElementById("g-segments");
  if(!t){ box.innerHTML = `<p class="empty" style="padding:16px">템플릿을 먼저 선택하세요</p>`; return; }
  if(!segmentList.length){ box.innerHTML = `<p class="empty" style="padding:16px">구간을 추가하세요</p>`; return; }
  box.innerHTML = segmentList.map((seg, si) => {
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
        <b style="font-size:14px">${si+1}. ${seg.name}</b>
        <div style="display:flex;gap:6px">
          <button type="button" class="btn sm ghost" data-seg-rand="${si}">🎲</button>
          <button type="button" class="btn sm ghost" data-seg-del="${si}">✕</button></div></div>
      ${cats}</div>`;
  }).join("");
  box.querySelectorAll("button[data-seg-rand]").forEach(b =>
    b.onclick = () => randomizeSegment(b.dataset.segRand));
  box.querySelectorAll("button[data-seg-del]").forEach(b =>
    b.onclick = () => removeSegment(Number(b.dataset.segDel)));
}

function addSegment(){
  segmentList.push({name: scenarioName(segmentList.length)});
  renderSegments();
}
function removeSegment(i){
  segmentList.splice(i, 1);
  segmentList = segmentList.map((_, idx) => ({name: scenarioName(idx)}));
  renderSegments();
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
  return segmentList.map((seg, si) => {
    const selections = {};
    document.querySelectorAll(`#g-segments select[data-seg="${si}"]`).forEach(sel => {
      if(sel.value){
        const cat = t.categories.find(c => String(c.id) === sel.dataset.cat);
        selections[cat.name] = sel.value;
      }
    });
    return {name: seg.name, selections};
  });
}

function runAnimation(container, segs){
  const rows = segs.length ? segs.map((s,i) =>
    `<div class="progress-row"><span style="width:74px">${i+1}. ${s.name}</span>
     <span class="bar"><i></i></span>
     <span id="st-${i}" style="width:60px;text-align:right">${UI.badge("대기 중")}</span></div>`).join("") : "";
  container.innerHTML = rows
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

document.getElementById("g-template").addEventListener("change", () => {
  segmentList = currentTemplate() ? [{name: scenarioName(0)}] : [];
  renderSegments();
});
document.getElementById("add-seg").addEventListener("click", () => {
  if(currentTemplate()) addSegment();
});
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
git commit -m "feat: 구간 수동 추가/삭제 (템플릿 선택 시 1구간 자동)"
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

- `/generate` → 템플릿(뼈순이 id=1) 선택 → **1구간 자동 생성** 확인, 콘솔 에러 없음, 스크린샷
- "+ 구간 추가" 2회 클릭 → 2,3구간 추가(이름: 문제상황/제품소개) 확인, 스크린샷
- 2구간의 ✕ 삭제 → 구간이 2개로 줄고 번호/이름 재정렬 확인
- "전체 랜덤" → 드롭다운 값 채워짐 확인
- 광고명/제품명 입력 후 생성 요청 → 진행 애니메이션 + 완료 토스트

- [ ] **Step 3: 서버 종료 + 임시파일 정리**

Run: `pkill -f app.py; rm -rf .playwright-mcp *.png`

- [ ] **Step 4: master 병합 + push**

```bash
git checkout master
git merge --no-ff feature/manual-segment-add -m "Merge: 광고 생성 구간 수동 추가/삭제"
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
git add docs/superpowers/plans/2026-07-05-manual-segment-add.md
git commit -m "docs: 구간 수동 추가/삭제 구현 플랜"
git push origin master
```

---

## Self-Review

**1. Spec coverage:**
- "+ 구간 추가" 버튼 → Task 1 add-seg + addSegment ✅
- 구간 이름 시나리오 순서 자동(초과 시 구간N) → Task 1 scenarioName ✅
- 광고 길이–구간 분리(length change로 재생성 안 함) → Task 1 (length 리스너 없음) ✅
- 구간별 ✕ 삭제 + 번호 재정렬 → Task 1 removeSegment ✅
- 템플릿 선택 시 1구간 자동 → Task 1 template change 핸들러 ✅
- 구간별 🎲 / 전체 랜덤 → Task 1 randomizeSegment/randomizeAll ✅
- 수집 payload segments → Task 1 collectSegments ✅
- 진행 애니메이션(0구간이면 합본만) → Task 1 runAnimation(rows 빈 처리) ✅
- 데이터/API/스모크 무변경 → Task 1 파일 범위 ✅
- 육안 + 재배포 → Task 2 ✅

**2. Placeholder scan:** 실제 코드만, TODO/TBD 없음 ✅

**3. Type consistency:**
- `segmentList = [{name}]` — 생성/삭제/렌더/수집 전부 일관 ✅
- `scenarioName(i)` — addSegment/removeSegment/template change에서 동일 사용 ✅
- `data-seg`/`data-cat`/`data-seg-rand`/`data-seg-del` — 렌더·이벤트·수집 일치 ✅
- `segments:[{name, selections}]` — collectSegments 생성, runAnimation `s.name` 소비 일치 ✅
- `document.getElementById("gen-form").length` — `<select name="length">`와 정합(이전 기능에서 브라우저 검증됨) ✅

이슈 없음.
