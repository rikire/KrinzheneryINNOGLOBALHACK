export interface ITagProps {
  view: 'primary' | 'default' | 'top' | 'medium';
  children: React.ReactNode;
}

export const Tag = ({ children, view }: ITagProps) => {
  return <div className={`Tag Tag_${view}`}>{children}</div>;
};
