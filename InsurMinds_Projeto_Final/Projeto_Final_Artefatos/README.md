# InsurMinds — Artefatos do Projeto Final

**Autoria integral:** Curié Edge  
**Integrantes:** Luís Brito Vastag e Elizângela de Macêdo Brito

Esta pasta reúne os artefatos auxiliares e os entregáveis do projeto acadêmico InsurMinds, uma plataforma inteligente para análise e comparação de apólices D&O.

## Conteúdo

- `InsurMinds_Relatorio_Tecnico.pdf` — relatório técnico.
- `InsurMinds_Projeto_Final.pdf` — versão PDF do pitch deck.
- `pitch_deck_html/` — fonte editável dos slides.
- `InsurMinds_Projeto_Final.mp4` — vídeo demonstrativo narrado, com duração inferior a cinco minutos.
- `Apolice_Norte_2026.pdf` e `Apolice_Sul_2026.pdf` — documentos sintéticos usados na demonstração.
- `video_frames/` — quadros explicativos usados no vídeo.
- `demo_captures/` — capturas reais da interface processando e comparando as apólices.
- `NOTA_ENTREGA.md` — resumo das correções e limitações de formato.
- `LICENSE` — licença MIT.

## Execução do projeto

A execução deve ser feita a partir da raiz do repositório:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python InsurMinds_Projeto_Final/app.py
```

Depois, abra `http://localhost:3000` e clique em **Carregar as 2 amostras**. Em seguida, clique em **Comparar apólices** para visualizar os limites, retenções, coberturas e exclusões divergentes.

## Autoria e licença

O projeto foi desenvolvido integralmente pela **Curié Edge**, incluindo arquitetura, código, documentação, relatório técnico, pitch deck, vídeo e artefatos auxiliares.

A licença é **MIT**. Consulte o arquivo `LICENSE` na raiz do repositório.
