<template>
  <div class="metric-view">
    <div class="metric-header">
      <div class="row-count">
        Row count: {{ rowCount === null ? '-' : rowCount }}
      </div>
      <div class="header-actions">
        <span class="last-fetched">Last fetched: {{ lastFetched || '-' }}</span>
        <el-button :icon="User" @click="profileData" plain :loading="isLoading">Profile data</el-button>
      </div>
    </div>

    <el-table 
      :data="columnMetrics" 
      style="width: 100%" 
      class="metrics-table" 
      empty-text="暂无指标数据或加载失败"
      v-loading="isLoading"
      element-loading-text="正在加载指标数据..."
    >
    <el-table-column prop="columnName" label="Column" sortable min-width="180">
        <template #default="scope">
          <span class="column-name-text">{{ scope.row.columnName }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="type" label="Type" sortable min-width="150" />
      <el-table-column prop="min" label="Min" sortable min-width="100">
        <template #default="scope">
          {{ scope.row.min }}
        </template>
      </el-table-column>
      <el-table-column prop="max" label="Max" sortable min-width="100">
        <template #default="scope">
          {{ scope.row.max }}
        </template>
      </el-table-column>
      <el-table-column prop="mean" label="Mean" sortable min-width="100">
        <template #default="scope">
          {{ scope.row.mean }}
        </template>
      </el-table-column>
      <el-table-column prop="median" label="Median" sortable min-width="100">
        <template #default="scope">
          {{ scope.row.median}}
        </template>
      </el-table-column>
      <el-table-column prop="nullPercentage" label="Null %" sortable min-width="100">
        <template #default="scope">
          {{ scope.row.nullPercentage === '-' ? '-' : `${scope.row.nullPercentage}%` }}
        </template>
      </el-table-column>


    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { ElTable, ElTableColumn, ElButton, ElMessage } from 'element-plus';
import { User } from '@element-plus/icons-vue';
import { API_URL } from '@/config.js';
import axios from 'axios';


const props = defineProps({
  assetId: [String, Number]
});

const rowCount = ref(null);
const lastFetched = ref('');
// 或者使用骨架屏数据
const columnMetrics = ref([
  { columnName: '无信息', type: '-', min: '-', max: '-', mean: '-', median: '-', nullPercentage: '-' },
]);
const isLoading = ref(false);
const fetchMetricsData = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(`${API_URL}/pg/${props.assetId}/tablesInfo`);
    if (response.data.column_info) {
      const responseData = response.data;
      columnMetrics.value = responseData.column_info.map(colObj => {
        const columnName = Object.keys(colObj)[0];
        const type = colObj[columnName];
        return {
          columnName: columnName,
          type: type,
          min: '-',
          max: '-',
          mean: '-',
          median: '-',
          nullPercentage: '-',
        };
      });
    } else {
      columnMetrics.value = [];
    }
  } catch (error) {
    // 错误处理保持不变
  } finally {
    isLoading.value = false;
  }
};

const profileData = () => {
  ElMessage.info('“Profile data”功能尚未实现');
};

onMounted(() => {
  rowCount.value = null; // 根据需要设置默认值或通过API获取
  lastFetched.value = ''; // 根据需要设置默认值或通过API获取
    fetchMetricsData();
});


watch(() => props.assetId, (newAssetId, oldAssetId) => {
  if (newAssetId && newAssetId !== oldAssetId) {
    rowCount.value = null;
    lastFetched.value = '';
    fetchMetricsData();
  } else if (!newAssetId) {
    columnMetrics.value = [];
    rowCount.value = null;
    lastFetched.value = '';
  }
}, { immediate: false }); 

</script>

<style scoped>
.metric-view {
  padding: 20px;
  background-color: #fff; /* 与图片背景色一致 */
  height: 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px; /* 头部和表格之间的间距 */
  padding: 10px; /* 增加一些内边距 */
  background-color: #f9fafb; /* 头部背景色，类似图片 */
  border-radius: 4px; /* 轻微圆角 */
  border: 1px solid #e5e7eb; /* 边框 */
}

.row-count {
  font-size: 14px;
  color: #374151; /* 深灰色文字 */
  font-weight: 500;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px; /* 元素间距 */
}

.last-fetched {
  font-size: 12px;
  color: #6b7280; /* 浅灰色文字 */
}

.header-actions .el-button {
  font-size: 13px; /* 按钮字体大小 */
}

.metrics-table {
  flex-grow: 1;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  transition: opacity 0.3s ease-in-out;
}

.metrics-table :deep(.el-table__row) {
  transition: all 0.2s ease-in-out;
}

.metrics-table :deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

.metrics-table :deep(.el-table__header-wrapper th) {
  background-color: #f9fafb; /* 表头背景色 */
  color: #374151; /* 表头文字颜色 */
  font-weight: 500; /* 表头字体加粗 */
  font-size: 13px;
}

.metrics-table :deep(.el-table__row td) {
  font-size: 13px;
  color: #374151;
}
.metrics-table :deep(.el-table__row td .cell) {
  padding-top: 8px;
  padding-bottom: 8px;
}

.column-name-text {
  font-weight: 500; /* 字段名称加粗 */
}
</style>
   