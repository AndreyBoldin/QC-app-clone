<template>
    <table>
      <thead>
        <tr>
          <th rowspan="2" style="text-align: left; padding: 10px;">Metabolite</th>
          <th rowspan="2">Cal-1</th>
          <th rowspan="2">Cal-2</th>
          <th rowspan="2">Cal-3</th>
          <th rowspan="2">Cal-4</th>
          <th rowspan="2">Cal-5</th>
          <th rowspan="2">Cal-6</th>
          <th>LQC</th>
          <th>MQC</th>
          <th>HQC</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(metabolite, index) in metaboliteData"
          :key="index"
        >
          <td
            class="hover-effect"
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
          <td class="table-cell" :class="{ 'selected-metabolite-row': Metabolite === metabolite }" :title="metabolite.calibrators[0]">
            <div class="color-circle" :class="colorMap[metabolite.calibrators[0]]"></div>
          </td>
          <td class="table-cell" :class="{ 'selected-metabolite-row': Metabolite === metabolite }" :title="metabolite.calibrators[1]">
            <div class="color-circle" :class="colorMap[metabolite.calibrators[1]]"></div>
          </td>
          <td class="table-cell" :class="{ 'selected-metabolite-row': Metabolite === metabolite }" :title="metabolite.calibrators[2]">
            <div class="color-circle" :class="colorMap[metabolite.calibrators[2]]"></div>
          </td>
          <td class="table-cell" :class="{ 'selected-metabolite-row': Metabolite === metabolite }" :title="metabolite.calibrators[3]">
            <div class="color-circle" :class="colorMap[metabolite.calibrators[3]]"></div>
          </td>
          <td class="table-cell" :class="{ 'selected-metabolite-row': Metabolite === metabolite }" :title="metabolite.calibrators[4]">
            <div class="color-circle" :class="colorMap[metabolite.calibrators[4]]"></div>
          </td>
          <td class="table-cell" :class="{ 'selected-metabolite-row': Metabolite === metabolite }" :title="metabolite.calibrators[5]">
            <div class="color-circle" :class="colorMap[metabolite.calibrators[5]]"></div>
          </td>
          <td class="table-cell" :class="{ 'selected-metabolite-row': Metabolite === metabolite }" :title="getWorstLevel(metabolite.lqc)">
            <div class="color-circle" :class="colorMap[getWorstLevel(metabolite.lqc)]"></div>
          </td>
          <td class="table-cell" :class="{ 'selected-metabolite-row': Metabolite === metabolite }" :title="getWorstLevel(metabolite.mqc)">
            <div class="color-circle" :class="colorMap[getWorstLevel(metabolite.mqc)]"></div>
          </td>
          <td class="table-cell" :class="{ 'selected-metabolite-row': Metabolite === metabolite }" :title="getWorstLevel(metabolite.hqc)">
            <div class="color-circle" :class="colorMap[getWorstLevel(metabolite.hqc)]"></div>
          </td>
        </tr>
      </tbody>
    </table>
  </template>
  
  <script setup>
  import { inject, ref, onMounted } from 'vue'
  import { useExcelStore } from '@/stores/excelStore';

  const excelStore = useExcelStore()
  
  const emit = defineEmits(['select-metabolite'])
  
  const Metabolite = inject('selectedMetabolite')
  const metaboliteData = ref([])
  
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

  function getWorstLevel(levels) {
  const worstLevels = ['high', 'low', 'passed'];
  const levelCounts = {};
  levels.forEach(level => {
    levelCounts[level] = (levelCounts[level] || 0) + 1;
  });
  for (const level of worstLevels) {
    if (levelCounts[level] > 0) {
      if (levelCounts['high'] > 0 && levelCounts['low'] > 0) {
        return levelCounts['high'] > levelCounts['low'] ? 'low' : 'high';
      } else {
        return level;
      }
    }
  }
  return 'passed';
}
onMounted(async () => {
  try {
    const response = await axios.post(variables.API_URL + 'table_cal_qc/', excelStore.state.jsonData)
    console.log(response.data);
    metaboliteData.value = response.data
  } catch (e) {
    console.log(e);
  }
})
</script>
