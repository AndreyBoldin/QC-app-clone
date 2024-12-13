<template>
  <div>
    <div style="width: 100%; margin: auto;">
      <div class="upload-card" style="display: flex; justify-self: center; margin-top: 20px; width:fit-content; margin-bottom: 15px;">
        <div style="border-right: 1px solid #ccc; padding-right: 20px;">

          <h2 style="margin-bottom: 5px;">Создание нового батча</h2>
          <div style="display: flex; flex-direction: column; margin-top:10px">
            <input type="file" accept=".xlsx, .xls" @change="handleFileChange" />
            <label style="margin-top: 10px;">Номер батча</label>
            <input type="number" v-model="batchStore.state.batch_num"
            style="border-radius: 5px; padding: 3px;width: 50px; text-align: center;"
            min="1" step="1" />
            <label style="margin-top: 10px; width: max-content;">Выберите дату и время снятия батча</label>
            <VueDatePicker v-model="batchStore.state.batch_date" :enable-time-picker="false" model-type="yyyy-MM-dd"></VueDatePicker>
            <label style="margin-top: 10px;">Существующий проект</label>
            <select v-model="selectedProjectId_in_new" style="border-radius: 5px; padding: 3px;" @change="handleProjectChangeInNew">
              <option disabled value="">Выберите проект</option>
              <option v-for="project in projects_in_new" :key="project.id" :value="project.id">{{ project.project_name }}</option>
            </select>
            <div v-if="!selectedProjectId_in_new" style="display: flex; flex-direction: column">
            <p style="margin-top: 5px; margin-bottom: 5px;">или новый</p>
            <input  type="text" v-model="projectName" style="border-radius: 5px; padding: 3px;" placeholder="Введите название проекта">
            <label v-if="projectName" style="margin-top: 10px; width: max-content;">Выберите дату и время снятия батча</label>
            <VueDatePicker v-if="projectName" v-model="date_project" :enable-time-picker="false" model-type="yyyy-MM-dd"></VueDatePicker>
          </div>
          </div>
          <button v-if="isCreateBatchFormValid" class="confirm-btn" @click="saveNewBatch" style="margin-top: 10px;">Анализ нового батча</button>
        </div>
        <div style="display: flex; flex-direction: column; padding-left: 20px;">
    <h2 style="margin-bottom: 5px; width: max-content;">Выбор существующего батча</h2>
    <label style="margin-top: 10px;">Выбор проекта</label>
    <select v-model="selectedProjectId_in_old" style="border-radius: 5px; padding: 3px;" @change="handleProjectChangeInOld">
      <option v-for="project in projects_in_old" :key="project.id" :value="project.id">{{ project.project_name }}</option>
    </select>
    <label v-if="selectedProjectId_in_old" style="margin-top: 10px;">Выбор батча</label>
    <select v-model="selectedBatchId" style="border-radius: 5px; padding: 3px;" v-if="selectedProjectId_in_old">
  <option v-for="batch in batches.slice().sort((a, b) => a.batch_num - b.batch_num)" :key="batch.id" :value="batch.id">{{ batch.batch_num }}</option>
</select>
    <button v-if="isExistingBatchFormValid" @click="saveOldBatch" class="confirm-btn" style="margin-top: 10px;">Анализ существующего батча</button>
  </div>

      </div>
      <button  class="remove-all-btn" @click="handleRemoveAll" style="display: flex; margin-top: 10px; justify-self: center;">Очистить поля</button>
    </div>
    <transition name="saved-notification">
  <div v-if="showNotification" class="saved-notification">
    Данные загружены
  </div>
</transition>
<transition name="uploading-notification">
  <div v-if="uploading" class="uploading-notification">
    Данные загружаются, подождите...
  </div>
</transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useExcelStore, useBatchStore, useProjectStore } from '../stores/excelStore.ts'
import axios from 'axios'
import * as XLSX from 'xlsx';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

const excelStore = useExcelStore()
const batchStore = useBatchStore()
const projectStore = useProjectStore()

const date_project = ref(projectStore.state.length > 0 ? projectStore.state[0].project_date : null)

const projects_in_new = ref([])
const projects_in_old = ref([])
const batches = ref([])
const selectedBatchId = ref()

const selectedProjectId_in_new = ref(null)
const selectedProjectId_in_old = ref(null)
const selectedProjectDate_in_new = computed(() => {
  return selectedProjectId_in_new.value ? projects_in_new.value.find(project => project.id === selectedProjectId_in_new.value).project_date : null
})

const selectedProject = ref(null)
const projectName = ref('')

const showNotification = ref(false)
const uploading = ref(false)

let file = ref('none')

function handleFileChange(event) {
  file.value = event.target.files[0];
}

const isCreateBatchFormValid = computed(() => {
  return (
    file.value !== 'none' && batchStore.state.batch_num !== null &&
    (selectedProjectId_in_new.value !== null || projectName.value !== '' && date_project.value !== null)
  );
});

const isExistingBatchFormValid = computed(() => {
  return selectedProjectId_in_old.value !== null && selectedBatchId.value !== null;
})


async function handleProjectChangeInOld() {
    if (selectedProjectId_in_old.value) {
      selectedProject.value = projects_in_old.value.find(project => project.id === selectedProjectId_in_old.value)
      await getBatchesByProjectId(selectedProjectId_in_old.value)
    } else {
      batches.value = []
    }
  }

  async function getBatchesByProjectId(projectId) {
    try {
      const response = await axios.get(variables.API_URL + 'batches/' + '?project_id=' + projectId)
      batches.value = response.data
    } catch (error) {
      console.error(error)
    }
  }

async function saveNewBatch() {
  console.log('saveNewBatch called');
  const reader = new FileReader();
  reader.onload = async (event) => {
    console.log('reader.onload called');
    const data = event.target.result;
    const workbook = XLSX.read(data, { type: 'array' });
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    const jsonData = XLSX.utils.sheet_to_json(sheet);
    console.log('Clearing existing data in store');
    excelStore.clearData();
    console.log('Saving new data to store');
    const dataToSave = {
      jsonData: jsonData
    };
    excelStore.saveData(dataToSave);

    // Save data to Batch store
    const batchData = {
      id: 0, 
      batch_num: batchStore.state.batch_num, 
      batch_date: batchStore.state.batch_date,
      batch_normalized: false,
    }
    batchStore.saveBatch(batchData);

    // Save data to Project store
    if (selectedProjectId_in_new.value) {
      const projectData = {
        id: selectedProjectId_in_new.value,
        project_name: selectedProject.value.project_name,
        project_date: selectedProjectDate_in_new.value
      }
      projectStore.saveProject(projectData);
    } else {
  const projectData = {
    id: 0,
    project_name: projectName.value,
    project_date: date_project.value
  }
  projectStore.saveProject(projectData);
}
  };
  reader.readAsArrayBuffer(file.value);

  showNotification.value = true;
  setTimeout(() => {
    showNotification.value = false;
  }, 3000);

}

onMounted(async () => {
  try {
    axios.get(variables.API_URL + 'projects')
    .then(response => {
      console.log(response.data);
      projects_in_new.value = response.data;
      projects_in_old.value = response.data;
    })
    .catch(error => {
      console.error(error);
    });
  
  } catch (e) {
    console.log(e)
  }
  try {
    axios.get(variables.API_URL + 'batches/')
    .then(response => {
      console.log(response.data);
      batches.value = response.data;
    })
    .catch(error => {
      console.error(error);
    });


  } catch (e) {
    console.log(e)
  }
})

async function saveOldBatch() {
  uploading.value = true;
  try {
    const response = await axios.get(variables.API_URL + 'samples/?batch_id=' + selectedBatchId.value);
    const samples = response.data;

    const metaboliteResponse = await axios.get(variables.API_URL + 'metabolites/');
    const metabolites = metaboliteResponse.data;

    const projectResponse = await axios.get(variables.API_URL + 'projects/?id=' + selectedProjectId_in_old.value);
    const project = projectResponse.data;

    console.log('project', project);
    const batchResponse = await axios.get(variables.API_URL + 'batches/?id=' + selectedBatchId.value);
    const batch = batchResponse.data;
    console.log('batch', batch);

    const jsonData = {
      jsonData: []
    };

    for (let i = 0; i < samples.length; i++) {
      const sample = samples[i];
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
        Group: groupName,
        Sample: sample.sample_name,
        ...metaboliteConcObj
      };
      console.log('obj', obj);
      jsonData.jsonData.push(obj);
    }

    console.log('jsonData', jsonData);

    // Save the data to the Pinia store
    excelStore.clearData();
    excelStore.saveData(jsonData);

    console.log('Saving batch and project information', batch.id,batch.batch_num,batch.batch_date,project.id,project.project_name,project.project_date);
    // Save batch and project information
    const batchData = {
      id: batch[0].id,
      batch_num: batch[0].batch_num,
      batch_date: batch[0].batch_date,
      batch_normalized: false
    };
    batchStore.clearBatch();
    batchStore.saveBatch(batchData);

    const projectData = {
      id: project[0].id,
      project_name: project[0].project_name,
      project_date: project[0].project_date
    };
    projectStore.clearProject();
    projectStore.saveProject(projectData);

    showNotification.value = true;
    setTimeout(() => {
      showNotification.value = false;
    }, 3000);
  } catch (error) {
    console.error(error);
  } finally {
    uploading.value = false;
  }
}

function handleRemoveAll() {
  date_project.value = '';
  projectName.value = '';
  selectedProjectId_in_new.value = null;
  selectedProjectId_in_old.value = null;
  selectedProject.value = null;
  selectedBatchId.value = null;
  file.value = 'none';
}

function handleProjectChangeInNew() {
  if (selectedProjectId_in_new.value) {
    selectedProject.value = projects_in_new.value.find(project => project.id === selectedProjectId_in_new.value)
  }
}

</script>

<style scoped>
.uploading-notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #2196f3; /* blue background */
  color: #fff;
  padding: 10px 20px;
  border-radius: 5px;
  box-shadow: 0 3px 4px -1px rgba(0, 0, 0, 0.1);
}

.error-message {
  background-color: rgb(220, 89, 89);
  color:white;
  width: fit-content;
  font-weight: bold;
  border-radius: 8px;
  padding: 15px 25px 20px 25px;
  box-shadow: 0 3px 4px -1px rgba(0, 0, 0, 0.1);
}
.upload-card {
  background-color: var(--nav-bg-color);
  color: rgb(220, 240, 253);
  border-color: var(--border-color);
  border-radius: 8px;
  padding: 15px 25px 20px 25px;
  box-shadow: 0 3px 4px -1px rgba(0, 0, 0, 0.1);
}

.select-btn {
  border-radius: 2px;
  padding: 0 20px;
  height: 40px;
  width: 100%;
  cursor: pointer;
  background-color: #344c5c;
  border: 1px solid rgba(0, 0, 0, 0.16);
  box-shadow: 0px 1px 0px rgba(0, 0, 0, 0.05);
  transition: background-color 200ms;
}

input[type='file']::file-selector-button {
  border-radius: 6px;
  padding: 0 16px;
  height: 40px;
  width: 100%;
  cursor: pointer;
  background-color: #2d58a3;
  border: 1.5px solid rgba(45, 50, 91, 0.16);
  box-shadow: 0px 1px 0px rgba(0, 0, 0, 0.05);
  transition: background-color 200ms;
  display: flex;
  align-items: center;
  color:white;
  justify-content: center;
  margin-bottom: 10px;
}

/* file upload button hover state */
input[type='file']::file-selector-button:hover {
  background-color: #284478;
}

/* file upload button active state */
input[type='file']::file-selector-button:active {
  background-color: #3366c4;
}

.confirm-btn {
  background-color: rgb(66, 165, 66);
  border-radius: 5px;
  border: none;
  padding: 10px 20px;
  color: white;
  font-weight: bold;
  cursor: pointer;
}


.confirm-btn:hover {
  background-color: rgb(45, 122, 45);
}

.confirm-btn:active {
  background-color: rgb(0, 175, 0);
}

.remove-all-btn {
  background-color: rgb(105, 107, 112);
  border-radius: 5px;
  border: none;
  padding: 10px 20px;
  color: white;
  cursor: pointer;
}

.remove-all-btn:hover {
  background-color: rgb(44, 46, 52);
}

.remove-all-btn:active {
  background-color: rgb(33, 35, 41);
}

.add-btn {
  background-color: rgb(132, 133, 132);
  border-radius: 5px;
  border: none;
  padding: 10px 20px;
  color: white;
  font-weight: bold;
  cursor: pointer;
}

.add-btn:hover {
  background-color: rgb(86, 85, 85);
}
</style>
