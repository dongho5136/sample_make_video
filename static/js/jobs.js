async function load(){
  const el = document.getElementById("jobs-list"); UI.skeleton(el);
  try {
    const jobs = await API.get("/api/jobs");
    el.innerHTML = `<table class="table"><thead><tr>
      <th>작업명</th><th>템플릿</th><th>모델</th><th>길이</th><th>상태</th>
      <th>요청일</th><th>완료일</th><th></th></tr></thead><tbody>${
      jobs.map(j => `<tr><td>${j.name}</td><td>${j.template}</td><td>${j.model}</td>
        <td>${j.length}초</td><td>${UI.badge(j.status)}</td>
        <td>${j.requested_at}</td><td>${j.completed_at || "-"}</td>
        <td><button class="btn sm ghost" data-name="${j.name}">재생성</button></td></tr>`).join("")
    }</tbody></table>`;
    el.querySelectorAll("button[data-name]").forEach(b =>
      b.onclick = () => UI.toast(`'${b.dataset.name}' 재생성 요청됨`));
  } catch(e){ UI.showError(el, load); }
}
load();
