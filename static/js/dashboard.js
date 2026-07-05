const STAT_DEFS = [
  ["total", "전체 생성 광고"], ["completed", "생성 완료"],
  ["generating", "생성 중"], ["failed", "실패"],
  ["templates", "등록 템플릿"], ["pool_items", "총 풀 항목"]
];
async function load(){
  const statsEl = document.getElementById("stats");
  const recentEl = document.getElementById("recent");
  UI.skeleton(statsEl);
  try {
    const d = await API.get("/api/dashboard/stats");
    statsEl.innerHTML = STAT_DEFS.map(([k, label]) =>
      `<div class="card"><h3>${label}</h3><div class="stat-num">${d[k]}</div></div>`
    ).join("");
    recentEl.innerHTML = `<table class="table"><thead><tr>
      <th>광고명</th><th>템플릿</th><th>모델</th><th>상태</th><th>요청일</th>
      </tr></thead><tbody>${
        d.recent_jobs.map(j => `<tr><td>${j.name}</td><td>${j.template}</td>
        <td>${j.model}</td><td>${UI.badge(j.status)}</td><td>${j.requested_at}</td></tr>`).join("")
      }</tbody></table>`;
  } catch(e){ UI.showError(statsEl, load); recentEl.innerHTML = ""; }
}
load();
