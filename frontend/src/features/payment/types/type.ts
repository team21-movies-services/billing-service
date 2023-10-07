export type PaymentWay = {
  id: string;
  name: string;
  alias: string;
  currency_code: string;
  json_data: object;
};

export type PaymentWayAlias = PaymentWay['alias']

export type Tariff = {
  id: string;
  name: string;
  alias: string;
  cost: number;
  period: number;
  period_unit: string;
  json_sale: {};
};

export type TariffId = Tariff['id'];

export type Payment = {
  id: string;
  amount: number;
  pay_system: string,
  currency_code: string,
  pay_status: string,
  purpose: string,
  payment_id: string,
  json_sale: {};
};
