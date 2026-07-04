# AI 광고영상 제작 관리자 대시보드

Flask + Vanilla JS 기반 더미데이터 관리자 대시보드 (데모).

## 로컬 실행

```
pip install -r requirements.txt
python app.py
# http://localhost:5000
```

## 화면

대시보드 · 광고 생성 · 템플릿 관리 · 에셋 관리 · 생성 작업 목록 · 생성 결과 관리 · 설정

## 배포

Vercel 연동 후 자동 배포 (`vercel.json`).

## 구조

- `app.py` — 라우트 + `/api/*` 더미 JSON
- `data/dummy.py` — 더미데이터 단일 소스 (실 연동 시 이 파일 + API 핸들러만 교체)
- `templates/` — Jinja2 화면, `static/` — CSS/JS

> 상태(신규 등록/생성)는 프론트 세션에서만 유지되며 새로고침 시 초기화됩니다.
