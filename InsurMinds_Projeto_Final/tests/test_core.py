import json
from pathlib import Path
from insurminds_core import deterministic_extract, compare_policies, extract_text

APP_DIR = Path(__file__).resolve().parents[1]

def test_extract_pdf_sample():
    data = (APP_DIR / 'sample_data' / 'Apolice_Norte_2026.pdf').read_bytes()
    text, method = extract_text(data, 'Apolice_Norte_2026.pdf')
    assert 'LIMITE' in text
    assert 'PyMuPDF' in method or 'fallback' in method

def test_structure_and_compare():
    a = deterministic_extract('APÓLICE: A; SEGURADORA: X; LIMITE AGREGADO: R$ 10.000.000,00; FRANQUIA: R$ 250.000,00; COBERTURAS: Custos de Defesa; EXCLUSÕES: Fraude;', 'a.pdf', 'teste')
    b = deterministic_extract('APÓLICE: B; SEGURADORA: Y; LIMITE AGREGADO: R$ 15.000.000,00; FRANQUIA: R$ 500.000,00; COBERTURAS: Custos de Defesa; EXCLUSÕES: Fraude; Poluição;', 'b.pdf', 'teste')
    result = compare_policies([a,b])
    assert len(result['differences']) >= 2
    assert result['rows'][0]['limit'] != result['rows'][1]['limit']
    fields = {item['field'] for item in result['differences']}
    assert 'Exclusões divergentes' in fields
