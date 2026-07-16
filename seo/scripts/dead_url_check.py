# -*- coding: utf-8 -*-
"""Сторож мёртвых URL: всё, что Google реально показывает людям (GSC, 28 дней),
проверяется на живость. Любая цепочка, не кончающаяся на 200, — тревога.

Родился 2026-07-16: после переезда со старого WP ~5 из 13 недельных кликов
падали в 404 (/location/ на позиции 5.2!), потому что редиректов со старых URL
никто не поставил. Гонять ВМЕСТЕ с gsc_snapshot.py (еженедельно) и ОБЯЗАТЕЛЬНО
после любого переезда/переименования страниц.

Выход 0 = всё живое; выход 1 = есть мёртвые (список в stdout).
"""
import io
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SECRETS = Path(__file__).resolve().parents[2] / ".secrets"
SITE = "https://nonamelounge.ro/"


def load_env(name):
    env = {}
    for line in (SECRETS / name).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env


ads, full = load_env("google-ads.env"), load_env("google-oauth-full.env")
data = urllib.parse.urlencode({
    "client_id": ads["CLIENT_ID"], "client_secret": ads["CLIENT_SECRET"],
    "refresh_token": full["REFRESH_TOKEN_FULL"], "grant_type": "refresh_token",
}).encode()
tok = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data))

end = date.today() - timedelta(days=2)
start = end - timedelta(days=27)
base = ("https://www.googleapis.com/webmasters/v3/sites/"
        + urllib.parse.quote(SITE, safe="") + "/searchAnalytics/query")
req = urllib.request.Request(
    base,
    headers={"Authorization": f"Bearer {tok['access_token']}",
             "Content-Type": "application/json"},
    data=json.dumps({"startDate": str(start), "endDate": str(end),
                     "dimensions": ["page"], "rowLimit": 1000}).encode())
rows = json.load(urllib.request.urlopen(req)).get("rows", [])
print(f"GSC {start}..{end}: {len(rows)} страниц в выдаче — проверяю живость…")


def final_status(url):
    """HTTP-статус конца redirect-цепочки (кэш CF обходим кэш-бастером)."""
    u = url.split("#")[0] + ("&cb=1" if "?" in url else "?cb=1")
    for _ in range(6):
        req = urllib.request.Request(u, method="HEAD",
                                     headers={"User-Agent": "noname-seo-agent/1.0"})
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            return resp.status, url
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 307, 308):
                u = urllib.parse.urljoin(u, e.headers["Location"])
                u += ("&cb=1" if "?" in u else "?cb=1") if "cb=1" not in u else ""
                continue
            return e.code, u
        except Exception as e:  # noqa: BLE001 - сеть, отчитываемся как есть
            return f"ERR {e}", u
    return "LOOP", u


dead = []
for r in rows:
    page = r["keys"][0]
    status, where = final_status(page)
    if status != 200:
        dead.append((status, page, r["impressions"], where))

if not dead:
    print("OK: все страницы из выдачи заканчиваются на 200.")
    sys.exit(0)

print(f"\n⚠️ МЁРТВЫХ: {len(dead)} — нужен 301 на живой раздел (nginx snippets/noname-admin.conf):")
for status, page, impr, where in sorted(dead, key=lambda d: -d[2]):
    print(f"  [{status}] {impr} impr  {page.replace(SITE.rstrip('/'), '')}"
          + (f"  (обрыв на {where})" if where != page else ""))
sys.exit(1)
