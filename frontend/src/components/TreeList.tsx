export interface ITreeListProps {
  items: string[];
}

export const TreeList = ({ items }: ITreeListProps) => {
  if (!items || !items.length)
    return <p style={{ color: '#7d7d7d' }}>Список пуст</p>;
  return (
    <ul className="TreeList">
      {items.map((item, i) => (
        <li key={i} className="TreeList-Item">
          {item}
        </li>
      ))}
    </ul>
  );
};
