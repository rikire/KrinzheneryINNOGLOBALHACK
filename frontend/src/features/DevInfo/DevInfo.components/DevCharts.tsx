import { Chart } from '../../../components/Charts';

const option = {
  tooltip: {
    trigger: 'item',
  },
  legend: {
    bottom: '5%',
    left: 'center',
  },
  series: [
    {
      top: -60,
      name: 'Access From',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
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
          fontSize: 40,
          fontWeight: 'bold',
        },
      },
      labelLine: {
        show: false,
      },
      data: [
        { value: 1048, name: 'Search Engine' },
        { value: 735, name: 'Direct' },
        { value: 580, name: 'Email' },
        { value: 484, name: 'Union Ads' },
        { value: 300, name: 'Video Ads' },
      ],
    },
  ],
};

const candlesOptions = {
  title: {
    text: 'Динамика изменения кода в репозитории',
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow',
    },
    formatter: function (params) {
      let tar;
      if (params[1] && params[1].value !== '-') {
        tar = params[1];
      } else {
        tar = params[2];
      }
      return tar && tar.name + '<br/>' + tar.seriesName + ' : ' + tar.value;
    },
  },
  legend: {
    data: ['Добавлено', 'Удалено'],
    right: 0,
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true,
  },
  xAxis: {
    type: 'category',
    data: (function () {
      let list = [];
      for (let i = 1; i <= 11; i++) {
        list.push('Nov ' + i);
      }
      return list;
    })(),
  },
  yAxis: {
    type: 'value',
  },
  series: [
    {
      name: 'Placeholder',
      type: 'bar',
      stack: 'Total',
      silent: true,
      itemStyle: {
        borderColor: 'transparent',
        color: 'transparent',
      },
      emphasis: {
        itemStyle: {
          borderColor: 'transparent',
          color: 'transparent',
        },
      },
      data: [0, 900, 1245, 1530, 1376, 1376, 1511, 1689, 1856, 1495, 1292],
    },
    {
      name: 'Добавлено',
      type: 'bar',
      stack: 'Total',
      label: {
        show: true,
        position: 'top',
      },
      data: [900, 345, 393, '-', '-', 135, 178, 286, '-', '-', '-'],
    },
    {
      name: 'Удалено',
      type: 'bar',
      stack: 'Total',
      label: {
        show: true,
        position: 'bottom',
      },
      data: ['-', '-', '-', 108, 154, '-', '-', '-', 119, 361, 203],
    },
  ],
};

export const DevCharts = () => {
  return (
    <div className="">
      <div className="DeveloperCV-DoughnatCharts">
        <div className="DeveloperCV-ChartContainer">
          <p className="DeveloperCV-ChartHeader">Языки</p>
          <div className="DeveloperCV-Chart">
            <Chart options={option} />
          </div>
        </div>
        <div className="DeveloperCV-ChartContainer">
          <p className="DeveloperCV-ChartHeader">Стек</p>
          <div className="DeveloperCV-Chart">
            <Chart options={option} />
          </div>
        </div>
      </div>
      <div className="DeveloperCV-CandlesChart">
        <div className="DeveloperCV-Chart">
          <Chart options={candlesOptions} />
        </div>
      </div>
    </div>
  );
};
