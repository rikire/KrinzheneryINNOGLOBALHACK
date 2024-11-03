import FireSVG from '../../shared/icons/FireOutlined';
import AddToComandsSVG from '../../shared/icons/AddToComand';
import { Tag } from '../../components/Tag';

export interface IDeveloperCommonInfoProps {
  viewType: string;
  username: string;
  name: string;
  email: string;
  accountAge: number;
  avatarURL: string;

  followers: number;
  followCount: number;
}

const competenties: string[] = [
  'frontend',
  'backend',
  'devops',
  'data_science',
  'qa'
]

export const DeveloperCommonInfo = ({
  viewType,
  username,
  name,
  email,
  accountAge,
  avatarURL,

  followers,
  followCount,
}: IDeveloperCommonInfoProps) => {
  return (
    <div className="DeveloperCommonInfo">
      <img className="DeveloperCommonInfo-Avatar" src={avatarURL} alt="" />
      <div className="DeveloperCommonInfo-ContactInfo">
        <div className="DeveloperCommonInfo-ContactInfo-Username">
          <p>{username}</p>
          <button>
            <FireSVG height={28}/>
          </button>
          <button>
            <AddToComandsSVG height={26} width={26} />
          </button>
        </div>
        <p className="DeveloperCommonInfo-ContactInfo-Name">{name}</p>
        <p className="DeveloperCommonInfo-ContactInfo-Age">
          {getAge(accountAge)}
        </p>
        <p className="DeveloperCommonInfo-ContactInfo-Email">{email}</p>
        <div className="DeveloperCommonInfo-ContactInfo-Follow">
          <p>Подписки: {followCount}</p>
          <p>Подписчики: {followers}</p>
        </div>
      </div>
      <div
        className={
          'DeveloperCommonInfo-StatInfo ' +
          'DeveloperCommonInfo-StatInfo_' +
          viewType
        }>
          <div className='DeveloperCommonInfo-StatInfo-Competencies'>
            {competenties.map((item, i) => (
              <Tag key={i} view={i === 1 ? 'primary' : 'default'}>{item}</Tag>
            ))}
          </div>
        </div>
    </div>
  );
};

const getAge = (mounts: number) => {
  const years = Math.floor(mounts / 12);
  const months = mounts % 12;
  return `${years} ${years === 1 ? 'год' : 'года'} ${months} ${
    months === 1 ? 'месяц' : 'месяца на GitHub'
  }`;
};
