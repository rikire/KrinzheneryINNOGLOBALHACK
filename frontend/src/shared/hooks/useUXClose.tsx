import { useEffect } from 'react';

export const useUXClose = (
  isOpen: boolean,
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>,
) => {
  useEffect(() => {
    if (!isOpen) return;
    const close = () => {
      setIsOpen(false);
    };

    const keydownClose = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };
    setTimeout(() => {
      window.addEventListener('click', close);

      window.addEventListener('keydown', keydownClose);
    }, 0);

    return () => {
      window.removeEventListener('click', close);
      window.removeEventListener('keydown', keydownClose);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]);
};
