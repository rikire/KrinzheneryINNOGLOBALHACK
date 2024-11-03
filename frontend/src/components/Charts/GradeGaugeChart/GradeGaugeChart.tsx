import React from 'react';
import { Chart } from '../Chart/Chart';

export interface GradeGaugeChartData {
  value: number;
}

export interface GradeGaugeChartProps {
  data: GradeGaugeChartData;
}

/**
 * Creates options for a bar chart with the given data.
 * @param {GradeGaugeChartData} data The data for the chart.
 * @returns {echarts.EChartsOption} The options for the chart.
 */
const getOptions = (data: GradeGaugeChartData): echarts.EChartsOption => {
  return {
    series: [
      {
        type: 'gauge',
        startAngle: 180,
        endAngle: 0,
        center: ['50%', '75%'],
        radius: '88%',
        min: 0,
        max: 1,
        splitNumber: 8,
        axisLine: {
          lineStyle: {
            width: 6,
            color: [
              [0.25, '#FF6E76'],
              [0.5, '#FDDD60'],
              [0.75, '#58D9F9'],
              [1, '#7CFFB2'],
            ],
          },
        },
        pointer: {
          icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
          length: '12%',
          width: 20,
          offsetCenter: [0, '-60%'],
          itemStyle: {
            color: 'auto',
          },
        },
        axisTick: {
          length: 12,
          lineStyle: {
            color: 'auto',
            width: 2,
          },
        },
        splitLine: {
          length: 20,
          lineStyle: {
            color: 'auto',
            width: 5,
          },
        },
        axisLabel: {
          color: '#464646',
          fontSize: 12,
          distance: -40,
          rotate: 'tangential',
          formatter: function (value: number) {
            if (value === 0.875) {
              return 'Великолепно';
            } else if (value === 0.625) {
              return 'Хорошо';
            } else if (value === 0.375) {
              return 'Средне';
            } else if (value === 0.125) {
              return 'Плохо';
            }
            return '';
          },
        },
        title: {
          offsetCenter: [0, '-10%'],
          fontSize: 16,
        },
        detail: {
          fontSize: 30,
          offsetCenter: [0, '-35%'],
          valueAnimation: true,
          formatter: function (value: number) {
            return Math.round(value * 100) + '';
          },
          color: 'inherit',
        },
        data: [
          {
            value: data.value,
            name: 'Показатель качества',
          },
        ],
      },
    ],
  };
};

export const GradeGaugeChart = ({ data }: GradeGaugeChartProps) => {
  return <Chart options={getOptions(data)} />;
};
