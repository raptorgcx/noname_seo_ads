# -*- coding: utf-8 -*-
"""Смоук-тест Basic Access: доступность кабинета, валюта, конверсии, бюджеты."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient

SECRETS = Path(__file__).resolve().parents[2] / ".secrets" / "google-ads.yaml"
CUSTOMER_ID = "7997489829"

client = GoogleAdsClient.load_from_storage(str(SECRETS))
ga = client.get_service("GoogleAdsService")

q = """
  SELECT customer.descriptive_name, customer.currency_code, customer.time_zone
  FROM customer LIMIT 1"""
try:
    rows = list(ga.search(customer_id=CUSTOMER_ID, query=q))
except Exception as e:  # noqa: BLE001
    print("FAIL customer query:", e)
    sys.exit(1)
c = rows[0].customer
print(f"OK: {c.descriptive_name} | {c.currency_code} | {c.time_zone}")

for name, q2 in [
    ("campaigns", "SELECT campaign.id, campaign.name, campaign.status FROM campaign"),
    ("conversion_actions", "SELECT conversion_action.id, conversion_action.name, "
     "conversion_action.status, conversion_action.type FROM conversion_action "
     "WHERE conversion_action.status = 'ENABLED'"),
]:
    rows = list(ga.search(customer_id=CUSTOMER_ID, query=q2))
    print(f"{name}: {len(rows)}")
    for r in rows[:10]:
        if name == "campaigns":
            print("  -", r.campaign.id, r.campaign.name, r.campaign.status.name)
        else:
            ca = r.conversion_action
            print("  -", ca.id, ca.name, ca.type_.name, ca.status.name)
