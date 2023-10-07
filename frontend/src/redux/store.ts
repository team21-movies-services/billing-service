import { configureStore } from '@reduxjs/toolkit';
import { useDispatch } from 'react-redux';
import paymentSlice from '../features/payment/paymentSlice';

const store = configureStore({
  reducer: {
    payment: paymentSlice,
  },
});

export type AppDispatch = typeof store.dispatch;
export const useAppDispatch: () => AppDispatch = useDispatch;

export type RootState = ReturnType<typeof store.getState>;
export default store;
