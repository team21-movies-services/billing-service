import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { RootState, useAppDispatch } from '../../redux/store';
import { loadHistory } from './paymentSlice';
import './styles/style.css';

function PaymentHistory(): JSX.Element {
  const history = useSelector((store: RootState) => store.payment.history);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(loadHistory());
  }, []);
  return (
    <>
      <div className="container cont">
        <table className="history__table">
          <thead>
            <tr>
              <th>сумма</th>
              <th>валюта</th>
              <th>платежная система</th>
              <th>статус</th>
            </tr>
          </thead>
          <tbody>
            {history.map((el) => (
              <tr key={el.id}>
                <td>{el.amount}</td>
                <td>{el.currency_code}</td>
                <td>{el.pay_system}</td>
                <td>{el.pay_status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      ;
    </>
  );
}

export default React.memo(PaymentHistory);
