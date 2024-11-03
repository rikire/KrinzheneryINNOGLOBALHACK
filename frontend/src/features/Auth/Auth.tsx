import { useCallback, useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { selectIsShow, setShow } from '../../store/auth/slice';
import { useDispatch, useSelector } from 'react-redux';

export const Auth = () => {
  const isShow = useSelector(selectIsShow);

  if (!isShow) return null;

  return createPortal(<LoginForm />, document.body);
};

const LoginForm = () => {
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

  return (
    <div
      className="Paranja"
      onClick={(e) => {
        e.stopPropagation();
        close();
      }}>
      <form
        className="LoginForm Card"
        onSubmit={(e) => e.preventDefault()}
        onClick={(e) => e.stopPropagation()}>
        <button className="LoginForm-CloseButton" type="button" onClick={close}>
          x
        </button>
        <p className="LoginForm-Description">
          Чтобы пользоваться всеми возможностями сайта, войдите в аккаунт или
          зарегистрируйтесь.
        </p>
        <input
          className="LoginForm-Input"
          type="text"
          name="nickname"
          placeholder="Логин"
        />
        <input
          className="LoginForm-Input"
          type="password"
          name="password"
          placeholder="Пароль"
        />
        {isRegister && (
          <input
            className="LoginForm-Input"
            type="password"
            name="password_repeat"
            placeholder="Повторите пароль "
          />
        )}
        {isRegister ? (
          <button className="LoginForm-Button" type="submit">
            Зарегистрироваться
          </button>
        ) : (
          <button className="LoginForm-Button" type="submit">
            Войти
          </button>
        )}
        {isRegister ? (
          <button
            className="LoginForm-Button_secondary"
            type="button"
            onClick={() => setIsRegister(false)}>
            Уже есть аккаунт
          </button>
        ) : (
          <button
            className="LoginForm-Button_secondary"
            type="button"
            onClick={() => setIsRegister(true)}>
            Зарегистрироваться
          </button>
        )}
      </form>
    </div>
  );
};
