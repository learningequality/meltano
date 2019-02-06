import dashboardApi from '../../api/dashboards';
import designApi from '../../api/design';

const state = {
  activeDashboard: {},
  activeDashboardReports: [],
  dashboards: [],
  isAddDashboard: true,
  reports: [],
  saveDashboardSettings: { name: null, description: null },
};

const actions = {
  getDashboards({ dispatch, commit }, slug) {
    dashboardApi.getDashboards()
      .then((response) => {
        const dashboards = response.data;
        commit('setDashboards', dashboards);

        if (slug) {
          const dashboardMatch = dashboards.find(dashboard => dashboard.slug === slug);
          if (dashboardMatch) {
            dispatch('updateCurrentDashboard', dashboardMatch);
          }
        }
      });
  },
  getDashboard({ dispatch }, dashboard) {
    dashboardApi.getDashboard(dashboard.id)
      .then((response) => {
        dispatch('updateCurrentDashboard', response.data);
      });
  },
  getReports({ commit }) {
    designApi.loadReports()
      .then((response) => {
        commit('setReports', response.data);
      });
  },
  getActiveDashboardReportsWithQueryResults({ commit }) {
    const ids = state.activeDashboard.reportIds;
    const activeReports = state.reports.filter(report => ids.includes(report.id));
    dashboardApi.getActiveDashboardReportsWithQueryResults(activeReports)
      .then((response) => {
        commit('setActiveDashboardReports', response.data);
      });
  },
  setAddDashboard({ commit }, value) {
    commit('setAddDashboard', value);
  },
  saveDashboard({ dispatch, commit }, data) {
    dashboardApi.saveDashboard(data)
      .then((response) => {
        dispatch('updateCurrentDashboard', response.data);
        commit('addSavedDashboardToDashboards', response.data);
        commit('resetSaveDashboardSettings');
      });
  },
  addReportToDashboard({ dispatch }, data) {
    dashboardApi.addReportToDashboard(data)
      .then((response) => {
        dispatch('updateCurrentDashboard', response.data);
      });
  },
  removeReportFromDashboard({ dispatch }, data) {
    dashboardApi.removeReportFromDashboard(data)
      .then((response) => {
        dispatch('updateCurrentDashboard', response.data);
      });
  },
  updateCurrentDashboard({ commit }, dashboard) {
    commit('setAddDashboard', false);
    commit('setCurrentDashboard', dashboard);
  },
};

const mutations = {
  addSavedDashboardToDashboards(_, dashboard) {
    state.dashboards.push(dashboard);
  },
  resetSaveDashboardSettings() {
    state.saveDashboardSettings = { name: null, description: null };
  },
  setActiveDashboardReports(_, reports) {
    state.activeDashboardReports = reports;
  },
  setAddDashboard(_, value) {
    state.isAddDashboard = value;
  },
  setCurrentDashboard(_, dashboard) {
    state.activeDashboard = dashboard;
  },
  setDashboards(_, dashboards) {
    state.dashboards = dashboards;
  },
  setReports(_, reports) {
    state.reports = reports;
  },
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
};
