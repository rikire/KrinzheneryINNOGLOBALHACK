import { useParams } from 'react-router-dom';

export const ComparePage = () => {
  const p = useParams();
  return (
    <div className="ComparePage">
      <div className="Compare-User"></div>
      <div className="Compare-User"></div>
    </div>
  );
};
