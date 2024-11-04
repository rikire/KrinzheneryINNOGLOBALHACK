import { useState } from 'react';

import styles from './Tooltip.module.css';
import { useUXClose } from '../../shared/hooks/useUXClose';

interface ITooltipBaseProps {
  position?: 'top' | 'bottom';
  tooltipTitle?: string;
  tooltipContent?: JSX.Element;
  hasCloseButton?: boolean;
}

export interface IClickTooltipProps extends ITooltipBaseProps {
  children: React.ReactNode;
}

export const ClickTooltip = ({
  children,
  tooltipContent,
  ...props
}: IClickTooltipProps) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  if (!tooltipContent) return children;
  return (
    <div className={styles.TooltipTrigger}>
      <button
        onClick={() => {
          setIsOpen(!isOpen);
        }}>
        {children}
      </button>
      <Tooltip
        isOpen={isOpen}
        setIsOpen={setIsOpen}
        tooltipContent={tooltipContent}
        {...props}
      />
    </div>
  );
};

interface ITooltipProps extends ITooltipBaseProps {
  isOpen: boolean;
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

const Tooltip: React.FC<ITooltipProps> = ({
  position = 'top',
  isOpen,
  setIsOpen,
  tooltipTitle,
  hasCloseButton = true,
  tooltipContent,
}) => {
  useUXClose(isOpen, setIsOpen);
  return (
    <div
      onClick={(e) => e.stopPropagation()}
      className={
        styles.Tooltip +
        ' ' +
        styles.ClickTooltip +
        ' ' +
        styles[`Tooltip_${position}`] +
        (isOpen ? ' ' + styles.Tooltip_open : '')
      }>
      {tooltipTitle && (
        <div className={styles.TooltipHeader}>
          <p className={styles.TooltipTitle}>{tooltipTitle}</p>
          {hasCloseButton && (
            <button
              aria-label="Закрыть"
              className={styles.TooltipCloseButton}
              onClick={() => setIsOpen((current) => !current)}>
              X
            </button>
          )}
        </div>
      )}
      <div className={styles.TooltipContent}>{tooltipContent}</div>
    </div>
  );
};
