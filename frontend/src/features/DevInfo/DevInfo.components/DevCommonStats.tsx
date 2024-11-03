export interface IDevCommonStatsProps {
  commitsAmount: number;
  averageCommitSize: number;
  commitsPerDay: number;
  commitsPerWeek: number;
  commitsPerMonth: number;
  commitsPerYear: number;
}

export const DevCommonStats = ({
  commitsAmount,
  averageCommitSize,
  commitsPerDay,
  commitsPerWeek,
  commitsPerMonth,
  commitsPerYear,
}: IDevCommonStatsProps) => {
  return (
    <div className="DeveloperCV-Stats">
      <div className="DeveloperCV-CommonStats">
        <p className="DeveloperCV-StatTitle">Общая статистика</p>
        <p className="DeveloperCV-CommonStat">
          Средний размер коммита - {averageCommitSize}
        </p>
        <p className="DeveloperCV-CommonStat">
          Общее число коммитов - {commitsAmount}
        </p>
      </div>
      <div className="DeveloperCV-AverageStats">
        <p className="DeveloperCV-StatTitle">В среднем коммитов</p>
        <div className="DeveloperCV-AverageStatsWrapper">
          <div className="DeveloperCV-AverageStat">
            <p className="DeveloperCV-AverageStatValue">{commitsPerDay}</p>
            <p className="DeveloperCV-AverageStatLabel">за день</p>
          </div>
          <div className="DeveloperCV-AverageStat">
            <p className="DeveloperCV-AverageStatValue">{commitsPerWeek}</p>
            <p className="DeveloperCV-AverageStatLabel">за неделю</p>
          </div>
          <div className="DeveloperCV-AverageStat">
            <p className="DeveloperCV-AverageStatValue">{commitsPerMonth}</p>
            <p className="DeveloperCV-AverageStatLabel">за месяц</p>
          </div>
          <div className="DeveloperCV-AverageStat">
            <p className="DeveloperCV-AverageStatValue">{commitsPerYear}</p>
            <p className="DeveloperCV-AverageStatLabel">за год</p>
          </div>
        </div>
      </div>
    </div>
  );
};
