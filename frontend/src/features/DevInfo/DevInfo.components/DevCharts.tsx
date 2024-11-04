import { useSelector } from 'react-redux';
import { Chart } from '../../../components/Charts';
import { useGetCommitActivityQuery } from '../../../store/backend/api';
import { CommitInfo, RepoActivity } from '../../../types';
import { selectRepos } from '../../../store/repos/slice';

const option = {
  tooltip: {
    trigger: 'item',
  },
  legend: {
    bottom: '5%',
    left: 'center',
  },
  series: [
    {
      top: -60,
      name: 'Access From',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      padAngle: 5,
      itemStyle: {
        borderRadius: 10,
      },
      label: {
        show: false,
        position: 'center',
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 40,
          fontWeight: 'bold',
        },
      },
      labelLine: {
        show: false,
      },
      data: [
        { value: 1048, name: 'Search Engine' },
        { value: 735, name: 'Direct' },
        { value: 580, name: 'Email' },
        { value: 484, name: 'Union Ads' },
        { value: 300, name: 'Video Ads' },
      ],
    },
  ],
};

export interface IDevChartsProps {
  username: string;
  repo: string;
}

export const DevCharts = ({ username, repo: repoDefault }: IDevChartsProps) => {
  const repo = useSelector(selectRepos);
  const currRepo = repo || repoDefault;
  const { data, isLoading, isError } = useGetCommitActivityQuery({
    username,
    repo: currRepo,
  });
  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (isError || !data) {
    return <div>{username} Error</div>;
  }
  return (
    <div className="">
      <div className="DeveloperCV-DoughnatCharts">
        <div className="DeveloperCV-ChartContainer">
          <p className="DeveloperCV-ChartHeader">Языки</p>
          <div className="DeveloperCV-Chart">
            <Chart options={option} />
          </div>
        </div>
        <div className="DeveloperCV-ChartContainer">
          <p className="DeveloperCV-ChartHeader">Стек</p>
          <div className="DeveloperCV-Chart">
            <Chart options={option} />
          </div>
        </div>
      </div>
      <div className="DeveloperCV-CandlesChart">
        <div className="DeveloperCV-Chart">
          <Chart options={getCandlesOptions(data)} />
        </div>
      </div>
    </div>
  );
};

const getCandlesOptions = (data: RepoActivity) => {
  return {
    title: {
      text: 'Динамика изменения кода в репозитории',
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
      formatter: function (params) {
        let tar;
        if (params[1] && params[1].value !== '-') {
          tar = params[1];
        } else {
          tar = params[2];
        }
        return tar && tar.name + '<br/>' + tar.seriesName + ' : ' + tar.value;
      },
    },
    legend: {
      data: ['Добавлено', 'Удалено'],
      right: 0,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: data.commits.map((commit) => commit.commit_date),
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: 'Placeholder',
        type: 'bar',
        stack: 'Total',
        silent: true,
        itemStyle: {
          borderColor: 'transparent',
          color: 'transparent',
        },
        emphasis: {
          itemStyle: {
            borderColor: 'transparent',
            color: 'transparent',
          },
        },
        // data: [0, 900, 1245, 1530, 1376, 1376, 1511, 1689, 1856, 1495, 1292],
        data: getSums(data.commits),
      },
      {
        name: 'Добавлено',
        type: 'bar',
        stack: 'Total',
        label: {
          show: true,
          position: 'top',
        },
        data: data.commits.map((commit) =>
          commit.additions - commit.deletions > 0
            ? commit.additions - commit.deletions
            : '-',
        ),
      },
      {
        name: 'Удалено',
        type: 'bar',
        stack: 'Total',
        label: {
          show: true,
          position: 'bottom',
        },
        data: data.commits.map((commit) =>
          commit.deletions - commit.additions > 0
            ? commit.deletions - commit.additions
            : '-',
        ),
      },
    ],
  };
};

function getSums(commits: CommitInfo[]) {
  let currentSum = 0;
  const result: number[] = [currentSum];
  commits.forEach((commit) => {
    currentSum += commit.additions - commit.deletions;
    result.push(currentSum);
  });

  return result;
}
