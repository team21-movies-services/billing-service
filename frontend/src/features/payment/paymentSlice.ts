import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import State from './types/State';
import * as api from './api';
import { PaymentWayAlias, TariffId } from './types/type';

const initialState: State = {
  paymentWays: [],
  tariffs: [],
  history: [],
  error: undefined,
};

export const loadPaymentWays = createAsyncThunk('payment/loadPaymentWays', () =>
  api.fetchLoadPaymentWays()
);

export const loadTariffs = createAsyncThunk('payment/loadTariffs', () =>
  api.fetchLoadTariffs()
);

export const loadHistory = createAsyncThunk('payment/loadHistory', () =>
  api.fetchLoadHistory()
);

// export const makePayment = createAsyncThunk(
//   'payment/makePayment',
//   (payWayAlias: PaymentWayAlias, tariffId: TariffId) =>
//     api.fetchMakePayment(payWayAlias, tariffId)
// );

const paymentSlice = createSlice({
  name: 'payment',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(loadPaymentWays.fulfilled, (state, action) => {
        state.paymentWays = action.payload;
      })
      .addCase(loadPaymentWays.rejected, (state, action) => {
        state.error = action.error.message;
      })
      .addCase(loadTariffs.fulfilled, (state, action) => {
        state.tariffs = action.payload;
      })
      .addCase(loadTariffs.rejected, (state, action) => {
        state.error = action.error.message;
      })
      .addCase(loadHistory.fulfilled, (state, action) => {
        state.history = action.payload;
      })
      .addCase(loadHistory.rejected, (state, action) => {
        state.error = action.error.message;
      });
  },
});

export default paymentSlice.reducer;
