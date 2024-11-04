import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../store';

// Define a type for the slice state
interface IAuthState {
  showLoginForm: boolean;
  showNewTeamForm: boolean;
}

// Define the initial state using that type
const initialState: IAuthState = {
  showLoginForm: false,
  showNewTeamForm: false,
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setShow: (state, action: PayloadAction<boolean>) => {
      state.showLoginForm = action.payload;
    },
    setShowCreateTeamForm: (state, action: PayloadAction<boolean>) => {
      state.showNewTeamForm = action.payload;
    },
  },
});

export const { setShow, setShowCreateTeamForm } = authSlice.actions;

export const selectIsShow = (state: RootState) => state.auth.showLoginForm;
export const selectIsShowCreateTeamForm = (state: RootState) =>
  state.auth.showNewTeamForm;

export default authSlice.reducer;
