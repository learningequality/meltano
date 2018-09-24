<template>
  <div v-show="results.length">
    <component :is="chartType"
      :datasets="[4, 6, 5, 8, 7, 9]"
      :labels="resultMeasures"></component>
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
    console.log('columnHeaders', this.columnHeaders);
    console.log('resultMeasures', this.resultMeasures);
    console.log('results', JSON.stringify(this.results));
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
