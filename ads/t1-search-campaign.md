# Т1 — Google Search «горячий спрос», чертёж кампании

Свежесть: 2026-07-15. **Статус: СОБРАНА ЧЕРЕЗ API, PAUSED, ВСЁ НА РЕВЬЮ GOOGLE.**
Basic Access одобрен 2026-07-15; кампания 24032372159 собрана скриптом
`scripts/build_t1.py` (идемпотентен, безопасно перезапускать). Владелец сказал
«запускай» — включаем, как только ревью пропустит объявления/ключи.

## ФИНАЛЬНЫЙ ВЕРДИКТ 2026-07-16: Search для лаунжа ЗАКРЫТ политикой

Хронология: v1 (тексты с narghilea/hookah) — DISAPPROVED (TOBACCO+CAPITALIZATION).
v2 (стерильные тексты: лаунж/терраса/PS5/суши, «NoName» вместо капса) — снова
DISAPPROVED, только TOBACCO, флаг капса ушёл → режет не текст, а **связку
«ключи + сайт кальянной»**. Официальная политика (support.google.com/adspolicy/
answer/16489929) прямо перечисляет hookah lounges в запрещённых категориях:
«services that directly facilitate tobacco consumption». Это категорийный блок
бизнеса, не проблема креативов.

**Что НЕ делаем (осознанно):** лендинг-приманку «без кальяна» под рекламу,
циклы переподачи отклонённых объявлений, маскировку слов. Всё это Google
квалифицирует как Circumventing systems → бан всего аккаунта с верифицированным
брендом и платёжным профилем. Цена ошибки несоизмерима со 100 RON/день.

**Что остаётся:** кампания лежит PAUSED как есть (стоит 0; все 25 ключей
APPROVED — если политика/прецедент изменятся, включение = 1 вызов API).
Горячий спрос «narghilea bucuresti» забираем там, где Google его сам отдаёт:
**GBP map pack** (карточка наша, категория Hookah bar) + **SEO** (сайт,
каталог HookahRadar). Платный бюджет уходит в **Meta (Т3)** — креативы там
тоже без табачных слов/изображений (политика Meta аналогична), продаём
атмосферу/террасу/кухню/бронь.

## Реальность политики TOBACCO (главное открытие сборки)

Все кальянные ключи (narghilea/hookah/shisha, включая RU) и объявления Google
режет политикой **TOBACCO** («услуги, способствующие потреблению табака») —
это судьба всех кальянных в Google Ads. Ошибка пришла с `is_exemptible: true`,
поэтому всё подано через ОФИЦИАЛЬНЫЙ механизм исключений:
- ключи: `exempt_policy_violation_keys` (AG1: 9, AG2: 7; RU-ключи и бренд
  прошли без флага) → UNDER_REVIEW;
- объявления: `policy_validation_parameter.ignorable_policy_topics`
  (флагнулся только CAPITALIZATION — «NO NAME» в заголовках; бренд, имеем
  право) → REVIEW_IN_PROGRESS.
Никаких обходов (маскировка слов и т.п.) НЕ делаем — только штатное ревью.
Если TOBACCO-ключи не пропустят: план Б — группы без табачных слов
(lounge/terasa/бренд) + вес на Meta и GBP; решение после вердикта ревью.

## Конверсии — БЕЗ импорта из GA4 (решение 2026-07-15)

Созданы напрямую в Ads (WEBPAGE): `booking_submit` (primary, BOOK_APPOINTMENT),
`wa_click` (CONTACT), `tel_click` (PHONE_CALL_LEAD) — и сайт шлёт их сам:
analytics.js v6 конфигурит **AW-18321408074** и дублирует три события тегом
(noname_site 82a8571). Плюсы: нет зависимости от связки GA4↔Ads и нет лага
импорта; gclid-атрибуция работает, consent v2 уже granted после «Принять».
Связку GA4↔Ads всё равно сделаем позже для аудиторий — не блокер запуска.

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

- [x] Кабинет создан (RON, Bucharest), биллинг = карта владельца
- [x] Конверсии: прямой AW-тег на сайте (analytics.js v6), импорт из GA4 не нужен
- [x] Consent v2 на сайте отдаёт ad_storage granted после «Принять» (fix 2026-07-14)
- [x] booking_submit primary, wa_click/tel_click secondary (двойного счёта нет)
- [x] Кампания собрана НА ПАУЗЕ (24032372159); «запускай» получено 2026-07-15
- [ ] Ревью Google пропустило объявления и ключи (TOBACCO exemption) → ENABLE
- [ ] После включения: 3–4 дня не трогать (обучение), потом чистка search terms

## Правила чтения теста

Метрика решения: **стоимость (booking_submit + wa_click)**. Порог: ≤ 20–25% среднего
чека из /dash/. Первые 3–4 дня НЕ трогаем ничего (обучение). Дальше: чистим поисковые
термины (см. минусы), смотрим разбивку по группам — слабую группу душим ставкой, не
удаляем. Через 7 дней — вердикт по каждой группе, через 14 — по кампании.
