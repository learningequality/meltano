<script>
import Breadcrumbs from '@/components/navigation/Breadcrumbs'
import MainNav from '@/components/navigation/MainNav'
import Footer from '@/components/generic/Footer'
import TermsOfServiceModal from '@/components/generic/TermsOfServiceModal'

export default {
  name: 'App',
  components: {
    Breadcrumbs,
    MainNav,
    Footer,
    TermsOfServiceModal
  },
  created() {
    this.$store.dispatch('system/check')
    this.tryAcknowledgeAnalyticsTracking()
  },
  methods: {
    tryAcknowledgeAnalyticsTracking() {
      if (this.$flask.isSendAnonymousUsageStats) {
        const hasAcknowledgedTracking =
          'hasAcknowledgedTracking' in localStorage &&
          localStorage.getItem('hasAcknowledgedTracking') === 'true'
        if (!hasAcknowledgedTracking) {
          this.$toasted.global.acknowledgeAnalyticsTracking()
        }
      }
    }
  }
}
</script>

<template>
  <div id="app">
    <main-nav />
    <Breadcrumbs />
    <router-view />
    <Footer />
    <TermsOfServiceModal />
  </div>
</template>

<style lang="scss">
@import 'scss/_index.scss';

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
