import { configureStore } from '@reduxjs/toolkit';
import { reposApi } from './repos/api';
import { backendApi } from './backend/api';
import reposReduser from './repos/slice';

export const store = configureStore({
  reducer: {
    repos: reposReduser,
    [backendApi.reducerPath]: backendApi.reducer,
    [reposApi.reducerPath]: reposApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat([reposApi.middleware, backendApi.middleware]),
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch;
