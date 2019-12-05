<script>

export default {
  name: 'TermsOfServiceModal',
  data() {
    return {
      isActive: false
    }
  },
  created() {
    this.tryAcknowledgeTermsOfService()
  },
  methods: {
    acknowledge() {
      localStorage.setItem('hasAcknowledgedTermsOfService', true)
      this.isActive = false
      this.selfDestruct()
    },
    selfDestruct() {
      this.$destroy()
      this.$el.parentNode.removeChild(this.$el)
    },
    tryAcknowledgeTermsOfService() {
      const hasAcknowledgedTermsOfService =
        'hasAcknowledgedTermsOfService' in localStorage &&
        localStorage.getItem('hasAcknowledgedTermsOfService') === `true`
      if (!hasAcknowledgedTermsOfService) {
        this.isActive = true
      }
    }
  }
}
</script>

<template>
  <div class="modal" :class="{ 'is-active': isActive }">
    <div class="modal-background"></div>
    <div class="modal-card is-wide">
      <header class="modal-card-head">
        <p class="modal-card-title">
          Terms of Service
        </p>
      </header>
      <section ref="log-view" class="modal-card-body is-overflow-y-scroll">
        <div class="content">
          <p>TOS here...</p>
        </div>
      </section>
      <footer class="modal-card-foot buttons is-right">
        <button class="button is-interactive-primary" @click="acknowledge">Acknowledge</button>
      </footer>
    </div>
  </div>
</template>

<style lang="scss"></style>
