<template>
    <div style=" margin: auto;">
      <div class="upload-card" style="display: flex; justify-content: space-between; flex-direction: column;">
            <h2 style="width:max-content">Сохранить батч {{ batchStore.state.batch_num }} в проект {{ projectStore.state.project_name }}?</h2>
            
            <p style="margin-top: 20px;"> Дата создания проекта: {{ projectStore.state.project_date }}</p>
            
            <p> Дата создания батча: {{ batchStore.state.batch_date }}</p>
          
            <p style="margin-top: 15px;"> Проводилась нормализация данных: {{ batchStore.state.batch_normalized ? 'Да' : 'Нет' }}</p>
            
            <h3 style="width:max-content; margin-top: 70px">Данные будут сохранены в базу данных</h3>
            <div style="display: flex; flex-direction: row; justify-content: center; margin-top: 20px;">
              <button @click="accept" class="confirm-btn" style="margin-right: 18px;">Сохранить</button>
              <button @click="decline" class="reject-btn">Отменить</button>
            </div>
      </div>
    </div>
</template>

<script setup>
import { ref  } from 'vue'
import axios from 'axios';

// Временныехранилища из pinia
import { useExcelStore, useBatchStore, useProjectStore } from '../stores/excelStore.ts'

import { useRouter } from 'vue-router';

const router = useRouter();

const excelStore = useExcelStore()
const batchStore = useBatchStore()
const projectStore = useProjectStore()

// Сохранение проекта и батча
function saveProjectAndBatch() {

  // Подтягивает данные из временных хранилищ для батча и проекта
  const batchData = {
    batch_num: batchStore.state.batch_num,
    batch_date: batchStore.state.batch_date,
    batch_normalized: batchStore.state.batch_normalized
  };

  let projectData = {
    project_name: projectStore.state.project_name,
    project_date: projectStore.state.project_date
  };
  // Проверка на существующий проект
  if (projectStore.state.id !== 0) {
    projectData.id = projectStore.state.id;

    axios.get(variables.API_URL + 'projects/' + projectData.id)
      .then(response => {
        if (response.data) {
          console.log('Project already exists in the database.');
          // Проект существует, проверяем наличие батча
          axios.get(variables.API_URL + 'batches/?project_id=' + projectData.id + '&batch_num=' + batchData.batch_num)
            .then(response => {
              if (response.data.length === 0) {
                // Батча не существует, создаем новый батч
                axios.post(variables.API_URL + 'batches/', { ...batchData, project_id: projectData.id })
                  .then(() => {
                    console.log('Batch saved successfully');
                  })
                  .catch(error => {
                    console.error('Error saving batch:', error);
                  });
              } else {
                console.log('Batch already exists in the project.');
              }
            })
            .catch(error => {
              console.error('Error checking for existing batch:', error);
            });
        } else {
          console.log('Project does not exist, but ID is provided. This should not happen.');
        }
      })
      .catch(error => {
        console.error('Error checking for existing project:', error);
      });
  } else {
    // Проекта нет, создаем новый
    axios.get(variables.API_URL + 'projects/?project_name=' + projectData.project_name)
      .then(response => {
        if (response.data.length > 0) {
          console.log('Project with this name already exists');
        } else {
          // Создаем новый проект
          axios.post(variables.API_URL + 'projects/', projectData)
            .then(response => {
              console.log('Project created response:', response.data);
              // Получаем ID нового проекта
              axios.get(variables.API_URL + 'projects/?project_name=' + projectData.project_name)
                .then(response => {
                  const newProjectId = response.data[0].id;
                  console.log('New project ID:', newProjectId);
                  // Сохраняем новый батч
                  axios.post(variables.API_URL + 'batches/', { ...batchData, project_id: newProjectId })
                    .then(response => {
                      console.log('Batch saved successfully:', response.data);
                    })
                    .catch(error => {
                      console.error('Error saving batch:', error);
                    });
                })
                .catch(error => {
                  console.error('Error getting newly created project:', error);
                });
            })
            .catch(error => {
              console.error('Error saving project:', error);
            });
        }
      })
      .catch(error => {
        console.error('Error checking for existing project:', error);
      });
  }
}

// Сохранение групп и образцов с проверкой на существование
async function saveGroupsAndSamples(batchId) {
  // Подтягиваю из хранилища JSON загруженных данных
  const jsonData = excelStore.state.jsonData;
  // Создаю массив уникальных названий групп
  const uniqueGroupNames = Array.from(new Set(jsonData.map(item => item.Group)));

  // Проверка на существующие группы в базе
  for (const groupName of uniqueGroupNames) {
    const response = await axios.get(variables.API_URL + 'groups/?group_name=' + groupName);
    if (response.data.length === 0) {
      // Группа не существует, сохраняем
      await axios.post(variables.API_URL + 'groups/', { group_name: groupName });
      console.log(`Group ${groupName} saved successfully`);
    } else {
      console.log(`Group ${groupName} already exists in the database`);
    }
  }

  // Проверка на существующие образцы в этом батче по id батча в базе
  const batchResponse = await axios.get(variables.API_URL + 'samples/?batch_id=' + batchId);
  if (batchResponse.data.length === 0) {
    // Образцы не существуют, сохраняем их
    for (const item of jsonData) {
      const sampleName = item.Sample;
      const groupName = item.Group;
      // Получаем ID группы с помощью асинхронной функции getGroupId
      const groupId = await getGroupId(groupName);

      await axios.post(variables.API_URL + 'samples/', {
        sample_name: sampleName,
        group_id: groupId,
        batch_id: batchId
      });
      console.log(`Sample ${sampleName} saved successfully`);
    }
  } else {
    console.log(`Batch with ID ${batchId} is not empty, skipping sample save`);
  }

 // Сохранение концентраций метаболитов в базе
for (const item of jsonData) {
  const sampleName = item.Sample;
  const sampleId = await getSampleId(sampleName);
  console.log(`Sample ID: ${sampleId}`);

  // Получаем ID метаболита с помощью асинхронной функции getMetaboliteId и делаем так для всех метаболитов
  for (const metaboliteName in item) {
    if (metaboliteName !== 'Sample' && metaboliteName !== 'Group') {
      const concentration = item[metaboliteName];
      const metaboliteId = await getMetaboliteId(metaboliteName);
      console.log(`Metabolite ID: ${metaboliteId}`);

      // Проверка на существующие концентрации метаболитов в базе
      const response = await axios.get(variables.API_URL + 'metabolite_conc/?sample_id=' + sampleId + '&metabolite_id=' + metaboliteId);
      if (response.data.length === 0) {
        // Концентрация метаболита не существует, сохраняем
        await axios.post(variables.API_URL + 'metabolite_conc/', {
          concentration: concentration,
          sample_id: sampleId,
          metabolite_id: metaboliteId
        });
        console.log(`Metabolite concentration saved successfully for ${sampleName} and ${metaboliteName}`);
      } else {
        // Концентрация метаболита уже существует
        console.log(`Metabolite concentration for ${sampleName} and ${metaboliteName} already exists in the database`);
      }
    }
  }
}}

const groupID = ref(null);

// Функция для получения ID группы
function getGroupId(groupName) {
  // Имея имя группы получаю его ID
  return axios.get(variables.API_URL + 'groups/?group_name=' + groupName)
    .then(response => {
      groupID.value = response.data[0].id; // Сохраняем ID в переменную groupID
      return response.data[0].id;
    })
    .catch(error => {
      console.error(error);
      return null;
    });
}

// Функция для получения ID образца по имени образца и ID батча
function getSampleId(sampleName) {
  return axios.get(variables.API_URL + 'samples/?sample_name=' + sampleName+ '&batch_id=' + batchStore.state.id)
    .then(response => {
      if (response.data.length > 0) {
        return response.data[0].id;  
      } else {
        throw new Error(`Sample not found: ${sampleName}`);
      }
    })
    .catch(error => {
      console.error(error);
      throw error;
    });
}

// Функция для получения ID метаболита по имени метаболита
function getMetaboliteId(metaboliteName) {
  return axios.get(variables.API_URL + 'metabolites/?metabolite_name=' + metaboliteName)
    .then(response => {
      if (response.data.length > 0) {
        return response.data[0].id;
      } else {
        // Метаболит не существует, сохраняем
        return axios.post(variables.API_URL + 'metabolites/', { metabolite_name: metaboliteName })
          .then(response => response.data.id);
      }
    });
}

//  Функция для обновления ID батча в Pinia для нового проекта
function updateBatchProjectId() {
  const projectName = projectStore.state.project_name;

  // Проверка на существующий проект с именем projectName
  axios.get(variables.API_URL + 'projects/')
    .then(response => {
      const projects = response.data;
      console.log(projects)
      const project = projects.find(project => project.project_name === projectName);
      if (project) {
        const projectId = project.id;
        projectStore.state.id = projectId;

        // Проверка на существующий батч с batchNum
        const batchNum = batchStore.state.batch_num;
        axios.get(variables.API_URL + 'batches/?project_id=' + projectId + '&batch_num=' + batchNum)
          .then(response => {
            const batches = response.data;
            if (batches.length > 0) {
              // Если батч существует, обновляем ID батча в Pinia
              batchStore.state.id = batches[0].id;
            }
          })
          .catch(error => {
            console.error('Error checking for existing batch:', error);
          });
      } else {
        console.error('Project not found:', projectName);
      }
    })
    .catch(error => {
      console.error('Error fetching projects:', error);
    });
    
}

function accept() {
  saveProjectAndBatch();
  updateBatchProjectId()
  saveGroupsAndSamples(batchStore.state.id);
}

function decline() {
  router.push({ name: 'analysis' }); 
}

</script>

<style scoped>
.upload-card {
  background-color: var(--nav-bg-color);
  color: rgb(220, 240, 253);
  border-color: var(--border-color);
  border-radius: 8px;
  padding: 15px 25px 20px 25px;
  box-shadow: 0 3px 4px -1px rgba(0, 0, 0, 0.1);
}

.confirm-btn {
  background-color: rgb(66, 165, 66);
  border-radius: 5px;
  border: none;
  padding: 10px 20px;
  color: white;
  cursor: pointer;
}


.confirm-btn:hover {
  background-color: rgb(45, 122, 45);
}

.confirm-btn:active {
  background-color: rgb(0, 175, 0);
}

.reject-btn {
  background-color: rgb(224, 93, 81);
  border-radius: 5px;
  border: none;
  padding: 10px 20px;
  color: white;
  cursor: pointer;
}

.reject-btn:hover { 
  background-color: rgb(194, 73, 61);
}

.reject-btn:active {
  background-color: red;
}
</style>