import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { RootState, useAppDispatch } from '../../redux/store';
import { loadHistory, loadPaymentWays, loadTariffs } from './paymentSlice';
// import './styles/style.scss';
import './styles/style.css';
import * as api from './api';
import PaymentHistory from './PaymentHistory';

function PaymentPage(): JSX.Element {
  const [tariffSelected, setTariffSelected] = useState('');
  const [paymentWaySelected, setPaymentWaySelected] = useState('');
  const [showHistory, setShowHistory] = useState(false);
  const [autoProlongation, setAutoProlongation] = useState(false);

  const paymentWays = useSelector(
    (store: RootState) => store.payment.paymentWays
  );
  const tariffs = useSelector((store: RootState) => store.payment.tariffs);

  const handlePayment: React.FormEventHandler<HTMLFormElement> = async (
    event
  ) => {
    event.preventDefault();
    const data = await api.fetchMakePayment(paymentWaySelected, tariffSelected);
    if (data) {
      window.location.replace(data.redirect_url);
    }
  };

  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(loadPaymentWays());
    dispatch(loadTariffs());
  }, []);

  useEffect(() => {
    if (paymentWays.length) setPaymentWaySelected(paymentWays[0].alias);
  }, [paymentWays]);

  return (
    <>
      <div className="container cont">
        <div className="container__header cont">
          <h1 className="bold_word">Payment</h1>
        </div>
        <div className="container__main cont " style={{ display: 'flex' }}>
          <div className="container__main__membership cont">
            <h2 className="bold_word">Membership</h2>
            <button className="btn" type="button">
              Cancel Membership
            </button>

            <button
              type="button"
              className="btn"
              onClick={() => setShowHistory((prev) => !prev)}>
              {showHistory ? 'Hide payments history' : 'Show payments history'}
            </button>
          </div>
          <div className="container__main__form cont">
            <h2 className="bold_word">Payment form</h2>
            <form onSubmit={handlePayment}>
              <select
                required
                onChange={(event) => setTariffSelected(event.target.value)}>
                <option disabled selected>
                  Выберите тарифный план
                </option>
                {tariffs.map((el) => (
                  <option key={el.id} value={el.id}>
                    {`${el.name} - ${el.cost} per ${el.period} ${el.period_unit}`}
                  </option>
                ))}
              </select>
              <br />
              <p>Выберите способ оплаты</p>
              {paymentWays.map((el) => (
                <label key={el.id} htmlFor={`paymentWay-${el.alias}`}>
                  <input
                    key={el.id}
                    type="radio"
                    id={`paymentWay-${el.alias}`}
                    name="paymentWay"
                    checked={paymentWaySelected === el.alias}
                    value={el.alias}
                    onChange={(event) =>
                      setPaymentWaySelected(event.target.value)
                    }
                    required
                  />
                  {el.name}{' '}
                </label>
              ))}
              <p>
                {`к оплате: ${
                  tariffs.length && tariffSelected.length
                    ? tariffs.filter((el) => el.id === tariffSelected)[0].cost
                    : ''
                }`}
              </p>
              <label>
                <input
                  className="checkbox"
                  type="checkbox"
                  checked={autoProlongation}
                  onChange={() => setAutoProlongation((prev) => !prev)}
                />
                автопродление
              </label>
              <button className="btn" type="submit">
                Оплатить
              </button>
            </form>
          </div>
        </div>
      </div>
      {showHistory && <PaymentHistory />}
    </>
  );
}

export default PaymentPage;
