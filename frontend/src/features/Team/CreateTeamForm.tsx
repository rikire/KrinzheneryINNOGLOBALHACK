import { useState, useCallback, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  selectIsShowCreateTeamForm,
  setShowCreateTeamForm,
} from '../../store/auth/slice';
import { getAccountInfo } from '../../shared/utils/getAccountInfo';

const Form = () => {
  const dispatch = useDispatch();
  const [selectedDevelopers, setSelectedDevelopers] = useState<string[]>([]);
  // TODO протестить добавление новой команды
  const close = useCallback(() => {
    dispatch(setShowCreateTeamForm(false));
  }, [dispatch]);

  useEffect(() => {
    const keydownClose = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        close();
      }
    };
    document.addEventListener('keydown', keydownClose);
    return () => {
      document.removeEventListener('keydown', keydownClose);
    };
  }, [close]);
  const isVisible = useSelector(selectIsShowCreateTeamForm);
  if (!isVisible) return null;
  const accountInfo = getAccountInfo(dispatch);

  const formSubmitHandler = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const json = Object.fromEntries(formData);
    const body = {
      login: accountInfo!.login,
      command: {
        command_name: json.teamName,
        participants: selectedDevelopers,
      },
    };

    fetch('http://0.0.0.0:8000/command', {
      headers: { 'Content-Type': 'application/json' },
      method: 'POST',
      body: JSON.stringify(body),
    })
      .then((response) =>
        response.ok ? response.json() : Promise.reject(response),
      )
      .then((data) => {
        localStorage.setItem('accountInfo', JSON.stringify(data));
        close();
      })
      .catch((error) => console.error('Error creating team:', error));
  };

  const handleDeveloperSelection = (name: string) => {
    setSelectedDevelopers((prevSelected) =>
      prevSelected.includes(name)
        ? prevSelected.filter((devId) => devId !== name)
        : [...prevSelected, name],
    );
  };

  return (
    <div
      className="Paranja"
      onClick={(e) => {
        e.stopPropagation();
        close();
      }}>
      <form
        className="Form Card"
        onSubmit={formSubmitHandler}
        onClick={(e) => e.stopPropagation()}>
        <button className="Form-CloseButton" type="button" onClick={close}>
          x
        </button>
        <p className="Form-Description">
          Создайте новую команду, указав название.
          <br />
          Вы можете выбрать разработчиков из списка ниже. Там находятся все те,
          кого вы сохраняли ранее.
        </p>
        <input
          className="Form-Input"
          type="text"
          name="teamName"
          placeholder="Название команды"
          required
        />
        <fieldset className="Form-Fieldset">
          <legend>Выберите разработчиков:</legend>
          {accountInfo?.favorites.length ? (
            accountInfo.favorites.map((dev) => (
              <label key={dev}>
                <input
                  type="checkbox"
                  name="developers"
                  value={dev}
                  checked={selectedDevelopers.includes(dev)}
                  onChange={() => handleDeveloperSelection(dev)}
                />
                {dev}
              </label>
            ))
          ) : (
            <p className="Form-Description">
              Вы еще не сохранили ни одного разработчика в избранное
            </p>
          )}
        </fieldset>
        <button className="Form-Button" type="submit">
          Создать команду
        </button>
      </form>
    </div>
  );
};

export default Form;
