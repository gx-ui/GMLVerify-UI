<template>
  <div class="create-expectations-drawer">
    <!-- 表单视图 -->
    <div v-if="currentView === 'form'" class="expectation-form-view">
      <component
        :is="activeFormComponent"
        :expectation-type="selectedTypePayload.type"
        :type-display-name="selectedTypePayload.displayName"
        :asset-fields="assetFields" 
        @back="showTypeList"
        @save="handleSaveExpectation"
      />
    </div>
    <!-- 类型选择列表视图 -->
    <div v-else class="type-selection-view">
      <div class="drawer-header">
        <div class="header-content">
          <div class="title-wrapper">
            <div class="title-icon">
              <el-icon><Edit /></el-icon>
            </div>
            <h3>创建期望</h3>
          </div>
          <div class="header-decoration"></div>
        </div>
        <el-button :icon="CloseIcon" @click="closeDrawer" class="close-btn" text></el-button>
      </div>
      
      <div class="search-section">
        <div class="search-wrapper">
          <el-input
            v-model="searchQuery"
            placeholder="按关键词搜索期望名称"
            clearable
            class="search-input"
          >
            <template #prefix>
              <el-icon class="search-icon"><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </div>
      
      <div class="expectations-scope">
        <div class="scope-section">
          <div class="scope-header">
            <div class="scope-icon">
              <el-icon><DataBoard /></el-icon>
            </div>
            <p class="scope-title">整体的期望</p>
          </div>
          <div class="expectation-types">
            <div class="type-row">
              <div class="type-card schema-card" @click="selectType('schema', '模式')">
                <div class="type-icon">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="type-info">
                  <h4>模式</h4>
                  <p>列的存在、类型和数量</p>
                </div>
                <div class="card-decoration"></div>
              </div>
              <div class="type-card volume-card" @click="selectType('volume', '数量')">
                <div class="type-icon">
                  <el-icon><DataLine /></el-icon>
                </div>
                <div class="type-info">
                  <h4>数量</h4>
                  <p>行数</p>
                </div>
                <div class="card-decoration"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="scope-section">
          <div class="scope-header">
            <div class="scope-icon">
              <el-icon><Grid /></el-icon>
            </div>
            <p class="scope-title">一个或多个特定列中的期望</p>
          </div>
          <div class="expectation-types">
            <div class="type-row">
              <div class="type-card completeness-card" @click="selectType('completeness', '完整性')">
                <div class="type-icon">
                  <el-icon><Check /></el-icon>
                </div>
                <div class="type-info">
                  <h4>完整性</h4>
                  <p>空值和非空值</p>
                </div>
                <div class="card-decoration"></div>
              </div>
              <div class="type-card uniqueness-card" @click="selectType('uniqueness', '唯一性')">
                <div class="type-icon">
                  <el-icon><Key /></el-icon>
                </div>
                <div class="type-info">
                  <h4>唯一性</h4>
                  <p>唯一值和列基数</p>
                </div>
                <div class="card-decoration"></div>
              </div>
            </div>
            <div class="type-row">
              <div class="type-card numeric-card" @click="selectType('numeric', '数值')">
                <div class="type-icon">
                  <el-icon><Histogram /></el-icon>
                </div>
                <div class="type-info">
                  <h4>数值</h4>
                  <p>列值范围和聚合</p>
                </div>
                <div class="card-decoration"></div>
              </div>
              <div class="type-card validity-card" @click="selectType('validity', '有效性')">
                <div class="type-icon">
                  <el-icon><CircleCheck /></el-icon>
                </div>
                <div class="type-info">
                  <h4>有效性</h4>
                  <p>值模式匹配</p>
                </div>
                <div class="card-decoration"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="scope-section custom-section">
          <div class="scope-header">
            <div class="scope-icon">
              <el-icon><Setting /></el-icon>
            </div>
            <p class="scope-title">自定义期望</p>
          </div>
          <div class="type-card sql-card" @click="selectType('sql', 'SQL')">
            <div class="type-icon">
              <el-icon><Edit /></el-icon> 
            </div>
            <div class="type-info">
              <h4>SQL</h4>
              <p>写自己的SQL语句</p>
            </div>
            <div class="card-decoration"></div>
          </div>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, shallowRef, onMounted } from 'vue'; 
import axios from 'axios';
import { API_URL } from '@/config';
import {
  Search, Document, DataLine, Check, Key, Histogram, CircleCheck, Edit, Close as CloseIcon,
  DataBoard, Grid, Setting
} from '@element-plus/icons-vue';

// 导入表单组件
import ExpectationSchemaForm from './expectationForms/Schema.vue';
import ExpectationVolumeForm from './expectationForms/Volume.vue';
import ExpectationCompletenessForm from './expectationForms/Completeness.vue';
import ExpectationUniquenessForm from './expectationForms/Uniqueness.vue';
import ExpectationNumericForm from './expectationForms/Numeric.vue';
import ExpectationValidityForm from './expectationForms/Validity.vue';

const searchQuery = ref('');
const currentView = ref('list'); 
const selectedTypePayload = ref({ type: null, displayName: null });

// 定义 props 接收 assetId
const props = defineProps({
  assetId: {
    type: [String, Number],
    required: true
  }
});

const emit = defineEmits(['close', 'create-expectation']);

const formComponents = {
  schema: ExpectationSchemaForm,
  volume: ExpectationVolumeForm,
  completeness: ExpectationCompletenessForm,
  uniqueness: ExpectationUniquenessForm,
  numeric: ExpectationNumericForm,
  validity: ExpectationValidityForm,
};

const activeFormComponent = shallowRef(null);

const assetFields =ref({});
onMounted(async () => {
  try {
    const response = await axios.get(`${API_URL}/pg/${props.assetId}/tablesInfo`);
    assetFields.value = response.data;  
  } catch (error) {
  }
});


const selectType = (type, displayName) => {
  selectedTypePayload.value = { type, displayName };
  if (formComponents[type]) {
    activeFormComponent.value = formComponents[type];
    currentView.value = 'form';
  } else {
    console.warn(`No form component defined for type: ${type}`);
  }
};

const showTypeList = () => {
  currentView.value = 'list';
  activeFormComponent.value = null;
  selectedTypePayload.value = { type: null, displayName: null };

};

const closeDrawer = () => {
  emit('close');
};


const handleSaveExpectation = (isSaveAndAddMore) => {
   isSaveAndAddMore ? currentView.value = 'form' : showTypeList(); 
  emit('create-expectation', flag.update);
};

</script>

<style scoped>

:root {
  --primary-color: #409eff;
  --primary-light: #79bbff;
  --primary-lighter: #a0cfff;
  --success-color: #67c23a;
  --warning-color: #e6a23c;
  --danger-color: #f56c6c;
  --info-color: #909399;
  --text-primary: #303133;
  --text-regular: #606266;
  --text-secondary: #909399;
  --text-placeholder: #c0c4cc;
  --border-light: #e4e7ed;
  --border-lighter: #ebeef5;
  --bg-color: #ffffff;
  --bg-light: #f5f7fa;
}

.create-expectations-drawer {
  padding: 0 ;
  height: 100%;
  display: flex;
  flex-direction: column;
  /* background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); */
  position: relative;
  overflow: hidden;
}


.create-expectations-drawer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;

  background: 
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.type-selection-view,
.expectation-form-view {
  padding: 10px 10px;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  position: relative;
  z-index: 1;
}

/* 头部样式 */
.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  flex-shrink: 0;
}

.header-content {
  flex: 1;
}

.title-wrapper {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.title-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  margin-right: 12px;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.title-icon .el-icon {
  font-size: 20px;
  color: rgb(0, 0, 0);
}
.drawer-header h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);

}

.header-decoration {
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color) 0%, var(--primary-light) 100%);
  border-radius: 2px;
  margin-top: 4px;
}

.close-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  transition: all 0.3s ease;
  color: var(--text-secondary);
}

.close-btn:hover {
  background-color: rgba(64, 158, 255, 0.1);
  color: var(--primary-color);
  transform: scale(1.05);
}

/* 搜索区域样式 */
.search-section {
  margin-bottom: 36px;
  flex-shrink: 0;
}

.search-wrapper {
  position: relative;
}

.search-input {
  --el-input-border-radius: 12px;
  --el-input-bg-color: rgba(255, 255, 255, 0.8);
  --el-input-border-color: rgba(228, 231, 237, 0.6);
  --el-input-focus-border-color: var(--primary-color);
}

.search-input :deep(.el-input__wrapper) {
  backdrop-filter: blur(10px);
  border: 1px solid rgba(228, 231, 237, 0.6);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.search-input :deep(.el-input__wrapper:hover) {
  border-color: var(--primary-light);
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.1);
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.search-icon {
  color: var(--text-placeholder);
  transition: color 0.3s ease;
}

.search-input:hover .search-icon,
.search-input.is-focus .search-icon {
  color: var(--primary-color);
}

/* 期望范围样式 */
.expectations-scope {
  overflow-y: auto;
  overflow-x: hidden; 
  flex-grow: 1;
}

.scope-section {
  margin-bottom: 36px;
}

.scope-section:last-child {
  margin-bottom: 0;
}

.scope-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.scope-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--primary-lighter) 0%, var(--primary-light) 100%);
  margin-right: 12px;
}

.scope-icon .el-icon {
  font-size: 16px;
  color: var(--primary-color);
}

.scope-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-regular);
  margin: 0;
}

.expectation-types {
  margin-bottom: 24px;
}

.type-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.type-row:last-child {
  margin-bottom: 0;
}

/* 类型卡片样式 */
.type-card {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 20px;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.type-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, transparent 0%, rgba(255, 255, 255, 0.1) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.type-card:hover::before {
  opacity: 1;
}

.type-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}

/* .card-decoration {
  display: none;
}

.type-card:hover .card-decoration {
  opacity: 0.2;
} */

/* 不同类型卡片的主题色 */
.schema-card {
  background: linear-gradient(135deg, rgba(103, 194, 58, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%);
}

.schema-card .card-decoration {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.schema-card .type-icon {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.volume-card {
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%);
}

.volume-card .card-decoration {
  background: linear-gradient(135deg, #409eff 0%, #79bbff 100%);
}

.volume-card .type-icon {
  background: linear-gradient(135deg, #409eff 0%, #79bbff 100%);
}

.completeness-card {
  background: linear-gradient(135deg, rgba(230, 162, 60, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%);
}

.completeness-card .card-decoration {
  background: linear-gradient(135deg, #e6a23c 0%, #ebb563 100%);
}

.completeness-card .type-icon {
  background: linear-gradient(135deg, #e6a23c 0%, #ebb563 100%);
}

.uniqueness-card {
  background: linear-gradient(135deg, rgba(245, 108, 108, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%);
}

.uniqueness-card .card-decoration {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
}

.uniqueness-card .type-icon {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
}

.numeric-card {
  background: linear-gradient(135deg, rgba(144, 147, 153, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%);
}

.numeric-card .card-decoration {
  background: linear-gradient(135deg, #909399 0%, #a6a9ad 100%);
}

.numeric-card .type-icon {
  background: linear-gradient(135deg, #909399 0%, #a6a9ad 100%);
}

.validity-card {
  background: linear-gradient(135deg, rgba(103, 194, 58, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%);
}

.validity-card .card-decoration {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.validity-card .type-icon {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.sql-card {
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.1) 0%, rgba(255, 255, 255, 0.9) 100%);
}

.sql-card .card-decoration {
  background: linear-gradient(135deg, #409eff 0%, #79bbff 100%);
}

.sql-card .type-icon {
  background: linear-gradient(135deg, #409eff 0%, #79bbff 100%);
}

.type-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  margin-right: 16px;
  position: relative;
  z-index: 2;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.type-icon .el-icon {
  font-size: 24px;
  color: white;
}

.type-info {
  flex: 1;
  position: relative;
  z-index: 2;
}

.type-info h4 {
  margin: 0 0 6px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.type-info p {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.custom-section {
  margin-top: 32px;
}

.custom-section .type-card {
  max-width: none;
}



@media (max-width: 768px) {
  .type-row {
    flex-direction: column;
    gap: 12px;
  }
  
  .type-card {
    padding: 16px;
  }
  
  .type-icon {
    width: 40px;
    height: 40px;
  }
  
  .type-icon .el-icon {
    font-size: 20px;
  }
  
  .type-info h4 {
    font-size: 16px;
  }
  
  .type-info p {
    font-size: 13px;
  }
}






/* 动画效果已移除，界面加载更加直接流畅 */
</style>