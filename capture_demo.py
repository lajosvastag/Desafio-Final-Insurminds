from pathlib import Path
import subprocess, time
from playwright.sync_api import sync_playwright

root = Path('/home/ubuntu/InsurMinds_Entrega')
app_dir = root / 'InsurMinds_Projeto_Final'
out = app_dir / 'Projeto_Final_Artefatos' / 'demo_captures'
out.mkdir(parents=True, exist_ok=True)
venv = '/tmp/insurminds-final-venv/bin/python'
proc = subprocess.Popen([venv, 'app.py'], cwd=app_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    time.sleep(2)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1280, 'height': 900}, device_scale_factor=1)
        page.goto('http://127.0.0.1:3000/', wait_until='networkidle')
        page.screenshot(path=str(out / '01_interface_inicial.png'), full_page=True)
        page.get_by_role('button', name='Carregar as 2 amostras').click()
        page.wait_for_timeout(3000)
        page.screenshot(path=str(out / '02_documentos_processados.png'), full_page=True)
        page.get_by_role('button', name='Comparar apólices').click()
        page.wait_for_timeout(700)
        page.screenshot(path=str(out / '03_comparacao_clausulas.png'), full_page=True)
        browser.close()
finally:
    proc.terminate()
    try: proc.wait(timeout=5)
    except subprocess.TimeoutExpired: proc.kill()
print('capturas:', *sorted(str(p) for p in out.glob('*.png')), sep='\n')
