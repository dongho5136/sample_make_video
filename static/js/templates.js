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
