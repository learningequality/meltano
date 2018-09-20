<template>
  <div v-show="results.length">
    <component :is="chartType"
      :datasets="[4, 6, 5, 8, 7, 9]"
      :labels="['a','b','c','d','e','f']"></component>
  </div>
</template>
<script>
import { mapState } from 'vuex';
// import { BarChart, LineChart, AreaChart, ScatterChart } from './charts';
import { BarChart } from 'meltano-dashboard';

export default {
  name: 'Bar',
  components: {
    BarChart,
  },
  mounted() {
    console.log('BarChart', BarChart);
  },
  computed: {
    ...mapState('explores', [
      'results',
      'chartType',
    ]),
  },
};
</script>
