const STATUS_CLASS = {
  "완료": "ok", "생성 중": "info", "합본 생성 중": "info",
  "구간 생성 완료": "info", "대기 중": "muted", "실패": "err",
  "사용": "ok", "미사용": "muted"
};
window.UI = {
  openModal(id){ document.getElementById(id).classList.add("open"); },
  closeModal(id){ document.getElementById(id).classList.remove("open"); },
  badge(status){
    const cls = STATUS_CLASS[status] || "muted";
    return `<span class="badge ${cls}">${status}</span>`;
  },
  toast(msg){
    const t = document.getElementById("toast");
    t.textContent = msg; t.classList.add("show");
    clearTimeout(this._tt);
    this._tt = setTimeout(() => t.classList.remove("show"), 2500);
  },
  showError(container, retryFn){
    container.innerHTML = `<div class="error-box">데이터를 불러오지 못했습니다.
      <br><button class="btn sm ghost" style="margin-top:12px">재시도</button></div>`;
    container.querySelector("button").onclick = retryFn;
  },
  skeleton(container){ container.innerHTML = `<div class="empty">불러오는 중…</div>`; }
};
