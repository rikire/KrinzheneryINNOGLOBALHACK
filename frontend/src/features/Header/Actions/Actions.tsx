import TeamSVG from '../../../shared/icons/Teams';
import FireSVG from '../../../shared/icons/FireOutlined';
import AuthSVG from '../../../shared/icons/Login';
import { useState } from 'react';
import { getAccountInfo } from '../../../shared/utils/getAccountInfo';
import { useDispatch } from 'react-redux';
import { setShowCreateTeamForm } from '../../../store/auth/slice';

type IViewType = 'teams' | 'favorites' | 'auth' | null;

export const Actions = () => {
  const [current, setCurrent] = useState<IViewType>(null);
  return (
    <div className="Actions">
      <button className="Actions-Button" onClick={() => setCurrent('teams')}>
        <TeamSVG />
      </button>
      <button
        className="Actions-Button"
        onClick={() => setCurrent('favorites')}>
        <FireSVG />
      </button>
      <button className="Actions-Button" onClick={() => setCurrent('auth')}>
        <AuthSVG />
      </button>
      <ActionsMain viewType={current} />
    </div>
  );
};

interface ActionsMainProps {
  viewType: IViewType;
}

const ActionsMain = ({ viewType }: ActionsMainProps) => {
  const dispatch = useDispatch();

  if (!viewType) return null;

  const accountInfo = getAccountInfo(dispatch);

  const items =
    viewType === 'teams'
      ? Object.keys(accountInfo?.command_list || {})
      : viewType === 'favorites'
      ? accountInfo?.favorites
      : [accountInfo?.login];

  let actionButton = null;
  let icon = null;

  if (viewType === 'teams') {
    actionButton = (
      <button
        className="Actions-MainButton"
        onClick={() => {
          dispatch(setShowCreateTeamForm(true));
        }}>
        + Создать новую
      </button>
    );
    icon = <TeamSVG height={20} width={20} />;
  } else if (viewType === 'favorites') {
    icon = <FireSVG height={20} width={20} />;
  }
  return (
    <div className="Actions-Main">
      <p className="Actions-MainHeader">
        {viewType === 'auth'
          ? 'Авторизация'
          : viewType === 'favorites'
          ? 'Избранное'
          : 'Команды'}
      </p>
      <ul className="Actions-MainItems">
        {items?.map((item) => (
          <li key={item} className="Actions-MainItem">
            {icon}
            <p className="Actions-MainItemText">{item}</p>
          </li>
        ))}
      </ul>
      {actionButton}
    </div>
  );
};
