import { useEffect, useLayoutEffect, useRef } from 'react';
import styles from './Toggle.module.css';

export interface ToggleProps {
  toggleHandler: (name: string) => void;
  current: string;
  options: {
    name: string;
    label: string;
  }[];
}

export const Toggle = ({ toggleHandler, current, options }: ToggleProps) => {
  const highlightRef = useRef<HTMLDivElement>(null);
  const navigationswitchRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const activeBtn = navigationswitchRef.current?.querySelector(
      `button[data-value="${current}"]`,
    );

    if (!activeBtn) return;

    const w = activeBtn?.clientWidth || 0;
    const x = (activeBtn as HTMLElement)?.offsetLeft || 0;

    if (highlightRef.current) {
      highlightRef.current.style.width = `${w + 25}px`;
      highlightRef.current.style.transform = `translateX(${x - 12}px)`;
    }
  }, [current]);

  useEffect(() => {
    if (!highlightRef.current) return;
    highlightRef.current.classList.add(
      styles.NavigationSwitchHighlight_animated,
    );
  }, []);

  return (
    <div className={styles.NavigationSwitchContainer} ref={navigationswitchRef}>
      <div
        className={
          styles.NavigationSwitch +
          (current ? ' ' + styles.NavigationSwitch_active : '')
        }>
        <div className={styles.NavigationSwitchHighlight} ref={highlightRef} />
        {options.map((option) => (
          <button
            key={option.name}
            data-value={option.name}
            className={
              current === option.name
                ? `${styles.NavigationSwitchButton} ${styles.NavigationSwitchButton_active}`
                : styles.NavigationSwitchButton
            }
            onClick={() => toggleHandler(option.name)}>
            {option.label}
          </button>
        ))}
      </div>
    </div>
  );
};
