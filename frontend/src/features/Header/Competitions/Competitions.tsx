import { useCallback } from 'react';
import { Toggle, ToggleProps } from '../../../components/Toggle';
import { useSearchParams } from 'react-router-dom';

const competencies: ToggleProps['options'] = [
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

export const Competencies = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const toggleHandler = useCallback(
    (name: string) => {
      setSearchParams({ competencies: name });
    },
    [setSearchParams],
  );

  return (
    <div className="Competencies Card">
      <Toggle
        toggleHandler={toggleHandler}
        current={searchParams.get('competencies') || ''}
        options={competencies}
      />
    </div>
  );
};
