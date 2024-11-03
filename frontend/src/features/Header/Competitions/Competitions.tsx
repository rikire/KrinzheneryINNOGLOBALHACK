import { useCallback, useState } from 'react';
import { Toggle, ToggleProps } from '../../../components/Toggle';

const competitions: ToggleProps['options'] = [
  {
    name: 'frontend',
    label: 'frontend',
  },
  {
    name: 'backend',
    label: 'backend',
  },
  {
    name: 'devops',
    label: 'devops',
  },
  {
    name: 'data_science',
    label: 'data science',
  },
  {
    name: 'mobile',
    label: 'mobile',
  },
  {
    name: 'embedded',
    label: 'embedded',
  },
  {
    name: 'gamedev',
    label: 'gamedev',
  },
  {
    name: 'others',
    label: 'others',
  },
];

export const Competitions = () => {
  const [current, setCurrent] = useState('');
  const toggleHandler = useCallback((name: string) => {
    setCurrent(name);
  }, []);
  return (
    <div className="Competitions Card">
      <Toggle
        toggleHandler={toggleHandler}
        current={current}
        options={competitions}
      />
    </div>
  );
};
