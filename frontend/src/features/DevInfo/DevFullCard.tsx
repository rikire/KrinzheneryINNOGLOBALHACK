import { TagCarousel } from '../../components/TagCarousel';
import { useGetUserInfoQuery } from '../../store/backend/api';
import { Avatar } from './DevInfo.components/Avatar';
import { DevCharts } from './DevInfo.components/DevCharts';
import { DevCommonStats } from './DevInfo.components/DevCommonStats';
import { DevCompetencies } from './DevInfo.components/DevCompetencies';
import { DevCompetenciesTrees } from './DevInfo.components/DevCompetenciesTrees';
import { DevCounts } from './DevInfo.components/DevCounts';
import { DevStack } from './DevInfo.components/DevStack';
import { DevSubtitle } from './DevInfo.components/DevSubtitle';
import { DevTitle } from './DevInfo.components/DevTitle';

import './DevInfo.scss';

export interface DevFullCardProps {
  username: string;
}

export const DevFullCard = ({ username }: DevFullCardProps) => {
  const { data, isLoading, isError } = useGetUserInfoQuery({
    username,
  });
  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (!data || isError) {
    return <div>{username} Error</div>;
  }
  return (
    <div className="DevFullCard Card">
      <div className="DevFullCard-Header">
        <Avatar avatarURL={data?.avatar_url} />
        <div className="DevFullCard-HeaderMain">
          <DevTitle
            username={username}
            name={data?.name}
            accountAge={data?.account_age}
          />
          <DevSubtitle
            email={data.email}
            followCount={data.following}
            followers={data.followers}
          />
        </div>

        <div className="DevFullCard-HeaderStats">
          {/* TODO: прокинуть компетенции */}
          <DevCompetencies competencies={['frontend', 'backend', 'devops']} />
          <DevCounts
            countTeamProjects={data?.team_projects}
            countSoloProjects={data?.solo_projects}
          />
        </div>
      </div>
      <div className="DevFullCard-Stack">
        {/* TODO: прокинуть стек */}
        <DevStack
          stack={[
            'react',
            'angular',
            'vue',
            'svelte',
            'next',
            'nuxt',
            'gatsby',
          ]}
        />
      </div>

      <div className="Divider" />
      <div style={{ textAlign: 'justify' }}>
        {/* TODO: прокинуть описание пользователя Lamma */}
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Eius, beatae
        aut! Nesciunt placeat natus, earum odio, commodi deserunt necessitatibus
        omnis asperiores est praesentium eos. Quibusdam, voluptatum? Dolorem
        earum ducimus ullam. Lorem ipsum dolor sit amet consectetur adipisicing
        elit. Nobis quis, iste, explicabo eos optio quo asperiores consequatur
        ipsa soluta, magni ratione cum reiciendis. Nihil dicta deserunt
        reiciendis, eveniet repellendus quaerat! Lorem ipsum dolor sit amet,
        consectetur adipisicing elit. Animi error natus et eaque labore qui quod
        veritatis, possimus rerum cumque alias est, minima quia sit atque
        maiores quaerat iure eveniet!
      </div>
      <div className="Divider" />

      <DevCompetenciesTrees
        competencies={[]}
        stack={[]}
        languages={[]}
        ghFeatures={[]}
      />

      <div className="Divider" />

      <DevCommonStats
        commitsAmount={data.total_commits}
        averageCommitSize={0}
        commitsPerDay={0}
        commitsPerWeek={0}
        commitsPerMonth={0}
        commitsPerYear={0}
      />

      <div className="Divider" />
      <div className="DeveloperCV-ReposCarousel">
        <TagCarousel tags={data.repos} />
      </div>
      <DevCharts username={username} repo={'Ten-Do/EBUS'} />
    </div>
  );
};
