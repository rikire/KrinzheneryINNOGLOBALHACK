

export interface ITreeListProps {
  items: string[]
}

export const TreeList = ({items}: ITreeListProps) => {
  return (
    <ul className="TreeList">
        {items.map((item, i) => (
          <li key={i} className="TreeList-Item">
            {item}
          </li>
        ))}
    </ul>
  )
}
