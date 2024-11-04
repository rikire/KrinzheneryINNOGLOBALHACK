export interface ITagProps {
  view: 'primary' | 'default' | 'top' | 'medium';
  children: React.ReactNode;
  onClick?: () => void;
}

export const Tag = ({ children, view, onClick }: ITagProps) => {
  return (
    <div onClick={onClick} className={`Tag Tag_${view}`}>
      {children}
    </div>
  );
};
