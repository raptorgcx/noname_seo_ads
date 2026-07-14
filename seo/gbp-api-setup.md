# GBP API — программный доступ к карточке

Свежесть: 2026-07-14 (вечер). Статус: робот = Менеджер профиля; карточка
оптимизирована под диктовку (категория Hookah bar, сайт /gm, меню, брони,
описание RO+EN, атрибуты); **заявка на API подана, case 9-1215000041861**.
Этот файл — путь к автономии (ответы на отзывы, посты, часы — кодом).

## Почему нельзя «просто подключиться»

Business Profile APIs (My Business *) — закрытые: любой Cloud-проект получает
**квоту 0** до одобрения заявки. Это та же история, что Basic Access в Ads API,
только форма другая. Без одобрения все вызовы падают 429 RESOURCE_EXHAUSTED.

## План

1. **Заявка ПОДАНА 2026-07-14** (вечер, форма через
   support.google.com/business/contact/api_default → «Application For Basic API
   Access», от робота). **Case ID: 9-1215000041861.** Ревью ~7–10 раб. дней
   (их формулировка: high volume of allowlist requests). Проект:
   **noname-ads-api**, number **768112830575** (тот же, что Ads API + brand
   verification; номер в .secrets/google-ads.env → GCP_PROJECT_NUMBER).
   Поданный use case: собственный профиль, 1 локация, ответы на отзывы /
   часы / атрибуты / посты, internal only.
2. После одобрения — включить в проекте: My Business Account Management API,
   My Business Business Information API, Business Profile Performance API.
3. **Новый refresh token** с добавленным scope
   `https://www.googleapis.com/auth/business.manage` (текущий токен — только
   adwords). Тот же oauth_flow (loopback), один клик владельца/робота в браузере.
4. Проверка: accounts.list → locations.list → ответ на тестовый отзыв.

## Пока API нет — рабочий режим

- Правки карточки: диктовка владельцу (чек-лист: seo/gbp-checklist.md).
- Мониторинг отзывов: владелец скидывает скриншот новых → я пишу ответы.
- Ссылка на отзыв и тейбл-тент уже в проде (print/review-tent.html).
