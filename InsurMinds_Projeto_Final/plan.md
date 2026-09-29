# Plano técnico — InsurMinds

## Objetivo
Construir um MVP didático, reproduzível e demonstrável para ingestão, extração, estruturação e comparação de apólices D&O.

## Arquitetura
- **Interface web**: HTML/CSS/JavaScript servido por Flask, em português e responsivo.
- **API**: endpoints para saúde, upload/análise e comparação.
- **Agentes lógicos**: recepção/validação, extração PDF/OCR, estruturação, análise por LLM/fallback e comparação.
- **Persistência**: SQLite local para documentos, análises e comparações.
- **IA Generativa**: endpoint OpenAI-compatible via `OPENAI_API_BASE` e `OPENAI_API_KEY`, com saída JSON; sem credenciais, usa fallback heurístico explicitamente identificado.
- **Publicação**: aplicação containerizada/servida por um único processo; conteúdo dinâmico e API no mesmo origin para simplificar o MVP.

## Rotas
`/`, `/api/health`, `/api/analyze`, `/api/compare`, `/api/sample-policies`, `/manus-routes.json`.

## Cache e privacidade
Respostas de análise e comparação são privadas e não devem ser compartilhadas em cache; arquivos enviados ficam no diretório temporário e os resultados persistem apenas como metadados estruturados no SQLite.

## Critérios de aceitação
A solução aceita PDF e imagens, extrai texto automaticamente, estrutura dados, compara duas apólices, destaca diferenças, utiliza IA Generativa quando configurada e funciona de forma demonstrável sem serviço externo.

## Autoria
Curié Edge — autoria integral do projeto, documentação e artefatos.
