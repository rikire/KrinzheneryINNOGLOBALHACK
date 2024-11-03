import { useParams } from 'react-router-dom';
import { DeveloperCard } from '../../features/DeveloperCard/DeveloperCard';
import { Toggle } from '../../components/Toggle';
import { useState } from 'react';

const usernames = [
  'Ten-Do',
  'Rudenko',
  'Denis',
  'Ivanov',
  'Petrov',
  'Sidorov',
  'Kozlov',
  'Volkov',
  'Popov',
  'Semenov',
];

const options = [
  {
    name: 'python',
    label: 'python',
  },
  {
    name: 'php',
    label: 'php',
  },
  {
    name: 'javascript',
    label: 'javascript',
  },
  {
    name: 'java',
    label: 'java',
  },
  {
    name: 'c++',
    label: 'c++',
  },
  {
    name: 'c#',
    label: 'c#',
  },
  {
    name: 'kotlin',
    label: 'kotlin',
  },
];

export const SearchPage = () => {
  const p = useParams();
  const [current, setCurrent] = useState('');
  return (
    <div>
      <div className="Competencies Card" style={{ marginBottom: 20 }}>
        <Toggle
          options={options}
          toggleHandler={(name) => setCurrent(name)}
          current={current}
        />
      </div>
      <div>
        {usernames.map((username) => (
          <DeveloperCard key={username} username={username} />
        ))}
      </div>
    </div>
  );
};
