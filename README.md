# InsurMinds — Análise Inteligente de Apólices D&O

**Projeto Final | Autoria:** Luís Brito Vastag e Elizângela de Macêdo Brito — Curié Edge

## Visão geral

O InsurMinds é um MVP acadêmico para uma primeira leitura comparativa de apólices de seguro Directors & Officers (D&O). A plataforma recebe PDFs ou imagens, extrai o conteúdo, identifica campos relevantes, organiza os dados em JSON, persiste o processamento em SQLite e compara duas ou mais apólices, apresentando diferenças de valores e cláusulas identificadas.

O sistema combina **IA Generativa opcional** via endpoint OpenAI-compatible com um **fallback determinístico auditável**, permitindo a demonstração mesmo sem credenciais externas.

## Funcionalidades

- Recebimento de PDFs e imagens (`.pdf`, `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`).
- Extração de texto de PDFs com camada textual via PyMuPDF.
- OCR Tesseract para imagens quando o executável estiver instalado.
- Estruturação de seguradora, segurado, vigência, limite, retenção, coberturas, exclusões e alertas.
- IA Generativa com saída JSON Schema quando configurada.
- Fallback reproduzível baseado em regras e expressões regulares.
- Comparação de pelo menos duas apólices com diferenças de limite, retenção, coberturas e exclusões específicas.
- Persistência local em SQLite.
- Interface web em português e dados sintéticos para demonstração.

## Instalação e execução local

Requer Python 3.11+.

```bash
git clone https://github.com/lajosvastag/Desafio-Final---Insurminds.git
cd Desafio-Final---Insurminds
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python InsurMinds_Projeto_Final/app.py
```

Abra <http://localhost:3000>.

Para executar os testes:

```bash
pip install -r requirements-dev.txt
pytest -q InsurMinds_Projeto_Final/tests
```

Para OCR de imagens, instale também o Tesseract no sistema. PDFs escaneados sem camada textual devem ser convertidos em imagem antes do upload nesta versão do MVP.

## Execução com Docker

A partir da raiz do repositório:

```bash
docker build -f InsurMinds_Projeto_Final/Dockerfile -t insurminds .
docker run --rm -p 3000:3000 insurminds
```

## IA Generativa

Sem configuração adicional, a aplicação usa o fallback determinístico e informa o método na interface. Para ativar a extração por IA, configure:

```bash
export OPENAI_API_KEY="sua-chave"
export OPENAI_API_BASE="https://seu-endpoint/v1"
export INSURMINDS_MODEL="gpt-5-mini"
```

As credenciais não são armazenadas no código nem nos artefatos. O modelo deve devolver JSON compatível com o schema documentado em `InsurMinds_Projeto_Final/insurminds_core.py`.

## Demonstração

1. Execute a aplicação.
2. Abra <http://localhost:3000>.
3. Clique em **Carregar as 2 amostras**.
4. Confira a leitura estruturada das duas apólices.
5. Clique em **Comparar apólices**.
6. Observe as diferenças de limite, retenção, coberturas e exclusões específicas.

Os documentos em `InsurMinds_Projeto_Final/sample_data/` são sintéticos e foram criados exclusivamente para a demonstração acadêmica.

## Arquitetura

`InsurMinds_Projeto_Final/app.py` expõe a interface e a API. `insurminds_core.py` concentra a recepção, extração, estruturação, persistência e comparação. O fluxo usa PyMuPDF/OCR, IA ou regras, SQLite e JSON estruturado. `templates/index.html` implementa a experiência web.

## Artefatos

Os materiais de entrega ficam em `InsurMinds_Projeto_Final/Projeto_Final_Artefatos/`:

- `InsurMinds_Relatorio_Tecnico.pdf` — relatório técnico.
- `InsurMinds_Projeto_Final.pdf` — versão PDF do pitch deck.
- `pitch_deck_html/` — fonte editável do pitch deck em HTML.
- `InsurMinds_Projeto_Final.mp4` — vídeo demonstrativo.
- `Apolice_Norte_2026.pdf` e `Apolice_Sul_2026.pdf` — dados sintéticos.

O arquivo ZIP completo da entrega é gerado como `InsurMinds_Projeto_Final.zip` na raiz deste pacote.

## Limitações conhecidas

O MVP não substitui a leitura jurídica, não interpreta profundamente a semântica das cláusulas, não calcula preço ou probabilidade atuarial e não valida força legal. OCR depende do executável e idioma instalados. A análise por LLM depende de endpoint e credenciais configuradas. Os scores são indicativos e não constituem recomendação de compra.

## Autoria e integrantes

O projeto foi desenvolvido integralmente pela **Curié Edge**, responsável pela arquitetura, desenvolvimento, documentação, relatório técnico, pitch deck, vídeo e artefatos auxiliares.

**Integrantes:** Luís Brito Vastag e Elizângela de Macêdo Brito.

## Licença

MIT License. Consulte `LICENSE`.
