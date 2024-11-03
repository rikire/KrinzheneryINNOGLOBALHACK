import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export interface IStat {
  average_commit_size: number;
  commits_per_day: number;
  commits_per_week: number;
  commits_per_year: number;
  commits_total: number;
  competencies: string[];
  languages: {
    [key: string]: number;
  }[];
  score: {
    [key: string]: number;
  }[];
  stack: string[];
  username: string;
  using_github_features: string[];

  contributed_repos: number;
  public_repos: number;
}

export interface IGlobalStat extends IStat {
  contributed_repos: number;
  public_repos: number;
}

export interface IRepoStat extends IStat {
  name: string;
  url: string;
}

export interface IRepos {
  global_stat: IGlobalStat;
  repositories: IRepoStat[];
  username: string;
}

export const reposApi = createApi({
  reducerPath: 'reposApi',
  baseQuery: fetchBaseQuery({ baseUrl: 'https://pokeapi.co/repo/' }),
  endpoints: (builder) => ({
    getReposByUserName: builder.query<IRepos, string>({
      query: (name) => `${name}`,
    }),
  }),
});

// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const { useGetReposByUserNameQuery } = reposApi;
