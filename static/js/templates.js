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
