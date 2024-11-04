import { setShow } from '../../store/auth/slice';
import { Dispatch } from '@reduxjs/toolkit/react';

export const getAccountInfo = (dispatch: Dispatch) => {
  try {
    const accountInfo = JSON.parse(localStorage.getItem('accountInfo')!) as {
      login: string;
      command_list: Record<string, string[]>;
      favorites: string[];
    };

    if (
      !accountInfo ||
      !accountInfo.login ||
      !Array.isArray(accountInfo.command_list) ||
      !Array.isArray(accountInfo.favorites)
    ) {
      dispatch(setShow(true));
    } else {
      return accountInfo;
    }
  } catch {
    // не судьба
  }
};
