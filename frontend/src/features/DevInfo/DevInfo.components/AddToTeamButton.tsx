import { useDispatch } from 'react-redux';
import AddToComandsSVG from '../../../shared/icons/AddToComand';
import { setShowCreateTeamForm } from '../../../store/auth/slice';
import { getAccountInfo } from '../../../shared/utils/getAccountInfo';
import { ClickTooltip } from '../../../components/Tooltip';

interface AddToTeamButtonProps {
  username: string;
}

export const AddToTeamButton: React.FC<AddToTeamButtonProps> = ({
  username,
}) => {
  const dispatch = useDispatch();
  let accountInfo = null;
  if (localStorage.getItem('accountInfo') === null) {
    accountInfo = getAccountInfo(dispatch);
  }
  return (
    <ClickTooltip position="bottom" tooltipContent={<Tooltip />}>
      <div
        className={
          'AddToTeamButton' +
          (accountInfo &&
          checkIsDeveloperInAnyTeam(username, accountInfo?.command_list)
            ? '_active'
            : '')
        }>
        <AddToComandsSVG height={26} width={26} />
      </div>
    </ClickTooltip>
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

const Tooltip = () => {
  const dispatch = useDispatch();
  const accountInfo = getAccountInfo(dispatch);
  const teams = Object.keys(accountInfo?.command_list || {});

  // TODO проверить произошла ли ошибка и добавился ли новый юзер
  const handleClick = (team: string) => {
    fetch('http://0.0.0.0:8000/command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ login: accountInfo?.login, command: team }),
    })
      .then((response) =>
        response.ok ? response.json() : Promise.reject(response),
      )
      .then((data) => {
        localStorage.setItem('accountInfo', JSON.stringify(data));
      })
      .catch((error) => console.error('Error logging out:', error));
  };
  return (
    <div>
      {teams.length ? (
        teams.map((t) => (
          <button className={'AddToTeamButton'} onClick={() => handleClick(t)}>
            {t}
          </button>
        ))
      ) : (
        <p>Еще нет команд.</p>
      )}

      <button onClick={() => dispatch(setShowCreateTeamForm(true))}>
        Создать новую команду
      </button>
    </div>
  );
};
