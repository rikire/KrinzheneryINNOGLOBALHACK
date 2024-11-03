import React from 'react';
import { Chart } from '../Chart/Chart';
import { CHART_PADDING, longStringFormatter } from '../helpers';

export interface BarChartData {
  labels: string[];
  values: number[][];
  legend?: string[];
}

export interface BarChartProps {
  data: BarChartData;
  showBackground?: boolean;
}

/**
 * Creates options for a bar chart with the given data.
 * @param {BarChartData} data The data for the chart.
 * @param {boolean} showBackground Whether to show the background of the bars.
 * @returns {echarts.EChartsOption} The options for the chart.
 */
const getOptions = (
  data: BarChartData,
  showBackground?: boolean,
): echarts.EChartsOption => {
  const series: echarts.EChartsOption['series'] = data.values.map(
    (values, i) => ({
      name: data.legend?.[i],
      type: 'bar',
      data: values,
      showBackground,
      backgroundStyle: {
        color: 'rgba(180, 180, 180, 0.2)',
      },
    }),
  );

  return {
    grid: {
      top: CHART_PADDING + 36,
      left: CHART_PADDING + 36,
      right: CHART_PADDING + 36,
      bottom: CHART_PADDING + 36,
    },
    tooltip: {},
    legend: {
      top: 0,
      left: CHART_PADDING,
      data: data.legend,
    },
    xAxis: {
      type: 'category',
      data: data.labels,
      axisLabel: {
        rotate: 30,
        interval: 0,
        formatter: (value) => longStringFormatter(value),
      },
    },
    yAxis: {
      type: 'value',
    },
    series,
  };
};

export const BarChart = ({ data, showBackground }: BarChartProps) => {
  return <Chart options={getOptions(data, showBackground)} />;
};
