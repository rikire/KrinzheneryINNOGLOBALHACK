export interface IDevSubtitleProps {
  email: string;
  followCount: number;
  followers: number;
}

export const DevSubtitle = ({
  email,
  followCount,
  followers,
}: IDevSubtitleProps) => {
  return (
    <div className="DevInfo-Title-Info">
      <p className="DevInfo-Title-Email">{email}</p>
      <div className="DevInfo-Title-Follow">
        <p>Подписки: {followCount}</p>
        <p>Подписчики: {followers}</p>
      </div>
    </div>
  );
};
