# Результаты дипломной работы

Ссылка на репозиторий - https://github.com/team21-movies-services/billing-service

Архитектурная схема проекта - https://miro.com/app/board/uXjVNdKG4aU=/?share_link_id=151324860603

В рамках дипломной работы был разработана система биллинга для онлайн-кинотеатра.

## Технологии:

1. В качестве backend фрейморка использовался Fastapi.
2. В качестве внешнего платежного шлюза использовалась [ЮKassa](https://promo.yookassa.ru/one_ruble). Это позволяет избежать хранения данных платежных карт непосредственно в сервисе биллинга. В архитектуру проекта также заложено подключение других различных платежных систем например [CloudPayments](https://cloudpayments.ru/), [Rocket Money](https://www.rocketmoney.com/) и т.п.
3. Для выполнения выполнения фоновых задач по обновлениям статусов платежей, деактивация просроченных подписок, автопродление подписок был разработан и внедрен планировщик заданий на основе библиотеки [scheduler](https://pypi.org/project/scheduler/). Запуск осуществляется изолированно в рамках docker контейнера с возможностью масштабирования.
4. EventService отправляет события на API **event-service**, который кладёт события в кафку, чтобы в дальнейшем **auth-service** и **notify-service** смогли учесть новые изменения.


## Эндпоинты и схема взаимодействия

![Schema](./doc/Endpoints.png)

1. Оплата подписки пользователя - https://github.com/team21-movies-services/billing-service/blob/main/src/app/api/routers/v1/subscriptions.py#L17
2. Текущая подписка пользователя - https://github.com/team21-movies-services/billing-service/blob/main/src/app/api/routers/v1/subscriptions.py#L37
3. Отмена автопродления подписки - https://github.com/team21-movies-services/billing-service/blob/main/src/app/api/routers/v1/subscriptions.py#L50
4. Список поддерживаемых систем оплат - https://github.com/team21-movies-services/billing-service/blob/main/src/app/api/routers/v1/pay_systems.py#L19
5. Список тарифов - https://github.com/team21-movies-services/billing-service/blob/main/src/app/api/routers/v1/tariffs.py#L19
6. История пользовательских платежей - https://github.com/team21-movies-services/billing-service/blob/main/src/app/api/routers/v1/payments.py#L26

## Выполнение фоновых задач

![Schema](./doc/Worker.png)


1. Автоматическое обновление статусов платежа c активацией подписок - https://github.com/team21-movies-services/billing-service/blob/main/src/worker/services/payment.py#L24
2. Деактивация просроченных подписок - https://github.com/team21-movies-services/billing-service/blob/main/src/worker/services/subscription.py#L25
3. Автопродление подписок с автоматическими платежами - https://github.com/team21-movies-services/billing-service/blob/main/src/worker/services/subscription.py#L34


## Схема базы данных

Ссылка - https://drive.google.com/file/d/1vjEMku2iBeXOBpgojDEb3eaz7e-r1w4M/view?usp=sharing

![Schema](./doc/DB.png)

Авторы:

* [Михаил Спиридонов](https://github.com/mspiridonov2706)
* [Леонид Баxметьев](https://github.com/leonidbkh)
* [Павел Xрамов](https://github.com/KhramovKhramov)
* [Ярослав Орлов](https://github.com/Avis20)

