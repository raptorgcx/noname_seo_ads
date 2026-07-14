# GBP API — программный доступ к карточке

Свежесть: 2026-07-14. Статус: робот = Менеджер профиля (владелец добавил, инвайт принят).
Правки карточки пока идут «под диктовку»; этот файл — путь к автономии (ответы на
отзывы, посты, часы — кодом).

## Почему нельзя «просто подключиться»

Business Profile APIs (My Business *) — закрытые: любой Cloud-проект получает
**квоту 0** до одобрения заявки. Это та же история, что Basic Access в Ads API,
только форма другая. Без одобрения все вызовы падают 429 RESOURCE_EXHAUSTED.

## План (когда дойдут руки — не блокер)

1. **Заявка на доступ**: https://developers.google.com/my-business/content/prereqs
   → «Request access to the API» (форма). Заполнять от робота
   (noname.seo.bot@gmail.com), Cloud-проект тот же, что для Ads API
   («My First Project» робота, номер проекта — в Cloud Console).
   Черновики ответов: business = BUCHARESTCLOUDS S.R.L. (CUI 49299704), один
   собственный профиль (NO NAME Lounge, București), use case = управление
   собственной карточкой: ответы на отзывы, обновление часов/атрибутов, посты.
   НЕ агентство, НЕ сторонние профили.
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
