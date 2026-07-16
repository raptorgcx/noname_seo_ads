# -*- coding: utf-8 -*-
"""Достаём evidences отклонённых объявлений: текст или destination?"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient

SECRETS = Path(__file__).resolve().parents[2] / ".secrets" / "google-ads.yaml"
CID = "7997489829"
client = GoogleAdsClient.load_from_storage(str(SECRETS))
ga = client.get_service("GoogleAdsService")

q = ("SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, "
     "ad_group_ad.policy_summary.policy_topic_entries FROM ad_group_ad "
     "WHERE ad_group_ad.status = 'ENABLED'")
for r in ga.search(customer_id=CID, query=q):
    print(f"== {r.ad_group.name} ad {r.ad_group_ad.ad.id}")
    for e in r.ad_group_ad.policy_summary.policy_topic_entries:
        print(f"  topic={e.topic} type={e.type_.name}")
        for ev in e.evidences:
            which = ev._pb.WhichOneof("value")
            print(f"    evidence: {which}")
            if which == "destination_text_list":
                for t in ev.destination_text_list.destination_texts:
                    print(f"      dest_text: {t[:80]}")
            elif which == "text_list":
                for t in ev.text_list.texts:
                    print(f"      text: {t[:80]}")
            elif which == "website_list":
                for w in ev.website_list.websites:
                    print(f"      website: {w}")
        for c in e.constraints:
            print(f"    constraint: {c._pb.WhichOneof('value')}")
