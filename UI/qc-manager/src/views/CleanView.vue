<template>
    <div>
    <h1 style="margin-top: 10px; margin-bottom: 5px;">Очистка данных</h1>
    <pre style="overflow-y: auto; max-height: 60vh; width: 500px;"> {{ excelStore.state.jsonData }}</pre>
    <p> {{ projects }}</p>
    <p> {{ batches }}</p>
    </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import axios from 'axios'
import {useExcelStore} from '../stores/excelStore.ts'

const excelStore = useExcelStore()

const projects = ref('')
const batches = ref('')

onMounted(() => {
  axios.get(variables.API_URL + 'projects')
    .then(response => {
      console.log(response.data);
      projects.value = response.data;
    })
    .catch(error => {
      console.error(error);
    });

  axios.get(variables.API_URL + 'batches')
    .then(response => {
      console.log(response.data);
      batches.value = response.data;
    })
    .catch(error => {
      console.error(error);
    });
});
</script>

