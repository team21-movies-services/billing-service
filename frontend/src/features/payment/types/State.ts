import { Payment, PaymentWay, Tariff } from './type';

type State = {
  paymentWays: PaymentWay[];
  tariffs: Tariff[];
  error: undefined | string;
  history: Payment[]
};

export default State;
