<template>
  <div class="expectations-content">
    <div class="validate-asset-section">
      <div class="validate-header">
        <div class="validate-title">
          <el-icon>
            <Files />
          </el-icon>
          <span>验证数据资产</span>
        </div>

        <div class="validate-actions">

          <el-button text @click="editBatchConfig">
            <el-icon>
              <EditPen />
            </el-icon> No scheduled validation
          </el-button>

          <el-button type="primary" :icon="VideoPlay" @click="validateAsset"
            :disabled="totalExpectationsCount === 0 || isValidating" :loading="isValidating">
            {{ isValidating ? 'Validating...' : 'Validate' }}
          </el-button>

        </div>
      </div>


      <div class="expectation-list-main-header" v-if="totalExpectationsCount > 0">
        <div class="header-col-expectation">
          <span>Expectation</span>
          <el-dropdown trigger="click" placement="bottom-start" 
            v-model:visible="filterDropdownVisible" v-if="filterableColumns.length > 0">
            <el-icon class="filter-icon" :class="{ 'filter-active': isFilterActive }">
              <Filter />
            </el-icon>
            <template #dropdown>
              <el-dropdown-menu>
                <div class="filter-dropdown-content">
                  <el-checkbox-group v-model="selectedFilterColumns">
                    <el-checkbox v-for="col in filterableColumns" :key="col" :value="col" class="filter-checkbox-item">
                      {{ col != ASSET_LEVEL_FILTER_KEY ? col : ASSET_LEVEL_FILTER_KEY }}
                    </el-checkbox>
                  </el-checkbox-group>
                  <div class="filter-dropdown-actions">
                    <el-button text @click.stop="handleFilterReset">Reset</el-button>
                    <el-button type="primary" size="small" @click.stop="handleFilterOk">OK</el-button>
                  </div>
                </div>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
        <div class="header-col-last-validated">Last validated</div>
        <div class="header-col-actions">Actions</div>
      </div>
      <el-collapse v-model="activeCollapseNames" v-if="totalExpectationsCount > 0">
        <el-collapse-item v-for="category in processedExpectations" :key="category.name" :name="category.name"
          :class="{ 'category-has-expectations': category.items.length > 0 }">
          <template #title>
            <div class="category-title-content">
              <el-icon class="collapse-arrow-icon">
                <component :is="activeCollapseNames.includes(category.name) ? ArrowDown : ArrowRight" />
              </el-icon>
              <el-icon class="category-icon">
                <Document v-if="category.name === 'Schema'" />
                <DataLine v-else-if="category.name === 'Volume'" />
                <Check v-else-if="category.name === 'Completeness'" />
                <Key v-else-if="category.name === 'Uniqueness'" />
                <Histogram v-else-if="category.name === 'Numeric'" />
                <CircleCheck v-else-if="category.name === 'Validity'" />
              </el-icon>

              <span class="category-name">{{ category.name }}</span>
              <span class="category-count" :class="{
                'passed-color': category.countText === 'All passed',
                'failed-color': category.countText.includes('Failed')
              }">{{ category.countText }} </span>
            </div>
          </template>

          <div v-if="category.items.length > 0">

            <el-table :data="category.items" :show-header="false" row-class-name="expectation-row">
              <el-table-column label="Expectation" class-name="expectation-col-expectation-data">
                <template #default="scope">
                  <div class="expectation-cell-content">
                    <el-icon v-if="scope.row.status === 'passed'" color="#67C23A" class="status-icon">
                      <CircleCheckFilled />
                    </el-icon>
                    <el-icon v-else-if="scope.row.status === 'failed'" color="#F56C6C" class="status-icon">
                      <CircleCloseFilled />
                    </el-icon>
                    <el-icon v-else color="#909399" class="status-icon">
                      <QuestionFilled />
                    </el-icon>

                    <div class="expectation-text-details">
                      <div class="description">{{ scope.row.description }}</div>
                      <div v-if="scope.row.statusText"
                        :class="['status-detail-text', scope.row.status === 'passed' ? 'passed-color' : 'failed-color']">
                        {{ scope.row.statusText }}
                      </div>
                    </div>

                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="lastValidated" label="Last validated"
                class-name="expectation-col-last-validated-data">
                <template #default="scope">
                  <span :class="[
                    'validation-time-text',
                    scope.row.status === 'passed' ? 'passed-color' :
                      scope.row.status === 'failed' ? 'failed-color' :
                        'validation-time-default'
                  ]">
                    {{ scope.row.lastValidated }}
                  </span>
                </template>
              </el-table-column>

              <el-table-column label="Actions" class-name="expectation-col-actions-data">
                <template #default="scope">
                  <el-tooltip content="Edit" placement="top">
                    <el-button link type="primary" :icon="Edit" @click="editExpectation(scope.row.raw)"
                      size="small"></el-button>
                  </el-tooltip>
                  <el-tooltip content="Delete" placement="top">
                    <el-button link type="danger" :icon="Delete" @click="deleteExpectation(scope.row.raw)"
                      size="small"></el-button>
                  </el-tooltip>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <div v-else class="no-expectations-in-category">
            此种类下目前还没有期望
          </div>
        </el-collapse-item>
      </el-collapse>

      <div v-else class="empty-state-message">
        {{ selectedFilterColumns.length > 0 ? 'No expectations match the current filter.' : 'Add your first Expectation to start validating your Asset' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed ,watch} from 'vue';
import { useRoute } from 'vue-router';
import { useExpectationStore } from '@/stores/expectationStore'

import {
  ElButton, ElIcon, ElTable, ElTableColumn, ElTooltip, ElCollapse, ElCollapseItem,
  ElDropdown, ElDropdownMenu, ElCheckbox, ElCheckboxGroup, ElMessage
} from 'element-plus';
import {
  Files,
  EditPen,
  VideoPlay,
  Edit,
  Delete,
  Histogram,
  DataLine,
  Check,
  Key,
  CircleCheckFilled,
  CircleCheck,
  CircleCloseFilled,
  QuestionFilled,
  ArrowRight,
  ArrowDown,
  Document,
  Filter
} from '@element-plus/icons-vue';
import axios from 'axios';
import { API_URL } from '@/config';
const expectationStore = useExpectationStore()
const route = useRoute();
const assetId = computed(() => route.params.assetId);
const ASSET_LEVEL_FILTER_KEY = '其它期望';
const processedExpectations = ref([
  { name: 'Schema', items: [], countText: '0 Expectations', typeIdPrefix: 1 },
  { name: 'Volume', items: [], countText: '0 Expectations', typeIdPrefix: 2 },
  { name: 'Completeness', items: [], countText: '0 Expectations', typeIdPrefix: 3 },
  { name: 'Uniqueness', items: [], countText: '0 Expectations', typeIdPrefix: 4 },
  { name: 'Numeric', items: [], countText: '0 Expectations', typeIdPrefix: 5 },
  { name: 'Validity', items: [], countText: '0 Expectations', typeIdPrefix: 6 },
]);
const originalProcessedExpectations = ref([]);
const filterableColumns = ref([]);
const selectedFilterColumns = ref([]);
const filterDropdownVisible = ref(false);
const isValidating = ref(false);
const lastValidationTime = ref(null);
const isFilterActive = computed(() => selectedFilterColumns.value.length > 0);

// 列表默认收起
const activeCollapseNames = ref([]);
const totalExpectationsCount = computed(() => {
  return processedExpectations.value.reduce((total, category) => total + category.items.length, 0);
});

watch(() => expectationStore.needsRefresh,async (newValue) => {
    if (newValue) {
      const fetchResult = await fetchExpectations();
      if (fetchResult) {
         processExpectationsData(fetchResult.expectationsData, fetchResult.validationResults);
      }
      expectationStore.resetRefresh();
    }
  }
)

// 时间格式化
const formatValidationTime = (timestamp) => {
  if (!timestamp) return 'Never';
  const date = new Date(timestamp);
  const today = new Date();

  if (date.toDateString() === today.toDateString()) {
    return `Today at ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
  } else {
    return date.toLocaleDateString();
  }
  
};


const fetchExpectations = async () =>{
  let expectationsData = [];
  let validationResults = [];
  try {
    const [expectationsResponse, validationResponse] = await Promise.all([
      axios.get(`${API_URL}/dataasset/${assetId.value}/expectation`),
      axios.get(`${API_URL}/dataasset/${assetId.value}/validate`)
    ]);
    expectationsData = expectationsResponse.data;
    validationResults = validationResponse.data;
    console.log('期望数据:', expectationsData);
    console.log('验证结果:', validationResults);
    return {
      expectationsData:expectationsData,
      validationResults:validationResults
    }
  } catch (error) {
    console.error('Error fetching data:', error);
    ElMessage.error('网络请求失败，请检查网络连接');
    return;
  }

}


// 提取数据处理逻辑为独立函数
const processExpectationsData = (expectationsData, validationResults) => {
  // 重置数据
  processedExpectations.value.forEach(category => {
    category.items = [];
    category.countText = '0 Expectations';
  });
  
  const tempFilterableCols = new Set();
  let hasAssetLevelExpectations = false;
  const validationMap = new Map();
  
  // 确保 validationResults 是数组
  if (Array.isArray(validationResults)) {
    validationResults.forEach(result => {
      validationMap.set(result.expectation_suite_id, result);
    });
  }

  expectationsData.forEach(expectation => {
    const firstDigit = Math.floor(expectation.type_id / 100);
    const targetCategory = processedExpectations.value.find(cat => {
      return cat.typeIdPrefix === firstDigit;
    });
    if (targetCategory) {
      const validationResult = validationMap.get(expectation.id);
      let status, statusText, lastValidated;
      if (validationResult) {
        status = validationResult.success ? 'passed' : 'failed';
        statusText = validationResult.success ? 'passed' : 'Failed';
        lastValidated = formatValidationTime(validationResult.validation_time);
      } else {
        status = 'unknown';
        statusText = 'Not validated yet';
        lastValidated = '待验证';
      }
      const processedItem = {
        id: expectation.id,
        description: expectation.description,
        status: status,
        statusText: statusText,
        lastValidated: lastValidated,
        raw: expectation
      };
      targetCategory.items.push(processedItem);
      const itemColumn = expectation.suite_json.expectations[0].kwargs.column;
      itemColumn ? tempFilterableCols.add(itemColumn) : hasAssetLevelExpectations = true;
    }
  });
  
  // 设置过滤列和统计信息
  const sortedCols = Array.from(tempFilterableCols).sort();
  filterableColumns.value = hasAssetLevelExpectations ? [ASSET_LEVEL_FILTER_KEY, ...sortedCols] : sortedCols;
  setCountText();
  originalProcessedExpectations.value = JSON.parse(JSON.stringify(processedExpectations.value));
};

// 修改 onMounted
onMounted(async () => {
  const fetchResult = await fetchExpectations();
  if (fetchResult) {
    await processExpectationsData(fetchResult.expectationsData, fetchResult.validationResults);
  }
});

function applyColumnFilter() {
  const sourceData = JSON.parse(JSON.stringify(originalProcessedExpectations.value));

  if (selectedFilterColumns.value.length === 0) {
    processedExpectations.value = sourceData;
  } else {
    const filteredResult = sourceData.map(category => {
      const newItems = category.items.filter(item => {
        const effectiveItemColumn = item.raw.suite_json.expectations[0].kwargs.column;
        const isAssetLevel = effectiveItemColumn === undefined || effectiveItemColumn === null;
        return (selectedFilterColumns.value.includes(ASSET_LEVEL_FILTER_KEY) && isAssetLevel) ||
          (effectiveItemColumn && selectedFilterColumns.value.includes(effectiveItemColumn));
      });
      category.items = newItems;
      return category;
    });
    processedExpectations.value = filteredResult;
  }
  setCountText()
}

function setCountText() {
    let totalCount=0
    let failedCount=0
    let passedCount=0
  processedExpectations.value.forEach(category => {
    totalCount=category.items.length;
    failedCount = category.items.filter(item => item.status === 'failed').length;
    passedCount = category.items.filter(item => item.status === 'passed').length;
    category.countText = `${totalCount} Expectations`;
    if (totalCount != 0&&failedCount!=0) {
            category.countText=`${failedCount}/${totalCount} Failed`     
    }else if (totalCount==passedCount&&totalCount!=0){
      category.countText = 'All passed';  
    }
  });
}
function handleFilterOk() {
  applyColumnFilter();
  setTimeout(() => {
    forceCloseDropdown();
  }, 30);
}
function handleFilterReset() {
  selectedFilterColumns.value = [];
  applyColumnFilter();
  setTimeout(() => {
    forceCloseDropdown();
  }, 30);
}
function forceCloseDropdown() {
  const event = new MouseEvent('click', {
    view: window,
    bubbles: true,
    cancelable: true
  });
  document.body.dispatchEvent(event);
}
// 点击提交期望进行验证
const validateAsset = async () => {
  if (isValidating.value) return;
  isValidating.value = true;
  try {
    const response = await axios.post(`${API_URL}/dataasset/${assetId.value}/validate`);
    if (response.data ) {
      const validationResults = response.data;
      lastValidationTime.value = new Date().toISOString();
      updateExpectationStatus(validationResults);
      console.log('验证完成，结果:', validationResults);
    }
  } catch (error) {
    ElMessage.error('验证失败，请稍后重试');
  } finally {
    isValidating.value = false;
  }
};

const updateExpectationStatus = (validationResults) => {
  const currentTime = new Date();
  const timeString = `Today at ${String(currentTime.getHours()).padStart(2, '0')}:${String(currentTime.getMinutes()).padStart(2, '0')}`;
  const resultMap = new Map();
  validationResults.forEach(result => {
    resultMap.set(result.expectation_suite_id, result);
  });
  processedExpectations.value.forEach(category => {
    category.items.forEach(item => {
      const expectationId = item.raw.id;
      const validationResult = resultMap.get(expectationId);
      if (validationResult) {
        item.status = validationResult.success ? 'passed' : 'failed';
        item.statusText = validationResult.success ? ' passed' : 'Failed';
        item.lastValidated = timeString;
      }
    });
  });
  setCountText();

};
const editBatchConfig = () => { console.log('Edit batch configuration for asset ID:', assetId.value); };
const editExpectation = (expectationRawData) => { console.log('Edit expectation:', expectationRawData); };
const deleteExpectation = (expectationRawData) => { console.log('Delete expectation:', expectationRawData); };
</script>

<style scoped>
.expectations-content {
  height: 100%;
  overflow-y: auto;
  padding: 20px;
  box-sizing: border-box;
  background-color: #f7f8fa;
}

.validate-asset-section {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.validate-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.validate-title {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.validate-title .el-icon {
  margin-right: 8px;
  font-size: 22px;
}

.validate-actions .el-button {
  margin-left: 10px;
}

.validate-actions .el-button--text {
  color: #606266;
}

.validate-actions .el-button--text .el-icon {
  margin-right: 4px;
}

.expectation-list-main-header {
  display: flex;
  align-items: center;
  padding: 10px 0px 10px 0px;
  /* 调整整体内边距，特别是左侧，与内容对齐 */
  margin-bottom: 0px;
  font-weight: bold;
  color: #606266;
  font-size: 14px;
  border-bottom: 1px solid #ebeef5;
}

.header-col-expectation {
  flex: 1;
  min-width: 0;
  display: flex;

  align-items: center;
  padding-left: 38px;

}

.header-col-last-validated {
  flex: 1;
  text-align: left;
  flex-shrink: 0;
  padding-left: 70px;
  padding-right: 10px;
}

.header-col-actions {
  flex: 1;
  text-align: center;
  flex-shrink: 0;
  padding-left: 10px;
  padding-right: 10px;
}

.filter-icon {
  margin-left: 8px;
  cursor: pointer;
  color: #909399;
  font-size: 18px;
}

.filter-icon:hover {
  color: #409EFF;
}


.filter-icon.filter-active {
  color: #409EFF;
}

.filter-dropdown-content {
  padding: 12px 15px;
  min-width: 100px;
}

.filter-dropdown-content .el-checkbox-group {
  display: flex;
  flex-direction: column;
  max-height: 200px;

  overflow-y: auto;
  margin-bottom: 10px;
}

.filter-checkbox-item.el-checkbox {
  margin-bottom: 8px;
  margin-right: 0;
}

.filter-checkbox-item.el-checkbox:last-child {
  margin-bottom: 0;
}

.filter-dropdown-actions {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #ebeef5;
  padding-top: 10px;
}


.el-collapse-item :deep(.el-collapse-item__arrow) {
  display: none;
}

.el-collapse-item :deep(.el-collapse-item__header) {
  font-size: 16px;
  font-weight: normal;
  border-bottom: 1px solid #ebeef5;
  height: 80px;
  padding: 0 10px;
  box-sizing: border-box;
}

.el-collapse-item :deep(.el-collapse-item__wrap) {
  border-bottom: none;
}


.category-title-content {
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
}

.collapse-arrow-icon {
  font-size: 16px;
  margin-right: 10px;
  color: #606266;
}

.category-icon {
  font-size: 25px;
  margin-right: 8px;
  color: #606266;
}

.category-name {
  font-weight: 500;
  color: #303133;
}

.el-collapse-item.category-has-expectations .category-title-content .category-name {
  color: #67C23A;
  /* Green color when expectations exist */
}

/* New CSS selector for category icon */
.el-collapse-item.category-has-expectations .category-title-content .category-icon {
  color: #67C23A;
  /* Green color for icon when expectations exist */
}

.category-count {
  margin-left: 12px;
  font-size: 14px;
  color: #909399;
}

.expectation-row .el-table__cell {
  padding: 20px 0;
}

.expectation-cell-content {
  display: flex;
  align-items: center;
  padding-left: 38px;
}

.status-icon {
  font-size: 18px;
  margin-right: 10px;
  flex-shrink: 0;
}

.expectation-text-details {
  display: flex;
  flex-direction: column;
}

.expectation-text-details .description {
  font-size: 14px;
  color: #303133;
  line-height: 1.5;
}

.status-detail-text {
  font-size: 12px;
  margin-top: 4px;
}

.passed-color {
  color: #67C23A;
}

.failed-color {
  color: #F56C6C;
}

.no-expectations-in-category {
  padding: 20px 0px 20px 38px;
  text-align: left;
  color: #909399;
  font-size: 14px;
}

.empty-state-message {
  text-align: center;
  color: #909399;
  padding: 40px 0;
  font-size: 15px;
}

:deep(.expectation-col-expectation-data .cell) {
  padding-left: 0 !important;
  padding-right: 10px !important;
}

:deep(.expectation-col-last-validated-data .cell) {
  padding-left: 60px !important;
  padding-right: 10px !important;
  text-align: left;
  font-size: 14px;
  color: #303133;
}

:deep(.expectation-col-actions-data .cell) {
  padding-left: 10px !important;
  padding-right: 10px !important;
  text-align: center;
}

.expectation-col-last-validated-data {
  width: 200px !important;
  flex-shrink: 0;
}

.expectation-col-actions-data {
  width: 120px !important;
  flex-shrink: 0;
}
.validation-time-text {
  font-size: 14px;
}
.validation-time-default {
  color: #303133;

}
</style>