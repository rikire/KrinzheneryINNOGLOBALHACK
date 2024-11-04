import { useParams } from 'react-router-dom';
import { Chart } from '../../components/Charts';

const options = {};
export const ComparePage = () => {
  const p = useParams();
  return (
    <div className="ComparePage">
      <div className="Compare-Chart">
        <Chart options={} />
      </div>
      <div className="Compare-Users">
        <div className="Compare-User"></div>
        <div className="Compare-User"></div>
      </div>
    </div>
  );
};
