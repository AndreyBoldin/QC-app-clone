<template>
  <div>
    <table >
      <thead>
        <tr style="background-color: #202c34; color: white">
          <th rowspan="2" style="text-align: left; padding: 10px;">Metabolite</th>
          <th :colspan="labqcLength">LabQC</th>
        </tr>
        <tr>
          <th v-for ="i in labqcLength" :key="i">{{ i }}</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(metabolite, index) in metaboliteData"
          :key="index"
          
        >
          <td
            style="background-color: var(--primary-color); color: var(--text-color);"
            @click="handleSelectMetabolite(metabolite)"
          >
            <p
              class="hover-effect"
              :class="{
            'selected-metabolite-th': Metabolite === metabolite}"
              style="width: 180px; padding:3px 0px 3px 10px ; text-align: left;"
            >
              {{ metabolite.name }}
            </p>
          </td>
          <td v-for="(value, index) in metabolite.labqc" class="table-cell" :class="{ 'selected-metabolite-row': Metabolite === metabolite }" :key="index">
            <div class="color-circle" :class="colorMap[value]" :title="metabolite.labqc[index]" ></div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  </template>
  
<script setup>
import { inject, ref, onMounted } from 'vue'
import { useExcelStore } from '@/stores/excelStore';

const excelStore = useExcelStore()

const metaboliteData = ref([])
const labqcLength = ref()

onMounted(async () => {
  try {
    const response = await axios.post(variables.API_URL + 'table_labqc/', excelStore.state.jsonData)
    console.log(response.data);
    metaboliteData.value = response.data
    labqcLength.value = response.data.length > 0 ? response.data[0].labqc.length : 0
  } catch (e) {
    console.log(e);
  }
})

  const emit = defineEmits(['select-metabolite'])
  
  const Metabolite = inject('selectedMetabolite')

  
  const colorMap = {
    passed: 'passed-color',
    semi_low: 'semi_low-color',
    low: 'low-color',
    semi_high: 'semi_high-color',
    high: 'high-color',
  }
  
  function handleSelectMetabolite(metabolite) {
    Metabolite.value = metabolite
    emit('select-metabolite', metabolite)
  }
  </script>
  