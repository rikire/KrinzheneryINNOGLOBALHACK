export interface IAvatarProps {
  className?: string;
  avatarURL: string;
}

export const Avatar = ({ className, avatarURL }: IAvatarProps) => {
  console.log(avatarURL);
  return (
    <img className={'DevInfo-Avatar ' + className} src={avatarURL} alt="" />
  );
};
