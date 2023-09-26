from shared.database.models.tariff import Tariff
from sqladmin import ModelView


class TariffsAdminView(ModelView, model=Tariff):  # type: ignore
    column_list = [
        Tariff.id,
        Tariff.name,
        Tariff.cost,
        Tariff.period,
        Tariff.period_unit,
        Tariff.json_sale,
    ]
