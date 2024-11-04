import styles from './Tooltip.module.css';

export interface IHoverTooltipProps {
  children: React.ReactNode;
  position?: 'top' | 'bottom';
  hasTail?: boolean;
  tooltipText?: string;
  tooltipDescription?: string;
}

export const HoverTooltip = ({
  children,
  position = 'top',
  hasTail = true,
  tooltipText,
  tooltipDescription,
}: IHoverTooltipProps) => {
  if (!tooltipText && !tooltipDescription) return children;
  return (
    <div className={styles.TooltipTrigger + ' ' + styles.HoverTooltip}>
      {children}
      <div
        className={
          styles.Tooltip +
          ' ' +
          styles[`Tooltip_${position}`] +
          (hasTail ? ' ' + styles.Tooltip_hasTail : '')
        }>
        {Boolean(tooltipText) && (
          <p className={styles.TooltipText}>{tooltipText}</p>
        )}
        {Boolean(tooltipDescription) && (
          <p className={styles.TooltipDescription}>{tooltipDescription}</p>
        )}
      </div>
    </div>
  );
};
