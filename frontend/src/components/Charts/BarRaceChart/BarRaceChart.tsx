import React from 'react';
import { Chart } from '../Chart/Chart';
import { CHART_PADDING, longStringFormatter } from '../helpers';

export interface BarRaceChartData {
  labels: string[];
  values: number[];
}

export interface BarRaceChartProps {
  data: BarRaceChartData;
  bgText?: string;
}

/**
 * Creates options for a barrace chart with the given data.
 * @param {BarRaceChartData} data The data for the chart.
 * @returns {echarts.EChartsOption} The options for the chart.
 */
const getOptions = (
  data: BarRaceChartData,
  bgText?: string,
): echarts.EChartsOption => {
  return {
    tooltip: {
      show: true,
    },
    grid: {
      top: CHART_PADDING,
      bottom: CHART_PADDING + 20,
      left: CHART_PADDING + 80,
      right: CHART_PADDING + 20,
    },
    xAxis: {
      max: 'dataMax',
    },
    yAxis: {
      data: data.labels,
      type: 'category',
      inverse: true,
      max: data.labels.length - 1,
      axisLabel: {
        show: true,
        fontSize: 14,
        rotate: 30,
        formatter: (value) => longStringFormatter(value),
      },
      animationDuration: 300,
      animationDurationUpdate: 300,
    },
    series: [
      {
        data: data.values,
        realtimeSort: true,
        seriesLayoutBy: 'column',
        type: 'bar',
        encode: {
          x: 0,
          y: 3,
        },
        label: {
          show: true,
          precision: 1,
          position: 'right',
          fontFamily: 'monospace',
        },
      },
    ],
    graphic: bgText
      ? {
          elements: [
            {
              type: 'text',
              right: 50,
              bottom: CHART_PADDING + 20,
              style: {
                text: bgText,
                font: 'bolder 20px monospace',
                fill: 'rgba(100, 100, 100, 0.25)',
              },
              z: 100,
            },
          ],
        }
      : undefined,
  };
};

export const BarRaceChart = ({ data, bgText }: BarRaceChartProps) => {
  return <Chart options={getOptions(data, bgText)} />;
};
