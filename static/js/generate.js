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
