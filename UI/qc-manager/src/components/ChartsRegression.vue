<template>
  <div v-show="$props.showRegressionGraph" class="rounded-card" style="margin-top: 10px">
    <h3>График регрессии</h3>
    <div
      style="
        background-color: gray;
        color: white;
        width: auto;
        height: 200px;
        text-align: center;
        line-height: 200px;
      "
    >
      График
    </div>
  </div>
</template>

<script setup>
const $props = defineProps({
  showRegressionGraph: Boolean
})
</script>
