<template>
  <div
    :class="{ in: showMainTable, out: !showMainTable }"
    style="height: 90vh;  margin-bottom: 10px;"
  >
  <div style="display: flex; flex-direction: row; justify-content: space-between;  margin-bottom: 10px">
    <div v-if = "showMainTable" style="display: flex; flex-direction: row; position: relative;  background-color:var(--nav-bg-color); border-radius: 10px; padding: 5px;">
    <div @click = "showCalQC = true; showLacQC = false; showSamples = false;" :class = "{'select-btn-active': showCalQC}" class = "select-btn" style="width:200px; border-radius: 8px; background-color: #3d4553; color:#686e79; display: flex; justify-content: center; align-items: center;"><h3 style="margin: 0;">Калибраторы и QC</h3></div>
    <div @click = "showCalQC = false; showLacQC = true; showSamples = false;" :class = "{'select-btn-active': showLacQC}" class = "select-btn" style="width:100px; border-radius: 8px; background-color: #3d4553; color:#686e79;margin-left: 5px; display: flex; justify-content: center; align-items: center;"><h3 style="margin: 0;">LabQC</h3></div>
    <div @click = "showCalQC = false; showLacQC = false; showSamples = true;" :class = "{'select-btn-active': showSamples}" class = "select-btn" style="width:100px;border-radius: 8px; background-color: #3d4553;color:#686e79; margin-left: 5px; display: flex; justify-content: center; align-items: center;"><h3 style="margin: 0;">Образцы</h3></div>
  </div>
  
  <div :title= "showMainTable ? 'Скрыть таблицу' : 'Показать таблицу'" style="display:flex; justify-content: center;align-items: center; background-color: var(--nav-bg-color); border-radius: 10px;padding: 5px">
    <svg v-if = "showMainTable" @click="showTable" class = "hide-btn" xmlns="http://www.w3.org/2000/svg" height="28px" viewBox="0 -960 960 960" width="28px" :fill="!showMainTable ? '#fff' : '#808080'"><path d="m644-428-58-58q9-47-27-88t-93-32l-58-58q17-8 34.5-12t37.5-4q75 0 127.5 52.5T660-500q0 20-4 37.5T644-428Zm128 126-58-56q38-29 67.5-63.5T832-500q-50-101-143.5-160.5T480-720q-29 0-57 4t-55 12l-62-62q41-17 84-25.5t90-8.5q151 0 269 83.5T920-500q-23 59-60.5 109.5T772-302Zm20 246L624-222q-35 11-70.5 16.5T480-200q-151 0-269-83.5T40-500q21-53 53-98.5t73-81.5L56-792l56-56 736 736-56 56ZM222-624q-29 26-53 57t-41 67q50 101 143.5 160.5T480-280q20 0 39-2.5t39-5.5l-36-38q-11 3-21 4.5t-21 1.5q-75 0-127.5-52.5T300-500q0-11 1.5-21t4.5-21l-84-82Zm319 93Zm-151 75Z"/></svg>
    <svg v-if = "!showMainTable" @click="showTable" class = "hide-btn" xmlns="http://www.w3.org/2000/svg" height="28px" viewBox="0 -960 960 960" width="28px" :fill="showMainTable ? '#fff' : '#808080'"><path d="M480-320q75 0 127.5-52.5T660-500q0-75-52.5-127.5T480-680q-75 0-127.5 52.5T300-500q0 75 52.5 127.5T480-320Zm0-72q-45 0-76.5-31.5T372-500q0-45 31.5-76.5T480-608q45 0 76.5 31.5T588-500q0 45-31.5 76.5T480-392Zm0 192q-146 0-266-81.5T40-500q54-137 174-218.5T480-800q146 0 266 81.5T920-500q-54 137-174 218.5T480-200Zm0-300Zm0 220q113 0 207.5-59.5T832-500q-50-101-144.5-160.5T480-720q-113 0-207.5 59.5T128-500q50 101 144.5 160.5T480-280Z"/></svg>
  </div>
  </div>
  <div style="overflow: auto; padding-bottom: 5px; padding-right: 5px; height: 85vh;">
  <div style="padding: 10px; width:fit-content;height: fit-content; background-color: var(--thirdary-color); border-radius: 14px;">
  <TableCalQC v-if = "showCalQC" v-show="showMainTable" />
  <TableLabQC v-if = "showLacQC" v-show="showMainTable"  />
  <TableSamples v-if = "showSamples" v-show="showMainTable"  />
  </div>
</div>
  </div>
  
</template>

<script setup>
import { ref } from 'vue'
import TableCalQC from './TableCalQC.vue'
import TableLabQC from './TableLabQC.vue'
import TableSamples from './TableSamples.vue';

const $emit = defineEmits(['update:showMainTable', 'select-metabolite'])

const showMainTable = ref(true)
const showCalQC = ref(true)
const showLacQC = ref(false)
const showSamples = ref(false)

function showTable() {
  showMainTable.value = !showMainTable.value
  $emit('update:showMainTable', showMainTable.value)
}

</script>

<style>
.selected-metabolite-th {
  font-weight: bold;
}

.selected-metabolite-row {
  background-color: var(--hover) !important;
  color: var(--text-color) !important;
}

.hover-effect {
  transition:
    background-color 0.2s,
    color 0.2s;
}

.hover-effect:hover {
  color: var(--text-color);
  font-weight: bold;
  cursor: pointer;
}


thead {
  position: sticky;
  top: 0;
  background-color: #202c34;
  z-index: 1;
  height: 60px;
  width: 60px;
}

table {
  border-spacing: 5px;
}

td {
  border-radius: 6px;
  background-color: var(--primary-color); 
  color: var(--text-color);
}

th {
  min-width: 45px;
  border-radius: 6px;
  text-align: center;
  font-size: 15px;
  background-color: var(--th-color);
  color: white
}

.table-cell {
  background: var(--secondary-color);
}

.table-cell:hover {
  border: 2.5px solid !important;
  border-color: #181bb9 !important;
  background-color: var(--hover-color) !important;
}

.hide-btn:hover {
  cursor: pointer;
  fill: #fff;
}

.select-btn:hover {
  cursor: pointer;
  background-color: #7d838c !important;
  color:#111827 !important;
}

.select-btn:active {
  background-color: #e9eaec !important;
  color:#111827 !important;
}
.select-btn-active {
  background-color: #e9eaec !important;
  color:#111827 !important;
}


.passed-color {
  background-color: #5ddc5c;
}

.semi_low-color {
  background-color: #93d0f1;
}

.semi_passed-color {
  background-color: #feca57;
}

.low-color {
  background-color: #54a0ff;
}

.semi_high-color {
  background-color: #ffb095;
}

.high-color {
  background-color: #ff6b6b;
}

.color-circle {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  margin: 0 auto;
}

table:has(td:nth-child(1):hover, th:nth-child(1):hover) {
  & tbody td:nth-child(1) {
    background: var(--hover);
  }
}

table:has(td:nth-child(2):hover, th:nth-child(2):hover) {
  & tbody td:nth-child(2) {
    background: var(--hover);
  }
}
table:has(td:nth-child(3):hover, th:nth-child(3):hover) {
  & tbody td:nth-child(3) {
    background: var(--hover);
  }
}
table:has(td:nth-child(4):hover, th:nth-child(4):hover) {
  & tbody td:nth-child(4) {
    background: var(--hover);
  }
}
table:has(td:nth-child(5):hover, th:nth-child(5):hover) {
  & tbody td:nth-child(5) {
    background: var(--hover);
  }
}
table:has(td:nth-child(6):hover, th:nth-child(6):hover) {
  & tbody td:nth-child(6) {
    background: var(--hover);
  }
}

table:has(td:nth-child(7):hover, th:nth-child(7):hover) {
  & tbody td:nth-child(7) {
    background: var(--hover);
  }
}

table:has(td:nth-child(8):hover, th:nth-child(8):hover) {
  & tbody td:nth-child(8) {
    background: var(--hover);
  }
}

table:has(td:nth-child(9):hover, th:nth-child(9):hover) {
  & tbody td:nth-child(9) {
    background: var(--hover);
  }
}

table:has(td:nth-child(10):hover, th:nth-child(10):hover) {
  & tbody td:nth-child(10) {
    background: var(--hover);
  }
}

.tr:hover {
  background-color: #344c5c !important;
}

table:has(tr:hover) tr:hover td {
  background: var(--hover);
}

</style>
