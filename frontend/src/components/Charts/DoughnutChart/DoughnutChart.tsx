import React from 'react';
import { Chart } from '../Chart/Chart';
import { CHART_PADDING } from '../helpers';

export interface DoughnutChartData {
  labels: string[];
  values: number[];
}

export interface DoughnutChartProps {
  data: DoughnutChartData;
}

/**
 * Creates options for a bar chart with the given data.
 * @param {DoughnutChartData} data The data for the chart.
 * @returns {echarts.EChartsOption} The options for the chart.
 */
const getOptions = (data: DoughnutChartData): echarts.EChartsOption => {
  const seriesData = data.labels.map((label, index) => ({
    value: data.values[index],
    name: label,
  }));
  return {
    tooltip: {
      trigger: 'item',
    },
    legend: {
      top: '0',
      left: CHART_PADDING,
    },
    series: [
      {
        bottom: -40,
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: true,
        padAngle: 5,
        itemStyle: {
          borderRadius: 10,
        },
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold',
          },
        },
        labelLine: {
          show: false,
        },
        data: seriesData,
      },
    ],
  };
};

export const DoughnutChart = ({ data }: DoughnutChartProps) => {
  return <Chart options={getOptions(data)} />;
};
