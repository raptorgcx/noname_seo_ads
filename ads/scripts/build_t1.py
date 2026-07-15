# -*- coding: utf-8 -*-
"""Сборка Т1 по чертежу ads/t1-search-campaign.md. Кампания создаётся PAUSED.

Идемпотентно: каждый объект ищется по имени перед созданием, повторный запуск
досоздаёт недостающее и ничего не дублирует.
"""
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

CAMPAIGN_NAME = "T1_search_hot_bucuresti"
BUDGET_NAME = "T1_budget_100RON_day"
VENUE_LAT, VENUE_LNG = 44.488698, 26.0846089

# --- каталоги контента ---------------------------------------------------
CONVERSIONS = [
    # (name, category, primary)
    ("booking_submit", "BOOK_APPOINTMENT", True),
    ("wa_click", "CONTACT", False),
    ("tel_click", "PHONE_CALL_LEAD", False),
]

AD_GROUPS = {
    "AG1_RO_generic": {
        "final_url": "https://nonamelounge.ro/",
        "phrase": ["narghilea bucuresti", "lounge narghilea bucuresti", "bar narghilea",
                   "localuri cu narghilea", "cafenea cu narghilea bucuresti",
                   "narghilea sector 1", "terasa cu narghilea bucuresti"],
        "exact": ["narghilea bucuresti", "localuri cu narghilea bucuresti"],
        "headlines": ["Narghilea în Băneasa", "NO NAME Hookah Lounge",
                      "Fum dens, seri fără grabă", "Narghilea de la 150 lei",
                      "Terasă + camere private PS5", "Deschis zilnic de la 13:00",
                      "Rezervă masa pe WhatsApp", "Sushi, cocktailuri, narghilea",
                      "Parcare proprie, Băneasa", "Rezervare în 30 de secunde"],
        "descriptions": [
            "Narghilea artizanală, sushi și cocktailuri în Băneasa. Rezervă pe WhatsApp în 30 sec.",
            "Mixuri de autor, terasă de vară și camere private cu PlayStation. Zilnic 13:00–01:00.",
            "Prețuri fără steluțe: narghilea clasică de la 150 lei. Masă doar cu rezervare.",
            "La 5 minute de aeroport, cu parcare proprie. Rezervă acum — răspundem rapid."],
    },
    "AG2_EN_generic": {
        "final_url": "https://nonamelounge.ro/en/",
        "phrase": ["hookah bucharest", "hookah lounge bucharest", "shisha bucharest",
                   "shisha bar bucharest", "best hookah in bucharest"],
        "exact": ["hookah lounge bucharest", "shisha bucharest"],
        "headlines": ["Hookah Lounge in Bucharest", "NO NAME Hookah Lounge",
                      "Thick Smoke, Slow Nights", "Hookah From 150 Lei",
                      "Summer Terrace + PS5 Rooms", "Open Daily From 1 PM",
                      "Book a Table on WhatsApp", "Sushi, Cocktails & Shisha",
                      "Băneasa · Own Parking", "Table in 30 Seconds"],
        "descriptions": [
            "Handcrafted hookah, sushi and signature cocktails in Băneasa. Book on WhatsApp.",
            "Signature mixes, summer terrace and private PlayStation rooms. Open 1 PM – 1 AM.",
            "Honest prices: classic hookah from 150 lei. Tables guaranteed with a booking.",
            "5 minutes from the airport, own parking. Book now — we reply fast on WhatsApp."],
    },
    "AG3_RU_generic": {
        "final_url": "https://nonamelounge.ro/ru/",
        "phrase": ["кальян бухарест", "кальянная бухарест", "кальянная в бухаресте",
                   "кальян в бухаресте"],
        "exact": ["кальянная бухарест"],
        "headlines": ["Кальянная в Бухаресте", "NO NAME Hookah Lounge",
                      "Плотный дым, вечер без спешки", "Кальян от 150 лей",
                      "Терраса и PS5-комнаты", "Открыто ежедневно с 13:00",
                      "Бронь стола в WhatsApp", "Суши, коктейли, кальян",
                      "Бэняса · своя парковка", "Стол за 30 секунд"],
        "descriptions": [
            "Премиум-лаунж в Бэнясе: авторские кальяны, суши и коктейли. Бронь в WhatsApp за 30 сек.",
            "Авторские миксы, летняя терраса и приватные PlayStation-комнаты. Ежедневно 13:00–01:00.",
            "Цены без звёздочек: классический кальян от 150 лей. Стол — по подтверждённой брони.",
            "5 минут от аэропорта, своя парковка. Бронируй — отвечаем в WhatsApp быстро."],
    },
    "AG4_Brand_protect": {
        "final_url": "https://nonamelounge.ro/",
        "phrase": [],
        "exact": ["noname lounge", "no name lounge bucharest", "noname lounge baneasa",
                  "нонейм лаунж"],
        "headlines": ["NO NAME Hookah Lounge", "Narghilea în Băneasa",
                      "Site oficial — rezervări", "Terasă + camere private PS5",
                      "Deschis zilnic de la 13:00", "Rezervă masa pe WhatsApp",
                      "Fum dens, seri fără grabă", "Parcare proprie, Băneasa"],
        "descriptions": [
            "Pagina oficială NO NAME Lounge Băneasa. Meniu, prețuri și rezervări online.",
            "Narghilea artizanală, sushi și cocktailuri. Rezervă pe WhatsApp în 30 de secunde.",
            "Terasă de vară și camere private cu PlayStation. Zilnic 13:00–01:00.",
            "La 5 minute de aeroport, cu parcare proprie. Răspundem rapid pe WhatsApp."],
    },
}

NEGATIVES = ["magazin", "shop", "cumpar", "cumpără", "de vanzare", "vanzare",
             "pret narghilea magazin", "livrare", "delivery", "aluminiu", "carbune",
             "carbuni", "tutun", "accesorii", "piese", "furtun", "ieftin", "olx",
             "emag", "aliexpress", "second hand", "купить", "магазин", "доставка",
             "табак", "уголь", "komis", "wholesale", "angro", "en-gros", "cluj",
             "iasi", "constanta", "timisoara", "brasov"]

SITELINKS = [
    ("Meniu", "https://nonamelounge.ro/meniu-qr/", "Meniul complet cu prețuri", "Narghilea, sushi, cocktailuri"),
    ("Prețuri", "https://nonamelounge.ro/#preturi", "Narghilea de la 150 lei", "Prețuri fără steluțe"),
    ("PlayStation", "https://nonamelounge.ro/#playstation", "Camere private cu PS5", "Pentru grupuri de prieteni"),
    ("Rezervă", "https://nonamelounge.ro/#rezerva", "Masă în 30 de secunde", "Confirmare pe WhatsApp"),
]
CALLOUTS = ["Terasă de vară", "Camere private PS5", "Parcare proprie", "5 min de aeroport"]
PHONE = ("RO", "+40751153588")

# --- валидация лимитов ----------------------------------------------------
for g, cfg in AD_GROUPS.items():
    for h in cfg["headlines"]:
        assert len(h) <= 30, f"{g} headline >30: {h!r} ({len(h)})"
    for d in cfg["descriptions"]:
        assert len(d) <= 90, f"{g} description >90: {d!r} ({len(d)})"
for text, _, l1, l2 in SITELINKS:
    assert len(text) <= 25 and len(l1) <= 35 and len(l2) <= 35, f"sitelink limits: {text}"
for c in CALLOUTS:
    assert len(c) <= 25, f"callout >25: {c}"

# --- helpers ---------------------------------------------------------------
def rows(q):
    return list(ga.search(customer_id=CID, query=q))

def find_one(q):
    r = rows(q)
    return r[0] if r else None

created = []

def mutate(service_name, operations, method="mutate"):
    svc = client.get_service(service_name)
    fn = getattr(svc, [m for m in dir(svc) if m.startswith("mutate_")][0])
    return fn(customer_id=CID, operations=operations)

# --- 1. конверсии ----------------------------------------------------------
conv_svc = client.get_service("ConversionActionService")
for name, cat, primary in CONVERSIONS:
    if find_one(f"SELECT conversion_action.id FROM conversion_action WHERE conversion_action.name = '{name}'"):
        continue
    op = client.get_type("ConversionActionOperation")
    ca = op.create
    ca.name = name
    ca.type_ = enums.ConversionActionTypeEnum.WEBPAGE
    ca.category = getattr(enums.ConversionActionCategoryEnum, cat)
    ca.status = enums.ConversionActionStatusEnum.ENABLED
    ca.primary_for_goal = primary
    ca.counting_type = enums.ConversionActionCountingTypeEnum.ONE_PER_CLICK
    conv_svc.mutate_conversion_actions(customer_id=CID, operations=[op])
    created.append(f"conversion:{name}")

# --- 2. бюджет + кампания ---------------------------------------------------
b = find_one(f"SELECT campaign_budget.resource_name FROM campaign_budget WHERE campaign_budget.name = '{BUDGET_NAME}'")
if b:
    budget_rn = b.campaign_budget.resource_name
else:
    op = client.get_type("CampaignBudgetOperation")
    cb = op.create
    cb.name = BUDGET_NAME
    cb.amount_micros = 100_000_000  # 100 RON
    cb.delivery_method = enums.BudgetDeliveryMethodEnum.STANDARD
    cb.explicitly_shared = False
    budget_rn = client.get_service("CampaignBudgetService").mutate_campaign_budgets(
        customer_id=CID, operations=[op]).results[0].resource_name
    created.append("budget")

c = find_one(f"SELECT campaign.resource_name FROM campaign WHERE campaign.name = '{CAMPAIGN_NAME}'")
if c:
    campaign_rn = c.campaign.resource_name
else:
    op = client.get_type("CampaignOperation")
    cp = op.create
    cp.name = CAMPAIGN_NAME
    cp.status = enums.CampaignStatusEnum.PAUSED
    cp.advertising_channel_type = enums.AdvertisingChannelTypeEnum.SEARCH
    cp.campaign_budget = budget_rn
    ns = cp.network_settings
    ns.target_google_search = True
    ns.target_search_network = False
    ns.target_content_network = False
    ns.target_partner_search_network = False
    cp.target_spend.cpc_bid_ceiling_micros = 3_000_000  # потолок CPC 3 RON
    cp.geo_target_type_setting.positive_geo_target_type = \
        enums.PositiveGeoTargetTypeEnum.PRESENCE
    cp.geo_target_type_setting.negative_geo_target_type = \
        enums.NegativeGeoTargetTypeEnum.PRESENCE
    if hasattr(cp, "contains_eu_political_advertising"):
        cp.contains_eu_political_advertising = \
            enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    campaign_rn = client.get_service("CampaignService").mutate_campaigns(
        customer_id=CID, operations=[op]).results[0].resource_name
    created.append("campaign")

# --- 3. критерии кампании: гео, радиус, расписание, минус-слова -------------
crit_svc = client.get_service("CampaignCriterionService")
existing_crit = {(r.campaign_criterion.type_.name, r.campaign_criterion.display_name or
                  str(r.campaign_criterion.criterion_id))
                 for r in rows("SELECT campaign_criterion.type, campaign_criterion.display_name, "
                               "campaign_criterion.criterion_id FROM campaign_criterion "
                               f"WHERE campaign_criterion.campaign = '{campaign_rn}'")}

def crit_types():
    return {r.campaign_criterion.type_.name
            for r in rows("SELECT campaign_criterion.type FROM campaign_criterion "
                          f"WHERE campaign_criterion.campaign = '{campaign_rn}'")}

have = crit_types()
ops = []

if "LOCATION" not in have:
    gts = client.get_service("GeoTargetConstantService")
    req = client.get_type("SuggestGeoTargetConstantsRequest")
    req.locale = "en"
    req.country_code = "RO"
    req.location_names.names.append("Bucharest")
    best = None
    for s in gts.suggest_geo_target_constants(request=req).geo_target_constant_suggestions:
        g = s.geo_target_constant
        if g.target_type in ("City", "Capital") and g.country_code == "RO":
            best = g
            break
    assert best, "Bucharest geo constant not found"
    op = client.get_type("CampaignCriterionOperation")
    op.create.campaign = campaign_rn
    op.create.location.geo_target_constant = best.resource_name
    ops.append(op)
    created.append(f"geo:{best.name}({best.id})")

if "PROXIMITY" not in have:
    op = client.get_type("CampaignCriterionOperation")
    op.create.campaign = campaign_rn
    px = op.create.proximity
    px.geo_point.latitude_in_micro_degrees = int(VENUE_LAT * 1_000_000)
    px.geo_point.longitude_in_micro_degrees = int(VENUE_LNG * 1_000_000)
    px.radius = 15
    px.radius_units = enums.ProximityRadiusUnitsEnum.KILOMETERS
    ops.append(op)
    created.append("proximity:15km")

if "AD_SCHEDULE" not in have:
    for day in ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]:
        for start, end in [(11, 24), (0, 1)]:
            op = client.get_type("CampaignCriterionOperation")
            op.create.campaign = campaign_rn
            s = op.create.ad_schedule
            s.day_of_week = getattr(enums.DayOfWeekEnum, day)
            s.start_hour, s.end_hour = start, end
            s.start_minute = enums.MinuteOfHourEnum.ZERO
            s.end_minute = enums.MinuteOfHourEnum.ZERO
            ops.append(op)
    created.append("schedule:7d x (11-24,0-1)")

have_neg = {r.campaign_criterion.keyword.text
            for r in rows("SELECT campaign_criterion.keyword.text FROM campaign_criterion "
                          f"WHERE campaign_criterion.campaign = '{campaign_rn}' "
                          "AND campaign_criterion.negative = TRUE")}
for kw in NEGATIVES:
    if kw in have_neg:
        continue
    op = client.get_type("CampaignCriterionOperation")
    op.create.campaign = campaign_rn
    op.create.negative = True
    op.create.keyword.text = kw
    op.create.keyword.match_type = enums.KeywordMatchTypeEnum.BROAD
    ops.append(op)

if ops:
    crit_svc.mutate_campaign_criteria(customer_id=CID, operations=ops)
    created.append(f"criteria:{len(ops)}")

# --- 4. группы, ключи, объявления -------------------------------------------
ag_svc = client.get_service("AdGroupService")
agc_svc = client.get_service("AdGroupCriterionService")
ad_svc = client.get_service("AdGroupAdService")

for ag_name, cfg in AD_GROUPS.items():
    r = find_one(f"SELECT ad_group.resource_name FROM ad_group WHERE ad_group.name = '{ag_name}'")
    if r:
        ag_rn = r.ad_group.resource_name
    else:
        op = client.get_type("AdGroupOperation")
        agp = op.create
        agp.name = ag_name
        agp.campaign = campaign_rn
        agp.type_ = enums.AdGroupTypeEnum.SEARCH_STANDARD
        agp.status = enums.AdGroupStatusEnum.ENABLED
        ag_rn = ag_svc.mutate_ad_groups(customer_id=CID, operations=[op]).results[0].resource_name
        created.append(f"ad_group:{ag_name}")

    have_kw = {(r.ad_group_criterion.keyword.text, r.ad_group_criterion.keyword.match_type.name)
               for r in rows("SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type "
                             f"FROM ad_group_criterion WHERE ad_group_criterion.ad_group = '{ag_rn}'")}
    kw_ops = []
    for text, mt in [(t, "PHRASE") for t in cfg["phrase"]] + [(t, "EXACT") for t in cfg["exact"]]:
        if (text, mt) in have_kw:
            continue
        op = client.get_type("AdGroupCriterionOperation")
        agc = op.create
        agc.ad_group = ag_rn
        agc.status = enums.AdGroupCriterionStatusEnum.ENABLED
        agc.keyword.text = text
        agc.keyword.match_type = getattr(enums.KeywordMatchTypeEnum, mt)
        kw_ops.append(op)
    if kw_ops:
        # Кальянные ключи бьются об политику TOBACCO (is_exemptible) — прикладываем
        # официальный запрос исключения и повторяем: Google рассмотрит вручную.
        try:
            agc_svc.mutate_ad_group_criteria(customer_id=CID, operations=kw_ops)
            created.append(f"keywords:{ag_name}:{len(kw_ops)}")
        except GoogleAdsException as ex:
            exempted = 0
            for err in ex.failure.errors:
                pvd = err.details.policy_violation_details
                if pvd.is_exemptible and err.location.field_path_elements:
                    idx = err.location.field_path_elements[0].index
                    kw_ops[idx].exempt_policy_violation_keys.append(pvd.key)
                    exempted += 1
            if not exempted:
                raise
            agc_svc.mutate_ad_group_criteria(customer_id=CID, operations=kw_ops)
            created.append(f"keywords:{ag_name}:{len(kw_ops)} (exemption requested: {exempted})")

    if not find_one("SELECT ad_group_ad.ad.id FROM ad_group_ad "
                    f"WHERE ad_group_ad.ad_group = '{ag_rn}'"):
        op = client.get_type("AdGroupAdOperation")
        aga = op.create
        aga.ad_group = ag_rn
        aga.status = enums.AdGroupAdStatusEnum.ENABLED
        rsa = aga.ad.responsive_search_ad
        for h in cfg["headlines"]:
            a = client.get_type("AdTextAsset")
            a.text = h
            rsa.headlines.append(a)
        for d in cfg["descriptions"][:4]:
            a = client.get_type("AdTextAsset")
            a.text = d
            rsa.descriptions.append(a)
        aga.ad.final_urls.append(cfg["final_url"])
        # Для объявлений тот же механизм зовётся policy_validation_parameter:
        # первый вызов возвращает policy_finding, повтор с ignorable_policy_topics
        # отправляет объявление на ручное ревью.
        try:
            ad_svc.mutate_ad_group_ads(customer_id=CID, operations=[op])
            created.append(f"rsa:{ag_name}")
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
            created.append(f"rsa:{ag_name} (exemption requested: {topics})")

# --- 5. assets: sitelinks, callouts, call ------------------------------------
asset_svc = client.get_service("AssetService")
ca_svc = client.get_service("CampaignAssetService")
have_assets = {r.asset.name: r.asset.resource_name
               for r in rows("SELECT asset.name, asset.resource_name FROM asset")}
have_links = {(r.campaign_asset.field_type.name, r.campaign_asset.asset)
              for r in rows("SELECT campaign_asset.field_type, campaign_asset.asset "
                            f"FROM campaign_asset WHERE campaign_asset.campaign = '{campaign_rn}'")}

def link(asset_rn, field_type):
    if (field_type, asset_rn) in have_links:
        return
    op = client.get_type("CampaignAssetOperation")
    op.create.campaign = campaign_rn
    op.create.asset = asset_rn
    op.create.field_type = getattr(enums.AssetFieldTypeEnum, field_type)
    ca_svc.mutate_campaign_assets(customer_id=CID, operations=[op])

for text, url, l1, l2 in SITELINKS:
    aname = f"T1_sitelink_{text}"
    if aname in have_assets:
        rn = have_assets[aname]
    else:
        op = client.get_type("AssetOperation")
        a = op.create
        a.name = aname
        a.sitelink_asset.link_text = text
        a.sitelink_asset.description1 = l1
        a.sitelink_asset.description2 = l2
        a.final_urls.append(url)
        rn = asset_svc.mutate_assets(customer_id=CID, operations=[op]).results[0].resource_name
        created.append(f"asset:{aname}")
    link(rn, "SITELINK")

for text in CALLOUTS:
    aname = f"T1_callout_{text}"
    if aname in have_assets:
        rn = have_assets[aname]
    else:
        op = client.get_type("AssetOperation")
        a = op.create
        a.name = aname
        a.callout_asset.callout_text = text
        rn = asset_svc.mutate_assets(customer_id=CID, operations=[op]).results[0].resource_name
        created.append(f"asset:{aname}")
    link(rn, "CALLOUT")

aname = "T1_call_main"
if aname in have_assets:
    rn = have_assets[aname]
else:
    op = client.get_type("AssetOperation")
    a = op.create
    a.name = aname
    a.call_asset.country_code = PHONE[0]
    a.call_asset.phone_number = PHONE[1]
    rn = asset_svc.mutate_assets(customer_id=CID, operations=[op]).results[0].resource_name
    created.append(f"asset:{aname}")
link(rn, "CALL")

# --- 6. отчёт ----------------------------------------------------------------
print("CREATED:", ", ".join(created) if created else "(nothing — everything already exists)")
cts = find_one("SELECT customer.conversion_tracking_setting.conversion_tracking_id FROM customer")
print("AW_ID:", cts.customer.conversion_tracking_setting.conversion_tracking_id)
for r in rows("SELECT conversion_action.name, conversion_action.tag_snippets, "
              "conversion_action.primary_for_goal FROM conversion_action "
              "WHERE conversion_action.status = 'ENABLED' AND conversion_action.type = 'WEBPAGE'"):
    ca = r.conversion_action
    label = ""
    for sn in ca.tag_snippets:
        if sn.type_.name == "TRACKING" and "send_to" in sn.event_snippet:
            import re
            m = re.search(r"AW-\d+/([\w-]+)", sn.event_snippet)
            if m:
                label = m.group(1)
                break
    print(f"CONV: {ca.name} primary={ca.primary_for_goal} label={label}")
print("CAMPAIGN:", campaign_rn, "status=PAUSED")
