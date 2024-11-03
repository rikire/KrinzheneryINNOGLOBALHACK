import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../store';

// Define a type for the slice state
interface IReposState {
  currentUser: string | null;
}

// Define the initial state using that type
const initialState: IReposState = {
  currentUser: null,
};

export const reposSlice = createSlice({
  name: 'repos',
  initialState,
  reducers: {
    setCurrentUser: (state, action: PayloadAction<string>) => {
      state.currentUser += action.payload;
    },
  },
});

export const { setCurrentUser } = reposSlice.actions;

export const selectRepos = (state: RootState) => state.repos;

export default reposSlice.reducer;
