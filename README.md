# Investe Simples

Site estático de análise de empresas da B3. Não tem servidor nem banco de dados: o `index.html` lê `companies.json` e `data/<empresa>.json`.

## Como publicar (GitHub Pages, grátis)

1. Crie uma conta em github.com e um repositório **público** (ex.: `investesimples`).
2. Envie todos os arquivos desta pasta para o repositório (botão *Add file > Upload files*; inclua as pastas `data`, `scripts` e `.github`).
3. Em *Settings > Pages*, escolha *Deploy from a branch*, branch `main`, pasta `/ (root)`. Em ~1 minuto o site abre em `https://SEU-USUARIO.github.io/investesimples/`.
4. Esse é o link para colocar na bio do Instagram.

## Atualização diária das cotações

1. Crie uma conta em brapi.dev e copie seu token.
2. No repositório: *Settings > Secrets and variables > Actions > New repository secret*. Nome: `BRAPI_TOKEN`; valor: o token.
3. Aba *Actions > Atualizar cotações > Run workflow* para testar uma vez. Se ficar verde, o `data/*.json` terá cotações novas.
4. A partir daí roda sozinho às 19h (Brasília), de segunda a sexta. Se falhar, o GitHub avisa por e-mail e o site continua com a última cotação boa.

O script só atualiza cotação, data e gráfico de preço. Resultados trimestrais, teses e premissas continuam sendo revisados à mão, uma vez por temporada de balanços.

## Adicionar uma empresa

Veja `SCHEMA.md`.

## Aviso

Conteúdo educacional. Não é recomendação de investimento.
