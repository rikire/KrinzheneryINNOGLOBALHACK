import { useCallback, useState } from 'react';

export interface InputProps {
  actionButton?: JSX.Element;
  inputProps?: React.InputHTMLAttributes<HTMLInputElement>;
}
export const Input = ({ actionButton, inputProps }: InputProps) => {
  const [state, setState] = useState('');
  const changeHandler = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setState(e.target.value);
      inputProps?.onChange?.(e);
    },
    [inputProps],
  );

  return (
    <div className="Input-Container">
      <input
        className="Input"
        value={state}
        onChange={changeHandler}
        {...inputProps}
      />

      {actionButton && <div className="Input-ActionButton">{actionButton}</div>}
    </div>
  );
};
