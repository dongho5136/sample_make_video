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
    for path in ["/api/dashboard/stats", "/api/templates", "/api/assets",
                 "/api/jobs", "/api/results", "/api/settings", "/api/meta"]:
        r = c.get(path)
        if r.status_code != 200:
            FAIL.append(f"{path} -> {r.status_code}")
    if c.get("/nonexistent").status_code != 404:
        FAIL.append("404 handler missing")

if FAIL:
    print("SMOKE FAIL:", *FAIL, sep="\n  ")
    sys.exit(1)
print("SMOKE OK: all routes green")
