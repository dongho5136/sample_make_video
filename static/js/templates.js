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
