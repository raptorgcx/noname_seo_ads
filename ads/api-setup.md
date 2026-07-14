# Google Ads API — путь к автономному управлению

Свежесть: 2026-07-14. Цель: агент управляет кампаниями из кода (google-ads Python lib):
создание/правка кампаний, минус-слова, ставки, чистка search terms, отчёты — без кликов
владельца. Ниже — что для этого нужно и кто что делает.

## Из чего состоит «дать API» (4 компонента)

| # | Компонент | Откуда берётся | Кто делает |
|---|---|---|---|
| 1 | Обычный кабинет Ads (customer id) | ads.google.com, Expert Mode, RON | владелец, 5 мин UI |
| 2 | **Manager Account (MCC)** + developer token | ads.google.com/home/tools/manager-accounts → создать; затем в MCC: Tools → API Center → токен появляется сразу (уровень Test) | владелец, 5 мин UI |
| 3 | Basic access для токена | заявка из API Center (Test-токен не пускает в реальные аккаунты). Текст заявки готовит агент; одобрение Google 1–3 раб. дня | агент готовит, владелец жмёт Submit |
| 4 | OAuth-клиент (client_id + secret) + refresh token | console.cloud.google.com под роботом: новый проект → APIs & Services → Credentials → OAuth client (Desktop). Refresh token дальше добывает агент консольным flow: печатает URL → владелец открывает под роботом → Allow → присылает код | владелец 5 мин UI + 1 клик Allow |

Плюс: MCC должен получить доступ к кабинету (из MCC «Link existing account» → принять
приглашение в кабинете) — 2 клика.

Итог хранится в `.secrets/google-ads.env`: DEVELOPER_TOKEN, CLIENT_ID, CLIENT_SECRET,
REFRESH_TOKEN, LOGIN_CUSTOMER_ID (MCC), CUSTOMER_ID (кабинет). В git не попадает.

## Что агент сможет сам после этого

- собрать/править кампании, группы, ключи, объявления (T1 из t1-search-campaign.md — кодом);
- ежедневная гигиена: search terms → минусы, ставки, паузы слабых групп;
- отчёты цена-брони по группам/ключам (join с GA4);
- НЕ сможет: вводить карту (биллинг — только владелец в UI) и создавать самый первый
  кабинет/MCC (тоже UI).

## Порядок на практике

1. Сегодня: владелец делает №1 и №2 (10 мин, под роботом), агент диктует.
2. Сразу же: агент отдаёт текст заявки Basic (№3), владелец жмёт Submit.
3. Пока заявка едет (1–3 дня): кампанию Т1 собираем руками под диктовку — запуск не ждёт API.
4. №4 (OAuth) — в любой момент, 5 минут; после одобрения Basic агент переходит на код.

## Текст заявки Basic access (черновик, EN)

Company: BUCHARESTCLOUDS S.R.L. (hookah lounge, Bucharest, Romania).
Use case: managing our own single advertising account (no third parties, no resale).
Tool: internal scripts on google-ads-python to manage search campaigns for our venue
site nonamelounge.ro: campaign/ad group/keyword management, negative keyword hygiene
based on search terms reports, bid adjustments, and reporting joined with our GA4 data.
API access is used by the business owner's automation account only. Expected volume:
low (single account, a few hundred operations/day max).
