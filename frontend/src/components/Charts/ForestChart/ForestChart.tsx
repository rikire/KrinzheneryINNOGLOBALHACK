import React from 'react';
import { Chart } from '../Chart/Chart';

export interface ForestChartData {
  value: number;
  label: string;
}

export interface ForestChartProps {
  data: ForestChartData;
}

const treeDataURI =
  'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAA2CAYAAADUOvnEAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA5tJREFUeNrcWE1oE0EUnp0kbWyUpCiNYEpCFSpIMdpLRTD15s2ePHixnj00N4/GoyfTg2fbiwdvvagHC1UQ66GQUIQKKgn1UAqSSFua38b3prPJZDs7s5ufKn0w7CaZ2W/fe9/73kyMRqNB3Nrj1zdn4RJ6du9T2u1a2iHYSxjP4d41oOHGQwAIwSUHIyh8/RA8XeiXh0kLGFoaXiTecw/hoTG4ZCSAaFkY0+BpsZceLtiAoV2FkepZSDk5EpppczBvpuuQCqx0YnkYcVVoqQYMyeCG+lFdaGkXeVOFNu4aEBalOBk6sbQrQF7gSdK5JXjuHXuYVIVyr0TZ0FjKDeCs6km7JYMUdrWAUVmZUBtmRnVPK+x6nIR2xomH06R35ggwJPeofWphr/W5UjPIxq8B2bKgE8C4HVHWvg+2gZjXj19PkdFztY7bk9TDCH/g6oafDPpaoMvZIRI5WyMB/0Hv++HkpTKE0kM+A+h20cPAfN4GuRyp9G+LMTW+z8rCLI8b46XO9zRcYZTde/j0AZm8WGb3Y2F9KLlE2nqYkjFLJAsDOl/lea0q55mqxXcL7YBc++bsCPMe8mUyU2ZIpnCoblca6TZA/ga2Co8PGg7UGUlEDd0ueptglbrRZLLE7poti6pCaWUo2pu1oaYI1CF9b9cCZPO3F8ikJQ/rPpQT5YETht26ss+uCIL2Y8vHwJGpA96GI5mjOlaKhowUy6BcNcgIhDviTGWCGFaqEuufWz4pgcbCh+w0gEOyOjTlTtYYlIWPYWKEsLDzOs+nhzaO1KEpd+MXpOoTUgKiNyhdy5aSMPNVqxtSsJFgza5EWA4zKtCJ2OGbLn0JSLu8+SL4G86p1Fpr7ABXdGFF/UTD4rfmFYFw4G9VAJ9SM3aF8l3yok4/J6IV9sDVb36ynmtJ2M5+CwxTYBdKNMBaocKGV2nYgkz6r+cHBP30MzAfi4Sy+BebSoPIOi8PW1PpCCvr/KOD4k9Zu0WSH0Y0+SxJ2awp/nlwKtcGyHOJ8vNHtRJzhPlsHr8MogtlVtwUU0tSM1x58upSKbfJnSKUR07GVMKkDNfXpzpv0RTHy3nZMVx5IOWdZIaPabGFvfpwpjnvfmJHXLaEvZUTseu/TeLc+xgAPhEAb/PbjO6PBaOTf6LQRh/dERde23zxLtOXbaKNhfq2L/1fAOPHDUhOpIf5485h7l+GNHHiSYPKE3Myz9sFxoJuAyazvwIMAItferha5LTqAAAAAElFTkSuQmCC';

const beginValue = 0;
const lineCount = 10;

function makeCategoryData() {
  const categoryData = [];
  for (let i = 0; i < lineCount; i++) {
    categoryData.push(i + 'a');
  }
  return categoryData;
}

function makeSeriesData(
  value: number,
  negative?: boolean,
): echarts.PictorialBarSeriesOption['data'] {
  const r = (value - beginValue + 1) * 10;
  const seriesData = [];

  for (let i = 0; i < lineCount; i++) {
    const sign = negative
      ? -1 * (i % 3 ? 0.9 : 1)
      : 1 * ((i + 1) % 3 ? 0.9 : 1);
    seriesData.push({
      value:
        sign *
        (value <= beginValue + 1
          ? Math.abs(i - lineCount / 2 + 0.5) < lineCount / 5
            ? 5
            : 0
          : (lineCount - Math.abs(i - lineCount / 2 + 0.5)) * r),
      symbolOffset: i % 2 ? ['50%', 0] : undefined,
    });
  }
  return seriesData;
}

/**
 * Creates options for a bar chart with the given data.
 * @param {ForestChartData} data The data for the chart.
 * @returns {echarts.EChartsOption} The options for the chart.
 */
const getOptions = (data: ForestChartData): echarts.EChartsOption => {
  const value = Math.round(data.value / 10);
  return {
    color: ['#e54035'],
    xAxis: {
      axisLine: { show: false },
      axisLabel: { show: false },
      axisTick: { show: false },
      splitLine: { show: false },
      name: data.label,
      nameLocation: 'middle',
      nameGap: 10,
      nameTextStyle: {
        color: 'green',
        fontSize: 20,
        fontFamily: 'Arial',
      },
      min: -2800,
      max: 2800,
    },
    yAxis: {
      data: makeCategoryData(),
      show: false,
    },
    grid: {
      top: 'center',
      height: 170,
    },
    series: [
      {
        name: 'all',
        type: 'pictorialBar',
        symbol: 'image://' + treeDataURI,
        symbolSize: [18, 33],
        symbolRepeat: true,
        data: makeSeriesData(value),
        animationEasing: 'elasticOut',
      },
      {
        name: 'all',
        type: 'pictorialBar',
        symbol: 'image://' + treeDataURI,
        symbolSize: [18, 33],
        symbolRepeat: true,
        data: makeSeriesData(value, true),
        animationEasing: 'elasticOut',
      },
    ],
  };
};

export const ForestChart = ({ data }: ForestChartProps) => {
  return <Chart options={getOptions(data)} />;
};
