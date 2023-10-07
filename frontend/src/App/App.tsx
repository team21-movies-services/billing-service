import React from 'react';
import './App.css';
import PaymentPage from '../features/payment/PaymentPage';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

function App(): JSX.Element {
  return <PaymentPage />;
}

export default App;
