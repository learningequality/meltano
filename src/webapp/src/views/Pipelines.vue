<script>
import { mapGetters, mapState } from 'vuex'

import RouterViewLayout from '@/views/RouterViewLayout'
import Step from '@/components/generic/bulma/Step'

export default {
  name: 'Pipelines',
  components: {
    RouterViewLayout,
    Step
  },
  data() {
    return {
      steps: [
        {
          name: 'extractors',
          routeMatches: ['extractors', 'extractorSettings']
        },
        {
          name: 'loaders',
          routeMatches: ['loaders', 'loaderSettings']
        },
        {
          name: 'transforms',
          routeMatches: ['transforms']
        },
        {
          name: 'schedules',
          routeMatches: ['schedules', 'createSchedule', 'runLog']
        }
      ]
    }
  },
  computed: {
    ...mapGetters('plugins', [
      'getIsStepLoadersMinimallyValidated',
      'getIsStepTransformsMinimallyValidated',
      'getIsStepScheduleMinimallyValidated'
    ]),
    ...mapState('plugins', ['installedPlugins']),
    ...mapState('configuration', ['installedPlugins']),
    currentStep() {
      return this.steps.find(step =>
        step.routeMatches.find(match => this.$route.name === match)
      )
    },
    getIsActiveStep() {
      return stepName => this.currentStep.name === stepName
    },
    getModalName() {
      return this.$route.name
    },
    isModal() {
      return this.$route.meta.isModal
    }
  },
  created() {
    this.$store.dispatch('plugins/getAllPlugins')
    this.$store.dispatch('plugins/getInstalledPlugins')
  },
  methods: {
    setStep(stepName) {
      const targetStep = this.steps.find(step => step.name === stepName)
      this.$router.push(targetStep)
    }
  }
}
</script>

<template>
  <router-view-layout>
    <div class="container view-body is-fluid">
      <div id="steps-data-setup" class="steps is-small">
        <div class="steps-content">
          <Step>
            <router-view></router-view>
            <div v-if="isModal">
              <router-view :name="getModalName"></router-view>
            </div>
          </Step>
        </div>
      </div>
    </div>
  </router-view-layout>
</template>

<style lang="scss">
.steps .steps-content {
  margin-top: 0;
}
</style>
