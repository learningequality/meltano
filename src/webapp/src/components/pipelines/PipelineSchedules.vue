<script>
import { mapGetters, mapState } from 'vuex'

import Dropdown from '@/components/generic/Dropdown'
import ScheduleTableHead from '@/components/pipelines/ScheduleTableHead'

import utils from '@/utils/utils'

export default {
  name: 'PipelineSchedules',
  components: {
    Dropdown,
    ScheduleTableHead
  },
  computed: {
    ...mapState('configuration', ['pipelines']),
    ...mapGetters('configuration', ['getHasPipelines']),
    ...mapGetters('plugins', ['getIsPluginInstalled']),
    getFormattedDateStringYYYYMMDD() {
      return val => utils.formatDateStringYYYYMMDD(val)
    }
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (from.name === 'transforms') {
        vm.goToCreatePipeline()
      }
    })
  },
  created() {
    this.$store.dispatch('configuration/getAllPipelineSchedules')
  },
  methods: {
    goToCreatePipeline() {
      this.$router.push({ name: 'createSchedule' })
    },
    goToLog(jobId) {
      this.$router.push({ name: 'runLog', params: { jobId } })
    },
    runELT(pipeline) {
      this.$store.dispatch('configuration/run', pipeline)
    }
  }
}
</script>

<template>
  <div>
    <div class="columns is-vcentered">
      <div class="column">
        <h2 class="title is-5">Add Dataset Connection</h2>
      </div>
    </div>

    <div class="box">
      <table class="table is-fullwidth is-narrow is-hoverable">
        <thead>
          <tr>
            <th>
              <span>Name</span>
              <span
                class="icon has-text-grey-light tooltip is-tooltip-multiline is-tooltip-right"
                data-tooltip="The unique identifier for an ELT pipeline schedule and its settings."
              >
                <font-awesome-icon icon="info-circle"></font-awesome-icon>
              </span>
            </th>
            <th>
              <span>Data Source</span>
              <span
                class="icon has-text-grey-light tooltip is-tooltip-multiline"
                data-tooltip="The connector for data extraction within a scheduled ELT pipeline."
              >
                <font-awesome-icon icon="info-circle"></font-awesome-icon>
              </span>
            </th>
            <th>
              <span>Update Interval</span>
              <span
                class="icon has-text-grey-light tooltip is-tooltip-multiline"
                data-tooltip="The connector for data loading within a scheduled ELT pipeline."
              >
                <font-awesome-icon icon="info-circle"></font-awesome-icon>
              </span>
            </th>
            <th class="has-text-right">
              <span>Actions</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <div class="field">
                <div class="control">
                  <input
                    class="input"
                    type="text"
                    placeholder="Connection Name"
                    value="GitLab - Meltano"
                  />
                </div>
              </div>
            </td>
            <td>
              <div class="field">
                <div class="control">
                  <div class="select is-fullwidth">
                    <select>
                      <option>GitLab</option>
                      <option>Google Analytics</option>
                    </select>
                  </div>
                </div>
              </div>
            </td>
            <td>
              <div class="field">
                <div class="control">
                  <div class="select is-fullwidth">
                    <select>
                      <option>Hourly</option>
                      <option>Daily</option>
                    </select>
                  </div>
                </div>
              </div>
            </td>
            <td class="has-text-right">
              <a class="button is-success">
                Add
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <br />

    <div class="columns is-vcentered">
      <div class="column">
        <h2 class="title is-5">Connected Datasets</h2>
      </div>
    </div>

    <div v-if="getHasPipelines" class="box">
      <table class="table is-fullwidth is-narrow is-hoverable">
        <thead>
          <tr>
            <th>
              <span>Name</span>
              <span
                class="icon has-text-grey-light tooltip is-tooltip-multiline is-tooltip-right"
                data-tooltip="The unique identifier for an ELT pipeline schedule and its settings."
              >
                <font-awesome-icon icon="info-circle"></font-awesome-icon>
              </span>
            </th>
            <th>
              <span>Data Source</span>
              <span
                class="icon has-text-grey-light tooltip is-tooltip-multiline"
                data-tooltip="The connector for data extraction within a scheduled ELT pipeline."
              >
                <font-awesome-icon icon="info-circle"></font-awesome-icon>
              </span>
            </th>
            <th>
              <span>Update Interval</span>
              <span
                class="icon has-text-grey-light tooltip is-tooltip-multiline"
                data-tooltip="The connector for data loading within a scheduled ELT pipeline."
              >
                <font-awesome-icon icon="info-circle"></font-awesome-icon>
              </span>
            </th>
            <th>
              <span>Last Updated</span>
              <span
                class="icon has-text-grey-light tooltip is-tooltip-multiline"
                data-tooltip="The connector for data loading within a scheduled ELT pipeline."
              >
                <font-awesome-icon icon="info-circle"></font-awesome-icon>
              </span>
            </th>
            <th>
              <span>Start Date</span>
              <span
                class="icon has-text-grey-light tooltip is-tooltip-multiline"
                data-tooltip="The connector for data loading within a scheduled ELT pipeline."
              >
                <font-awesome-icon icon="info-circle"></font-awesome-icon>
              </span>
            </th>
            <th>
              <span>Status</span>
              <span
                class="icon has-text-grey-light tooltip is-tooltip-multiline"
                data-tooltip="The connector for data loading within a scheduled ELT pipeline."
              >
                <font-awesome-icon icon="info-circle"></font-awesome-icon>
              </span>
            </th>
            <th class="has-text-right">
              <span>Actions</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              Google Analytics - Marketing Website
            </td>
            <td>
              Google Analytics
            </td>
            <td>
              Weekly
            </td>
            <td>
              Three days ago
            </td>
            <td>
              11/1/19
            </td>
            <td>
              <a class="button is-small">Log</a>
            </td>
            <td class="has-text-right">
              <Dropdown
                label="Reports"
                button-classes="is-interactive-primary is-outlined is-small"
                icon-open="chart-line"
                icon-close="caret-down"
                is-right-aligned
                is-up
              ></Dropdown>
            </td>
          </tr>
          <tr>
            <td>
              Google Analytics - MAUI
            </td>
            <td>
              Google Analytics
            </td>
            <td>
              Daily
            </td>
            <td>
              Yesterday
            </td>
            <td>
              11/1/19
            </td>
            <td>
              <a class="button is-small">Log</a>
            </td>
            <td class="has-text-right">
              <Dropdown
                label="Reports"
                button-classes="is-interactive-primary is-outlined is-small"
                icon-open="chart-line"
                icon-close="caret-down"
                is-right-aligned
                is-up
              ></Dropdown>
            </td>
          </tr>
          <tr>
            <td>
              Google Analytics - CLI
            </td>
            <td>
              Google Analytics
            </td>
            <td>
              Weekly
            </td>
            <td>
              Three days ago
            </td>
            <td>
              11/1/19
            </td>
            <td>
              <a class="button is-small">Log</a>
            </td>
            <td class="has-text-right">
              <Dropdown
                label="Reports"
                button-classes="is-interactive-primary is-outlined is-small"
                icon-open="chart-line"
                icon-close="caret-down"
                is-right-aligned
                is-up
              ></Dropdown>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="content">
      <p>
        There are no pipelines scheduled yet.
        <router-link to="schedules/create"
          >Schedule your first Pipeline</router-link
        >
        now.
      </p>
    </div>
  </div>
</template>

<style lang="scss"></style>
