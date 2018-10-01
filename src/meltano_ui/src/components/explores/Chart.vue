<template>
  <div v-show="results.length">
    <component :is="chartType"
      :datasets="[4, 6, 5, 8, 7, 9]"
      :labels="[1,2,3,4,5,6]"></component>
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
  },
  computed: {
    ...mapState('explores', [
      'results',
      'resultMeasures',
      'columnHeaders',
      'chartType',
    ]),
  },
};
</script>
