import { setShow } from '../../store/auth/slice';
import { Dispatch } from '@reduxjs/toolkit/react';

export const getAccountInfo = (dispatch: Dispatch) => {
  try {
    const accountInfo = JSON.parse(localStorage.getItem('accountInfo')!) as {
      username: string;
      teams: Record<string, string[]>;
      favorites: string[];
    };
    if (
      !accountInfo ||
      !accountInfo.username ||
      !accountInfo.teams ||
      !accountInfo.favorites
    ) {
      dispatch(setShow(true));
    } else {
      return accountInfo;
    }
  } catch {
    // не судьба
  }
};
