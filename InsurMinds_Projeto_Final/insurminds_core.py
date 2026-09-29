from __future__ import annotations

import base64
import json
import os
import re
import sqlite3
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None
try:
    from PIL import Image
    import pytesseract
except Exception:
    Image = None
    pytesseract = None

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "insurminds.db"
SAMPLE_DIR = BASE_DIR / "sample_data"

SCHEMA = {
    "type": "object",
    "properties": {
        "policy_name": {"type": "string"}, "insurer": {"type": "string"},
        "insured": {"type": "string"}, "policy_period": {"type": "string"},
        "limit": {"type": "string"}, "retention": {"type": "string"},
        "coverages": {"type": "array", "items": {"type": "string"}},
        "exclusions": {"type": "array", "items": {"type": "string"}},
        "alerts": {"type": "array", "items": {"type": "string"}},
        "confidence": {"type": "number"}, "method": {"type": "string"}
    },
    "required": ["policy_name", "insurer", "insured", "policy_period", "limit", "retention", "coverages", "exclusions", "alerts", "confidence", "method"],
    "additionalProperties": False
}


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as con:
        con.execute("CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, filename TEXT, media_type TEXT, extracted_text TEXT, analysis_json TEXT, created_at TEXT)")
        con.execute("CREATE TABLE IF NOT EXISTS comparisons (id INTEGER PRIMARY KEY, policy_ids TEXT, result_json TEXT, created_at TEXT)")


def extract_text(file_bytes: bytes, filename: str) -> tuple[str, str]:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf" and fitz:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc).strip()
        if text:
            return text, "PDF text layer (PyMuPDF)"
    if suffix in {".png", ".jpg", ".jpeg", ".tiff", ".bmp"} and Image and pytesseract:
        try:
            text = pytesseract.image_to_string(Image.open(__import__('io').BytesIO(file_bytes)), lang="por+eng").strip()
            if text:
                return text, "OCR Tesseract"
        except Exception:
            pass
    return file_bytes.decode("utf-8", errors="ignore").strip(), "Texto direto/fallback"


def money_to_float(value: str) -> float:
    raw = re.sub(r"[^0-9,.-]", "", value or "").replace(".", "").replace(",", ".")
    try:
        return float(raw)
    except ValueError:
        return 0.0


def first(pattern: str, text: str, default: str = "Não identificado") -> str:
    m = re.search(pattern, text, re.I | re.M)
    return m.group(1).strip() if m else default


def deterministic_extract(text: str, filename: str, method: str) -> dict[str, Any]:
    normalized = re.sub(r"\s+", " ", text).strip()
    coverages = []
    for item in ["Responsabilidade Civil de Administradores", "Custos de Defesa", "Investigações Regulatórias", "Crise e Comunicação"]:
        if item.lower() in normalized.lower():
            coverages.append(item)
    exclusions = []
    for item in ["fraude", "ato doloso", "poluição", "lesão corporal", "danos materiais", "conflito de interesses"]:
        if item.lower() in normalized.lower():
            exclusions.append(item.title())
    limit = first(r"(?:limite agregado|limite máximo|limite da apólice)\s*[:\-]?\s*(R\$\s*[\d\.\,]+)", normalized)
    retention = first(r"(?:franquia|retenção)\s*[:\-]?\s*(R\$\s*[\d\.\,]+)", normalized)
    period = first(r"(?:vigência|período de vigência)\s*[:\-]?\s*([^.;]+)", normalized)
    insurer = first(r"(?:seguradora|insurer)\s*[:\-]?\s*([^.;]+)", normalized)
    insured = first(r"(?:segurado|tomador|insured)\s*[:\-]?\s*([^.;]+)", normalized)
    policy_name = first(r"(?:apólice|policy)\s*[:\-]?\s*([^.;]+)", normalized, Path(filename).stem.replace("_", " ").title())
    alerts = []
    if not coverages: alerts.append("Coberturas não identificadas automaticamente")
    if not exclusions: alerts.append("Exclusões não identificadas automaticamente")
    if money_to_float(retention) > 500000: alerts.append("Retenção elevada em relação ao limite")
    if "retroativa" in normalized.lower(): alerts.append("Verificar data de retroatividade")
    return {"policy_name": policy_name, "insurer": insurer, "insured": insured, "policy_period": period,
            "limit": limit, "retention": retention, "coverages": coverages, "exclusions": exclusions,
            "alerts": alerts, "confidence": 0.82 if coverages and exclusions else 0.64, "method": method + " + regras auditáveis"}


def llm_extract(text: str, filename: str, method: str) -> dict[str, Any] | None:
    key = os.getenv("OPENAI_API_KEY")
    base = os.getenv("OPENAI_API_BASE")
    if not key or not base:
        return None
    try:
        import requests
        payload = {"model": os.getenv("INSURMINDS_MODEL", "gpt-5-mini"), "messages": [
            {"role": "system", "content": "Você é um analista de seguros D&O. Retorne exclusivamente JSON conforme o schema solicitado. Não invente campos: use 'Não identificado' quando não houver evidência."},
            {"role": "user", "content": f"Extraia a apólice {filename} e retorne JSON com estes campos: policy_name, insurer, insured, policy_period, limit, retention, coverages (array), exclusions (array), alerts (array), confidence (number), method. Texto:\n{text[:30000]}"}
        ], "response_format": {"type": "json_schema", "json_schema": {"name": "do_policy", "strict": True, "schema": SCHEMA}}}
        r = requests.post(base.rstrip("/") + "/chat/completions", headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json=payload, timeout=45)
        r.raise_for_status()
        data = r.json()
        result = json.loads(data["choices"][0]["message"]["content"])
        result["method"] = "IA Generativa + " + method
        return result
    except Exception:
        return None


def analyze_document(file_bytes: bytes, filename: str, media_type: str = "") -> dict[str, Any]:
    text, method = extract_text(file_bytes, filename)
    result = llm_extract(text, filename, method) or deterministic_extract(text, filename, method)
    with sqlite3.connect(DB_PATH) as con:
        cur = con.execute("INSERT INTO documents(filename, media_type, extracted_text, analysis_json, created_at) VALUES(?,?,?,?,?)", (filename, media_type, text, json.dumps(result, ensure_ascii=False), datetime.utcnow().isoformat()))
        result["document_id"] = cur.lastrowid
    return {"analysis": result, "text": text, "extractor": method}


def compare_policies(policies: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for p in policies:
        rows.append({"policy_name": p.get("policy_name"), "insurer": p.get("insurer"), "limit": p.get("limit"), "retention": p.get("retention"), "period": p.get("policy_period"), "coverages": len(p.get("coverages", [])), "exclusions": len(p.get("exclusions", [])), "alerts": len(p.get("alerts", [])), "coverage_items": p.get("coverages", []), "exclusion_items": p.get("exclusions", [])})
    differences = []
    if len(rows) >= 2:
        a, b = rows[0], rows[1]
        if money_to_float(a["limit"]) != money_to_float(b["limit"]): differences.append({"field": "Limite", "a": a["limit"], "b": b["limit"], "impact": "Maior limite tende a ampliar a capacidade de proteção, sujeito às condições."})
        if money_to_float(a["retention"]) != money_to_float(b["retention"]): differences.append({"field": "Franquia / retenção", "a": a["retention"], "b": b["retention"], "impact": "Retenção menor reduz desembolso inicial do segurado."})
        coverage_only_a = sorted(set(a["coverage_items"]) - set(b["coverage_items"]))
        coverage_only_b = sorted(set(b["coverage_items"]) - set(a["coverage_items"]))
        if coverage_only_a or coverage_only_b: differences.append({"field": "Coberturas divergentes", "a": coverage_only_a or ["Nenhuma exclusiva"], "b": coverage_only_b or ["Nenhuma exclusiva"], "impact": "Verificar lacunas de cobertura e diferenças de escopo."})
        exclusion_only_a = sorted(set(a["exclusion_items"]) - set(b["exclusion_items"]))
        exclusion_only_b = sorted(set(b["exclusion_items"]) - set(a["exclusion_items"]))
        if exclusion_only_a or exclusion_only_b: differences.append({"field": "Exclusões divergentes", "a": exclusion_only_a or ["Nenhuma exclusiva"], "b": exclusion_only_b or ["Nenhuma exclusiva"], "impact": "Mais exclusões ou exclusões específicas podem significar proteção mais restritiva."})
        if a["alerts"] != b["alerts"]: differences.append({"field": "Alertas", "a": a["alerts"], "b": b["alerts"], "impact": "Priorizar leitura humana dos pontos sinalizados."})
    score = []
    for p in policies:
        score.append({"policy_name": p.get("policy_name"), "score": max(0, min(100, round(60 + len(p.get("coverages", []))*8 - len(p.get("exclusions", []))*4 - len(p.get("alerts", []))*7)))})
    result = {"rows": rows, "differences": differences, "recommendation": "A comparação é um apoio à análise e não substitui a leitura jurídica da apólice.", "scores": score}
    with sqlite3.connect(DB_PATH) as con:
        con.execute("INSERT INTO comparisons(policy_ids, result_json, created_at) VALUES(?,?,?)", (json.dumps([p.get("document_id") for p in policies]), json.dumps(result, ensure_ascii=False), datetime.utcnow().isoformat()))
    return result


def sample_documents() -> list[dict[str, Any]]:
    return [{"filename": "Apolice_Norte_2026.pdf", "path": str(SAMPLE_DIR / "Apolice_Norte_2026.pdf")}, {"filename": "Apolice_Sul_2026.pdf", "path": str(SAMPLE_DIR / "Apolice_Sul_2026.pdf")}]

init_db()
