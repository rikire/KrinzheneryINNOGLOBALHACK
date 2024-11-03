import FireSVG from '../../shared/icons/FireOutlined';
import AddToComandsSVG from '../../shared/icons/AddToComand';
import { Tag } from '../../components/Tag';

export interface IDevInfoProps {
  viewType: 'competencies' | 'stats' | 'compare';
  username: string;
  name: string;
  email: string;
  accountAge: number;
  avatarURL: string;

  followers: number;
  followCount: number;
}

const getRandomNumber = () => Math.floor(Math.random() * 100);

const stack: string[] = [
  'React',
  'Vue',
  'Node.js',
  'Django',
  'Flask',
  'Spring',
];

const competencies: string[] = [
  'frontend',
  'backend',
  'devops',
  'data_science',
  'qa',
];

export const DevInfo = ({
  viewType,
  username,
  name,
  email,
  accountAge,
  avatarURL,

  followers,
  followCount,
}: IDevInfoProps) => {
  return (
    <div className={'DevInfo' + ' DevInfo_' + viewType}>
      <img className="DevInfo-Avatar" src={avatarURL} alt="" />
      <div className="DevInfo-Title">
        <div className="DevInfo-Title-Username">
          <p>{username}</p>
          <button>
            <FireSVG height={28} />
          </button>
          <button>
            <AddToComandsSVG height={26} width={26} />
          </button>
        </div>
        <p className="DevInfo-Title-Name">{name}</p>
        <p className="DevInfo-Title-Age">{getAge(accountAge)}</p>
        <div className="DevInfo-Title-Info">
          <p className="DevInfo-Title-Email">{email}</p>
          <div className="DevInfo-Title-Follow">
            <p>Подписки: {followCount}</p>
            <p>Подписчики: {followers}</p>
          </div>
        </div>
      </div>
      <div className="DevInfo-StatInfo">
        <div className="DevInfo-StatInfo-Competencies">
          {competencies.map((item, i) => (
            <Tag key={i} view={i === 1 ? 'primary' : 'default'}>
              {item}
            </Tag>
          ))}
        </div>
        <div className="DevInfo-StatInfo-Counts">
          <p className="DevInfo-StatInfo-CountValue">
            Кол-во гистов: {getRandomNumber()}
          </p>
          <p className="DevInfo-StatInfo-CountValue">
            Кол-во собственных проектов: {getRandomNumber()}
          </p>
          <p className="DevInfo-StatInfo-CountValue">
            Кол-во командных проектов: {getRandomNumber()}
          </p>
        </div>
        <div className="DevInfo-StatInfo-Stack">
          {stack.map((item, i) => (
            <Tag key={i} view={i === 1 ? 'primary' : 'default'}>
              {item}
            </Tag>
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
