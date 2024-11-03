import { useGetUserInfoQuery } from '../../store/backend/api';
import { UserInfo } from '../../types';
import { Avatar } from './DevInfo.components/Avatar';
import { DevCompetencies } from './DevInfo.components/DevCompetencies';
import { DevCounts } from './DevInfo.components/DevCounts';
import { DevStack } from './DevInfo.components/DevStack';
import { DevTitle } from './DevInfo.components/DevTitle';

import './DevInfo.scss';

const defaultProps = {
  username: 'Ten-Do',
  name: 'Руденко Юрий',
  accountAge: 40,
  avatarURL: '/photo_2024-10-25_22-19-57.jpg',
  followers: 0,
  followCount: 0,
  stack: ['react', 'vue', 'node', 'django', 'flask', 'spring'],
  competencies: ['frontend', 'backend', 'devops', 'data_science', 'qa'],
  countTeamProjects: 0,
  countSoloProjects: 0,
};

// TODO - убрать дефолтные пропсы
export const DevInfoShortCard = ({ username = 'Ten-Do' }) => {
  const { data, isLoading, isError } = useGetUserInfoQuery({
    username: 'Ten-Do',
  });
  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (isError) {
    return <div>Всё. Тю - Тю...</div>;
  }
  return (
    <div className="DevInfoShortCard Card">
      <Avatar avatarURL={data?.avatar_url} />
      <div className="DevInfoShortCard-Info">
        <DevTitle
          username={username}
          name={data?.name}
          accountAge={data?.account_age}
        />
        <DevCounts
          countTeamProjects={data?.team_projects}
          countSoloProjects={data?.solo_projects}
        />
      </div>
      <div className="DevInfoShortCard-Stats">
        <DevCompetencies competencies={defaultProps.competencies} />
        <DevStack stack={defaultProps.stack} />
      </div>
    </div>
  );
};

const data: UserInfo = {
  username: 'Ten-Do',
  name: null,
  email: null,
  team_projects: 0,
  solo_projects: 13,
  solo_gist: 0,
  account_age: 2,
  avatar_url: 'https://avatars.githubusercontent.com/u/107281193?v=4',
  html_url: 'https://github.com/Ten-Do',
  followers: 0,
  following: 0,
  repos: [
    'Ten-Do/B2P',
    'Ten-Do/B2P_admin',
    'Ten-Do/B2P_S',
    'Ten-Do/ctf_admin',
    'Ten-Do/cyberpolygon_client',
    'Ten-Do/EBUS',
    'Ten-Do/EBUS_edrive',
    'Ten-Do/ebus_emap',
    'Ten-Do/hackich',
    'Ten-Do/MAGHACK',
    'Ten-Do/ToDoList',
    'Ten-Do/trsis-3',
    'Ten-Do/ymap3-components',
  ],
};
console.log(data);
