# InsurMinds — Relatório Técnico

**Autoria:** Curié Edge  
**Data:** 2026  
**Natureza:** protótipo acadêmico / MVP

## 1. Resumo executivo

O InsurMinds reduz o trabalho manual de uma primeira leitura comparativa de apólices D&O. O usuário envia PDFs ou imagens, o sistema extrai o conteúdo, transforma sinais jurídicos em dados estruturados e apresenta diferenças entre apólices. A proposta prioriza transparência: o método de extração aparece na interface e existe um fallback determinístico para que a demonstração não dependa de uma API externa.

## 2. Arquitetura da solução

A solução é formada por uma interface web Flask, uma API de processamento, um módulo central de domínio e SQLite. O fluxo é: recepção e validação do arquivo; extração de camada de texto do PDF via PyMuPDF ou OCR Tesseract para imagens; identificação de entidades e cláusulas; estruturação em JSON; persistência do resultado; comparação de duas ou mais apólices; apresentação de diferenças e alertas.

```text
Usuário → Interface web → API Flask → Agente de recepção
                                  ↓
                    PDF/PyMuPDF ou imagem/OCR
                                  ↓
                 Agente de estruturação + IA/fallback
                                  ↓
                         SQLite + JSON estruturado
                                  ↓
                  Agente de comparação → diferenças
```

## 3. Agentes desenvolvidos

**Agente de recepção:** valida extensão, tamanho, nome e presença do arquivo. **Agente de extração:** escolhe PyMuPDF para PDFs com camada de texto e Tesseract para imagens. **Agente de estruturação:** identifica seguradora, segurado, vigência, limite, retenção, coberturas, exclusões e alertas. **Agente de análise:** usa saída JSON estruturada de um modelo OpenAI-compatible quando as variáveis de ambiente estão presentes; caso contrário usa regras auditáveis. **Agente de comparação:** cria tabela lado a lado, impactos textuais e score indicativo.

## 4. Uso de IA Generativa

A aplicação foi preparada para usar um modelo de IA Generativa com `response_format` JSON Schema. A instrução pede que o modelo não invente evidências e use “Não identificado” quando um campo não puder ser encontrado. O modelo configurável padrão é `gpt-5-mini`, adequado a extração estruturada. A chave não é persistida no repositório. O fallback mantém a solução funcional para aulas, banca e ambientes sem credenciais.

## 5. Modelo de dados

A tabela `documents` guarda nome, tipo MIME, texto extraído, JSON de análise e data. A tabela `comparisons` guarda os IDs comparados, o JSON de diferenças e data. A camada de apresentação consome apenas o JSON estruturado, mantendo separação entre domínio e interface.

## 6. Decisões técnicas

Flask foi escolhido por reduzir complexidade de infraestrutura e tornar o MVP fácil de executar. SQLite atende à persistência local pedida sem exigir banco externo. PDFs e imagens são tratados por bibliotecas amplamente conhecidas. A interface é HTML/CSS/JavaScript sem dependência de build, favorecendo demonstração rápida e portabilidade.

## 7. Resultados demonstráveis

Com as duas amostras sintéticas, o sistema identifica que a apólice Norte possui limite de R$ 10 milhões, retenção de R$ 250 mil, quatro coberturas e quatro exclusões; a apólice Sul possui limite de R$ 15 milhões, retenção de R$ 500 mil, três coberturas e seis exclusões. A interface destaca as diferenças e recomenda leitura humana dos pontos restritivos.

## 8. Limitações conhecidas

A extração por regras não interpreta semântica jurídica profunda. OCR varia conforme qualidade da imagem e idioma instalado. A IA pode cometer erros e exige revisão. Os documentos da demonstração são sintéticos, não dados reais de seguradoras. O score não é uma recomendação de compra e não substitui subscrição, compliance ou parecer jurídico.

## 9. Evolução futura

As próximas etapas seriam incorporar um catálogo de cláusulas com embeddings e busca semântica, permitir revisão humana com evidência por página, suportar tabelas e anexos, adicionar autenticação e armazenamento de objetos, versionar prompts e modelos, incluir avaliação com conjunto anotado e integrar controles de auditoria e exportação para PDF.

## 10. Fontes e transparência

Os arquivos em `sample_data/` são documentos sintéticos produzidos pela autoria Curié Edge para a demonstração. Não foram usados dados pessoais nem contratos reais. As bibliotecas utilizadas estão listadas em `requirements.txt`.
