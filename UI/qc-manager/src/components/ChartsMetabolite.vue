<template>
  <div
    v-if="$props.selectedMetabolite"
    style="display: flex; flex-direction: column; height: 90vh; margin-left: 15px; width: 100%;"
  >
    <div class="rounded-card gradient-bg" style="display: flex; justify-content: space-between">
      <h2 style="font-weight: 500">{{ $props.selectedMetabolite.name }}</h2>
      <button @click="clearSelectedMetabolite" class="btn">
        <p>Закрыть</p>
      </button>
    </div>
    <div class="rounded-card-inter" style="margin-top: 10px; display: flex; align-items: center; justify-content: space-between">
      <button @click="fetchIntraProjectInfo" class="btn">
            Сравнить внутри проекта
          </button>
          <input type="file" multiple @change="handleFileChange" ref="fileInput" />
    </div>
    <div
      style="
        overflow-y: auto;
        flex-direction: column;
        margin-top: 10px;
        padding-right: 10px;
      "
    >
      <div style="overflow-y: auto">
        <div class="rounded-card">
          <h3>1. Калибраторы</h3>

          <div class="chart-grid">
            <div v-for="(url, index) in urls_cal" :key="index">
              <img v-if="url" style="width: 100%; height: 100%; object-fit: contain;" :src="url" alt="Graph" />
            </div>
          </div>
        </div>
        <div class="rounded-card" style="margin-top: 10px">
          <h3>2. QC</h3>
          <div class="chart-grid">
            <div v-for="(url, index) in urls_qc" :key="index">
              <img v-if="url" style="width: 100%; height: 100%; object-fit: contain;" :src="url" alt="Graph" />
            </div>
          </div>
        </div>
        <div class="rounded-card" style="margin-top: 10px">
          <h3>3. LAB QC</h3>
              <img v-if="urls_labqc[0]" style="width: 100%; height: 100%; object-fit: contain;" :src="urls_labqc[0]" alt="Graph" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import * as XLSX from 'xlsx';
import { useExcelStore, useProjectStore, useIntraProjectInfo, useUserMergedExcelStore } from '../stores/excelStore.ts'
import axios from 'axios'

const userMergedExcelStore = useUserMergedExcelStore();

const intraProjectInfoStore = useIntraProjectInfo()

const projectStore = useProjectStore()

const excelStore = useExcelStore()

const fileInput = ref(null)

const $props = defineProps({
  selectedMetabolite: Object
})

const emit = defineEmits(['clear-selected-metabolite'])

function compareBatches() {
    fileInput.value.value = ''
  }

function clearSelectedMetabolite() {
  emit('clear-selected-metabolite')
}

async function handleFileChange(event) {
  const files = Array.from(event.target.files);
  let jsonData = [];

  for (const file of files) {
    const reader = new FileReader();
    reader.onload = async (event) => {
      const data = event.target.result;
      const workbook = XLSX.read(data, { type: 'array' });
      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];
      const fileData = XLSX.utils.sheet_to_json(sheet);

      const selectedMetaboliteName = $props.selectedMetabolite.name
      const filteredFileData = fileData.filter((metabolite) => Object.keys(metabolite).includes(selectedMetaboliteName)).map((metabolite) => ({
        metabolite: selectedMetaboliteName,
        concentration: metabolite[selectedMetaboliteName],
        group: metabolite['Group'],
        sample: metabolite['Sample'],
        batch: file.name.replace('.xlsx', '')
      }));

      jsonData.push(...filteredFileData);
    };
    reader.readAsArrayBuffer(file);
  }

  await Promise.all(files.map((file) => new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = resolve;
    reader.readAsArrayBuffer(file);
  })));

  userMergedExcelStore.clearData();
  userMergedExcelStore.saveData({ jsonData });
  await fetchUserMergedImages()
}

// Filtered by metabolite name json
const filteredData = computed(() => {
  const selectedMetaboliteName = $props.selectedMetabolite.name
  return excelStore.state.jsonData.filter((metabolite) => Object.keys(metabolite).includes(selectedMetaboliteName)).map((metabolite) => ({
    metabolite: selectedMetaboliteName,
    concentration: metabolite[selectedMetaboliteName],
    group: metabolite['Group'],
    sample: metabolite['Sample'],
  }))
  
})

const filteredDataIntra = computed(() => {
  const selectedMetaboliteName = $props.selectedMetabolite.name
  return intraProjectInfoStore.state.jsonData.filter((metabolite) => Object.keys(metabolite).includes(selectedMetaboliteName)).map((metabolite) => ({
    metabolite: selectedMetaboliteName,
    concentration: metabolite[selectedMetaboliteName],
    group: metabolite['Group'],
    sample: metabolite['Sample'],
    batch: metabolite['Batch'],
  }))
})

const urls_cal = ref([])
const urls_qc = ref([])
const urls_labqc = ref([])

async function fetchImages() {
    try {
      const data = filteredData.value
      const response = await axios.post(variables.API_URL + 'generate_cal_plots/', data)
      console.log(response.data)
      console.log(data)
      urls_cal.value = []
      for (let i = 1; i <= 6; i++) {
        const response = await axios.get(variables.API_URL + `get_cal_plot/${i}/`, { responseType: 'blob' })
        console.log(response.data) // log the API response
        urls_cal.value.push(URL.createObjectURL(response.data))
      }
    } catch (error) {
      console.error(error)
    }
    try {
        const data = filteredData.value
        const response = await axios.post(variables.API_URL + 'generate_qc_plots/', data)
        console.log(response.data)
        console.log(data)
        urls_qc.value = []
        for (let i = 1; i <= 3; i++) {
          const response = await axios.get(variables.API_URL + `get_qc_plot/${i}/`, { responseType: 'blob' })
          console.log(response.data) // log the API response
          urls_qc.value.push(URL.createObjectURL(response.data))
        }
      } catch (error) {
        console.error(error)
      }
      try {
        const data = filteredData.value
        const response = await axios.post(variables.API_URL + 'generate_labqc_plots/', data)
        console.log(response.data)
        console.log(data)
        urls_labqc.value = []
        const response_2 = await axios.get(variables.API_URL + 'get_labqc_plot/', { responseType: 'blob' })
        console.log(response_2.data) // log the API response
        urls_labqc.value.push(URL.createObjectURL(response_2.data))
        }
      catch (error) {
        console.error(error)
      }
}

async function fetchIntraProjectCalImages() {
  try {
    const data = filteredDataIntra.value
    const response = await axios.post(variables.API_URL + 'generate_cal_intra_projects_plots/', data)
    console.log(response.data)
    urls_cal.value = []
    for (let i = 1; i <= 6; i++) {
      const response = await axios.get(variables.API_URL + `get_cal_intra_projects_plot/${i}/`, { responseType: 'blob' })
      console.log(response.data) // log the API response
      urls_cal.value.push(URL.createObjectURL(response.data))
    }
  } catch (error) {
    console.error(error)
  }
  try {
    const data = filteredDataIntra.value
    const response = await axios.post(variables.API_URL + 'generate_intra_qc_plots/', data)
    console.log(response.data)
    urls_qc.value = []
    for (let i = 1; i <= 3; i++) {
      const response = await axios.get(variables.API_URL + `get_intra_qc_plots/${i}/`, { responseType: 'blob' })
      console.log(response.data) // log the API response
      urls_qc.value.push(URL.createObjectURL(response.data))
    }
  } catch (error) {
    console.error(error)
  }
  
  try {
        const data = filteredDataIntra.value
        const response = await axios.post(variables.API_URL + 'generate_intra_labqc_plots/', data)
        console.log(response.data)
        console.log(data)
        urls_labqc.value = []
        const response_2 = await axios.get(variables.API_URL + 'get_intra_labqc_plot/', { responseType: 'blob' })
        console.log(response_2.data) // log the API response
        urls_labqc.value.push(URL.createObjectURL(response_2.data))
        }
      catch (error) {
        console.error(error)
      }
}

async function fetchUserMergedImages() {
  try {
    const data =  userMergedExcelStore.state.jsonData
    console.log('Данные', data)
    const response = await axios.post(variables.API_URL + 'generate_cal_intra_projects_plots/', data)
    console.log(response.data)
    console.log(data)
    urls_cal.value = []
    for (let i = 1; i <= 6; i++) {
      const response = await axios.get(variables.API_URL + `get_cal_intra_projects_plot/${i}/`, { responseType: 'blob' })
      console.log(response.data) // log the API response
      urls_cal.value.push(URL.createObjectURL(response.data))
    }
  } catch (error) {
    console.error(error)
  }
  try {
    const data =  userMergedExcelStore.state.jsonData
    const response = await axios.post(variables.API_URL + 'generate_intra_qc_plots/', data)
    console.log(response.data)
    console.log(data)
    urls_qc.value = []
    for (let i = 1; i <= 3; i++) {
      const response = await axios.get(variables.API_URL + `get_intra_qc_plots/${i}/`, { responseType: 'blob' })
      console.log(response.data) // log the API response
      urls_qc.value.push(URL.createObjectURL(response.data))
    }
  } catch (error) {
    console.error(error)
  }
  try {
    const data =  userMergedExcelStore.state.jsonData
    const response = await axios.post(variables.API_URL + 'generate_intra_labqc_plots/', data)
    console.log(response.data)
    console.log(data)
    urls_labqc.value = []
    const response_2 = await axios.get(variables.API_URL + 'get_intra_labqc_plot/', { responseType: 'blob' })
    console.log(response_2.data) // log the API response
    urls_labqc.value.push(URL.createObjectURL(response_2.data))
  } catch (error) {
    console.error(error)
  }
}

async function fetchIntraProjectInfo() {
  compareBatches();
  if (intraProjectInfoStore.state.jsonData.length > 0) {
  await fetchIntraProjectCalImages();
    return;
  }
  else {
  const projectId = projectStore.state.id;
  try {
    const response = await axios.get(variables.API_URL + 'batches/?project_id=' + projectId);
    const batches = response.data;
    const jsonData = {
      jsonData: []
    };
    const metaboliteResponse = await axios.get(variables.API_URL + 'metabolites/');
    const metabolites = metaboliteResponse.data;
    for (let i = 0; i < batches.length; i++) {
      const batch = batches[i];
      const batchName = batch.batch_num;
      const samplesResponse = await axios.get(variables.API_URL + 'samples/?batch_id=' + batch.id);
      const samples = samplesResponse.data;
      for (let j = 0; j < samples.length; j++) {
        const sample = samples[j];
        const metaboliteConcResponse = await axios.get(variables.API_URL + 'metabolite_conc/?sample_id=' + sample.id);
        const metaboliteConc = metaboliteConcResponse.data;
        const groupResponse = await axios.get(variables.API_URL + 'groups/?id=' + sample.group_id);
        const groupName = groupResponse.data[0].group_name;
        const metaboliteConcObj = {};
        metaboliteConc.forEach((conc) => {
          const metabolite = metabolites.find((m) => m.id === conc.metabolite_id);
          if (metabolite) {
            metaboliteConcObj[`${metabolite.metabolite_name}`] = conc.concentration;
          }
        });
        const obj = {
          Batch: batchName,
          Group: groupName,
          Sample: sample.sample_name,
          ...metaboliteConcObj
        };
        console.log(obj);
        jsonData.jsonData.push(obj);
      }
    }
    intraProjectInfoStore.saveIntraProjectInfo(jsonData);
  } catch (error) {
    console.error(error);
  } 
  await fetchIntraProjectCalImages();}
}

  onMounted(() => {
    fetchImages()
  })

  watch($props, () => {
    fetchImages()
  })

  // onUnmounted(() => {
  //   intraProjectInfoStore.clearIntraProjectInfo()
  // })
</script>

<style>

</style>