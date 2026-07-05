import sys
sys.path.insert(0, ".")
from app import app, PAGES

FAIL = []
with app.test_client() as c:
    for p in PAGES:
        r = c.get(f"/{p['slug']}")
        if r.status_code != 200:
            FAIL.append(f"/{p['slug']} -> {r.status_code}")
    if c.get("/").status_code not in (301, 302):
        FAIL.append("/ redirect missing")
    for path in ["/api/dashboard/stats", "/api/templates",
                 "/api/jobs", "/api/results", "/api/settings", "/api/meta"]:
        r = c.get(path)
        if r.status_code != 200:
            FAIL.append(f"{path} -> {r.status_code}")
    # 신규: 템플릿 상세
    if c.get("/api/templates/1").status_code != 200:
        FAIL.append("/api/templates/1 -> not 200")
    if c.get("/api/templates/999999").status_code != 404:
        FAIL.append("/api/templates/<bad> not 404")
    # 신규: 카테고리/항목 추가 (더미 201)
    if c.post("/api/templates/1/categories", json={"name": "x", "type": "prompt"}).status_code != 201:
        FAIL.append("POST categories not 201")
    if c.post("/api/templates/1/categories/11/items", json={"name": "x", "prompt": "y"}).status_code != 201:
        FAIL.append("POST items not 201")
    # 제거 확인: 에셋 페이지/API 404
    if c.get("/assets").status_code != 404:
        FAIL.append("/assets page should be 404")
    if c.get("/api/assets").status_code != 404:
        FAIL.append("/api/assets should be 404")
    # 404 핸들러
    if c.get("/nonexistent").status_code != 404:
        FAIL.append("404 handler missing")

if FAIL:
    print("SMOKE FAIL:", *FAIL, sep="\n  ")
    sys.exit(1)
print("SMOKE OK: all routes green")
