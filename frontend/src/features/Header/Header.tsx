import { Actions } from './Actions/Actions';
import { Competitions } from './Competitions/Competitions';
import { Search } from './Search/Search';

export const Header = () => {
  return (
    <div className="Header">
      <div className="Heaader-Search">
        <Search />
      </div>
      <Competitions />
      <Actions />
    </div>
  );
};
