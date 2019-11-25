<script>
import { mapActions, mapState } from 'vuex'
import Chart from '@/components/analyze/Chart'
import NewDashboardModal from '@/components/dashboards/NewDashboardModal'
import RouterViewLayout from '@/views/RouterViewLayout'

export default {
  name: 'Dashboards',
  components: {
    Chart,
    NewDashboardModal,
    RouterViewLayout
  },
  data() {
    return {
      isActiveDashboardLoading: false,
      isInitializing: false,
      isNewDashboardModalOpen: false
    }
  },
  computed: {
    ...mapState('dashboards', [
      'activeDashboard',
      'activeDashboardReports',
      'dashboards',
      'reports'
    ]),
    isActive() {
      return dashboard => dashboard.id === this.activeDashboard.id
    }
  },
  watch: {
    activeDashboard() {
      this.isActiveDashboardLoading = true
      this.getActiveDashboardReportsWithQueryResults().then(() => {
        this.isActiveDashboardLoading = false
      })
    }
  },
  beforeDestroy() {
    this.$store.dispatch('dashboards/resetActiveDashboard')
    this.$store.dispatch('dashboards/resetActiveDashboardReports')
  },
  created() {
    this.isInitializing = true
    this.initialize(this.$route.params.slug).then(() => {
      this.isInitializing = false
    })
  },
  methods: {
    ...mapActions('dashboards', [
      'initialize',
      'updateCurrentDashboard',
      'getActiveDashboardReportsWithQueryResults'
    ]),
    goToDashboard(dashboard) {
      this.updateCurrentDashboard(dashboard).then(() => {
        this.$router.push({ name: 'dashboard', params: dashboard })
      })
    },
    goToDesign(report) {
      const params = {
        design: report.design,
        model: report.model,
        namespace: report.namespace
      }
      this.$router.push({ name: 'analyzeDesign', params })
    },
    goToReport(report) {
      this.$router.push({ name: 'report', params: report })
    },
    toggleNewDashboardModal() {
      this.isNewDashboardModalOpen = !this.isNewDashboardModalOpen
    }
  }
}
</script>

<template>
  <router-view-layout>
    <div class="container view-body is-fluid">
      <section>
        <div class="columns is-vcentered">
          <div class="column">
            <h2 class="title is-5">{{ activeDashboard.name }}</h2>
            <h3 v-if="activeDashboard.description" class="subtitle">
              {{ activeDashboard.description }}
            </h3>
          </div>
        </div>

        <div class="columns">
          <div class="column">
            <template v-if="activeDashboard.name">
              <progress
                v-if="isActiveDashboardLoading"
                class="progress is-small is-info"
              >
              </progress>
              <template v-else>
                <template v-if="activeDashboardReports.length > 0">
                  <div
                    v-for="report in activeDashboardReports"
                    :key="report.id"
                    class='box'
                  >
                    <div class="level">
                      <div class="level-left">
                        <div class="level-item">
                          <div class="content">
                            <h5 class="has-text-centered">
                              {{ report.name }}
                            </h5>
                          </div>
                        </div>
                      </div>
                      <div class="level-right">
                        <div class="level-item">
                          <div class="buttons">
                            <a
                              class="button is-small"
                              @click="goToReport(report)"
                              >Edit</a
                            >
                            <a
                              class="button is-small"
                              @click="goToDesign(report)"
                              >Explore</a
                            >
                          </div>
                        </div>
                      </div>
                    </div>
                    <chart
                      :chart-type="report.chartType"
                      :results="report.queryResults"
                      :result-aggregates="report.queryResultAggregates"
                    ></chart>
                  </div>
                </template>
                <div v-else class="content">
                  <p>There are no reports added to this dashboard yet.</p>
                  <router-link
                    class="button is-interactive-primary is-outlined"
                    :to="{ name: 'model' }"
                    >Analyze Some Data First</router-link
                  >
                </div>
              </template>
            </template>

            <template v-else>
              <div class="column content">
                <p>
                  Select a dashboard or click "New" to the left and add
                  reports to it to view them here.
                </p>
                <p>You can add a report by:</p>
                <ul>
                  <li>
                    In Analyze, clicking "Add to Dashboard" after creating a
                    report
                  </li>
                  <li>
                    Clicking the "Add Report" button to an existing dashboard
                    (coming soon)
                  </li>
                </ul>
              </div>
            </template>

            <NewDashboardModal
              v-if="isNewDashboardModalOpen"
              @close="toggleNewDashboardModal"
            />
          </div>
        </div>
      </section>
    </div>
  </router-view-layout>
</template>

<style lang="scss"></style>
