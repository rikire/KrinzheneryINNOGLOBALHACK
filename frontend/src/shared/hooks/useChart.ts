import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

export const useChart = (options: echarts.EChartsOption) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;
    // Initialize the chart
    const myChart = echarts.init(containerRef.current);
    // Draw the chart
    myChart.setOption(options);
  }, [options]);

  return containerRef;
};
