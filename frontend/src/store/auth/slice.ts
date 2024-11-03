import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../store';

// Define a type for the slice state
interface IAuthState {
  show: boolean;
}

// Define the initial state using that type
const initialState: IAuthState = {
  show: false,
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setShow: (state, action: PayloadAction<boolean>) => {
      state.show = action.payload;
    },
  },
});

export const { setShow } = authSlice.actions;

export const selectIsShow = (state: RootState) => state.auth.show;

export default authSlice.reducer;
