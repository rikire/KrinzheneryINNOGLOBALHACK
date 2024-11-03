import { Chart } from '../Chart/Chart';

export interface PieChartData {
  labels: string[];
  values: number[];
}

export interface PieChartProps {
  data: PieChartData;
}

/**
 * Creates options for a bar chart with the given data.
 * @param {PieChartData} data The data for the chart.
 * @returns {echarts.EChartsOption} The options for the chart.
 */
const getOptions = (data: PieChartData): echarts.EChartsOption => {
  const preparedData = data.labels.map((label, index) => ({
    value: data.values[index],
    name: label,
  }));
  return {
    tooltip: {
      trigger: 'item',
    },
    series: [
      {
        name: 'Access From',
        type: 'pie',
        radius: '60%',
        data: preparedData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  };
};

export const PieChart = ({ data }: PieChartProps) => {
  return <Chart options={getOptions(data)} />;
};
