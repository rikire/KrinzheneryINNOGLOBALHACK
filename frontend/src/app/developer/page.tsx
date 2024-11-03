import { useParams } from 'react-router-dom';
import { DeveloperCV } from '../../features/DeveloperCV/DeveloperCV';

export const DeveloperPage = () => {
  const p = useParams();
  console.log(p);
  return <DeveloperCV />;
};
