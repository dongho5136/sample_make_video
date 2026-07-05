from flask import Flask, render_template, redirect, jsonify, request
from data import dummy

app = Flask(__name__)

PAGES = [
    {"slug": "dashboard", "label": "대시보드", "icon": "📊"},
    {"slug": "generate", "label": "광고 생성", "icon": "🎬"},
    {"slug": "templates", "label": "템플릿 관리", "icon": "🧩"},
    {"slug": "jobs", "label": "생성 작업 목록", "icon": "⏳"},
    {"slug": "results", "label": "생성 결과 관리", "icon": "✅"},
    {"slug": "settings", "label": "설정", "icon": "⚙️"},
]
_LABELS = {p["slug"]: p["label"] for p in PAGES}


def render_page(slug):
    return render_template(f"{slug}.html", pages=PAGES,
                           active=slug, title=_LABELS[slug])


@app.route("/")
def index():
    return redirect("/dashboard")


@app.route("/<slug>")
def page(slug):
    if slug not in _LABELS:
        return render_template("404.html", pages=PAGES, active="", title="404"), 404
    return render_page(slug)


@app.route("/api/dashboard/stats")
def api_stats():
    return jsonify(dummy.get_stats())


@app.route("/api/templates", methods=["GET", "POST"])
def api_templates():
    if request.method == "POST":
        return jsonify({"ok": True, "item": request.get_json()}), 201
    return jsonify(dummy.TEMPLATES)


@app.route("/api/templates/<int:tid>")
def api_template_detail(tid):
    for t in dummy.TEMPLATES:
        if t["id"] == tid:
            return jsonify(t)
    return jsonify({"error": "not found"}), 404


@app.route("/api/templates/<int:tid>/categories", methods=["POST"])
def api_add_category(tid):
    return jsonify({"ok": True, "item": request.get_json()}), 201


@app.route("/api/templates/<int:tid>/categories/<int:cid>/items", methods=["POST"])
def api_add_item(tid, cid):
    return jsonify({"ok": True, "item": request.get_json()}), 201


@app.route("/api/jobs", methods=["GET", "POST"])
def api_jobs():
    if request.method == "POST":
        return jsonify({"ok": True, "item": request.get_json()}), 201
    return jsonify(dummy.JOBS)


@app.route("/api/results")
def api_results():
    return jsonify(dummy.RESULTS)


@app.route("/api/settings")
def api_settings():
    return jsonify(dummy.SETTINGS)


@app.route("/api/meta")
def api_meta():
    return jsonify({"models": dummy.MODELS, "ratios": dummy.RATIOS,
                    "scenario": dummy.SEGMENT_SCENARIO})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
