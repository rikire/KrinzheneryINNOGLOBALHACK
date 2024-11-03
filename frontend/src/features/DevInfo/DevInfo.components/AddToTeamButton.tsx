import { useDispatch } from 'react-redux';
import AddToComandsSVG from '../../../shared/icons/AddToComand';
import { setShow } from '../../../store/auth/slice';
import { useState } from 'react';
import { getAccountInfo } from '../../../shared/utils/getAccountInfo';

interface AddToTeamButtonProps {
  username: string;
}

export const AddToTeamButton: React.FC<AddToTeamButtonProps> = ({
  username,
}) => {
  const dispatch = useDispatch();
  const [isActive, setIsActive] = useState(false);

  const handleClick = () => {
    const accountInfo = getAccountInfo(dispatch);
    if (!accountInfo) {
      dispatch(setShow(true));
    } else {
      if (checkIsDeveloperInAnyTeam(username, accountInfo.teams)) {
        setIsActive(true);
      }
    }
  };

  return (
    <button
      onClick={handleClick}
      className={'AddToTeamButton' + (isActive ? '_active' : '')}>
      <AddToComandsSVG height={26} width={26} />
    </button>
  );
};

const checkIsDeveloperInAnyTeam = (
  username: string,
  teams: Record<string, string[]>,
) => {
  for (const team in teams) {
    if (teams[team].includes(username)) {
      return true;
    }
  }
  return false;
};
