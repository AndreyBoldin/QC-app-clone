<template>
  <div style="margin-top: 20px;">
  <div :class = "{'grid': showMainTable === true, 'no-table-grid': showMainTable === false}">
    <MainTable @select-metabolite=" handleSelectedMetabolite" @update:showMainTable="handleShowMainTableChange" />
  <div style="display: flex; justify-content: center; flex-wrap: nowrap; width: 100%">
    <ChartsMetabolite
      v-if="selectedMetabolite"
      style="grid-column: 1;"
      :selected-metabolite="selectedMetabolite"
      @clear-selected-metabolite="handleClearSelectedMetabolite"
    />
    <div
      v-if="!selectedMetabolite"
      style="
        height: 90vh;
        flex-grow: 1;    
        overflow-y: auto;
        margin-left: 15px;
        flex-direction: column;
        padding-right: 10px;
      "
    >
      <div class="rounded-card" style="display: flex; justify-content: space-between">
        <h2 style="font-weight: 500">Регрессия для LabQC</h2>
        <button class="btn" @click="showRegressionGraph = !showRegressionGraph">
          <p v-if="showRegressionGraph">Закрыть</p>
          <p v-else>Открыть</p>
        </button>
      </div>
      <ChartsRegression :show-regression-graph="showRegressionGraph" />
      <div
        class="rounded-card"
        style="margin-top: 10px; display: flex; justify-content: space-between"
      >
        <h2 style="font-weight: 500">Оценка нормализации</h2>
        <button class="btn" @click="showNormalizationGraph = !showNormalizationGraph">
          <p v-if="showNormalizationGraph">Закрыть</p>
          <p v-else>Открыть</p>
        </button>
      </div>
      <ChartsNormalization :show-normalization-graph="showNormalizationGraph" />
    </div>
  </div>
  </div>
</div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted, provide } from 'vue';
import MainTable from '../components/MainTable.vue'
import ChartsMetabolite from '../components/ChartsMetabolite.vue'
import ChartsRegression from '../components/ChartsRegression.vue'
import ChartsNormalization from '../components/ChartsNormalization.vue'

const showMainTable = ref(true)

const selectedMetabolite = ref(null)

provide('selectedMetabolite', selectedMetabolite)

const showRegressionGraph = ref(false)
const showNormalizationGraph = ref(false)

function handleSelectedMetabolite(metabolite) {
  selectedMetabolite.value = metabolite
}

function handleClearSelectedMetabolite() {
  selectedMetabolite.value = null
}

function handleShowMainTableChange() {
  showMainTable.value = !showMainTable.value
}

const projects = ref([]);

onMounted(() => {
  axios.get(variables.API_URL + 'projects')
    .then(response => {
      console.log(response.data);
      projects.value = response.data;
    })
    .catch(error => {
      console.error(error);
    });
});
</script>

<style>
.grid {
  display: grid;
  grid-template-columns: minmax(600px, 1.1fr) 1fr
}

.no-table-grid {
  display: grid;
  grid-template-columns: 45px auto;
}

.gradient-bg {
  background-image: radial-gradient(
    circle 1292px at -13.6% 81.7%,
    rgb(0, 27, 68) 0%,
    rgb(107, 120, 157) 70%,
    rgba(1, 27, 83, 0.817) 100%
  );
  color: white !important;
}




.btn {
  background-color: #e7e5e6;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  margin-left: 10px;
  border-radius: 5px;
}
.btn:hover {
  background-color: #2c3a43;
  color: white;
}
.btn:active {
  background-color: #161890 !important;
  color: white;
}
</style>
