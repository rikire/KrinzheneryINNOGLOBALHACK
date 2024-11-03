import { DevInfo } from '../DeveloperCommonInfo/DeveloperCommonInfo';

const generageDataByUsername = (username: string): IDevInfoProps => {
  return {
    viewType: 'competencies',
    username,
    name: username,
    email: username + '@gmail.com',
    accountAge: getRandomNumber(),
    avatarURL:
      Math.random() > 0.5
        ? `/photo_2024-10-25_22-19-57.jpg`
        : `/photo_2023-11-16_21-08-18.jpg`,
    followers: getRandomNumber(),
    followCount: getRandomNumber(),
  };
};

export interface IDeveloperCardProps {
  username: string;
}

export const DeveloperCard = ({ username }: IDeveloperCardProps) => {
  return (
    <div className="DeveloperCard Card">
      <DevInfo {...generageDataByUsername(username)} />
    </div>
  );
};
function getRandomNumber(): number {
  return Math.floor(Math.random() * 100);
}
