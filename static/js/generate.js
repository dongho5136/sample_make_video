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
