<template>
  <div class="validation-results-page">
    <div class="toolbar">
      <el-button-group>
        <el-button :type="activeFilter === 'all' ? 'primary' : 'default'" @click="activeFilter = 'all'">Show all</el-button>
        <el-button :type="activeFilter === 'failures' ? 'primary' : 'default'" @click="activeFilter = 'failures'">Failures only</el-button>
      </el-button-group>
    </div>

    <el-row :gutter="20" class="main-content-area">
      <!-- Left Sidebar -->
      <el-col :span="6">
        <el-card class="sidebar-card batches-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>Batches & run history ({{ runHistory.length }})</span>
            </div>
          </template>
          <el-scrollbar class="history-list-scrollbar">
            <div
              v-for="run in runHistory"
              :key="run.id"
              :class="['history-item', { selected: run.id === selectedRunId }]"
              @click="selectedRunId = run.id"
            >
              <el-icon :size="18" :color="run.status === 'failed' ? '#F56C6C' : '#67C23A'" class="status-icon">
                <CircleCloseFilled v-if="run.status === 'failed'" />
                <WarningFilled v-else-if="run.status === 'warning'" />
                <CircleCheckFilled v-else />
              </el-icon>
              <div class="history-item-details">
                <span class="timestamp">{{ run.timestamp }}</span>
                <span class="full-timestamp">{{ run.fullTimestamp }}</span>
              </div>
            </div>
          </el-scrollbar>
        </el-card>

        <el-card class="sidebar-card toc-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>Table of contents ({{ tocItems.length }})</span>
            </div>
          </template>
          <el-input v-model="tocSearch" placeholder="Search" :prefix-icon="Search" clearable class="toc-search"/>
          <el-scrollbar class="toc-list-scrollbar">
            <div
              v-for="item in filteredTocItems"
              :key="item.id"
              class="toc-item"
              @click="scrollToExpectation(item.id)"
            >
              {{ item.title }}
            </div>
          </el-scrollbar>
        </el-card>
      </el-col>

      <!-- Right Content Area -->
      <el-col :span="18">
        <div v-if="loading" class="loading-container">
          <el-loading text="Loading validation results..."></el-loading>
        </div>
        <div v-else-if="error" class="error-container">
          <el-alert :title="error" type="error" show-icon></el-alert>
        </div>
        <div v-else class="results-list">
          <el-card v-for="result in filteredValidationResults" :key="result.id" class="result-card" :id="`expectation-${result.id}`" shadow="never">
            <template #header>
              <div class="result-card-header">
                <el-icon class="collapse-icon" @click="toggleExpectationGroup(result.id)">
                  <ArrowDown v-if="result.expanded" />
                  <ArrowRight v-else />
                </el-icon>
                <span>{{ result.title }}</span>
                <el-tag :type="result.status === 'passed' ? 'success' : 'danger'" effect="light" size="small" class="status-tag">
                  <el-icon :size="12" style="margin-right: 3px;">
                    <CircleCheckFilled v-if="result.status === 'passed'" />
                    <CircleCloseFilled v-else />
                  </el-icon>
                  {{ result.statusText }}
                </el-tag>
              </div>
            </template>
            
            <div v-show="result.expanded">
              <div v-for="(expectation, index) in result.expectations" :key="index" class="expectation-detail">
                <div class="expectation-description">
                  <span :class="['indicator-bar', expectation.success ? 'success' : 'failure']"></span>
                  <p v-html="expectation.description"></p>
                </div>
                
                <div v-if="expectation.observedValue !== null && expectation.observedValue !== undefined" class="observed-value">
                  Observed value: <strong>{{ formatObservedValue(expectation.observedValue) }}</strong>
                </div>

                <div v-if="expectation.successRate !== undefined" class="success-rate-section">
                  <span>Success rate:</span>
                  <el-progress :percentage="expectation.successRate" :color="expectation.successRate < 50 ? '#F56C6C' : (expectation.successRate < 100 ? '#E6A23C' : '#67C23A')" class="success-progress">
                     <span style="font-size: 12px;">{{ expectation.successRate }}%</span>
                  </el-progress>
                </div>

                <div v-if="expectation.sampleUnexpectedValues && expectation.sampleUnexpectedValues.length > 0" class="sample-values">
                  <span>Sample unexpected values:</span>
                  <span v-for="(val, i) in expectation.sampleUnexpectedValues" :key="i" class="sample-value-tag">{{ val }}</span>
                  <span v-if="expectation.hasMoreUnexpectedValues" class="see-all-link" @click="showAllUnexpectedValues(expectation)">See all</span>
                </div>

                <div v-if="expectation.showValidationHistory" class="validation-history-section">
                  <el-button text type="primary" :icon="expectation.historyExpanded ? ArrowDown : ArrowRight" @click="toggleValidationHistory(expectation)" class="validation-history-toggle">
                    Validation History
                  </el-button>
                  
                  <div v-show="expectation.historyExpanded" class="validation-history-content">
                    <el-table :data="expectation.validationHistory" size="small" class="history-table">
                      <el-table-column prop="runTime" label="Run Time" width="150"></el-table-column>
                      <el-table-column prop="observedValue" label="Observed Value" width="120">
                        <template #default="scope">
                          <span :class="scope.row.success ? 'success-value' : 'failed-value'">
                            {{ formatObservedValue(scope.row.observedValue) }}
                            <el-icon v-if="scope.row.success" color="#67C23A" :size="14">
                              <Check />
                            </el-icon>
                            <el-icon v-else color="#F56C6C" :size="14">
                              <Close />
                            </el-icon>
                          </span>
                        </template>
                      </el-table-column>
                      <el-table-column prop="expectedValue" label="Expected Value" width="120"></el-table-column>
                    </el-table>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import {
  ElRow, ElCol, ElCard, ElButton, ElButtonGroup, ElScrollbar, ElInput, ElIcon, ElTag, ElProgress, ElLoading, ElAlert, ElMessage, ElTable, ElTableColumn
} from 'element-plus';
import {
  Search, CircleCheckFilled, CircleCloseFilled, WarningFilled, ArrowRight, ArrowDown, Check, Close
} from '@element-plus/icons-vue';
import axios from 'axios';
import { API_URL } from '@/config';

const route = useRoute();
const assetId = computed(() => route.params.assetId);

const activeFilter = ref('all');
const selectedRunId = ref(null);
const tocSearch = ref('');
const loading = ref(false);
const error = ref('');

const runHistory = ref([]);
const validationResults = ref([]);
const rawValidationData = ref([]);

// 时间格式化函数
const formatValidationTime = (timestamp) => {
  if (!timestamp) return 'Never';
  const date = new Date(timestamp);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / (1000 * 60));
  
  // 获取今天、昨天的日期（只比较年月日，忽略时分秒）
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const yesterday = new Date(today.getTime() - 24 * 60 * 60 * 1000);
  const targetDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  
  if (diffMins < 1) {
    return 'Less than a minute ago';
  } else if (diffMins < 60) {
    return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
  } else if (targetDate.getTime() === today.getTime()) {
    return `Today at ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
  } else if (targetDate.getTime() === yesterday.getTime()) {
    return `Yesterday at ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
  } else {
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${month}/${day} at ${hours}:${minutes}`;
  }
};

const formatFullTimestamp = (timestamp) => {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  return `${date.getFullYear()}/${String(date.getMonth() + 1).padStart(2, '0')}/${String(date.getDate()).padStart(2, '0')} GMT+8 ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}:${String(date.getSeconds()).padStart(2, '0')}`;
};

// 格式化观察值
const formatObservedValue = (value) => {
  if (Array.isArray(value)) {
    return value.join(', ');
  }
  return value;
};

// 处理验证结果数据
const processValidationData = (data) => {
  // 生成运行历史
  const history = data.map(item => ({
    id: item.id,
    status: item.success ? 'passed' : 'failed',
    timestamp: formatValidationTime(item.validation_time),
    fullTimestamp: formatFullTimestamp(item.validation_time),
    validationTime: item.validation_time
  }));
  
  // 按时间倒序排列
  runHistory.value = history.sort((a, b) => new Date(b.validationTime) - new Date(a.validationTime));
  
  // 默认选择最新的运行记录
  if (runHistory.value.length > 0) {
    selectedRunId.value = runHistory.value[0].id;
  }
  
  // 处理验证结果
  processCurrentValidationResults();
};

// 处理当前选中的验证结果
const processCurrentValidationResults = () => {
  const currentData = rawValidationData.value.find(item => item.id === selectedRunId.value);
  if (!currentData) {
    validationResults.value = [];
    return;
  }
  
  const results = currentData.result_json.results || [];
  const groupedResults = new Map();
  
  // 按期望类型分组
  results.forEach(result => {
    const expectationType = result.expectation_config.type;
    const column = result.expectation_config.kwargs.column || 'Table level';
    
    const key = column === 'Table level' ? 'table_level' : column;
    
    if (!groupedResults.has(key)) {
      groupedResults.set(key, {
        id: key,
        title: column === 'Table level' ? 'Table level Expectations' : column,
        expectations: [],
        successCount: 0,
        totalCount: 0,
        expanded: true // 默认展开
      });
    }
    
    const group = groupedResults.get(key);
    group.totalCount++;
    
    if (result.success) {
      group.successCount++;
    }
    
    // 直接使用接口返回的描述信息
    let description =`Expectation:  ${ currentData.result_json.description}` || `Expectation: ${result.expectation_config.type}`;
   
    // 生成验证历史数据（模拟）
    const validationHistory = generateValidationHistory(result, currentData.validation_time);
    
    const expectation = {
      success: result.success,
      description: description,
      observedValue: extractObservedValue(result),
      successRate: extractSuccessRate(result),
      sampleUnexpectedValues: extractSampleValues(result),
      hasMoreUnexpectedValues: hasMoreUnexpectedValues(result),
      showValidationHistory: true,
      historyExpanded: false,
      validationHistory: validationHistory
    };
    
    group.expectations.push(expectation);
  });
  
  // 转换为最终格式
  validationResults.value = Array.from(groupedResults.values()).map(group => ({
    id: group.id,
    title: group.title,
    status: group.successCount === group.totalCount ? 'passed' : 'failed',
    statusText: group.successCount === group.totalCount ? 
      'All Expectations met' : 
      `${group.totalCount - group.successCount} failed Expectation${group.totalCount - group.successCount > 1 ? 's' : ''}`,
    expectations: group.expectations,
    expanded: group.expanded
  }));
};



// 提取观察值
const extractObservedValue = (result) => {
  if (result.result && result.result.observed_value !== undefined) {
    return result.result.observed_value;
  }
  return null;
};

// 提取成功率
const extractSuccessRate = (result) => {
  if (result.result && result.result.unexpected_percent !== undefined) {
    return Math.round(100 - result.result.unexpected_percent);
  }
  return undefined;
};

// 提取样本值
const extractSampleValues = (result) => {
  if (result.result && result.result.partial_unexpected_list) {
    return result.result.partial_unexpected_list.slice(0, 8); // 最多显示8个
  }
  return [];
};

// 检查是否有更多意外值
const hasMoreUnexpectedValues = (result) => {
  if (result.result && result.result.partial_unexpected_list) {
    return result.result.partial_unexpected_list.length > 8;
  }
  return false;
};

// 生成验证历史数据（模拟）
const generateValidationHistory = (result, currentTime) => {
  const history = [];
  const currentDate = new Date(currentTime);
  
  // 添加当前记录
  history.push({
    runTime: formatValidationTime(currentTime),
    observedValue: extractObservedValue(result),
    expectedValue: getExpectedValue(result.expectation_config),
    success: result.success
  });
  
  return history;
};

// 获取期望值
const getExpectedValue = (config) => {
  switch (config.type) {
    case 'expect_table_row_count_to_equal':
      return config.kwargs.value;
    case 'expect_column_values_to_be_between':
      return `${config.kwargs.min_value}-${config.kwargs.max_value}`;
    default:
      return '-';
  }
};

// 计算属性
const tocItems = computed(() => validationResults.value.map(vr => ({ id: vr.id, title: vr.title })));

const filteredTocItems = computed(() => {
  if (!tocSearch.value) return tocItems.value;
  return tocItems.value.filter(item => item.title.toLowerCase().includes(tocSearch.value.toLowerCase()));
});

const filteredValidationResults = computed(() => {
  if (activeFilter.value === 'failures') {
    return validationResults.value.filter(result => result.status === 'failed');
  }
  return validationResults.value;
});

// 方法
const scrollToExpectation = (id) => {
  const element = document.getElementById(`expectation-${id}`);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};

const toggleExpectationGroup = (resultId) => {
  const result = validationResults.value.find(r => r.id === resultId);
  if (result) {
    result.expanded = !result.expanded;
  }
};

const toggleValidationHistory = (expectation) => {
  expectation.historyExpanded = !expectation.historyExpanded;
};

const showAllUnexpectedValues = (expectation) => {
  console.log('Show all unexpected values for:', expectation);
  // 这里可以实现显示所有意外值的逻辑
};

// 获取验证数据
const fetchValidationData = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    const response = await axios.get(`${API_URL}/dataasset/${assetId.value}/detail_validate`);
    rawValidationData.value = response.data;
    processValidationData(response.data);
    console.log('验证数据加载成功:', response.data);
  } catch (err) {
    console.error('获取验证数据失败:', err);
    error.value = '获取验证数据失败，请稍后重试';
    ElMessage.error('获取验证数据失败');
  } finally {
    loading.value = false;
  }
};

// 监听选中运行记录的变化
watch(selectedRunId, () => {
  if (selectedRunId.value) {
    processCurrentValidationResults();
  }
});

onMounted(async () => {
  console.log('Validation.vue mounted for asset ID:', assetId.value);
  await fetchValidationData();
});
</script>

<style scoped>
/* ... existing styles ... */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.error-container {
  padding: 20px;
}

.validation-results-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f0f2f5;
  padding: 20px;
  box-sizing: border-box;
}

.toolbar {
  margin-bottom: 20px;
  flex-shrink: 0;
}

.main-content-area {
  flex-grow: 1;
  overflow: hidden;
}

.sidebar-card {
  margin-bottom: 20px;
  border: 1px solid #e4e7ed;
}
.sidebar-card :deep(.el-card__header) {
  background-color: #fafafa;
  padding: 10px 15px;
  font-weight: 600;
  font-size: 14px;
  border-bottom: 1px solid #e4e7ed;
}
.sidebar-card :deep(.el-card__body) {
  padding: 0;
}

.batches-card .history-list-scrollbar,
.toc-card .toc-list-scrollbar {
  height: 200px;
}
.batches-card :deep(.el-card__body) {
  padding: 5px 0;
}
.toc-card :deep(.el-card__body) {
  padding: 10px;
}

.history-item {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  font-size: 13px;
}
.history-item:last-child {
  border-bottom: none;
}
.history-item:hover {
  background-color: #e6f7ff;
}
.history-item.selected {
  background-color: #bae7ff;
  border-right: 3px solid #1890ff;
}
.history-item .status-icon {
  margin-right: 10px;
}
.history-item-details {
  display: flex;
  flex-direction: column;
}
.history-item-details .timestamp {
  font-weight: 500;
  color: #303133;
}
.history-item-details .full-timestamp {
  font-size: 11px;
  color: #909399;
}

.toc-search {
  margin-bottom: 10px;
}
.toc-item {
  padding: 8px 5px;
  cursor: pointer;
  font-size: 13px;
  color: #303133;
  border-radius: 3px;
}
.toc-item:hover {
  background-color: #f5f5f5;
}

.results-list {
  height: calc(100vh - 120px);
  overflow-y: auto;
  padding-right: 5px;
}

.result-card {
  margin-bottom: 20px;
  border: 1px solid #e4e7ed;
}
.result-card :deep(.el-card__header) {
  padding: 12px 15px;
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
}
.result-card-header {
  display: flex;
  align-items: center;
  font-weight: 600;
  font-size: 15px;
}
.result-card-header .collapse-icon {
  margin-right: 8px;
  cursor: pointer;
  color: #909399;
}
.result-card-header .status-tag {
  margin-left: auto;
}

.expectation-detail {
  padding: 10px 0;
  border-bottom: 1px dashed #ebeef5;
}
.expectation-detail:last-child {
  border-bottom: none;
}

.expectation-description {
  display: flex;
  align-items: flex-start;
  margin-bottom: 8px;
}
.expectation-description p {
  margin: 0 0 0 10px;
  font-size: 14px;
  line-height: 1.6;
  color: #303133;
}
.expectation-description p strong {
  font-weight: 600;
  color: #000;
}
.indicator-bar {
  display: inline-block;
  width: 4px;
  min-height: 20px;
  border-radius: 2px;
  flex-shrink: 0;
}
.indicator-bar.success { background-color: #67C23A; }
.indicator-bar.failure { background-color: #F56C6C; }

.observed-value,
.success-rate-section,
.sample-values {
  font-size: 13px;
  color: #606266;
  margin-left: 14px;
  margin-bottom: 8px;
}
.observed-value strong {
  color: #303133;
}

.success-rate-section {
  display: flex;
  align-items: center;
}
.success-rate-section .success-progress {
  width: 120px;
  margin-left: 8px;
}
.success-rate-section :deep(.el-progress-bar__innerText) {
  font-size: 10px !important;
  color: #333 !important;
}

.sample-values .sample-value-tag {
  background-color: #f0f0f0;
  padding: 2px 6px;
  border-radius: 3px;
  margin-right: 5px;
  font-family: monospace;
  font-size: 12px;
  color: #555;
}

.sample-values .see-all-link {
  color: #409EFF;
  cursor: pointer;
  text-decoration: underline;
  margin-left: 5px;
}

.validation-history-section {
  margin-top: 10px;
  margin-left: 14px;
  padding-top: 10px;
  border-top: 1px dashed #ebeef5;
}

.validation-history-toggle {
  font-size: 13px;
  padding: 0;
  margin-bottom: 10px;
}

.validation-history-content {
  background-color: #fafafa;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
}

.history-table {
  width: 100%;
}

.success-value {
  color: #67C23A;
  display: flex;
  align-items: center;
  gap: 4px;
}

.failed-value {
  color: #F56C6C;
  display: flex;
  align-items: center;
  gap: 4px;
}

.results-list::-webkit-scrollbar, 
.history-list-scrollbar :deep(.el-scrollbar__wrap)::-webkit-scrollbar,
.toc-list-scrollbar :deep(.el-scrollbar__wrap)::-webkit-scrollbar {
  width: 6px;
}
.results-list::-webkit-scrollbar-thumb,
.history-list-scrollbar :deep(.el-scrollbar__thumb)::-webkit-scrollbar-thumb,
.toc-list-scrollbar :deep(.el-scrollbar__thumb)::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}
.results-list::-webkit-scrollbar-thumb:hover,
.history-list-scrollbar :deep(.el-scrollbar__thumb)::-webkit-scrollbar-thumb:hover,
.toc-list-scrollbar :deep(.el-scrollbar__thumb)::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>