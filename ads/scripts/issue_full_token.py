# -*- coding: utf-8 -*-
"""Выпуск refresh token со ВСЕМИ нужными scope одним согласием робота.

Loopback-флоу: скрипт поднимает локальный сервер, печатает URL — владелец
открывает его в браузере, где залогинен noname.seo.bot@gmail.com, жмёт
Allow. Токен пишется в .secrets/google-oauth-full.env. Старый Ads-токен
остаётся рабочим (Google держит до 50 живых refresh token на клиента).
"""
import io
import json
import sys
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SECRETS = Path(__file__).resolve().parents[2] / ".secrets"
env = {}
for line in (SECRETS / "google-ads.env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip()

PORT = 8766
REDIRECT = f"http://localhost:{PORT}"
SCOPES = " ".join([
    "https://www.googleapis.com/auth/adwords",          # Google Ads (как было)
    "https://www.googleapis.com/auth/webmasters",       # Search Console (+sitemaps)
    "https://www.googleapis.com/auth/analytics.readonly",  # GA4 Data API
    "https://www.googleapis.com/auth/business.manage",  # GBP (на будущее, кейс подан)
])

auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": env["CLIENT_ID"],
    "redirect_uri": REDIRECT,
    "response_type": "code",
    "scope": SCOPES,
    "access_type": "offline",
    "prompt": "consent",           # иначе refresh_token не вернётся повторно
    "login_hint": "noname.seo.bot@gmail.com",
})
print("=== ОТКРОЙ ЭТОТ URL В БРАУЗЕРЕ (аккаунт noname.seo.bot@gmail.com) ===")
print(auth_url)
print("=== жду код на", REDIRECT, "===", flush=True)

code_holder = {}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        if "code" in qs:
            code_holder["code"] = qs["code"][0]
            self.wfile.write("<h2>Готово — токен получаю, окно можно закрыть.</h2>".encode())
        else:
            self.wfile.write(f"<h2>Ошибка: {qs}</h2>".encode())

    def log_message(self, *a):
        pass


srv = HTTPServer(("localhost", PORT), Handler)
while "code" not in code_holder:
    srv.handle_request()

data = urllib.parse.urlencode({
    "client_id": env["CLIENT_ID"],
    "client_secret": env["CLIENT_SECRET"],
    "code": code_holder["code"],
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT,
}).encode()
tok = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data))
assert "refresh_token" in tok, tok

out = SECRETS / "google-oauth-full.env"
out.write_text(
    "# Refresh token робота noname.seo.bot со scope: adwords, webmasters,\n"
    "# analytics.readonly, business.manage. Выпущен 2026-07-16 (issue_full_token.py).\n"
    f"REFRESH_TOKEN_FULL={tok['refresh_token']}\n"
    f"SCOPES={tok.get('scope','')}\n",
    encoding="utf-8",
)
print("OK: сохранено в", out)
print("scopes:", tok.get("scope"))
