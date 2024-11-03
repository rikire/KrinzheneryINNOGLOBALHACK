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
export const DevInfoShortCard = () => {
  const props = defaultProps;
  console.log(props);
  return (
    <div className="DevInfoShortCard Card">
      <Avatar avatarURL={props.avatarURL} />
      <div className="DevInfoShortCard-Info">
        <DevTitle
          username={props.username}
          name={props.name}
          accountAge={props.accountAge}
        />
        <DevCounts
          countTeamProjects={props.countTeamProjects}
          countSoloProjects={props.countSoloProjects}
        />
      </div>
      <div className="DevInfoShortCard-Stats">
        <DevCompetencies competencies={props.competencies} />
        <DevStack stack={props.stack} />
      </div>
    </div>
  );
};
