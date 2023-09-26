from shared.database.models.tariff import Tariff
from sqladmin import ModelView


class TariffsAdminView(ModelView, model=Tariff):  # type: ignore
    name_plural = 'Тарифы'

    column_list = [
        Tariff.name,
        Tariff.cost,
        Tariff.period,
        Tariff.period_unit,
        Tariff.json_sale,
    ]

    column_labels = {
        Tariff.id: "ID записи",
        Tariff.alias: "Алиас для обращения в коде",
        Tariff.name: "Название",
        Tariff.cost: "Стоимость",
        Tariff.period: "Период действия",
        Tariff.period_unit: "Единица измерения периода",
        Tariff.json_sale: "Скидки на тариф",
        Tariff.updated_at: "Дата создания записи",
        Tariff.created_at: "Дата обновления записи",
    }
