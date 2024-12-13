<template>
  <div style="overflow: auto; height: 95vh; padding-right:10px">
    <div class="chart-grid" style="margin-top: 20px;">
      <div class="rounded-card right-bars">
        <h3 style="margin-bottom:10px">Количество образцов по группам</h3>
        <ApexChart type="bar" :options="chartOptions" :series="series"></ApexChart>
      </div>
      <div class="rounded-card left-PCA">
        <h2>PCA для всех данных</h2>
        <img style="width: 100%; height: 100%; object-fit: contain;" :src="imageStore.state.graphImage" alt="Graph" />
      </div>
      <div class="rounded-card right-table" >
        <h3 style="margin-bottom: 5px;">Таблица пропущенных значений</h3>
        <table>
          <thead>
            <tr style="color: var(--text-color); justify-content: center;">
              <th v-for="(column, index) in columns" :key="index">{{ column }} </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, rowIndex) in rows" :key="rowIndex">
              <td v-for="(value, colIndex) in row" style="color: var(--text-color);" :key="colIndex">{{ value }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getBarsData } from '@/services/controller';
import { useExcelStore } from '@/stores/excelStore';
import { useImageStore } from '@/stores/excelStore';

const imageStore = useImageStore()

const excelStore = useExcelStore()

const colors = ['#4a326e', '#485080', '#3c6682', '#337881', '#2e8e7e', '#45a778', '#77bf67',]

const series = ref([
  {
    data: Object.values(getBarsData(excelStore.state.jsonData).counts),
  }
])

const chartOptions = reactive({
  chart: {
    type: 'bar',
  },
  colors: colors,
  plotOptions: {
    bar: {
      columnWidth: '90%',
      distributed: true,
      dataLabels: {
        position: 'top'
      },
    }
  },
  dataLabels: {
    enabled: true,
    fontSize: '14px',
    style: {
      fontSize: '15px',
      fontWeight: 'bold',
    },
  },
  legend: {
    show: false
  },
  xaxis: {
    categories: getBarsData(excelStore.state.jsonData).categories,
    labels: {
      style: {
        colors: colors,
        fontSize: '14px'
      }
    }
  },
  yaxis: {
    labels: {
      style: {
        fontSize: '14px'
      }
    }
  }
})

const missingCounts = ref([])
const columns = ref([])
const rows = ref([])

onMounted(async () => {
  try {
    const response = await axios.post(variables.API_URL + 'missing_counts/', excelStore.state.jsonData)
    console.log(response.data);
    missingCounts.value = response.data
    columns.value = Object.keys(response.data[0])
    rows.value = response.data
  } catch (e) {
    console.log(e);
  }
  try {
      console.log('Making POST request to pca_plot endpoint');
      const response = await axios.post('http://127.0.0.1:8000/pca_plot/', { data: excelStore.state.jsonData }, { responseType: 'arraybuffer' });
      console.log('Received response from pca_plot endpoint');
      const plotData = response.data;
      const image = new Blob([plotData], { type: 'image/png' });
      const url = URL.createObjectURL(image);

      // Update the graphImage state in the excelStore
      console.log('Updating graphImage state in imageStore');
      imageStore.state.graphImage = url;
    } catch (error) {
      console.error(error);
    }
})
</script>

<style scoped>
table {
  border-collapse: separate;
  border-spacing: 5px; /* adjust the gap size as needed */
  width: 100%;
}

.chart-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-gap: 10px;
}

.left-PCA {
  grid-column: 1;
  grid-row: 1 / 3;
}

.right-table {
  grid-column: 2;
}

.right-bars {
  grid-column: 2;
}

td {
  min-width: 100px;
  border: 1.5px solid #ddd;
  text-align: center;
}

td {
  color: rgb(24, 27, 29);
}
</style>