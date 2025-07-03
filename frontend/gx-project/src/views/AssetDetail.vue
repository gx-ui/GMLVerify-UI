<template>
  <div class="asset-detail-view">
    <!-- Header (保持不变) -->
    <div class="asset-header">
      <div class="header-left">
        <el-button :icon="ArrowLeft" @click="goBack" text style="font-size: 24px; margin-right: 8px; padding: 0;"/>
        <img src="@/assets/pgsql_logo.svg" alt="Data source type icon" class="datasource-icon" />
        <h1 class="asset-name">{{ assetName }}</h1>
        <span class="expectations-count">{{ expectationsCount }} Expectations</span>
      </div>
      <div class="header-right">
        <el-button>Alerts</el-button>
        <el-button>
          Generate Expectations
          <el-tag type="info" size="small" effect="plain" style="margin-left: 5px;">BETA</el-tag>
        </el-button>
        <el-button type="primary" :icon="Plus" @click="showCreateExpectations">New Expectation</el-button>
      </div>
    </div>

    <!-- Tabs for Child Route Navigation -->
    <el-tabs v-model="activeChildRouteName" @tab-click="handleTabClick" class="asset-navigation-tabs">
      <el-tab-pane label="Expectations" name="AssetExpectations" ></el-tab-pane>
      <el-tab-pane label="Validations" name="AssetValidations"></el-tab-pane>
      <el-tab-pane label="Metrics" name="AssetMetrics"></el-tab-pane>
    </el-tabs>

    <!-- Router View for Child Components -->
    <div class="asset-content-area">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </transition>
      </router-view>
    </div>
    <!-- 添加 CreateExpectations 抽屉组件 -->
    <el-drawer
      v-model="showExpectationsDrawer"
      direction="rtl"
      size="600px"
      :show-close="false"
      :with-header="false"
    >
      <CreateExpectations
        @close="closeExpectationsDrawer"
        :asset-id="assetId"
      />
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter }from 'vue-router';
import {ElButton, ElTag, ElTabs, ElTabPane} from 'element-plus';
import {ArrowLeft, Plus} from '@element-plus/icons-vue';
import CreateExpectations from '@/components/CreateExpectations.vue';

// import { useExpectationStore } from '@/stores/expectationStore';
const route = useRoute();
const router = useRouter();

const assetId = ref('');
const assetName = ref('');
const assetStatus = ref(''); 
const expectationsCount = ref(0);

const activeChildRouteName = ref('AssetExpectations'); 

const childRouteNames = {
  expectations: 'AssetExpectations',
  validations: 'AssetValidations',
  metrics: 'AssetMetrics',
};







// 添加新的响应式变量
const showExpectationsDrawer = ref(false);
const assetFields = ref([]); // 新增：存储数据资产字段信息

onMounted( () => {
  assetId.value = route.params.assetId || 'N/A';
  assetName.value = route.params.assetName || 'Default Asset Name';
  


  updateActiveTabFromRoute();
  if (!route.name || route.name === 'assetDetail') {
    router.replace({ name: childRouteNames.expectations, params: route.params, query: route.query });
  }
});

watch(() => route.name, () => {
  updateActiveTabFromRoute();
});

const updateActiveTabFromRoute = () => {
  if (Object.values(childRouteNames).includes(route.name)) {
    activeChildRouteName.value = route.name;
  } else if (route.name === 'assetDetail') {
    activeChildRouteName.value = childRouteNames.expectations;
  }
};

const statusTagType = computed(() => {
  if (!assetStatus.value) return 'info';
  const lowerStatus = assetStatus.value.toLowerCase();
  if (lowerStatus === 'validated' || lowerStatus === 'valid' || lowerStatus === 'active') return 'success';
  if (lowerStatus === 'pending' || lowerStatus === 'validating') return 'warning';
  if (lowerStatus === 'error' || lowerStatus === 'invalid') return 'danger';
  if (lowerStatus === 'inactive') return 'default';
  return 'info';
});

const goBack = () => {
    router.push({ name: 'existing-assets' });
};

const handleTabClick = (tab) => {
  const targetRouteName = tab.props.name;
  if (targetRouteName && route.name !== targetRouteName) {
    router.push({ name: targetRouteName, params: { assetId: assetId.value, ...route.params } });
  }
};




// 添加新的方法
const showCreateExpectations = async () => {

  showExpectationsDrawer.value = true; 
};

const closeExpectationsDrawer = () => {
  showExpectationsDrawer.value = false;
  assetFields.value = []; 
};




// const expectationStore = useExpectationStore()


// const updataExpectation = async () => {
//   try {

//     expectationStore.triggerRefresh()
//   } catch (error) {
//     console.error('保存期望失败:', error)
//   }
// }
</script>

<style scoped>
.asset-detail-view {
  padding: 24px;
  background-color: #fff;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.asset-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px; /* 与图片保持一致 */
  padding-bottom: 16px; /* 在头部和tabs之间增加一些间距 */
  /* border-bottom: 1px solid #e5e7eb; */ /* 可选：在头部下方添加分割线 */
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.datasource-icon {
  width: 24px; /* 根据图片调整 */
  height: 24px; /* 根据图片调整 */
}
.asset-name {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  margin-left: 4px;
}
.status-tag {
  margin-left: 12px;
  font-size: 12px;
}
.expectations-count {
  margin-left: 12px;
  font-size: 12px;
  color: #6b7280;
}
.header-right {
  display: flex;
  gap: 12px;
}
.header-right .el-button {
  font-size: 14px;
}

.asset-navigation-tabs {
  margin-bottom: 10px; /* Tabs 和下方内容区域的间距 */
}

.asset-navigation-tabs :deep(.el-tabs__header) {
  margin-bottom: 0; /* 移除 el-tabs 头部默认的下边距，因为我们用 asset-navigation-tabs 的 margin-bottom */
}
.asset-navigation-tabs :deep(.el-tabs__nav-wrap::after) {
  /* 移除或调整 tabs 底部的默认边框线，如果需要的话 */
   height: 1px; /* 减小默认边框线的高度 */
}


.asset-content-area {
  flex-grow: 1; /* 让子路由内容区域占据剩余空间 */
  overflow-y: auto; /* 如果内容超出，则显示滚动条 */
  /* background-color: #f9fafb; */ /* 可以为内容区域设置背景色，类似图片中的浅灰色块 */
  /* padding: 16px; */ /* 为内容区域添加内边距 */
  /* border-radius: 6px; */
}

/* 移除原先特定于Expectations tab的样式，这些应移至Expectations.vue */
/* .coverage-section, .validate-asset-container, .expectations-table-header, .empty-expectations-message 等 */

/* 过渡动画样式 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>




