# -*- coding: utf-8 -*-
"""Удалить бюджет-сироту; дамп tag_snippets конверсий как есть."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient

SECRETS = Path(__file__).resolve().parents[2] / ".secrets" / "google-ads.yaml"
CID = "7997489829"
client = GoogleAdsClient.load_from_storage(str(SECRETS))
ga = client.get_service("GoogleAdsService")
rows = lambda q: list(ga.search(customer_id=CID, query=q))

# бюджет-сирота
for r in rows("SELECT campaign_budget.resource_name, campaign_budget.name, "
              "campaign_budget.reference_count FROM campaign_budget"):
    b = r.campaign_budget
    if b.reference_count == 0 and b.name == "T1_budget_100RON_day":
        op = client.get_type("CampaignBudgetOperation")
        op.remove = b.resource_name
        client.get_service("CampaignBudgetService").mutate_campaign_budgets(
            customer_id=CID, operations=[op])
        print("REMOVED orphan budget:", b.resource_name)

# сниппеты как есть
for r in rows("SELECT conversion_action.name, conversion_action.tag_snippets "
              "FROM conversion_action WHERE conversion_action.type = 'WEBPAGE' "
              "AND conversion_action.status = 'ENABLED'"):
    ca = r.conversion_action
    print(f"--- {ca.name}: {len(ca.tag_snippets)} snippets")
    for sn in ca.tag_snippets:
        print(f"  type={sn.type_.name} fmt={sn.page_format.name}")
        print("  EVENT:", (sn.event_snippet or "")[:300].replace("\n", " "))
