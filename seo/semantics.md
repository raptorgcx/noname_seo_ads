# Семантическая карта — кальянный спрос Бухареста

Свежесть: 2026-07-13. Источники: `noname_parser/config/keywords.yaml` (лексика, которой
реально ищут — проверена живым скрейпом), датасет 68 подтверждённых заведений Бухареста
(review_count = прокси объёма брендового спроса), тексты отзывов.
⚠️ Точных объёмов пока нет: Keyword Planner требует кабинет Ads, GSC копит первые дни.
Карта уточнится цифрами после бейзлайна (~2026-07-20).

## Кластер A — свой бренд (страница: главная nonamelounge.ro)

`noname lounge`, `no name lounge`, `noname lounge bucuresti / bucharest`, `noname baneasa`,
`no name hookah lounge`, RU: `нонейм лаунж бухарест`. + навигационные с опечатками.
Интент: найти нас. Задача — позиция 1 везде + map pack. Защита в Ads (Т2-зеркально:
конкуренты могут купить наш бренд — проверять выдачу раз в месяц).

## Кластер B — категория + город (страницы: хаб каталога + map pack GBP)

Ядро (из tier1/tier2 keywords.yaml, работает в трёх языках города):
- RO: `narghilea bucuresti`, `bar narghilea bucuresti`, `lounge narghilea`,
  `localuri cu narghilea bucuresti`, `cafenea cu narghilea`, `narghilea sector 1..6`
- EN: `hookah bucharest`, `hookah lounge bucharest`, `shisha bar bucharest`,
  `shisha bucharest`, `best hookah in bucharest` (экспаты + туристы)
- RU: `кальян бухарест`, `кальянная бухарест`, `кальянная в бухаресте` (живая
  RU-сцена — подтверждено датасетом: Nova Lounge рекламирует русскоговорящий персонал)
Это же ядро — семантика кампании Т1 в Ads.

## Кластер C — гео-уточнения (страницы: главная для Băneasa; секторные хабы — тест Т5)

`narghilea baneasa` / `hookah baneasa` — наш район, обязаны быть №1 (сейчас в title есть).
`narghilea sector N`, `hookah old town bucharest`, `narghilea centru vechi`,
`shisha herastrau / floreasca / dorobanti` — покрывается секторными хабами каталога (Т5).

## Кластер D — чужие бренды (страницы: карточки каталога)

68 подтверждённых заведений; страница на каждое сидячее = перехват запроса
«<название>» + «<название> preturi / rezervare / meniu». Прокси объёма — review_count:

**Покрыто (28):** Narco Lounge, NO NAME, KAPKANA, Ganesha ×3, Nova Lounge, Shisha
Bucuresti, Members, Tress 2, Costa's, Krishna Caffe, El Medina, Infinity Eminescu,
Hugo, Klaud, Shisha Elysium ×2, MROOM, RS Caffee, Hermanos, King Bar, Haze, Vol Cafe,
Trio, Atipico, Riviera, Valea Regilor.

**Не покрыто — приоритет на добавление (сидячие, по review_count):**
| Заведение | Отзывов | Kind |
|---|---|---|
| Zaitoone | 5952 | restaurant_with_hookah |
| HiroBay | 2015 | restaurant_with_hookah |
| Mezeya | 1347 | restaurant_with_hookah |
| Bemolle Cafe | 1273 | restaurant_with_hookah |
| Habibi By Ahmad | 1247 | restaurant_with_hookah |
| Al Wady | 999 | restaurant_with_hookah |
| Restaurant Bar Influence | 890 | restaurant_with_hookah |
| Tress | 838 | cafe_bar_with_hookah |
| UBUD Decebal | 719 | restaurant_with_hookah |
| Kanz | 542 | restaurant_with_hookah |
| Narco Burgers | 531 | restaurant_with_hookah |
| Amoom Unirii | 480 | restaurant_with_hookah |
| Caffe Republic Baneasa | 335 | restaurant_with_hookah |
| NYO Lounge | 259 | restaurant_with_hookah |
| Komodo Floreasca | 234 | restaurant_with_hookah |
| Komodo Old Town | 161 | restaurant_with_hookah |
| Cafe Nescafe | 116 | cafe_bar_with_hookah |
| Arc Food Lounge | 103 | restaurant_with_hookah |
| Mombu by Infinity | 77 | restaurant_with_hookah |
| Azul Shisha / Velazur / Smoky Hookah Bar | ≤3 | новые/малые — хвостом |

Не листим: shop (9 шт. — Narghilea de lux ×2, AMY Deluxe ×4, Merlin, HOOKAHpookah,
Shisha Master и пр.) и kind=other (Secret Massage, ALAS Gaming, PSG, Nar) — политика
каталога «только сидячие».

Этот же список (48 сидячих имён) = ключи кампании Т2.

## Кластер E — интент-модификаторы

- `terasa cu narghilea (bucuresti)` — сезон, лето. У нас терраса есть → Т6.
- `<venue/категория> + preturi / meniu / rezervare` — закрывается контентом карточек
  (цены и часы уже в шаблоне) и виджетом брони на главной.
- `narghilea livrare`, `magazin narghilea` — НЕ наш интент, не покрываем и не покупаем.
- Опечатки/транслит (sisha, nargila, кальян) — Google сам склеивает, отдельных страниц
  не делаем; в Ads phrase match подхватит.

## Правило посадочных

Один запрос — одна страница: бренд→главная, категория→хаб каталога / GBP,
чужой бренд→карточка, гео→секторный хаб. Главную под кластер B не затачиваем —
она конверсионный лендинг, категорию тащат каталог и map pack.
