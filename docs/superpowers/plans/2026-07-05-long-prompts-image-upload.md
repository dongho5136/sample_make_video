# 긴 프롬프트 더미 + 이미지 업로드 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 각 템플릿 prompt 카테고리에 긴 프롬프트 항목을 여러 개 채우고, 상세 페이지에서 긴 프롬프트를 말줄임+전체보기로 표시하며, asset 항목은 이미지 파일 업로드(base64 미리보기)로 등록한다.

**Architecture:** data/dummy.py에 긴 프롬프트 더미를 추가한다. template_detail.js가 프롬프트 셀 말줄임/토글과 asset 카테고리의 파일 업로드(FileReader→base64)를 처리하고, components.css에 말줄임/썸네일 클래스를 추가한다.

**Tech Stack:** Python Flask, Jinja2, Vanilla HTML/CSS/JS, Vercel

## Global Constraints

- 프론트: Vanilla HTML/CSS/JS만
- 상태: in-memory, 프론트 세션 유지, 새로고침 초기화
- 이미지: FileReader base64 data URL, 서버 저장 없음 (미리보기용)
- asset 항목: 파일 업로드로 교체(URL 입력 제거), prompt 항목은 파일 없음
- 긴 프롬프트: 테이블 셀 2줄 말줄임 + 클릭 토글 전체보기 + title 툴팁
- 데이터/API/스모크 라우트 변경 없음
- 검증: `venv/Scripts/python.exe scripts/smoke.py` → `SMOKE OK` + Playwright 육안

---

### Task 1: 긴 프롬프트 더미 확충 (data/dummy.py)

**Files:**
- Modify: `data/dummy.py`

**Interfaces:**
- Produces: 각 템플릿 prompt 카테고리 items에 긴 prompt(2~4문장) 다수. id 스키마/구조 불변, `get_stats().pool_items` 증가.

- [ ] **Step 1: 템플릿 1(뼈순이)의 후킹 문구/장면 구성 항목을 긴 프롬프트로 교체·확장**

`data/dummy.py`에서 id 12(후킹 문구) items와 id 13(장면 구성) items를 아래로 교체:

```python
        {"id": 12, "name": "후킹 문구", "type": "prompt", "items": [
            {"id": 121, "name": "D-30 시작", "image_url": "",
             "prompt": "3초 안에 시청자의 스크롤을 멈추게 할 강렬한 첫 문장으로 시작한다. "
                       "'오늘부터 D-30, 당신의 30일 후는 어떻게 달라질까요?'라는 질문을 화면 중앙 굵은 "
                       "노란 자막으로 띄우고, 카운트다운 숫자 30을 임팩트 있게 확대 애니메이션한다. "
                       "배경음은 경쾌한 비트, 캐릭터가 손을 흔들며 프레임 안으로 통통 튀어 들어온다."},
            {"id": 122, "name": "변화 예고", "image_url": "",
             "prompt": "'30일 뒤 달라진 나를 미리 만나보세요'라는 카피를 속삭이듯 시작해 점점 볼륨을 높인다. "
                       "화면은 흐릿한 실루엣에서 또렷한 애프터 컷으로 서서히 포커스가 맞춰지며, "
                       "하단에 진행률 바가 0%에서 100%로 차오르는 모션을 넣는다. "
                       "마지막에 캐릭터가 엄지를 치켜세우며 시선을 사로잡는다."},
            {"id": 123, "name": "공감형 오프닝", "image_url": "",
             "prompt": "'다이어트, 작심삼일로 끝난 적 있으신가요?'라는 공감 질문으로 문을 연다. "
                       "실패했던 순간들을 빠른 컷으로 몽타주하며 시청자의 고개를 끄덕이게 만든 뒤, "
                       "'이번엔 다릅니다'라는 반전 자막으로 전환한다. 톤은 친근하되 진지하게."},
        ]},
        {"id": 13, "name": "장면 구성", "type": "prompt", "items": [
            {"id": 131, "name": "비포애프터", "image_url": "",
             "prompt": "일자별 비포/애프터 컷을 좌우 분할 화면으로 전환하며 변화를 극적으로 대비시킨다. "
                       "각 컷 상단에 'DAY 01', 'DAY 15', 'DAY 30' 라벨을 붙이고, 넘어갈 때마다 "
                       "가벼운 스와이프 트랜지션과 셔터음을 넣어 리듬감을 준다."},
            {"id": 132, "name": "일기형", "image_url": "",
             "prompt": "매일의 기록을 손글씨 다이어리 페이지가 넘어가는 형식으로 구성한다. "
                       "캐릭터의 하루 루틴(운동·식단·컨디션)을 짧은 클립으로 보여주고, "
                       "페이지 모서리에 도장처럼 완료 스탬프가 찍히는 만족감 있는 모션을 반복한다."},
            {"id": 133, "name": "챌린지 인증형", "image_url": "",
             "prompt": "실사용자들의 인증샷을 콜라주처럼 빠르게 이어 붙여 신뢰감을 쌓는다. "
                       "화면 곳곳에 '나도 성공', 'D-30 완주' 같은 손글씨 스티커를 흩뿌리고, "
                       "마지막엔 모든 인증샷이 하트 모양으로 모이는 그리드 애니메이션으로 마무리한다."},
        ]},
```

- [ ] **Step 2: 템플릿 2·3·4의 prompt 카테고리를 긴 프롬프트로 교체·확장**

id 22(질문 스크립트), id 31(훅 문구), id 32(BGM 무드), id 41(후기 문구) items를 아래로 교체:

```python
        {"id": 22, "name": "질문 스크립트", "type": "prompt", "items": [
            {"id": 221, "name": "첫인상", "image_url": "",
             "prompt": "'처음 써보셨을 때 솔직히 어떠셨어요?'라고 편안하게 물으며 인터뷰이의 표정 변화를 "
                       "클로즈업으로 담는다. 답변 중 핵심 문장은 하단 자막으로 강조하고, 제품 클로즈업 "
                       "인서트를 자연스럽게 교차 편집해 진정성을 살린다."},
            {"id": 222, "name": "재구매", "image_url": "",
             "prompt": "'다시 구매하실 의향이 있나요? 그 이유는 무엇인가요?'라는 질문으로 신뢰를 증폭한다. "
                       "인터뷰이가 망설임 없이 '네'라고 답하는 순간을 슬로우 모션으로 잡고, "
                       "실제 재구매 화면(장바구니·주문내역)을 근거 인서트로 붙인다."},
            {"id": 223, "name": "비교 경험", "image_url": "",
             "prompt": "'다른 제품과 비교했을 때 가장 큰 차이는요?'라고 물어 차별점을 인터뷰이의 입으로 "
                       "말하게 한다. 경쟁 상황을 은근히 암시하는 B롤을 깔되 비방은 피하고, "
                       "'이건 확실히 다르더라고요'라는 자연스러운 멘트로 설득력을 높인다."},
        ]},
        {"id": 31, "name": "훅 문구", "type": "prompt", "items": [
            {"id": 311, "name": "3초 훅", "image_url": "",
             "prompt": "영상 시작 3초 안에 시선을 붙잡는 강한 첫 문장을 화면 정중앙 초대형 자막으로 띄운다. "
                       "'이거 모르면 진짜 손해예요'를 빠른 줌인과 함께 던지고, 곧바로 제품의 핵심 장면으로 "
                       "컷 전환해 궁금증이 식기 전에 몰입시킨다."},
            {"id": 312, "name": "궁금증 유발", "image_url": "",
             "prompt": "'왜 다들 이걸 사재기하는지 아세요?'라는 질문으로 호기심을 자극한다. "
                       "답을 바로 주지 않고 관련 없어 보이는 장면들을 빠르게 나열하다가, "
                       "마지막에 제품을 공개하며 '바로 이것 때문입니다' 반전으로 마무리한다."},
            {"id": 313, "name": "숫자 임팩트", "image_url": "",
             "prompt": "'재고 300개, 3시간 만에 완판'처럼 구체적인 숫자를 화면 가득 카운터 애니메이션으로 "
                       "보여준다. 숫자가 빠르게 올라가는 효과음과 함께 긴박감을 조성하고, "
                       "'지금이 마지막 기회'라는 자막으로 행동을 촉구한다."},
        ]},
        {"id": 32, "name": "BGM 무드", "type": "prompt", "items": [
            {"id": 321, "name": "트렌디", "image_url": "",
             "prompt": "요즘 숏폼에서 유행하는 업템포 비트를 깔되 저작권 안전한 트랙으로 선택한다. "
                       "비트 드롭 지점에 맞춰 제품 클로즈업 컷을 배치해 리듬과 편집을 싱크시키고, "
                       "후렴 구간에서 자막이 튀어오르는 키네틱 타이포로 흥을 끌어올린다."},
            {"id": 322, "name": "긴장감", "image_url": "",
             "prompt": "낮은 베이스가 서서히 고조되는 텐션 빌드업 트랙으로 기대감을 쌓는다. "
                       "제품 공개 직전 0.5초 무음을 넣어 시선을 집중시키고, 공개 순간 강한 임팩트음과 "
                       "함께 화면을 플래시로 전환해 카타르시스를 준다."},
        ]},
        {"id": 41, "name": "후기 문구", "type": "prompt", "items": [
            {"id": 411, "name": "별점 5점", "image_url": "",
             "prompt": "'★★★★★ 인생템 찾았어요'라는 리뷰를 실제 쇼핑몰 후기 화면처럼 재현해 신뢰를 준다. "
                       "별 다섯 개가 하나씩 채워지는 애니메이션과 함께 후기 텍스트를 타이핑 효과로 띄우고, "
                       "작성자 닉네임과 구매 인증 배지를 붙여 진짜 후기 같은 디테일을 살린다."},
            {"id": 412, "name": "재구매 후기", "image_url": "",
             "prompt": "'벌써 세 번째 재구매예요'라는 멘트로 반복 구매의 만족을 강조한다. "
                       "주문 내역 세 건을 스크롤하며 보여주고, '이젠 없으면 불안할 정도'라는 솔직한 코멘트로 "
                       "제품 의존도를 유쾌하게 표현한다."},
            {"id": 413, "name": "선물 후기", "image_url": "",
             "prompt": "'친구 선물했다가 저까지 재구매했어요'라는 확산형 후기로 입소문 효과를 노린다. "
                       "선물 포장을 여는 장면과 받은 사람의 놀란 반응을 담고, '주변에 다 추천했다'는 "
                       "멘트로 자연스러운 바이럴을 유도한다."},
        ]},
```

- [ ] **Step 3: 템플릿 5·7에 prompt 카테고리 추가 (현재 asset만 있음)**

id 5(Before & After)의 categories와 id 7(애니메이션)의 categories에 prompt 카테고리를 추가한다. id 5의 `"categories": [ ... ]`를 아래로 교체:

```python
     "categories": [
        {"id": 51, "name": "비교 대상", "type": "asset", "items": [
            {"id": 511, "name": "제품컷", "prompt": "product front shot, clean bg", "image_url": ""},
        ]},
        {"id": 52, "name": "대비 연출", "type": "prompt", "items": [
            {"id": 521, "name": "분할 비교", "image_url": "",
             "prompt": "화면을 좌(BEFORE)/우(AFTER)로 정확히 반 나눠 동일한 각도·조명에서 촬영한 "
                       "두 상태를 동시에 보여준다. 가운데 분할선을 좌우로 슬라이드시키며 변화 정도를 "
                       "인터랙티브하게 드러내고, 'BEFORE'/'AFTER' 라벨을 큼직하게 고정한다."},
            {"id": 522, "name": "타임랩스", "image_url": "",
             "prompt": "사용 전부터 후까지의 과정을 빠른 타임랩스로 압축해 극적인 변화를 한 컷에 담는다. "
                       "경과 시간을 화면 모서리 타이머로 표시하고, 변화가 두드러지는 구간에서 잠시 "
                       "속도를 늦춰 시청자가 차이를 확실히 인지하게 한다."},
        ]},
     ]},
```

id 7의 `"categories": [ ... ]`를 아래로 교체:

```python
     "categories": [
        {"id": 71, "name": "캐릭터", "type": "asset", "items": [
            {"id": 711, "name": "마스코트", "prompt": "brand mascot, flat illustration", "image_url": ""},
        ]},
        {"id": 72, "name": "모션 컨셉", "type": "prompt", "items": [
            {"id": 721, "name": "키네틱 타이포", "image_url": "",
             "prompt": "핵심 메시지를 글자 하나하나가 튀고 늘어나고 회전하는 키네틱 타이포그래피로 "
                       "표현한다. 색상은 브랜드 팔레트로 통일하고, 리듬감 있는 등장/퇴장 모션으로 "
                       "정보 전달과 시각적 즐거움을 동시에 잡는다."},
            {"id": 722, "name": "아이콘 설명형", "image_url": "",
             "prompt": "제품의 기능을 단순한 아이콘 애니메이션으로 하나씩 시각화해 이해를 돕는다. "
                       "각 기능이 등장할 때 짧은 효과음과 말풍선 설명을 붙이고, 마지막에 아이콘들이 "
                       "제품 로고로 모여드는 통합 모션으로 마무리한다."},
        ]},
     ]},
```

- [ ] **Step 4: import 검증**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe -c "from data import dummy; print('pool_items', dummy.get_stats()['pool_items']); print('t5 cats', len(dummy.TEMPLATES[4]['categories'])); print('t7 cats', len(dummy.TEMPLATES[6]['categories']))"`
Expected: `pool_items` 증가한 값 / `t5 cats 2` / `t7 cats 2`

- [ ] **Step 5: 스모크 실행**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 6: Commit**

```bash
git add data/dummy.py
git commit -m "feat: 각 템플릿 prompt 카테고리에 긴 프롬프트 더미 다수 추가"
```

---

### Task 2: 긴 프롬프트 표시(말줄임/토글) + 이미지 업로드 (template_detail)

**Files:**
- Modify: `static/css/components.css`
- Modify: `static/js/template_detail.js`

**Interfaces:**
- Consumes: `GET /api/templates/<id>`, `window.UI`, `API.post`
- 프롬프트 셀: `.prompt-cell`(2줄 말줄임) + 클릭 시 `.expanded` 토글 + `title` 전체
- asset 항목 추가: `<input type="file" accept="image/*">` → FileReader base64 → `item.image_url`
- 썸네일: `.thumb-img` (있으면 img, 없으면 `-`)

- [ ] **Step 1: components.css에 말줄임/썸네일 클래스 추가**

`static/css/components.css` 맨 끝에 추가:

```css
.prompt-cell{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
  overflow:hidden;cursor:pointer;max-width:420px;line-height:1.5}
.prompt-cell.expanded{-webkit-line-clamp:unset;overflow:visible}
.thumb-img{width:48px;height:48px;object-fit:cover;border-radius:8px;
  border:1px solid var(--border)}
```

- [ ] **Step 2: template_detail.js의 renderCategories를 프롬프트 토글 + 파일 업로드로 교체**

`static/js/template_detail.js`의 `renderCategories` 함수 전체를 아래로 교체:

```javascript
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
```

- [ ] **Step 3: 스모크 실행**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe scripts/smoke.py`
Expected: `SMOKE OK: all routes green`

- [ ] **Step 4: Commit**

```bash
git add static/css/components.css static/js/template_detail.js
git commit -m "feat: 긴 프롬프트 말줄임/전체보기 + asset 이미지 파일 업로드 미리보기"
```

---

### Task 3: 육안 검증 + Vercel 재배포

**Files:** (없음)

- [ ] **Step 1: 로컬 서버 기동**

Run: `cd "c:/Users/UserK/PycharmProjects/sample_make_video" && venv/Scripts/python.exe app.py` (백그라운드)
확인: `curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/templates/1` → `200`

- [ ] **Step 2: Playwright 육안 검증**

- `/templates/1` → 후킹 문구/장면 구성 카테고리에 항목 3개씩 + 긴 프롬프트가 말줄임(…)으로 표시, 스크린샷
- 프롬프트 셀 클릭 → 전체 프롬프트 펼쳐짐 확인
- 캐릭터(asset) 카테고리 항목 추가 폼에 파일 선택 input 존재 확인
- 파일 업로드는 실제 파일 다이얼로그라 자동화 대신, `image_url`에 data URL이 있으면 썸네일이 뜨는지 evaluate로 항목 push 후 재렌더 확인
- `/templates/6`(카테고리 없음)·`/templates/5`(prompt 추가됨) 스팟 확인

- [ ] **Step 3: 서버 종료 + 임시파일 정리**

Run: `pkill -f app.py; rm -rf .playwright-mcp *.png`

- [ ] **Step 4: master 병합 + push**

```bash
git checkout master
git merge --no-ff feature/long-prompts-image-upload -m "Merge: 긴 프롬프트 더미 + 이미지 업로드"
venv/Scripts/python.exe scripts/smoke.py   # SMOKE OK
git push origin master
```

- [ ] **Step 5: Vercel 프로덕션 재배포**

```bash
vercel deploy --prod --yes
```

- [ ] **Step 6: 프로덕션 스모크**

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://samplemakevideo.vercel.app/templates/1  # 200
```
Expected: 200

- [ ] **Step 7: 플랜 문서 커밋**

```bash
git add docs/superpowers/plans/2026-07-05-long-prompts-image-upload.md
git commit -m "docs: 긴 프롬프트 + 이미지 업로드 구현 플랜"
git push origin master
```

---

## Self-Review

**1. Spec coverage:**
- 모든 템플릿 prompt 카테고리 긴 프롬프트 다수 → Task 1 (템플릿1~5,7 / 템플릿6은 카테고리 없음 유지) ✅
- 긴 프롬프트 표시 말줄임+전체보기+title → Task 2 .prompt-cell + 토글 ✅
- asset 이미지 파일 업로드(base64) → Task 2 file input + FileReader ✅
- asset URL 입력 제거(교체) → Task 2 (image_url 텍스트 input 없음, file만) ✅
- 썸네일 미리보기 → Task 2 .thumb-img ✅
- 데이터/API/스모크 라우트 무변경 → Task 1/2 파일 범위 ✅
- 육안 + 재배포 → Task 3 ✅

**2. Placeholder scan:** 실제 코드/텍스트만, TODO/TBD 없음 ✅

**3. Type consistency:**
- item 스키마 `{id,name,prompt,image_url}` — Task 1 데이터와 Task 2 렌더/추가 일치 ✅
- `.prompt-cell`, `.thumb-img` — Task 2 CSS 정의·JS 사용 일치 ✅
- `f.image`(file input name="image") — Task 2 렌더·submit 핸들러 일치 ✅
- `renderCategories`/`TID`/`tpl` — 기존 template_detail.js 정의 재사용, 교체 함수 내 일관 ✅

이슈 없음.
