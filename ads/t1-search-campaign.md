# Т1 — Google Search «горячий спрос», чертёж кампании

Свежесть: 2026-07-14. Статус: ЖДЁТ КАБИНЕТ. Собираем по этому файлу, запускаем только
после «запускай» владельца. Бюджет одобрен: ~20–25 $/день (≈90–115 RON), тест ~1 неделя
(рекомендую 2, чтобы Google успел обучиться — решим по первым цифрам).

## Настройки кампании

| Параметр | Значение |
|---|---|
| Тип | Search, БЕЗ Display Expansion и без Search Partners (чистый тест) |
| Название | `T1_search_hot_bucuresti` |
| Гео | Бухарест + радиус 15 км; Presence only (находится в гео, не «интересуется») |
| Языки | все (языки интерфейса ≠ язык запроса; ключи сами разделят) |
| Бюджет | 100 RON/день |
| Ставки | старт: Maximize clicks с потолком CPC 3 RON → после ~20 конверсий: Maximize conversions |
| Расписание | пн–вс 11:00–01:00 (лаунж 13:00–01/02:00; звонки/брони чуть раньше открытия) |
| Конверсии | primary: `booking_submit` (импорт из GA4); secondary: `wa_click`, `tel_click` |
| UTM | НЕ вешаем (gclid атрибутирует сам — стандарт tracking/utm-standard.md) |

## Группы и ключи (phrase + exact; никакого broad на старте)

**AG1 — RO generic** (объявления RO):
"narghilea bucuresti", "lounge narghilea bucuresti", "bar narghilea", "localuri cu
narghilea", "cafenea cu narghilea bucuresti", "narghilea sector 1", "terasa cu narghilea
bucuresti", [narghilea bucuresti], [localuri cu narghilea bucuresti]

**AG2 — EN generic** (объявления EN, экспаты/туристы):
"hookah bucharest", "hookah lounge bucharest", "shisha bucharest", "shisha bar
bucharest", "best hookah in bucharest", [hookah lounge bucharest], [shisha bucharest]

**AG3 — RU generic** (объявления RU):
"кальян бухарест", "кальянная бухарест", "кальянная в бухаресте", "кальян в бухаресте",
[кальянная бухарест]

**AG4 — Brand protect** (дешёвая страховка, exact):
[noname lounge], [no name lounge bucharest], [noname lounge baneasa], [нонейм лаунж]

## Минус-слова (уровень кампании)

`magazin, shop, cumpar, cumpără, de vanzare, vanzare, pret narghilea magazin, livrare,
delivery, aluminiu, carbune, carbuni, tutun, accesorii, piese, furtun, ieftin, olx,
emag, aliexpress, second hand, купить, магазин, доставка, табак, уголь, komis, wholesale,
angro, en-gros, cluj, iasi, constanta, timisoara, brasov` (гео-минусы городов — чтобы
phrase не цеплял «narghilea cluj» у людей в Бухаресте).

## Объявления (RSA, по одному на группу)

**RO (AG1, AG4):**
- H: `Narghilea în Băneasa` · `#NO NAME Hookah Lounge` · `Fum dens, seri fără grabă` ·
  `Narghilea de la 150 lei` · `Terasă + camere private PS5` · `Deschis zilnic de la 13:00` ·
  `Rezervă masa pe WhatsApp` · `Sushi, cocktailuri, narghilea` · `Parcare proprie, Băneasa` ·
  `Rezervare în 30 de secunde`
- D: `Lounge premium în Băneasa: narghilea artizanală, sushi și cocktailuri. Rezervă pe WhatsApp în 30 de secunde.` ·
  `Mixuri de autor, terasă de vară și camere private cu PlayStation. Deschis zilnic 13:00–01:00.` ·
  `Prețuri fără steluțe: narghilea clasică de la 150 lei. Masă garantată doar cu rezervare confirmată.` ·
  `La 5 minute de aeroport, cu parcare proprie. Rezervă acum — răspundem rapid pe WhatsApp.`
- Final URL: `https://nonamelounge.ro/`

**EN (AG2):**
- H: `Hookah Lounge in Bucharest` · `#NO NAME Hookah Lounge` · `Thick Smoke, Slow Nights` ·
  `Hookah From 150 Lei` · `Summer Terrace + PS5 Rooms` · `Open Daily From 1 PM` ·
  `Book a Table on WhatsApp` · `Sushi, Cocktails & Shisha` · `Băneasa · Own Parking` ·
  `Table in 30 Seconds`
- D: `Premium lounge in Băneasa: handcrafted hookah, sushi and signature cocktails. Book via WhatsApp in 30 seconds.` ·
  `Signature mixes, summer terrace and private PlayStation rooms. Open daily 1 PM – 1 AM.` ·
  `Honest prices: classic hookah from 150 lei. Tables guaranteed only with a confirmed booking.` ·
  `5 minutes from the airport, own parking. Book now — we reply fast on WhatsApp.`
- Final URL: `https://nonamelounge.ro/en/`

**RU (AG3):**
- H: `Кальянная в Бухаресте` · `#NO NAME Hookah Lounge` · `Плотный дым, вечер без спешки` ·
  `Кальян от 150 лей` · `Терраса и PS5-комнаты` · `Открыто ежедневно с 13:00` ·
  `Бронь стола в WhatsApp` · `Суши, коктейли, кальян` · `Бэняса · своя парковка` ·
  `Стол за 30 секунд`
- D: `Премиум-лаунж в Бэнясе: авторские кальяны, суши и коктейли. Бронь в WhatsApp за 30 секунд.` ·
  `Авторские миксы, летняя терраса и приватные PlayStation-комнаты. Ежедневно 13:00–01:00.` ·
  `Цены без звёздочек: классический кальян от 150 лей. Стол — только по подтверждённой брони.` ·
  `5 минут от аэропорта, своя парковка. Бронируй — отвечаем в WhatsApp быстро.`
- Final URL: `https://nonamelounge.ro/ru/`

## Расширения (assets)

- Sitelinks: Meniu (/meniu-qr/), Prețuri (/#preturi), PlayStation (/#playstation),
  Rezervă (/#rezerva — проверить якорь виджета)
- Callouts: `Terasă de vară`, `Camere private PS5`, `Parcare proprie`, `5 min de aeroport`
- Call asset: +40 751 153 588 (расписание = часы работы)
- Location asset — ПОСЛЕ доступа к GBP.

## Чек-лист до включения

- [ ] Кабинет создан (RON, Bucharest), биллинг = карта владельца
- [ ] Связка Ads ↔ GA4 (робот Editor в GA4) + импорт конверсий booking_submit/wa_click/tel_click
- [x] Consent v2 на сайте отдаёт ad_storage granted после «Принять» (fix 2026-07-14, v=5)
- [ ] booking_submit назначен primary, клики — secondary (иначе двойной счёт конверсий)
- [ ] Кампания собрана НА ПАУЗЕ → показать владельцу → «запускай»

## Правила чтения теста

Метрика решения: **стоимость (booking_submit + wa_click)**. Порог: ≤ 20–25% среднего
чека из /dash/. Первые 3–4 дня НЕ трогаем ничего (обучение). Дальше: чистим поисковые
термины (см. минусы), смотрим разбивку по группам — слабую группу душим ставкой, не
удаляем. Через 7 дней — вердикт по каждой группе, через 14 — по кампании.
