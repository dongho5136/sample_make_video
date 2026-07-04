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
