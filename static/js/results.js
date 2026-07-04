let items = [];
function openDetail(r){
  document.getElementById("rm-title").textContent = r.name;
  document.getElementById("rm-body").innerHTML = `
    <div class="thumb" style="aspect-ratio:16/9;margin-bottom:16px">▶ 최종 영상 미리보기</div>
    <div style="display:flex;gap:8px;color:var(--muted);font-size:12px;margin-bottom:16px;flex-wrap:wrap">
      <span>🧩 ${r.template}</span><span>🤖 ${r.model}</span>
      <span>🖼 ${r.assets.join(", ")}</span><span>📅 ${r.created_at}</span></div>
    <h3 style="color:var(--muted);font-size:13px;margin-bottom:10px">구간별 영상</h3>
    <div class="grid" style="grid-template-columns:repeat(3,1fr)">${
      r.segments.map((s,i) => `<div><div class="thumb">${i+1}. ${s.name}</div></div>`).join("")}</div>
    <div style="display:flex;gap:8px;margin-top:20px">
      <button class="btn" onclick="UI.toast('다운로드를 시작합니다')">⬇ 다운로드</button>
      <button class="btn ghost" onclick="UI.toast('재생성 요청됨')">🔄 재생성</button></div>`;
  UI.openModal("result-modal");
}
async function load(){
  const el = document.getElementById("results-list"); UI.skeleton(el);
  try {
    items = await API.get("/api/results");
    el.innerHTML = items.map((r,i) => `
      <div class="card" data-i="${i}" style="cursor:pointer">
        <div class="thumb">▶ 미리보기</div>
        <h3 style="color:var(--text);font-size:15px;margin-top:10px">${r.name}</h3>
        <p style="color:var(--muted);font-size:12px;margin-top:6px">
          ${r.template} · ${r.segments.length}구간 · ${r.created_at}</p></div>`).join("");
    el.querySelectorAll(".card").forEach(c =>
      c.onclick = () => openDetail(items[c.dataset.i]));
  } catch(e){ UI.showError(el, load); }
}
load();
