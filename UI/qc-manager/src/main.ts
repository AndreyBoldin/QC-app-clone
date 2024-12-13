import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
// @ts-ignore
import App from './App.vue'
import router from './router'

// @ts-ignore
import VueApexCharts from 'vue3-apexcharts'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueApexCharts)

app.component('ApexChart', VueApexCharts)
app.component('VueDatePicker', VueDatePicker as any)

app.mount('#app')
