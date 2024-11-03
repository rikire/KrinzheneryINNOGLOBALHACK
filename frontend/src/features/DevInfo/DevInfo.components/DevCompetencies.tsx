import { useParams } from 'react-router-dom';
import { Tag } from '../../../components/Tag';

interface DevCompetenciesProps {
  competencies: string[];
}

export const DevCompetencies: React.FC<DevCompetenciesProps> = ({
  competencies,
}) => {
  const p = useParams();

  return (
    <div className="DevInfo-StatInfo-Competencies">
      {competencies.map((item, i) => (
        <Tag key={i} view={item === p.competencies ? 'primary' : 'default'}>
          {item}
        </Tag>
      ))}
    </div>
  );
};
