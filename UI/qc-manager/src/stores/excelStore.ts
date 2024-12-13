import { reactive } from 'vue'
import { defineStore } from 'pinia'
import { useLocalStorage } from '@vueuse/core'
import type { ExcelData, Batch, Project, intraProjectInfo } from '../services/models.ts'


// Хранит данные из загруженного Excel файла в формате JSON
export const useExcelStore = defineStore('excel', () => {
  const storedState = useLocalStorage('excel-state', {

    jsonData: {}
  })

  function saveData(data: ExcelData) {
    storedState.value = { ...storedState.value, ...data }
  }

  function clearData() {
    storedState.value = { jsonData: {} }
  }

  return {
    state: storedState,
    saveData,
    clearData
  }
})

// Хранит данные из загруженных Excel файлов (в компоненте ChartsMetabolites загрузка множества файлов) в формате JSON
export const useUserMergedExcelStore = defineStore('userMergedExcel', () => {
  const storedState = useLocalStorage('user-merged-excel-state', {
    jsonData: {}
  })

  function saveData(data: ExcelData) {
    storedState.value = { ...storedState.value, ...data }
  }

  function clearData() {
    storedState.value = { jsonData: {} }
  }

  return {
    state: storedState,
    saveData,
    clearData
  }
})

// Хранит данные о батче
export const useBatchStore = defineStore('batch', () => {
  const storedBatch = useLocalStorage('batch-state', {
    id: 0,
    batch_num: 1,
    batch_date: '21-10-2024',
    batch_normalized: false,
  })

  function saveBatch(data: Batch) {
    storedBatch.value = { ...storedBatch.value, ...data }
  }

  function clearBatch() {
    storedBatch.value = {
      id: 0,
      batch_num: 1,
      batch_date: '',
      batch_normalized: false,
    }
  }

  return {
    state: storedBatch,
    saveBatch,
    clearBatch
  }
})

// Хранит данные о Проекте
export const useProjectStore = defineStore('project', () => {
  const storedProject = useLocalStorage('project-state', {
    id: 0,
    project_name: '',
    project_date: ''
  })

  function saveProject(data: Project) {
    storedProject.value = { ...storedProject.value, ...data }
  }

  function clearProject() {
    storedProject.value = {
      id: 0,
      project_name: '',
      project_date: ''
    }
  }

  return {
    state: storedProject,
    saveProject,
    clearProject
  }
})

// Хранит картинку графика PCA на странице ReviewView
export const useImageStore = defineStore('image', () => {
  const state = reactive({
    graphImage: '',
  })
  
  const storedImage = useLocalStorage('image-state', state)
  return {
    state: storedImage,
  }
})

export const useIntraProjectInfo = defineStore('intraProjectInfo', () => {
  const storedIntraProjectInfo = useLocalStorage('intraProjectInfo-state', {
    jsonData: {},
  })

  function saveIntraProjectInfo(data: intraProjectInfo) {
    storedIntraProjectInfo.value = { ...storedIntraProjectInfo.value, ...data }
  }

  function clearIntraProjectInfo() {
    storedIntraProjectInfo.value = {
      jsonData: {},
    }
  }

  return {
    state: storedIntraProjectInfo,
    saveIntraProjectInfo,
    clearIntraProjectInfo
  }
})