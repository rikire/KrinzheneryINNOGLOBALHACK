import { useCallback, useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { selectIsShow, setShow } from '../../store/auth/slice';
import { useDispatch, useSelector } from 'react-redux';

export const Auth = () => {
  const isShow = useSelector(selectIsShow);

  if (!isShow) return null;

  return createPortal(<Form />, document.body);
};

const Form = () => {
  const [isRegister, setIsRegister] = useState(false);
  const dispatch = useDispatch();

  const close = useCallback(() => {
    dispatch(setShow(false));
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
  });

  const formSubmitHandler = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const body = new FormData(e.currentTarget);
    // transform body to json
    const json = Object.fromEntries(body);

    fetch('http://0.0.0.0:8000/' + (isRegister ? 'register' : 'login'), {
      headers: { 'Content-Type': 'application/json' },
      method: 'POST',
      body: JSON.stringify(json),
    })
      .then((r) => (r.ok ? r.json() : Promise.reject(r)))
      .then((d) => {
        localStorage.setItem('accountInfo', JSON.stringify(d));
        close();
      });
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
          Чтобы пользоваться всеми возможностями сайта, войдите в аккаунт или
          зарегистрируйтесь.
        </p>
        <input
          className="Form-Input"
          type="text"
          name="login"
          placeholder="Логин"
        />
        <input
          className="Form-Input"
          type="password"
          name="password"
          placeholder="Пароль"
        />
        {isRegister && (
          <input
            className="Form-Input"
            type="password"
            name="password_repeat"
            placeholder="Повторите пароль "
          />
        )}
        {isRegister ? (
          <button className="Form-Button" type="submit">
            Зарегистрироваться
          </button>
        ) : (
          <button className="Form-Button" type="submit">
            Войти
          </button>
        )}
        {isRegister ? (
          <button
            className="Form-Button_secondary"
            type="button"
            onClick={() => setIsRegister(false)}>
            Уже есть аккаунт
          </button>
        ) : (
          <button
            className="Form-Button_secondary"
            type="button"
            onClick={() => setIsRegister(true)}>
            Зарегистрироваться
          </button>
        )}
      </form>
    </div>
  );
};
