import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../store';

// Define a type for the slice state
interface IReposState {
  currRepo: string | null;
}

// Define the initial state using that type
const initialState: IReposState = {
  currRepo: null,
};

export const reposSlice = createSlice({
  name: 'repos',
  initialState,
  reducers: {
    setCurrRepo: (state, action: PayloadAction<string>) => {
      state.currRepo = action.payload;
    },
  },
});

export const { setCurrRepo } = reposSlice.actions;

export const selectRepos = (state: RootState) => state.repos.currRepo;

export default reposSlice.reducer;
