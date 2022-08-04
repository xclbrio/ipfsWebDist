<template>
  <div class="tooltip">
    <slot></slot>
  </div>
</template>

<script></script>

<style lang="scss">
@import "../_base.scss";
.tooltip {
  border: 5px solid $black-three;
  background-color: $black-four;
  padding: 15px;
  box-sizing: border-box;
  width: 377px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  z-index: 3;
}
</style>