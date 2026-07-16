# -*- coding: utf-8 -*-
"""Срез Search Console: позиции/клики/показы по запросам и страницам.

Использует REFRESH_TOKEN_FULL (scope webmasters) из .secrets/google-oauth-full.env.
Запуск: python gsc_snapshot.py [days=7]
"""
import io
import json
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SECRETS = Path(__file__).resolve().parents[2] / ".secrets"


def load_env(name):
    env = {}
    for line in (SECRETS / name).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env


ads = load_env("google-ads.env")
full = load_env("google-oauth-full.env")

data = urllib.parse.urlencode({
    "client_id": ads["CLIENT_ID"], "client_secret": ads["CLIENT_SECRET"],
    "refresh_token": full["REFRESH_TOKEN_FULL"], "grant_type": "refresh_token",
}).encode()
tok = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data))
HDR = {"Authorization": f"Bearer {tok['access_token']}", "Content-Type": "application/json"}


def api(url, body=None):
    req = urllib.request.Request(url, headers=HDR,
                                 data=json.dumps(body).encode() if body else None)
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, url)
        print(e.read().decode()[:800])
        sys.exit(1)


sites = api("https://www.googleapis.com/webmasters/v3/sites")
print("== PROPERTIES доступные роботу ==")
for s in sites.get("siteEntry", []):
    print(f"  {s['siteUrl']}  ({s['permissionLevel']})")

site = next((s["siteUrl"] for s in sites.get("siteEntry", [])
             if "nonamelounge" in s["siteUrl"]), None)
if not site:
    print("nonamelounge.ro среди property не найден — робот не добавлен в GSC?")
    sys.exit(1)

days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
end = date.today() - timedelta(days=2)   # GSC отстаёт ~на 2 дня
start = end - timedelta(days=days - 1)
base = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(site, safe='')}/searchAnalytics/query"
print(f"\n== {site}  {start} .. {end} ==")

for dim, label, limit in (("query", "ЗАПРОСЫ", 25), ("page", "СТРАНИЦЫ", 25)):
    r = api(base, {
        "startDate": str(start), "endDate": str(end),
        "dimensions": [dim], "rowLimit": limit,
    })
    rows = r.get("rows", [])
    print(f"\n-- ТОП {label} (по кликам, потом показам) --")
    if not rows:
        print("  (пусто — данных за период нет)")
    for row in rows:
        k = row["keys"][0]
        if dim == "page":
            k = k.replace("https://nonamelounge.ro", "")
        print(f"  clicks={row['clicks']:<4} impr={row['impressions']:<6} "
              f"pos={row['position']:<5.1f} ctr={row['ctr'] * 100:4.1f}%  {k}")

tot = api(base, {"startDate": str(start), "endDate": str(end), "dimensions": []})
for row in tot.get("rows", []):
    print(f"\nИТОГО за {days} дн: clicks={row['clicks']} impr={row['impressions']} "
          f"средняя позиция={row['position']:.1f}")
