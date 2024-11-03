import { AddToFavoritesButton } from './AddToFavoritesButton';
import { AddToTeamButton } from './AddToTeamButton';

export interface IDevTitleProps {
  username: string;
  name: string;
  accountAge: number;
}

export const DevTitle = ({ username, name, accountAge }: IDevTitleProps) => {
  return (
    <>
      <div className="DevInfo-Title-Username">
        <p>{username}</p>
        <AddToFavoritesButton username={username} />
        <AddToTeamButton username={username} />
      </div>
      <p className="DevInfo-Title-Name">{name}</p>
      <p className="DevInfo-Title-Age">{getAge(accountAge)}</p>
    </>
  );
};

const getAge = (mounts: number) => {
  const years = Math.floor(mounts / 12);
  const months = mounts % 12;
  return `${years} ${
    years === 1 ? 'год' : years > 5 ? 'лет' : 'года'
  } ${months} ${
    months === 1 ? 'месяц' : months < 5 ? 'месяца' : 'месяцев'
  } на GitHub`;
};
