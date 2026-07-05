# 긴 프롬프트 더미 + 이미지 업로드(미리보기) — 설계 문서

작성일: 2026-07-05

## 1. 목적

(1) 각 템플릿 상세의 prompt 카테고리에 **긴 프롬프트 풀 항목을 여러 개** 넣어
데모를 풍성하게 하고, (2) asset 카테고리 항목 등록 시 **이미지를 업로드**해
미리보기로 보여준다.

## 2. 결정 사항 (브레인스토밍 확정)

- 긴 프롬프트 범위: **모든 템플릿** prompt 카테고리에 여러 개씩
- 긴 프롬프트 표시: **줄임(…) + 전체보기** (테이블 셀 말줄임, 클릭 토글로 전체)
- 이미지 업로드: **보여주기용** — `FileReader` base64 data URL, 서버 저장 없음
- asset 이미지 입력: **파일 업로드로 교체** (URL 입력칸 제거)

## 3. 긴 프롬프트 더미 확충 (data/dummy.py)

각 템플릿의 `type:"prompt"` 카테고리 `items`에 실제 광고 프롬프트처럼 2~4문장
길이의 긴 프롬프트를 3~5개씩 채운다. `name`은 짧은 라벨, `prompt`는 긴 텍스트.

예시(구조):
```python
{"id": 121, "name": "D-30 시작",
 "prompt": "3초 안에 시청자의 스크롤을 멈추게 할 강렬한 첫 문장으로 시작한다. "
           "'오늘부터 D-30, 당신의 30일 후는 어떻게 달라질까요?'라는 질문을 "
           "화면 중앙 굵은 자막으로 띄우고, 카운트다운 숫자를 임팩트 있게 애니메이션한다. "
           "배경은 밝고 경쾌하게, 캐릭터가 손을 흔들며 등장한다.", "image_url": ""},
```

asset 카테고리 item의 `image_url`은 빈 문자열 유지(업로드로 채움).

## 4. 긴 프롬프트 표시 (template_detail)

- 풀 항목 테이블의 프롬프트 셀에 `.prompt-cell` 적용: 기본은 2줄 말줄임
  (`-webkit-line-clamp:2`), `title` 속성에 전체 프롬프트(호버 툴팁).
- 셀 클릭 시 `expanded` 클래스 토글 → 전체 프롬프트 표시/접기.
- `components.css`에 `.prompt-cell`(말줄임)과 `.prompt-cell.expanded`(전체) 추가.

## 5. 이미지 업로드 (template_detail)

- asset 타입 카테고리의 항목 추가 폼: 기존 `이미지 URL` 텍스트 input을
  **`<input type="file" accept="image/*">`** 로 교체.
- 파일 선택 시 `FileReader.readAsDataURL` → base64 data URL을 항목의
  `image_url`에 저장.
- 테이블 이미지 셀: `image_url` 있으면 `<img class="thumb-img">` 썸네일,
  없으면 `-`.
- 서버 업로드/저장 없음. 세션 내 미리보기용(새로고침 초기화).
- prompt 타입 카테고리는 파일 input 없음(기존과 동일).

### 항목 추가 흐름 (asset 카테고리)
1. 항목명 입력 + (선택) 파일 선택
2. 파일 있으면 FileReader로 data URL 생성 (비동기)
3. data URL 준비되면 `items.push({id, name, prompt, image_url:<dataURL>})` 후 재렌더
4. 파일 없으면 image_url 빈 문자열로 추가

## 6. 영향 범위

- 수정:
  - `data/dummy.py` — prompt 카테고리에 긴 프롬프트 다수 추가
  - `templates/template_detail.html` — (JS 렌더라 실제 변경은 최소, 필요 시 없음)
  - `static/js/template_detail.js` — 파일 input 렌더 + FileReader 처리,
    프롬프트 셀 말줄임/토글, 썸네일 렌더
  - `static/css/components.css` — `.prompt-cell`, `.thumb-img` 추가
- 변경 없음: `app.py`, `scripts/smoke.py`
- 통계: `pool_items` 수가 자연히 증가 (get_stats 로직 그대로)

## 7. 에러 처리

- 이미지가 아닌 파일: `accept="image/*"`로 1차 제한. FileReader 실패 시 항목은
  image_url 없이 추가(콘솔 경고 없이 graceful).
- 항목명 미입력: 기존대로 제출 무시.
- 긴 프롬프트 셀 토글: 순수 클래스 토글, 실패 여지 없음.

## 8. 검증

- `scripts/smoke.py`: 라우트 변경 없음 → 기존 스모크 통과 (pool_items 증가만)
- Playwright 육안:
  - 상세 페이지(`/templates/1` 등)에서 prompt 카테고리 항목이 여러 개 + 긴
    프롬프트가 말줄임(…)으로 표시, 클릭 시 전체 표시
  - asset 카테고리에서 파일 선택 → 항목 추가 → 테이블에 썸네일 미리보기
- 프로덕션 curl 스모크 후 Vercel 재배포

## 9. 배포

구현·검증 완료 후 GitHub push → `vercel deploy --prod`.
