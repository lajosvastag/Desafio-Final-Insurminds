from __future__ import annotations

import json
from pathlib import Path
from flask import Flask, jsonify, render_template, request, send_from_directory
from insurminds_core import analyze_document, compare_policies, sample_documents, init_db

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024
BASE_DIR = Path(__file__).parent

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/manus-routes.json")
def routes():
    return send_from_directory(BASE_DIR, "manus-routes.json", mimetype="application/json")

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "InsurMinds", "author": "Curié Edge"})

@app.get("/api/sample-policies")
def samples():
    return jsonify(sample_documents())

@app.post("/api/analyze")
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "Envie um arquivo no campo 'file'."}), 400
    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "O arquivo não possui nome."}), 400
    allowed = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".txt"}
    if Path(file.filename).suffix.lower() not in allowed:
        return jsonify({"error": "Formato não suportado. Use PDF ou imagem."}), 415
    try:
        result = analyze_document(file.read(), file.filename, file.mimetype or "")
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": f"Falha controlada no processamento: {exc}"}), 422

@app.post("/api/analyze-sample")
def analyze_sample():
    name = request.json.get("filename") if request.is_json else ""
    item = next((x for x in sample_documents() if x["filename"] == name), None)
    if not item or not Path(item["path"]).exists():
        return jsonify({"error": "Amostra não encontrada."}), 404
    return jsonify(analyze_document(Path(item["path"]).read_bytes(), item["filename"], "application/pdf"))

@app.post("/api/compare")
def compare():
    payload = request.get_json(silent=True) or {}
    policies = payload.get("policies", [])
    if len(policies) < 2:
        return jsonify({"error": "Selecione pelo menos duas apólices para comparar."}), 400
    return jsonify(compare_policies(policies))

@app.errorhandler(413)
def too_large(_):
    return jsonify({"error": "Arquivo excede o limite de 12 MB."}), 413

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=3000, debug=False)
