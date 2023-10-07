import { PaymentWay } from './type';

type Action =
  | { type: 'payment/loadPaymentWays'; payload: PaymentWay[] }
  | { type: 'payment/makePayment' };

export default Action;
