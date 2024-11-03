import { TreeList } from '../../../components/TreeList';

export interface IDevCompetenciesTreesProps {
  competencies: string[];
  stack: string[];
  languages: string[];
  ghFeatures: string[];
}

export const DevCompetenciesTrees = ({
  competencies,
  stack,
  languages,
  ghFeatures,
}: IDevCompetenciesTreesProps) => {
  return (
    <div className="DeveloperCV-Lists">
      {/* TODO: прокинуть scores */}
      <div>
        <p className="DeveloperCV-ListHeader">Компетенции</p>
        <TreeList items={competencies} />
      </div>
      <div>
        <p className="DeveloperCV-ListHeader">Языки</p>
        <TreeList items={languages} />
      </div>
      <div>
        <p className="DeveloperCV-ListHeader">Стек</p>
        <TreeList items={stack} />
      </div>
      <div>
        <p className="DeveloperCV-ListHeader">Инструменты GitHub</p>
        <TreeList items={ghFeatures} />
      </div>
    </div>
  );
};
