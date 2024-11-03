export function longStringFormatter(string: string, maxLength: number = 10) {
  if (string.length > maxLength + 1) {
    return string.slice(0, maxLength) + '...';
  }
  return string;
}

export const CHART_PADDING = 20;
