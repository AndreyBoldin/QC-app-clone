<template>
  <div v-show="$props.showNormalizationGraph" class="rounded-card" style="margin-top: 10px">
    <h3>График нормализации ДО</h3>
    <div
      style="
        background-color: gray;
        color: white;
        width: auto;
        height: 200px;
        text-align: center;
        line-height: 200px;
      "
    >
      График
    </div>
    <h3>График нормализации ПОСЛЕ</h3>
    <div
      style="
        background-color: gray;
        color: white;
        width: auto;
        height: 200px;
        text-align: center;
        line-height: 200px;
      "
    >
      График
    </div>
          <h3>Бокс-плоты</h3>
          <div>
          <ApexChart
            type="boxPlot"
            :options="BoxplotChartOptions"
            :series="BoxplotChartSeries"
          />
        </div>
  </div>

</template>

<script setup>

const BoxplotChartSeries = [
  {
    name: 'box',
    type: 'boxPlot',
    data: [
      {
        x: new Date('2017-01-01').getTime(),
        y: [54, 66, 69, 75, 88]
      },
      {
        x: new Date('2018-01-01').getTime(),
        y: [43, 65, 69, 76, 81]
      },
      {
        x: new Date('2019-01-01').getTime(),
        y: [31, 39, 45, 51, 59]
      },
      {
        x: new Date('2020-01-01').getTime(),
        y: [39, 46, 55, 65, 71]
      },
      {
        x: new Date('2021-01-01').getTime(),
        y: [29, 31, 35, 39, 44]
      }
    ]
  },
  {
    name: 'outliers',
    type: 'scatter',
    data: [
      {
        x: new Date('2017-01-01').getTime(),
        y: 32
      },
      {
        x: new Date('2018-01-01').getTime(),
        y: 25
      },
      {
        x: new Date('2019-01-01').getTime(),
        y: 64
      },
      {
        x: new Date('2020-01-01').getTime(),
        y: 27
      },
      {
        x: new Date('2021-01-01').getTime(),
        y: 15
      }
    ]
  }
]

const BoxplotChartOptions ={
  chart: {
    type: 'boxPlot',
    height: 350
  },
  colors: ['#008FFB', '#FEB019'],
  title: {
    text: 'BoxPlot - Scatter Chart',
    align: 'left'
  },
  xaxis: {
    type: 'datetime',
    tooltip: {
      formatter: function (val) {
        return new Date(val).getFullYear()
      }
    }
  },
  tooltip: {
    shared: false,
    intersect: true
  }
}

const $props = defineProps({
  showNormalizationGraph: Boolean
})
</script>
