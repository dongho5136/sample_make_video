async function load(){
  const el = document.getElementById("settings-body"); UI.skeleton(el);
  try {
    const s = await API.get("/api/settings");
    el.innerHTML = `
      <div class="card" style="margin-bottom:20px">
        <h2 style="margin-bottom:16px">회사 IP 제한</h2>
        <div class="form-field"><label>IP 제한 사용</label>
          <select><option ${s.ip_restrict_enabled?'selected':''}>사용</option>
          <option ${!s.ip_restrict_enabled?'selected':''}>미사용</option></select></div>
        <div class="form-field"><label>허용 IP 목록</label>
          <textarea rows="2">${s.allowed_ips.join("\n")}</textarea></div>
        <p style="color:var(--muted);font-size:12px">마지막 접속 IP: ${s.last_access_ip}</p>
        <h3 style="color:var(--muted);font-size:13px;margin:16px 0 8px">접속 로그</h3>
        <table class="table"><thead><tr><th>IP</th><th>시간</th><th>결과</th></tr></thead>
          <tbody>${s.access_logs.map(l=>`<tr><td>${l.ip}</td><td>${l.time}</td>
          <td>${UI.badge(l.result==="허용"?"사용":"실패")}</td></tr>`).join("")}</tbody></table>
      </div>
      <div class="card">
        <h2 style="margin-bottom:16px">기본 설정</h2>
        <div class="form-grid">
          <div class="form-field"><label>관리자 계정</label><input value="${s.admin_account}"></div>
          <div class="form-field"><label>기본 영상 비율</label><input value="${s.default_ratio}"></div>
          <div class="form-field"><label>기본 생성 모델</label><input value="${s.default_model}"></div>
          <div class="form-field"><label>기본 저장 경로</label><input value="${s.save_path}"></div>
        </div>
        <div class="form-field"><label>API 연동 설정</label><input placeholder="API Key (미설정)"></div>
        <div class="form-field"><label>광고 매체 연동</label><input placeholder="Meta / Google Ads (미설정)"></div>
        <button class="btn" onclick="UI.toast('설정이 저장되었습니다')">저장</button>
      </div>`;
  } catch(e){ UI.showError(el, load); }
}
load();
