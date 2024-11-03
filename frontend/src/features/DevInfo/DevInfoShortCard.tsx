import { useGetUserInfoQuery } from '../../store/backend/api';
import { Avatar } from './DevInfo.components/Avatar';
import { DevCompetencies } from './DevInfo.components/DevCompetencies';
import { DevCounts } from './DevInfo.components/DevCounts';
import { DevStack } from './DevInfo.components/DevStack';
import { DevTitle } from './DevInfo.components/DevTitle';

import './DevInfo.scss';

export interface DevInfoShortCardProps {
  username: string;
}

// TODO - убрать дефолтные пропсы
export const DevInfoShortCard = ({ username }: DevInfoShortCardProps) => {
  const { data, isLoading, isError } = useGetUserInfoQuery({
    username: 'rikire',
  });
  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (isError || !data) {
    return <div>{username} Error</div>;
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
