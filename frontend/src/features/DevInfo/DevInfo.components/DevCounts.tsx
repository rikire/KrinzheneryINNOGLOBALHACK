export interface IDevCountsProps {
  countTeamProjects: number;
  countSoloProjects: number;
}

export const DevCounts = ({
  countTeamProjects,
  countSoloProjects,
}: IDevCountsProps) => {
  return (
    <div className="DevInfo-Title-Stats">
      <p className="DevInfo-Title-Stat">
        Кол-во командных проектов: {countTeamProjects}
      </p>
      <p className="DevInfo-Title-Stat">
        Кол-во собственных проектов: {countSoloProjects}
      </p>
    </div>
  );
};
