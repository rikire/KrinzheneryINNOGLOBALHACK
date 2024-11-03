export interface IAvatarProps {
  className?: string;
  avatarURL: string;
}

export const Avatar = ({ className, avatarURL }: IAvatarProps) => {
  return (
    <img className={'DevInfo-Avatar ' + className} src={avatarURL} alt="" />
  );
};
