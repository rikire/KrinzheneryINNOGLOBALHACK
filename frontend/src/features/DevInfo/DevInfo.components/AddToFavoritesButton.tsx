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
      dispatch(setShow(true));
    } else {
      if (checkIsDeveloperInFavorites(username, accountInfo.favorites)) {
        setIsActive(true);
        // TODO: добавлять по клику в избранное
      }
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
