# Estrutura de uma empresa

Cada empresa é um arquivo `data/<slug>.json` (por exemplo `data/viva3.json`) e uma linha em `companies.json`. A página `index.html` não tem número nenhum escrito nela: tudo vem desses arquivos. Para abrir uma empresa, use `index.html#<slug>`.

## companies.json

Lista usada pela busca da página.

```json
[{ "ticker": "VIVA3", "slug": "viva3", "name": "Vivara Participações", "sector": "Varejo de joias e acessórios", "asof": "2026-11-19" }]
```

## data/<slug>.json

| Bloco | Conteúdo |
|---|---|
| `meta` | ticker, nome, setor, `price` (número), `price_date`, `asof`, `valuation_model`, aviso legal |
| `hero` | `headline` (3 partes; a do meio vira itálico verde), `lede`, `stats` (4 números: 2 à esquerda, 2 à direita), `strip` (frases da faixa), `events` (4 cartões) |
| `margins` | linhas `{label, value}` em % |
| `quarters` | `labels`, `revenue`, `ebitda` (use `null` para trimestre sem dado, aparece como "n/d"), `highlight` (índice do trimestre em destaque) |
| `compare` | comparação entre dois períodos: `a`, `b`, linhas `{label, a, b, unit}` (`unit: "%"` mostra diferença em p.p.) |
| `price_points` | pontos datados de cotação (`date` em AAAA-MM-DD), `low52`, `high52` |
| `indicators` | tabela de múltiplos; `tip` opcional aparece ao passar o mouse (fonte ou cálculo) |
| `dcf` | `base_revenue`, `net_debt`, `shares`, `fixed`, `presets` (bear, base, bull), `sliders`, `sens` |
| `targets` | preços-alvo de analistas com quem e quando |
| `macro` | `tiles`, `bullets`, `selic` (trajetória esperada) |
| `commodity` | título e barras de uma commodity relevante (ouro para a Vivara) |
| `thesis` | `pros`, `cons`, `guidance`, `watch` |
| `timeline`, `competitive`, `sources` | texto livre |

## Regras de qualidade

- Todo número vem com fonte e data (campo `tip`, `sources` ou rótulo). Se não houver valor confirmado, use `null` em vez de estimar.
- Textos são exibidos como texto puro (sem HTML).
- Se `dcf` não existir, a página esconde a seção de valuation. Isso permite empresas em que DCF não faz sentido (bancos, por exemplo) usarem outro modelo no futuro.
- O modelo de DCF é o mesmo para todas as empresas; só os parâmetros mudam. O resultado é uma faixa ilustrativa, não preço-alvo.
