<template>
  <div class="app-layout">
    <LeftSidebar 
      :username="username" 
      v-model:isSidebarCollapsed="isSidebarCollapsed" 
    />

    <div class="main-content" :class="{ 'content-shifted': !isSidebarCollapsed }">
      <div class="header">
        <HeaderBar 
          :validated-count="0"
          :total-count="dynamicDataAssetCount"
        />
      </div>
      <div class="container">
        <router-view
          class="content-view-fill" 
          :title="dynamicTitle"
          :dataSourceCount="dynamicDataSourceCount"
          :dataAssetCount="dynamicDataAssetCount"
          :dataSources="userPDataSources"
          @connect-to-source="handleConnectToSource"
          @use-demo="useDemo"
          @request-demo="requestDemo"
          @manage-data-sources="handleManageDataSources"
          @new-data-asset="handleNewDataAsset" />
      </div>
    </div>
    <NewDataAssetForm
      v-if="showDataAssetForm"
      :dataSourceType="selectedDataSourceType"
      @close="handleCloseDataAssetForm"
      @connect="handleCreateDataAsset" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import LeftSidebar from '@/components/LeftSidebar.vue'
import HeaderBar from '@/components/HeaderBar.vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { API_URL } from '../config'
import NewDataAssetForm from '@/components/NewDataAsset.vue'  // 添加这行导入语句

const router = useRouter()
const isSidebarCollapsed = ref(false)

// Props for views
const dynamicTitle = ref('动态数据资产')
const dynamicDataSourceCount = ref(0)
const dynamicDataAssetCount = ref(0)

// Controls for NewDataAssetForm
const showDataAssetForm = ref(false)
const selectedDataSourceType = ref('')

const username = ref('')
const userPDataSources = ref([])

onMounted(async () => {
  username.value = localStorage.getItem('username') || '';
  const userId = localStorage.getItem('userid');
  if (username.value && userId) {
    try {
      const response = await axios.get(`${API_URL}/pg/${userId}/dataSourceAndAsset`);
      const responseData = response.data;
      dynamicDataSourceCount.value = responseData.totalDataSourceCount;
      dynamicDataAssetCount.value = responseData.totalDataAssetCount;
      userPDataSources.value = responseData.dataSource;
      responseData.totalDataSourceCount > 0? router.replace({name:"existing-assets"}): router.replace({name:"creat-assets"})
    } catch (error) {
      ElMessage.error('获取数据源和资产信息失败: ' + (error.response?.data?.message || error.message));
      dynamicDataSourceCount.value = 0;
      dynamicDataAssetCount.value = 0;
      userPDataSources.value = [];
      router.push('/login')
    }
  } 
});

const handleConnectToSource = (source) => {
  selectedDataSourceType.value = source
  showDataAssetForm.value = true
}

const useDemo = () => {
  ElMessage({
    message: '正在加载演示数据...',
    type: 'info'
  })
}

const requestDemo = () => {
  ElMessage({
    message: '已发送演示请求',
    type: 'success'
  })
}

const handleCloseDataAssetForm = () => {
  showDataAssetForm.value = false
  selectedDataSourceType.value = ''
}

const handleCreateDataAsset = async (formData) => {
  handleCloseDataAssetForm();
  const userId = localStorage.getItem('userid');
  if (userId) {
    try {
      const response = await axios.get(`${API_URL}/pg/${userId}/dataSourceAndAsset`);
      const responseData = response.data;
      if (responseData && typeof responseData.totalDataSourceCount === 'number' && typeof responseData.totalDataAssetCount === 'number' && Array.isArray(responseData.dataSource)) {
        dynamicDataSourceCount.value = responseData.totalDataSourceCount;
        dynamicDataAssetCount.value = responseData.totalDataAssetCount;
        userPDataSources.value = responseData.dataSource;

        if (responseData.dataSource.length > 0) {
          router.push('/existing-assets')
        } else {
          router.push('/')
        }
      } else {
        dynamicDataSourceCount.value = 0;
        dynamicDataAssetCount.value = 0;
        userPDataSources.value = [];
        router.push('/')
      }
    } catch (error) {
      ElMessage.error('刷新数据源和资产信息失败: ' + (error.response?.data?.message || error.message));
      dynamicDataSourceCount.value = 0;
      dynamicDataAssetCount.value = 0;
      userPDataSources.value = [];
      router.push('/')
    }
  }
};

const handleManageDataSources = () => {
  console.log('管理数据源被点击');
}

const handleNewDataAsset = () => {
  console.log('新建数据资产被点击');
  router.push('/')
}
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  width: 100%;
  position: relative;
}

.main-content {
  flex: 1; 
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background-color: #f0f2f5;
  position: relative;
  padding-top: 60px;
  transition: margin-left 0.3s ease;
}

/* 当侧边栏展开时，header 的 left 值 */
.sidebar:not(.sidebar-collapsed)~.main-content .header {
  left: 250px;
}

/* 当侧边栏折叠时，header 的 left 值 */
.sidebar.sidebar-collapsed~.main-content .header {
  left: 60px;
}

.container {
  flex-grow: 1; 
  display: flex; 
  flex-direction: column; 
  padding: 0 0;
  max-width: 100%; 
  margin: 0 0; 
}

.content-view-fill {
  flex-grow: 1;
  display: flex; 
  flex-direction: column; 
  width: 100%;
  margin-left: 0;
  margin-right: 0;
  box-sizing: border-box;
}
</style>
