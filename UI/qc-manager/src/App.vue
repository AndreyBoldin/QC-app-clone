<template>
  <div class="main-grid" style="padding-top: 10px; padding-left: 5px;">
  <div>
    <div class="toolbar" style="margin-bottom: 30px;">
      <RouterLink to="/upload" style="padding-top: 13px; padding-bottom: 10px;" title="Загрузка данных"><svg class="upload" xmlns="http://www.w3.org/2000/svg" height="34px" viewBox="0 -960 960 960" width="34px" :fill="$route.path === '/upload'  ? '#fff' : '#808080'"><path d="M446.67-315.33v-356L332-556.67l-47.33-48L480-800l195.33 195.33-47.33 48-114.67-114.66v356h-66.66ZM226.67-160q-27 0-46.84-19.83Q160-199.67 160-226.67V-362h66.67v135.33h506.66V-362H800v135.33q0 27-19.83 46.84Q760.33-160 733.33-160H226.67Z"/></svg> </RouterLink>
    </div>
  <div class="toolbar">
    <RouterLink to="/review" style="margin-top:20px" title="Обзор данных"><svg  xmlns="http://www.w3.org/2000/svg" height="34px" viewBox="0 -960 960 960" width="34px" :fill="$route.path === '/review'  ? '#fff' : '#808080'"><path d="M401.79-302.92q106.21 0 181.09-74.64 74.87-74.64 74.87-181.11 0-105.92-74.89-180.17-74.9-74.25-180.99-74.25-105.99 0-180.02 74.27-74.04 74.27-74.04 180.07 0 106.55 74.04 181.19 74.03 74.64 179.94 74.64Zm-34.78-145.04v-269.18h71.77v269.18h-71.77Zm-144.6 0v-186.71h71.92v186.71h-71.92Zm289.05 0v-145.8h71.93v145.8h-71.93ZM833.89-73.3 607.12-300.75q-42.63 34-94.81 52.84-52.18 18.83-110.51 18.83-136.97 0-232.4-96.04T73.97-558.51q0-137.36 95.33-232.89 95.33-95.53 232.68-95.53 137.36 0 233.48 95.67 96.13 95.67 96.13 232.51 0 58.44-18.72 110.46-18.71 52.02-52.71 94.5l226.77 226.7-53.04 53.79Z"/></svg></RouterLink>
    <RouterLink to="/clean" style="margin-top: 20px;" title="Очистка данных"><svg  xmlns="http://www.w3.org/2000/svg" height="34px" viewBox="0 -960 960 960" width="34px" :fill="$route.path === '/clean'  ? '#fff' : '#808080'"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h357l-80 80H200v560h560v-278l80-80v358q0 33-23.5 56.5T760-120H200Zm280-360ZM360-360v-170l367-367q12-12 27-18t30-6q16 0 30.5 6t26.5 18l56 57q11 12 17 26.5t6 29.5q0 15-5.5 29.5T897-728L530-360H360Zm481-424-56-56 56 56ZM440-440h56l232-232-28-28-29-28-231 231v57Zm260-260-29-28 29 28 28 28-28-28Z"/></svg></RouterLink>
    <RouterLink to="/normalize" style="margin-top: 20px" title="Нормализация данных"><svg xmlns="http://www.w3.org/2000/svg" height="34px" viewBox="0 -960 960 960" width="34px" :fill="$route.path === '/normalize'  ? '#fff' : '#808080'"><path d="m456-200 174-340H510v-220L330-420h126v220Zm24 120q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/></svg></RouterLink>
    <RouterLink to="/analysis" style="margin-top: 20px;" title="Оценка контроля качества" ><svg  xmlns="http://www.w3.org/2000/svg" height="34px" viewBox="0 -960 960 960" width="34px" :fill ="$route.path === '/analysis' ? '#fff' : '#808080'"><path d="M280-280h80v-200h-80v200Zm320 0h80v-400h-80v400Zm-160 0h80v-120h-80v120Zm0-200h80v-80h-80v80ZM200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0-560v560-560Z"/></svg></RouterLink>
    <Suspense>
    <RouterLink to="/save" style="margin-top: 20px; margin-bottom: 15px" title="Сохранение в базу данных"><svg class="upload" xmlns="http://www.w3.org/2000/svg" height="34px" viewBox="0 -960 960 960" width="34px" :fill ="$route.path === '/save' ? '#fff' : '#808080'"><path d="M493-120v-.33.33q-46.33.33-110.33-8t-122.34-27.17Q202-174 161-204.5T120-280q0 45 41 75.5t99.33 49.33q58.34 18.84 122.34 27.17 64 8.33 110.33 8Zm-23-209.33v-.67.67q-47.33-.67-87.83-5.17t-75.17-13q-34.67-8.5-64.67-20.17-30-11.66-55.66-26.66 25.66 15 55.66 26.66 30 11.67 64.67 20.17 34.67 8.5 75.17 13t87.83 5.17ZM480-605q87 0 177.33-26.5Q747.67-658 768.67-689 747-720 656.83-746.67 566.67-773.33 480-773.33q-89 0-177.5 25.83T190.67-689q23.33 32.33 111.16 58.17Q389.67-605 480-605Zm230 487.67h33.33V-286l75.34 75.33L842-234 726.67-349.33 611.33-234l23.34 23.33L710-286v168.67ZM726.67-40Q647-40 590.17-96.5q-56.84-56.5-56.84-136.17 0-80.33 56.84-137.16 56.83-56.84 136.5-56.84 79.66 0 136.5 56.84Q920-313 920-232.67 920-153 863.17-96.5 806.33-40 726.67-40ZM471-187q3 18 8.67 34.67Q485.33-135.67 493-120q-46.33.33-110.33-8t-122.34-27.17Q202-174 161-204.5T120-280v-400q0-66 105.5-113T480-840q149 0 254.5 47T840-680v213q-15.67-7.67-32.33-13.33Q791-486 773.33-489v-116Q716.67-573.33 640-556q-76.67 17.33-160.67 17.33-85 0-162-17.33t-130.66-49v137q53 37 132.16 54.5Q398-396 479.33-396q12.34 0 23.84-.33 11.5-.34 23.83-1.67-13 15.33-22.83 32.67-9.84 17.33-17.5 36H470q-95.33-1.34-163.33-18.17-68-16.83-120-46.83v117q5.66 15.66 33.33 31.83 27.67 16.17 67.67 28.67t88.16 20.66Q424-188 471-187Z"/></svg></RouterLink>
    </Suspense>
  </div>
  <div class="toolbar" style="padding-top: 13px; padding-bottom: 13px; margin-top: 30px;">
    <svg v-if="isDarkMode === false" @click="DarkMode()" class="upload" xmlns="http://www.w3.org/2000/svg" height="34px" viewBox="0 -960 960 960" width="34px" fill="#999999"><path d="M480-346.67q55.33 0 94.33-39t39-94.33q0-55.33-39-94.33t-94.33-39q-55.33 0-94.33 39t-39 94.33q0 55.33 39 94.33t94.33 39Zm0 66.67q-83 0-141.5-58.5T280-480q0-83 58.5-141.5T480-680q83 0 141.5 58.5T680-480q0 83-58.5 141.5T480-280ZM200-446.67H40v-66.66h160v66.66Zm720 0H760v-66.66h160v66.66ZM446.67-760v-160h66.66v160h-66.66Zm0 720v-160h66.66v160h-66.66ZM260-655.33l-100.33-97 47.66-49 96 100-43.33 46Zm493.33 496-97.66-100.34 45-45.66 99.66 97.66-47 48.34Zm-98.66-541.34 97.66-99.66 49 47L702-656l-47.33-44.67ZM159.33-207.33 259-305l46.33 45.67-97.66 99.66-48.34-47.66ZM480-480Z"/></svg>
    <svg v-if="isDarkMode === true" @click="DarkMode()" class="upload" xmlns="http://www.w3.org/2000/svg" height="34px" viewBox="0 -960 960 960" width="34px" fill="#999999"><path d="M480-120q-150 0-255-105T120-480q0-150 105-255t255-105q10 0 20.5.67 10.5.66 24.17 2-37.67 31-59.17 77.83T444-660q0 90 63 153t153 63q53 0 99.67-20.5 46.66-20.5 77.66-56.17 1.34 12.34 2 21.84.67 9.5.67 18.83 0 150-105 255T480-120Zm0-66.67q102 0 179.33-61.16Q736.67-309 760.67-395.67q-23.34 9-49.11 13.67-25.78 4.67-51.56 4.67-117.46 0-200.06-82.61-82.61-82.6-82.61-200.06 0-22.67 4.34-47.67 4.33-25 14.66-55-91.33 28.67-150.5 107-59.16 78.34-59.16 175.67 0 122 85.66 207.67Q358-186.67 480-186.67Zm-6-288Z"/></svg>
  </div>

</div>
  <RouterView/>

  </div>  
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'

const isDarkMode = ref(true)

function DarkMode() {
  isDarkMode.value = !isDarkMode.value
  document.body.classList.toggle('dark-mode')
}


</script>


<style>
:root {
  --primary-color: #f6f9fa;
  --secondary-color: #f1f4fa;
  --thirdary-color: #d1d7e4;
  --background-color: #e4e4e8;
  --text-color: #1f3558;
  --th-color: #2a374a;
  --nav-bg-color: #2a374a;
  --border-color: #ddd;
  --hover-color: #ffffff;
  --hover: #cafcfa;
}

.dark-mode {
  --primary-color: #273040;
  --secondary-color: #1e2836;
  --thirdary-color: #161e2d;
  --background-color: #111827;
  --text-color: #fff;
  --th-color: #111827;
  --nav-bg-color: #273040;
  --border-color: #666;
  --hover-color: #aaa;
  --hover: #344c5c;
}

body {
  background-color: var(--background-color);
  color: var(--text-color);
}

.rounded-card {
  background-color: var(--primary-color);
  color: var(--text-color);
  border-color: var(--border-color);
}

.rounded-card {
  border-radius: 8px;
  padding: 15px 25px 20px 25px;
  box-shadow: 0 3px 4px -1px rgba(0, 0, 0, 0.1);
}

.rounded-card-inter {
  background-color: var(--primary-color);
  color: var(--text-color);
  border-color: var(--border-color);
}

.rounded-card-inter {
  border-radius: 8px;
  padding: 10px 25px 10px 25px;
  box-shadow: 0 3px 4px -1px rgba(0, 0, 0, 0.1);
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
  background-color: #1e2836;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background-color: #3b4557;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: #3b4557;
  cursor: grab;
}
::-webkit-scrollbar-thumb:active {
  cursor: grabbing;
}

::-webkit-scrollbar-track {
  background-color: var(--primary-color);
  border-radius: 10px;
}

.upload:hover {
  cursor: pointer;
  fill: #fff;
}


.toolbar {
  background-color: var(--nav-bg-color);
  border-radius: 10px;
  position: relative;
  width: 60px; /* adjust the width to your liking */
  z-index: 999;
  display: flex;
  align-items: center;
  flex-direction: column;
  margin-left: 5px; margin-top: 10px; max-height: fit-content;
}

.toolbar a:hover svg {
    fill: #fff;
  }

.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 10px;
}

.main-grid {    display: grid;
    grid-template-columns: 60px auto;
    gap: 20px;}

    .saved-notification {
  position: fixed;
  bottom: 30px;
  right: 40px;
  font-size: 1rem;
  background-color: #4caf50;
  color: #fff;
  padding: 10px 25px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.saved-notification-enter-active,
.saved-notification-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}

.saved-notification-enter-from,
.saved-notification-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>