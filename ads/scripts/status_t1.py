# -*- coding: utf-8 -*-
"""Статус Т1: политика по объявлениям/ключам, лейблы конверсий, бюджеты."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient

SECRETS = Path(__file__).resolve().parents[2] / ".secrets" / "google-ads.yaml"
CID = "7997489829"
client = GoogleAdsClient.load_from_storage(str(SECRETS))
ga = client.get_service("GoogleAdsService")
rows = lambda q: list(ga.search(customer_id=CID, query=q))

print("== BUDGETS ==")
for r in rows("SELECT campaign_budget.id, campaign_budget.name, campaign_budget.amount_micros, "
              "campaign_budget.reference_count FROM campaign_budget"):
    b = r.campaign_budget
    print(f"  {b.id} {b.name} {b.amount_micros/1e6:.0f} RON refs={b.reference_count}")

print("== ADS (policy) ==")
for r in rows("SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.policy_summary.approval_status, "
              "ad_group_ad.policy_summary.review_status, ad_group_ad.policy_summary.policy_topic_entries "
              "FROM ad_group_ad"):
    ps = r.ad_group_ad.policy_summary
    topics = [f"{e.topic}/{e.type_.name}" for e in ps.policy_topic_entries]
    print(f"  {r.ad_group.name}: {ps.approval_status.name} review={ps.review_status.name} {topics}")

print("== KEYWORDS (policy) ==")
agg = {}
for r in rows("SELECT ad_group.name, ad_group_criterion.keyword.text, "
              "ad_group_criterion.approval_status FROM ad_group_criterion "
              "WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE"):
    st = r.ad_group_criterion.approval_status.name
    agg.setdefault((r.ad_group.name, st), []).append(r.ad_group_criterion.keyword.text)
for (g, st), kws in sorted(agg.items()):
    print(f"  {g} [{st}]: {len(kws)} → {', '.join(kws[:12])}")

print("== CONVERSION SNIPPETS ==")
for r in rows("SELECT conversion_action.name, conversion_action.tag_snippets FROM conversion_action "
              "WHERE conversion_action.type = 'WEBPAGE' AND conversion_action.status = 'ENABLED'"):
    ca = r.conversion_action
    for sn in ca.tag_snippets:
        if sn.type_.name == "TRACKING" and sn.page_format.name == "HTML":
            m = re.search(r"AW-(\d+)/([-\w]+)", sn.event_snippet)
            print(f"  {ca.name}: aw={m.group(1) if m else '?'} label={m.group(2) if m else sn.event_snippet[:120]}")
