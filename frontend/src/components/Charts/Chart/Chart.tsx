import { useChart } from '../../../shared/hooks/useChart';

export interface IChartProps {
  options: echarts.EChartsOption;
}
export const Chart = ({ options }: IChartProps) => {
  const chartRef = useChart(options);

  return <div style={{ width: '100%', height: '100%' }} ref={chartRef}></div>;
};
