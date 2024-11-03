import { DevInfo } from '../DevInfo/DevInfo';

export const DeveloperCompare = () => {
  return (
    <div>
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
        <div className="DevInfo-Title-Stats">
          <p className="DevInfo-Title-Stat">
            Кол-во командных проектов: {getRandomNumber()}
          </p>
          <p className="DevInfo-Title-Stat">
            Кол-во собственных проектов: {getRandomNumber()}
          </p>
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
