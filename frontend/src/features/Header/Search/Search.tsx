import { Input } from '../../../components/Input';
import SearchSVG from '../../../shared/icons/SearchOutlined';

export const Search = () => {
  return (
    <Input
      actionButton={
        <button className="Search-Button">
          <SearchSVG />
        </button>
      }
      inputProps={{
        type: 'search',
        placeholder: 'GitHub nickname',
      }}
    />
  );
};
