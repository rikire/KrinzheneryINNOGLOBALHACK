import React from 'react';
import { DeveloperCommonInfo } from '../DeveloperCommonInfo/DeveloperCommonInfo';
import { Tag } from '../../components/Tag';
import { TreeList } from '../../components/TreeList';
import { TagCarousel } from '../../components/TagCarousel';
import { Chart } from '../../components/Charts';

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

const scores: string[] = [
  'frontend',
  'backend',
  'devops',
  'data_science',
  'qa',
  'mobile',
  'embedded',
  'gamedev',
  'design',
  'management',
  'product',
  'marketing',
  'python',
  'java',
  'c++',
  'c#',
  'kotlin',
  'go',
  'rust',
  'javascript',
  'typescript',
  'scala',
  'php',
  'ruby',
];

const generateRandomNumber = () => Math.floor(Math.random() * 100);

const DESC =
  'Lorem ipsum dolor sit amet consectetur adipisicing elit. Minima voluptate expedita at culpa, nobis qui laudantium rem enim rerum eveniet dolorum quidem? Soluta labore vero, dolorem hic fugit neque itaque.';

export const DeveloperCV = () => {
  return (
    <div className="Card DeveloperCV">
      <DeveloperCommonInfo
        viewType={''}
        username={'Ten-Do'}
        name={'Руденко Юрий'}
        email={'rydenko.urii@mail.ru'}
        accountAge={40}
        avatarURL={
          Math.random() > 0.5
            ? '/photo_2023-11-16_21-08-18.jpg'
            : '/photo_2024-10-25_22-19-57.jpg'
        }
        followers={0}
        followCount={0}
      />
      <div className="DeveloperCV-Scores">
        {scores.map((score) => (
          <Tag key={score} view={'default'}>
            {score}
          </Tag>
        ))}
      </div>

      <div className="DeveloperCV-Divider" />

      <p className="DeveloperCV-Description">
        {DESC + ' ' + DESC + ' ' + DESC}
      </p>

      <div className="DeveloperCV-Divider" />

      <div className="DeveloperCV-Lists">
        <div>
          <p className="DeveloperCV-ListHeader">Компетенции</p>
          <TreeList items={scores.slice(0, 6)} />
        </div>
        <div>
          <p className="DeveloperCV-ListHeader">Языки</p>
          <TreeList items={scores.slice(6, 15)} />
        </div>
        <div>
          <p className="DeveloperCV-ListHeader">Стек</p>
          <TreeList items={scores.slice(15, 20)} />
        </div>
        <div>
          <p className="DeveloperCV-ListHeader">Инструменты GitHub</p>
          <TreeList items={scores.slice(20, 24)} />
        </div>
      </div>

      <div className="DeveloperCV-Divider" />

      <div className="DeveloperCV-Stats">
        <div className="DeveloperCV-CommonStats">
          <p className="DeveloperCV-StatTitle">Общая статистика</p>
          <p className="DeveloperCV-CommonStat">
            Средний размер коммита - {generateRandomNumber()}
          </p>
          <p className="DeveloperCV-CommonStat">
            Общее число коммитов - {generateRandomNumber()}
          </p>
        </div>
        <div className="DeveloperCV-AverageStats">
          <p className="DeveloperCV-StatTitle">В среднем коммитов</p>
          <div className="DeveloperCV-AverageStatsWrapper">
            <div className="DeveloperCV-AverageStat">
              <p className="DeveloperCV-AverageStatValue">
                {generateRandomNumber()}
              </p>
              <p className="DeveloperCV-AverageStatLabel">за день</p>
            </div>
            <div className="DeveloperCV-AverageStat">
              <p className="DeveloperCV-AverageStatValue">
                {generateRandomNumber()}
              </p>
              <p className="DeveloperCV-AverageStatLabel">за неделю</p>
            </div>
            <div className="DeveloperCV-AverageStat">
              <p className="DeveloperCV-AverageStatValue">
                {generateRandomNumber()}
              </p>
              <p className="DeveloperCV-AverageStatLabel">за месяц</p>
            </div>
            <div className="DeveloperCV-AverageStat">
              <p className="DeveloperCV-AverageStatValue">
                {generateRandomNumber()}
              </p>
              <p className="DeveloperCV-AverageStatLabel">за год</p>
            </div>
          </div>
        </div>
      </div>

      <div className="DeveloperCV-Divider" />

      <div className="DeveloperCV-ReposStats">
        <p className="DeveloperCV-StatTitle">Статистика по репозиториям</p>
        <div className="DeveloperCV-ReposCarousel">
          <TagCarousel tags={scores} />
        </div>
        <div className="DeveloperCV-Charts">
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
      </div>
    </div>
  );
};
