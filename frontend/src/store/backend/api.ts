import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import {
  UserRepoStat,
  UserGlobalStat,
  UserInfo,
  Summary,
  AccountInfo,
  AccountRegister,
  SearchResult,
  CommandRequest,
  RepoActivity,
} from '../../types'; // замените на путь к вашим типам

export const backendApi = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://0.0.0.0:8000/' }), // Укажите базовый URL
  endpoints: (builder) => ({
    // Получение статистики репозитория
    getRepoStat: builder.query<
      UserRepoStat,
      { username: string; owner: string; repo: string }
    >({
      query: ({ username, owner, repo }) =>
        `/stat/${username}/${owner}/${repo}`,
    }),
    // Актуализация статистики репозитория
    actualizeRepoStat: builder.query<
      UserRepoStat,
      { username: string; owner: string; repo: string }
    >({
      query: ({ username, owner, repo }) =>
        `/actualize_stat/${username}/${owner}/${repo}`,
    }),
    // Глобальная статистика пользователя
    getGlobalStat: builder.query<UserGlobalStat, { username: string }>({
      query: ({ username }) => `/global_stat/${username}`,
    }),
    // Информация о пользователе
    getUserInfo: builder.query<UserInfo, { username: string }>({
      query: ({ username }) => `/user_info/${username}`,
    }),
    // Саммари о пользователе
    getSummary: builder.query<Summary, { username: string }>({
      query: ({ username }) => `/summary/${username}`,
    }),
    // Регистрация пользователя
    registerUser: builder.mutation<AccountInfo, AccountRegister>({
      query: (body) => ({
        url: `/register`,
        method: 'POST',
        body,
      }),
    }),
    // Авторизация пользователя
    loginUser: builder.mutation<AccountInfo, AccountRegister>({
      query: (body) => ({
        url: `/login`,
        method: 'POST',
        body,
      }),
    }),
    // CRUD для команд
    postCommand: builder.mutation<void, CommandRequest>({
      query: (body) => ({
        url: `/command`,
        method: 'POST',
        body,
      }),
    }),
    // Удаление команды
    deleteCommand: builder.mutation<void, CommandRequest>({
      query: (body) => ({
        url: `/command/delete`,
        method: 'POST',
        body,
      }),
    }),
    // Поиск пользователей по компетенциям
    searchUsers: builder.query<SearchResult, { query: string }>({
      query: ({ query }) => `/search/${query}`,
    }),
    // Получение активности по коммитам (динамика)
    getCommitActivity: builder.query<
      RepoActivity,
      { username: string; repo: string }
    >({
      query: ({ username, repo }) => `/activity/${username}/${repo}`,
    }),
  }),
});

export const {
  useGetRepoStatQuery,
  useActualizeRepoStatQuery,
  useGetGlobalStatQuery,
  useGetUserInfoQuery,
  useGetSummaryQuery,
  useRegisterUserMutation,
  useLoginUserMutation,
  usePostCommandMutation,
  useDeleteCommandMutation,
  useSearchUsersQuery,
  useGetCommitActivityQuery,
} = backendApi;
