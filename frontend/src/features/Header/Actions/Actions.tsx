import TeamSVG from '../../../shared/icons/Teams';
import FireSVG from '../../../shared/icons/FireOutlined';
import AuthSVG from '../../../shared/icons/Login';
import { useState } from 'react';
import { Auth } from '../../Auth/Auth';

const teams: string[] = [
  'frontend',
  'backend',
  'devops',
  'data_science',
  'mobile',
  'embedded',
  'gamedev',
];

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
      <ActionsMain
        viewType={current}
        close={() => setCurrent(null)}
        items={teams}
      />
    </div>
  );
};

interface ActionsMainProps {
  viewType: IViewType;
  items: string[];
  close: () => void;
}

const ActionsMain = ({ viewType, items, close }: ActionsMainProps) => {
  if (!viewType) return null;
  let actionButton = null;
  let icon = null;
  if (viewType === 'teams') {
    actionButton = (
      <button className="Actions-MainButton">+ Создать новую</button>
    );
    icon = <TeamSVG height={20} width={20} />;
  } else if (viewType === 'favorites') {
    icon = <FireSVG height={20} width={20} />;
  }
  return (
    <Auth cancel={close}>
      <div className="Actions-Main">
        <p className="Actions-MainHeader">
          {viewType === 'auth'
            ? 'Авторизация'
            : viewType === 'favorites'
            ? 'Избранное'
            : 'Команды'}
        </p>
        <ul className="Actions-MainItems">
          {items.map((item) => (
            <li key={item} className="Actions-MainItem">
              {icon}
              <p className="Actions-MainItemText">{item}</p>
            </li>
          ))}
        </ul>
        {actionButton}
      </div>
    </Auth>
  );
};
