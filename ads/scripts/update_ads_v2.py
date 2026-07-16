# -*- coding: utf-8 -*-
"""Т1 v2: замена объявлений на политику-чистые тексты (без табачных слов,
без капса NO NAME) + чистка табачных слов из sitelink-описаний.

Ключи трогать НЕ надо — они все APPROVED."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

SECRETS = Path(__file__).resolve().parents[2] / ".secrets" / "google-ads.yaml"
CID = "7997489829"
client = GoogleAdsClient.load_from_storage(str(SECRETS))
ga = client.get_service("GoogleAdsService")
enums = client.enums
rows = lambda q: list(ga.search(customer_id=CID, query=q))

ADS_V2 = {
    "AG1_RO_generic": {
        "final_url": "https://nonamelounge.ro/",
        "headlines": ["Lounge premium în Băneasa", "NoName Lounge București",
                      "Terasă de vară și PS5", "Seri lungi, fără grabă",
                      "Rezervă masa pe WhatsApp", "Deschis zilnic 13:00–01:00",
                      "Sushi și cocktailuri", "Camere private cu PS5",
                      "Parcare proprie, Băneasa", "Rezervare în 30 de secunde"],
        "descriptions": [
            "Lounge premium în Băneasa: atmosferă relaxată, sushi și cocktailuri semnătură.",
            "Terasă de vară și camere private cu PlayStation. Deschis zilnic 13:00–01:00.",
            "Rezervă pe WhatsApp în 30 de secunde — răspundem rapid.",
            "La 5 minute de aeroport, cu parcare proprie. Muzică lounge și seri lungi."],
    },
    "AG2_EN_generic": {
        "final_url": "https://nonamelounge.ro/en/",
        "headlines": ["Lounge & Terrace in Băneasa", "NoName Lounge Bucharest",
                      "Slow Nights, Lounge Music", "Summer Terrace + PS5 Rooms",
                      "Book a Table on WhatsApp", "Open Daily 1 PM – 1 AM",
                      "Sushi & Signature Cocktails", "Private PS5 Rooms",
                      "Băneasa · Own Parking", "Table in 30 Seconds"],
        "descriptions": [
            "Premium lounge in Băneasa: relaxed vibe, sushi and signature cocktails.",
            "Summer terrace and private PlayStation rooms. Open daily 1 PM – 1 AM.",
            "Book on WhatsApp in 30 seconds — we reply fast.",
            "5 minutes from the airport, own parking. Lounge music, slow nights."],
    },
    "AG3_RU_generic": {
        "final_url": "https://nonamelounge.ro/ru/",
        "headlines": ["Лаунж в Бэнясе, Бухарест", "NoName Lounge",
                      "Вечер без спешки", "Терраса и PS5-комнаты",
                      "Бронь стола в WhatsApp", "Ежедневно 13:00–01:00",
                      "Суши и авторские коктейли", "Приватные PS5-комнаты",
                      "Бэняса · своя парковка", "Стол за 30 секунд"],
        "descriptions": [
            "Премиум-лаунж в Бэнясе: расслабленная атмосфера, суши и авторские коктейли.",
            "Летняя терраса и приватные PlayStation-комнаты. Ежедневно 13:00–01:00.",
            "Бронь в WhatsApp за 30 секунд — отвечаем быстро.",
            "5 минут от аэропорта, своя парковка. Лаунж-музыка и долгие вечера."],
    },
    "AG4_Brand_protect": {
        "final_url": "https://nonamelounge.ro/",
        "headlines": ["NoName Lounge Băneasa", "Site oficial — rezervări",
                      "Lounge premium în Băneasa", "Terasă de vară și PS5",
                      "Deschis zilnic 13:00–01:00", "Rezervă masa pe WhatsApp",
                      "Parcare proprie, Băneasa", "Rezervare în 30 de secunde"],
        "descriptions": [
            "Pagina oficială NoName Lounge Băneasa. Meniu, prețuri și rezervări online.",
            "Atmosferă relaxată, sushi și cocktailuri semnătură. Rezervă în 30 de secunde.",
            "Terasă de vară și camere private cu PlayStation. Zilnic 13:00–01:00.",
            "La 5 minute de aeroport, cu parcare proprie. Răspundem rapid pe WhatsApp."],
    },
}

for g, cfg in ADS_V2.items():
    for h in cfg["headlines"]:
        assert len(h) <= 30, f"{g} H>30: {h!r} ({len(h)})"
    for d in cfg["descriptions"]:
        assert len(d) <= 90, f"{g} D>90: {d!r} ({len(d)})"

ad_svc = client.get_service("AdGroupAdService")

for ag_name, cfg in ADS_V2.items():
    r = rows(f"SELECT ad_group.resource_name FROM ad_group WHERE ad_group.name = '{ag_name}'")
    ag_rn = r[0].ad_group.resource_name

    # снять старые (disapproved) объявления
    old = rows("SELECT ad_group_ad.resource_name FROM ad_group_ad "
               f"WHERE ad_group_ad.ad_group = '{ag_rn}' AND ad_group_ad.status != 'REMOVED'")
    for o in old:
        op = client.get_type("AdGroupAdOperation")
        op.remove = o.ad_group_ad.resource_name
        ad_svc.mutate_ad_group_ads(customer_id=CID, operations=[op])
    print(f"{ag_name}: removed {len(old)} old ad(s)")

    # новое чистое объявление
    op = client.get_type("AdGroupAdOperation")
    aga = op.create
    aga.ad_group = ag_rn
    aga.status = enums.AdGroupAdStatusEnum.ENABLED
    rsa = aga.ad.responsive_search_ad
    for h in cfg["headlines"]:
        a = client.get_type("AdTextAsset"); a.text = h; rsa.headlines.append(a)
    for d in cfg["descriptions"]:
        a = client.get_type("AdTextAsset"); a.text = d; rsa.descriptions.append(a)
    aga.ad.final_urls.append(cfg["final_url"])
    try:
        ad_svc.mutate_ad_group_ads(customer_id=CID, operations=[op])
        print(f"{ag_name}: new ad created CLEAN")
    except GoogleAdsException as ex:
        topics = []
        for err in ex.failure.errors:
            for entry in err.details.policy_finding_details.policy_topic_entries:
                if entry.topic and entry.topic not in topics:
                    topics.append(entry.topic)
        if not topics:
            raise
        op.policy_validation_parameter.ignorable_policy_topics.extend(topics)
        ad_svc.mutate_ad_group_ads(customer_id=CID, operations=[op])
        print(f"{ag_name}: new ad created, exemption for {topics}")

# sitelinks: убрать «narghilea» из описаний
asset_svc = client.get_service("AssetService")
FIX = {
    "T1_sitelink_Meniu": ("Meniul complet cu prețuri", "Sushi, cocktailuri, ceaiuri"),
    "T1_sitelink_Prețuri": ("Prețuri corecte, fără surprize", "Vezi lista completă"),
}
for r in rows("SELECT asset.resource_name, asset.name FROM asset"):
    if r.asset.name in FIX:
        d1, d2 = FIX[r.asset.name]
        op = client.get_type("AssetOperation")
        a = op.update
        a.resource_name = r.asset.resource_name
        a.sitelink_asset.description1 = d1
        a.sitelink_asset.description2 = d2
        op.update_mask.paths.extend(["sitelink_asset.description1", "sitelink_asset.description2"])
        asset_svc.mutate_assets(customer_id=CID, operations=[op])
        print("sitelink fixed:", r.asset.name)
print("DONE")
