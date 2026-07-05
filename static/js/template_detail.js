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
        c.items.map(it => `<tr><td><b>${it.name}</b></td>
          <td><div class="prompt-cell" title="${(it.prompt||"").replace(/"/g,"&quot;")}">${it.prompt||""}</div></td>
          ${c.type === "asset" ? `<td>${it.image_url ? `<img class="thumb-img" src="${it.image_url}">` : "-"}</td>` : ""}</tr>`).join("")
          || `<tr><td colspan="3" style="color:var(--muted)">항목이 없습니다</td></tr>`
      }</tbody></table>
      <form class="add-item-form" data-cid="${c.id}" data-type="${c.type}"
            style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap;align-items:center">
        <input name="name" placeholder="항목명" style="flex:1;min-width:120px;background:var(--surface-2);
          border:1px solid var(--border);color:var(--text);padding:8px;border-radius:8px;font-size:12px">
        <input name="prompt" placeholder="프롬프트" style="flex:2;min-width:160px;background:var(--surface-2);
          border:1px solid var(--border);color:var(--text);padding:8px;border-radius:8px;font-size:12px">
        ${c.type === "asset" ? `<input name="image" type="file" accept="image/*" style="flex:1;min-width:120px;
          color:var(--muted);font-size:12px">` : ""}
        <button class="btn sm" type="submit">+ 항목</button>
      </form>
    </div>`).join("");

  box.querySelectorAll(".prompt-cell").forEach(cell =>
    cell.onclick = () => cell.classList.toggle("expanded"));

  box.querySelectorAll(".add-item-form").forEach(f =>
    f.addEventListener("submit", e => {
      e.preventDefault();
      const name = f.name.value.trim();
      if(!name) return;
      const cat = tpl.categories.find(c => String(c.id) === f.dataset.cid);
      const fileInput = f.image;
      const addItem = (img) => {
        cat.items.push({id: Date.now(), name, prompt: f.prompt.value, image_url: img || ""});
        try { API.post(`/api/templates/${TID}/categories/${cat.id}/items`,
          {name, prompt: f.prompt.value, image_url: img || ""}); } catch(_){}
        renderCategories(); UI.toast("항목이 추가되었습니다");
      };
      if(fileInput && fileInput.files && fileInput.files[0]){
        const reader = new FileReader();
        reader.onload = () => addItem(reader.result);
        reader.onerror = () => addItem("");
        reader.readAsDataURL(fileInput.files[0]);
      } else {
        addItem("");
      }
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
