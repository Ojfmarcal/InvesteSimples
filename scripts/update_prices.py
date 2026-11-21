#!/usr/bin/env python3
"""Atualiza cotação, data e série de preços de cada empresa usando a API da Brapi.

Uso local:   BRAPI_TOKEN=seu_token python3 scripts/update_prices.py
No GitHub:   roda sozinho pelo workflow .github/workflows/update-prices.yml

Só mexe em: meta.price, meta.price_date, meta.asof, meta.price_source e price_points.
Não toca em tese, resultados, indicadores nem premissas.
Se a Brapi falhar para um papel, o valor antigo é mantido e o erro é mostrado.
"""
import json, os, sys, time, glob, datetime, urllib.request, urllib.parse

TOKEN = os.environ.get('BRAPI_TOKEN', '')
BASE = 'https://brapi.dev/api/quote/'
MES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

def fetch(ticker):
    q = {'range': '1y', 'interval': '1mo'}
    if TOKEN:
        q['token'] = TOKEN
    url = BASE + urllib.parse.quote(ticker) + '?' + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={'User-Agent': 'investe-simples/1.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    res = data.get('results') or []
    if not res:
        raise ValueError('resposta sem resultados')
    return res[0]

def to_date(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return datetime.datetime.fromtimestamp(v, datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=-3)))
    return datetime.datetime.fromisoformat(str(v).replace('Z', '+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=-3)))

def update(path):
    d = json.load(open(path, encoding='utf-8'))
    tk = d['meta']['ticker']
    r = fetch(tk)
    price = r.get('regularMarketPrice')
    if not price or price <= 0:
        raise ValueError('preço inválido: %r' % price)
    when = to_date(r.get('regularMarketTime')) or datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
    d['meta']['price'] = round(float(price), 2)
    d['meta']['price_date'] = when.strftime('%d/%m/%Y')
    d['meta']['price_source'] = 'Brapi'
    d['meta']['asof'] = when.strftime('%d/%m/%Y')
    hist = r.get('historicalDataPrice') or []
    pts = []
    for h in hist:
        c, t = h.get('close'), to_date(h.get('date'))
        if c and t:
            pts.append({'date': t.strftime('%Y-%m-%d'), 'value': round(float(c), 2), 'label': '%s/%s' % (MES[t.month - 1], str(t.year)[2:])})
    pts.sort(key=lambda p: p['date'])
    if len(pts) >= 4:
        # o último ponto passa a ser a cotação atual
        pts = [p for p in pts if p['date'] < when.strftime('%Y-%m-01')]
        pts.append({'date': when.strftime('%Y-%m-%d'), 'value': d['meta']['price'], 'label': when.strftime('%d/%m')})
        vals = [p['value'] for p in pts]
        lo = r.get('fiftyTwoWeekLow')
        hi = r.get('fiftyTwoWeekHigh')
        d['price_points'] = {
            'sub': 'fechamento mensal de 12 meses e cotação atual · Brapi',
            'points': pts,
            'low52': round(float(lo), 2) if lo else min(vals),
            'high52': round(float(hi), 2) if hi else max(vals),
        }
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return tk, d['meta']['price'], len(pts)

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = sorted(glob.glob(os.path.join(root, 'data', '*.json')))
    ok = bad = 0
    for f in files:
        try:
            tk, price, n = update(f)
            print('ok  %-7s R$ %.2f  (%d pontos)' % (tk, price, n))
            ok += 1
        except Exception as e:
            print('ERRO %s: %s' % (os.path.basename(f), e), file=sys.stderr)
            bad += 1
        time.sleep(1.2)  # respeita o limite de requisições do plano gratuito
    if ok:
        cj = os.path.join(root, 'companies.json')
        c = json.load(open(cj, encoding='utf-8'))
        today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).strftime('%Y-%m-%d')
        for x in c:
            x['asof'] = today
        json.dump(c, open(cj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('%d atualizados, %d com erro' % (ok, bad))
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
