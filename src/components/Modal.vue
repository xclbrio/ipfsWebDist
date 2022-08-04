<template>
  <div class="modal">
    <div class="modal-container">
      <div class="modal-header">
        <slot name="header">
          {{ title }}
        </slot>
      </div>
      <div class="modal-content">
        <slot name="content">
          {{ content }}
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: '',
    },
    content: {
      type: String,
      default: ''
    }
  }
}

</script>