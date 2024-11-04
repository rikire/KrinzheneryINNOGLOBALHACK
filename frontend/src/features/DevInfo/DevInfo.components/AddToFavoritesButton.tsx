import { useDispatch } from 'react-redux';
import AddToFavoritessSVG from '../../../shared/icons/FireOutlined';
import { setShow } from '../../../store/auth/slice';
import { useState } from 'react';
import { getAccountInfo } from '../../../shared/utils/getAccountInfo';

interface AddToFavoritesButtonProps {
  username: string;
}

export const AddToFavoritesButton: React.FC<AddToFavoritesButtonProps> = ({
  username,
}) => {
  const dispatch = useDispatch();
  const [isActive, setIsActive] = useState(false);

  const handleClick = () => {
    const accountInfo = getAccountInfo(dispatch);
    if (!accountInfo) {
      dispatch(setShow(true)); // открыть форму авторизации
    } else {
      const isFavorite = checkIsDeveloperInFavorites(
        username,
        accountInfo.favorites,
      );
      setIsActive(!isFavorite);
      // TODO проверить произошла ли ошибка и добавился ли новый юзер
      fetch('http://0.0.0.0:8000/favorite/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          login: accountInfo.login,
          favorites: isFavorite
            ? accountInfo.favorites.filter((item) => item !== username)
            : [...accountInfo.favorites, username],
        }),
      })
        .then((response) =>
          response.ok ? response.json() : Promise.reject(response),
        )
        .then((data) => {
          localStorage.setItem('accountInfo', JSON.stringify(data));
        })
        .catch((error) => console.error('Error updating favorites:', error));
    }
  };

  return (
    <button
      onClick={handleClick}
      className={'AddToFavoritesButton' + (isActive ? '_active' : '')}>
      <AddToFavoritessSVG
        height={26}
        width={26}
        fill={isActive ? '#ff4d4f' : '#7d7d7d'}
      />
    </button>
  );
};

const checkIsDeveloperInFavorites = (username: string, favorites: string[]) => {
  if (favorites.includes(username)) {
    return true;
  }
  return false;
};
