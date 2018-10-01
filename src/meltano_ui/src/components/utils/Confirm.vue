<template>
  <div class="modal" :class="{'is-active': open}">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">{{title}}</p>
        <button class="delete" aria-label="close" @click="$emit('closed', false)"></button>
      </header>
      <section class="modal-card-body">
        {{content}}
      </section>
      <footer class="modal-card-foot">
        <button class="button is-primary" @click="$emit('closed', true)">{{primary}}</button>
        <button class="button" @click="$emit('closed', false)">{{secondary}}</button>
      </footer>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    open: {
      type: Boolean,
    },
    title: {
      type: String,
    },
    content: {
      type: String,
    },
    primary: {
      type: String,
      default: 'Ok',
    },
    secondary: {
      type: String,
      default: 'Cancel',
    },
  },
  data() {
    return {
      show: this.open,
    };
  },
};
</script>
