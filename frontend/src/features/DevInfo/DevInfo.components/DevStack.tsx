import { Tag } from '../../../components/Tag';

export interface IDevStackProps {
  stack: string[];
}

export const DevStack = ({ stack }: IDevStackProps) => {
  return (
    <div className="DevInfo-StatInfo-Stack">
      {stack.map((item, i) => (
        <Tag key={i} view={i === 1 ? 'primary' : 'default'}>
          {item}
        </Tag>
      ))}
    </div>
  );
};
