<template>
  <div class="existing-data-assets-view">
      <div class="header-controls">
        <div class="title-section">
          <div class="title-icon">
            <el-icon><DataBoard /></el-icon>
          </div>
          <h2>数据资产</h2>
        </div>
        <div class="actions">
          <el-button type="primary" @click="onNewDataAsset" class="primary-btn">
            <el-icon><Plus /></el-icon> 新建数据资产
          </el-button>
          <el-button @click="onManageDataSources" class="secondary-btn">管理数据源</el-button>
        </div>
      </div>

      <el-row :gutter="24" class="stats-overview">
        <el-col :span="12">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-item">
              <div class="stat-icon data-source-icon">
                <el-icon><DataBoard /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ dataSourceCount }}</div>
                <div class="stat-label">数据源总数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-item">
              <div class="stat-icon data-asset-icon">
                <el-icon><Files /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ dataAssetCount }}</div>
                <div class="stat-label">数据资产总数</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <div class="data-assets-list-container"> 
        <div class="section-header">
          <h3>数据资产详情</h3>
          <div class="header-decoration"></div>
        </div>
        
        <div class="table-toolbar">
          <el-input
            v-model="searchQuery"
            placeholder="搜索数据资产名或数据源名"
            clearable
            class="search-input"
          >
            <template #prepend>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>

        <div class="table-container">
          <el-table 
            :data="filteredTableData" 
            empty-text="暂无数据资产"
            @row-click="handleRowClick"
            row-class-name="clickable-row"
            highlight-current-row
            class="modern-table"
          >
            <el-table-column prop="assetName" label="数据资产名" sortable min-width="180"> 
                <template #default="scope">
                  <div class="asset-name-cell">
                    <div class="asset-icon">
                      <img src="@/assets/pgsql_logo.svg" alt="asset icon" /> 
                    </div>
                    <span class="asset-name">{{ scope.row.assetName }}</span>
                  </div>
                </template>
            </el-table-column>
            <el-table-column prop="dataSourceName" label="数据源名" sortable min-width="150" /> 
            <el-table-column prop="lastValidated" label="最后一次校验日期" sortable min-width="180" /> 
            <el-table-column prop="status" label="状态" sortable min-width="100"> 
              <template #default="scope">
                <el-tag :type="getStatusTagType(scope.row.status)" class="status-tag">
                  {{ scope.row.status || '未知' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="coverage" label="Coverage" sortable min-width="100" />
            <el-table-column label="操作" width="100" fixed="right"> 
              <template #default="scope">
                <el-tooltip content="删除" placement="top">
                  <el-button 
                    link 
                    type="danger" 
                    :icon="Delete" 
                    @click.stop="deleteAsset(scope.row)" 
                    class="action-btn"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div v-if="!filteredTableData || filteredTableData.length === 0 && !searchQuery" class="no-data-placeholder">
          <div class="empty-state">
            <div class="empty-icon">
              <el-icon><DocumentAdd /></el-icon>
            </div>
            <h4>暂无数据资产</h4>
            <p>您还没有添加任何数据资产，立即开始创建您的第一个数据资产。</p>
            <el-button type="primary" @click="onNewDataAsset" class="empty-action-btn">
              <el-icon><Plus /></el-icon>
              立即添加
            </el-button>
          </div>
        </div>
        
        <div v-if="filteredTableData.length === 0 && searchQuery" class="no-data-placeholder">
          <div class="empty-state">
            <div class="empty-icon">
              <el-icon><Search /></el-icon>
            </div>
            <h4>未找到匹配结果</h4>
            <p>未找到与 "{{ searchQuery }}" 匹配的数据资产，请尝试其他关键词。</p>
          </div>
        </div>
      </div>

    <router-view v-slot="{ Component }">
      <transition name="fade">
        <component :is="Component" :asset-data="selectedAsset"/>
      </transition>
    </router-view>
  </div>
</template>

<script setup>
import {
  Plus,
  Search,
  Delete,
  DataBoard,
  Files,
  DocumentAdd
} from '@element-plus/icons-vue';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
const router = useRouter();
const selectedAsset = ref(null);
const props = defineProps({
  dataSources: { 
    type: Array,
    default: () => []
  },
  dataSourceCount: {
    type: Number,
    default: 0
  },
  dataAssetCount: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['manage-data-sources', 'new-data-asset', 'delete-asset-intent']); 
const searchQuery = ref('');
const processedDataAssets = computed(() => {
  const allAssets = [];
  props.dataSources.forEach(dataSource => {
    if (dataSource.dataassets && Array.isArray(dataSource.dataassets)) {
      dataSource.dataassets.forEach(asset => {
        allAssets.push({
          assetId: asset.id, 
          assetName: asset.name, 
          dataSourceId: dataSource.id, 
          dataSourceName: dataSource.name, 
          lastValidated: asset.lastValidated || '暂不显示', 
          status: asset.status || 'Validated', 
          coverage: asset.coverage || '暂不显示', 

        });
      });
    }
  });
  return allAssets;
});

const filteredTableData = computed(() => {
  if (!searchQuery.value) {
    return processedDataAssets.value;
  }
  const lowerSearchQuery = searchQuery.value.toLowerCase();
  return processedDataAssets.value.filter(item => {
    const assetNameMatch = item.assetName && item.assetName.toLowerCase().includes(lowerSearchQuery);
    const dataSourceNameMatch = item.dataSourceName && item.dataSourceName.toLowerCase().includes(lowerSearchQuery);
    return assetNameMatch || dataSourceNameMatch;
  });
});

const onManageDataSources = () => {
  emit('manage-data-sources');
};

const onNewDataAsset = () => {
  emit('new-data-asset');
};

const getStatusTagType = (status) => {
  if (!status) return 'info';
  const lowerStatus = status.toLowerCase();
  if (lowerStatus === 'validated' || lowerStatus === 'valid') return 'success';
  if (lowerStatus === 'pending' || lowerStatus === 'validating') return 'warning';
  if (lowerStatus === 'error' || lowerStatus === 'invalid') return 'danger';
  return 'info';
};

const handleRowClick = (row, column) => {
  try {
    if (column && column.label === '操作') {
      return;
    }
    if (row) {
      router.push({
        name: 'assetDetail',
        params: { 
          assetId: row.assetId,
          dataSourceName: row.dataSourceName,
          assetName: row.assetName,
        }
      });
    } else {
     ElMessage.warning('无法访问该资产的详细信息');
    }
  } catch (error) {
    ElMessage.error('操作失败，请稍后重试');
  }
};

</script>

<style scoped>
.existing-data-assets-view {
  padding: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 头部控制区域 */
.header-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.title-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6, #2563eb) ;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}

.header-controls h2 {
  margin: 0;
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #3b82f6, #2563eb) ;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.actions {
  display: flex;
  gap: 16px;
}

.primary-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb) ;
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.secondary-btn {
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid #e1e8ed;
  border-radius: 12px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  color: #667eea;
  transition: all 0.3s ease;
}

.secondary-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: #667eea;
  transform: translateY(-2px);
}

/* 统计卡片区域 */
.stats-overview {
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 20px;
  border: none;
  overflow: hidden;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.stat-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
}

.stat-item {
  display: flex;
  align-items: center;
  padding: 20px;
  gap: 24px;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.data-source-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.data-asset-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 42px;
  font-weight: 800;
  color: #2d3748;
  margin-bottom: 8px;
  line-height: 1;
}

.stat-label {
  font-size: 18px;
  color: #718096;
  font-weight: 500;
}

/* 数据资产列表容器 */
.data-assets-list-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.section-header {
  position: relative;
  margin-bottom: 32px;
}

.section-header h3 {
  font-size: 24px;
  font-weight: 700;
  color: #2d3748;
  margin: 0;
  padding-bottom: 16px;
}

.header-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 4px;
  background: linear-gradient(135deg, #3b82f6, #2563eb) ;
  border-radius: 2px;
}

/* 搜索工具栏 */
.table-toolbar {
  margin-bottom: 24px;
}

.search-input {
  width: 400px;
  border-radius: 12px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.search-input :deep(.el-input__wrapper:hover) {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: #667eea;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.2);
}

.search-input :deep(.el-input-group__prepend) {
  background: linear-gradient(135deg, #3b82f6, #2563eb) ;
  color: white;
  border: none;
  border-radius: 12px 0 0 12px;
}

/* 表格容器 */
.table-container {
  flex-grow: 1;
  border-radius: 16px;
  overflow: hidden;
}

.modern-table {
  border-radius: 16px;
  overflow: hidden;
}

.modern-table :deep(.el-table__header) {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.modern-table :deep(.el-table__header th) {
  background: transparent;
  border: none;
  font-size: 16px;
  font-weight: 700;
  color: #2d3748;
  padding: 20px 16px;
}

.modern-table :deep(.el-table__body tr) {
  transition: all 0.3s ease;
}

.modern-table :deep(.el-table__body tr:hover) {
  background: rgba(102, 126, 234, 0.05);
  cursor: pointer;
}

.modern-table :deep(.el-table__body td) {
  border: none;
  padding: 16px;
  border-bottom: 1px solid #f1f5f9;
}

.asset-name-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.asset-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(102, 126, 234, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
}

.asset-icon img {
  width: 20px;
  height: 20px;
}

.asset-name {
  font-weight: 600;
  color: #2d3748;
}

.status-tag {
  border-radius: 8px;
  font-weight: 600;
  padding: 6px 12px;
}

.action-btn {
  font-size: 18px;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  transform: scale(1.1);
}

/* 空状态 */
.no-data-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 80px 0;
}

.empty-state {
  text-align: center;
  max-width: 400px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: linear-gradient(135deg, #3b82f6, #2563eb) ;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  color: white;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.empty-state h4 {
  font-size: 24px;
  font-weight: 700;
  color: #2d3748;
  margin: 0 0 16px 0;
}

.empty-state p {
  font-size: 16px;
  color: #718096;
  margin: 0 0 32px 0;
  line-height: 1.6;
}

.empty-action-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb) ;
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.empty-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .existing-data-assets-view {
    padding: 16px;
  }
  
  .header-controls {
    flex-direction: column;
    gap: 16px;
    padding: 20px;
  }
  
  .actions {
    width: 100%;
    justify-content: center;
  }
  
  .search-input {
    width: 100%;
  }
  
  .stats-overview {
    margin-bottom: 24px;
  }
  
  .stat-item {
    padding: 24px;
  }
  
  .data-assets-list-container {
    padding: 20px;
  }
}
</style>

