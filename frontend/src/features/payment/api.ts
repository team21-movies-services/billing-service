/* eslint-disable arrow-body-style */
import {
  Payment,
  PaymentWay,
  PaymentWayAlias,
  Tariff,
  TariffId,
} from './types/type';
// const API_BASE_URL = ''
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';
export const fetchLoadPaymentWays = async (): Promise<PaymentWay[]> => {
  const res = await fetch(`${API_BASE_URL}/api/v1/pay-systems`);
  return res.json();
};

export const fetchLoadTariffs = async (): Promise<Tariff[]> => {
  const res = await fetch(`${API_BASE_URL}/api/v1/tariffs`);
  return res.json();
};

export const fetchMakePayment = async (
  payWayAlias: PaymentWayAlias,
  tariffId: TariffId
): Promise<{redirect_url: string} | undefined> => {

  const res = await fetch(`${API_BASE_URL}/api/v1/subscriptions/${payWayAlias}/buy`, {
    method: 'POST',

    headers: {
      'Content-type': 'application/json',
      Authorization:
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdXRoZW50aWNhdGlvbiIsImV4cCI6MTY5NzczMzE4MywiaWF0IjoxNjk1NTczMTgzLCJyb2xlcyI6WyJzdWJzY3JpYmVyIl0sInVzZXJfaWQiOiI3ZTNkYWQ5My0xNDAxLTRjN2EtYTQwMS0xZWUwZjMzZDIwN2UiLCJpc19zdXBlcnVzZXIiOiJGYWxzZSJ9.ijEt_0T8VYEFNutSoCQLEgMUGEx_Rrk5uSHFg2uA_sQ',
    },
    body: JSON.stringify({
      tariff_id: tariffId,
      renew: true,
    }),
  });

  if (res.status === 200) {
    return res.json();
  }

  // const data = await res.json();
  // console.log(data);

};

export const fetchLoadHistory = async (): Promise<Payment[]> => {
  const res = await fetch(`${API_BASE_URL}/api/v1/payments/profile`, {
    method: 'GET',
    headers: {
      'Content-type': 'application/json',
      Authorization:
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdXRoZW50aWNhdGlvbiIsImV4cCI6MTY5NzczMzE4MywiaWF0IjoxNjk1NTczMTgzLCJyb2xlcyI6WyJzdWJzY3JpYmVyIl0sInVzZXJfaWQiOiI3ZTNkYWQ5My0xNDAxLTRjN2EtYTQwMS0xZWUwZjMzZDIwN2UiLCJpc19zdXBlcnVzZXIiOiJGYWxzZSJ9.ijEt_0T8VYEFNutSoCQLEgMUGEx_Rrk5uSHFg2uA_sQ',
    },
  });
  return res.json();
};
