<template>
    <div class="main-div">
    <table 
       v-for="group in uniqueGroups" :key="group"
       >
    <thead>
    <tr style=" color: white">
        <th>Samples</th>
        <th >{{ group }}</th>
    </tr>
    </thead>
    <tbody>
        <tr v-for="sample in filteredSamplesByGroup(group)"
        :class="{
            'selected-sample': Sample === sample,
            tr: Sample != sample
          }"
          align="center" :key="sample.sample_name">
          <td
          @click = "Sample = sample"
            class="hover-effect"
            style="background-color: var(--primary-color); color: var(--text-color);" >
            <p
            class="hover-sample"
              style="width: 100px; padding:3px 0px 3px 10px ; text-align: left;"
            >
              {{ sample.sample_name }}
            </p>
        
        </td>
          <td class="table-cell">
            <div class="color-circle" :class="colorMap[sample.level]"></div>
          </td>
        </tr>
    </tbody>
</table>
</div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useExcelStore } from '../stores/excelStore.ts'
import axios from 'axios';

const excelStore = useExcelStore()

const Sample = ref(null)
const sampleData = ref([])

onMounted(async () => {
  try {
    const response = await axios.post(variables.API_URL + 'table_samples/', excelStore.state.jsonData)
    console.log(response.data);
    sampleData.value = response.data
  } catch (e) {
    console.log(e);
  }
})

const uniqueGroups = computed(() => {
  return [...new Set(sampleData.value.map(item => item.group))]
})

function filteredSamplesByGroup(group) {
    return sampleData.value.filter(item => item.group === group)
}

const colorMap = {
passed: 'passed-color',
semi_passed: 'semi_passed-color',
not_passed: 'high-color',
}
</script>

<style scoped>
.main-div {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  max-height: 200vh;
}

.hover-sample:hover {
    color: var(--text-color);
    font-weight: bold;
}

.col {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
  </style>
