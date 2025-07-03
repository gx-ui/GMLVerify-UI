<template>
  <div class="new-data-asset-form-overlay">
    <div class="new-data-asset-form">
      <div class="form-header">
        <h3 v-if="currentStep === 1">创建新的数据集</h3>
        <h3 v-if="currentStep === 2">添加数据资产到 "{{ connectedDataSourceName }}"</h3>
        <h3 v-if="currentStep === 3">配置监控策略</h3>
        <el-button icon="el-icon-close" @click="closeForm" class="close-button" text>X</el-button>
      </div>
      <div class="form-steps">
        <span :class="{ 'active-step': currentStep === 1, 'completed-step': currentStep > 1 }">1 连接数据源 </span> &rarr;
        <span :class="{ 'active-step': currentStep === 2, 'completed-step': currentStep > 2 }">2 添加数据集 </span> &rarr;
        <span :class="{ 'active-step': currentStep === 3 }">3 监控策略 </span>
      </div>

      <!-- 步骤 1: 连接数据源 -->
      <div v-if="currentStep === 1" class="form-content">
        <h4>连接 {{ formattedDataSourceType }} 作为数据源</h4>
        <div class="info-box">
          <p><strong>想要在你自己的环境中连接数据吗？</strong></p>
          <p>默认情况下，GML-GX是通过云连接到你的数据源，将数据读取到云端进行处理。如果您的数据量过大，可能速度回比较慢。若想要更快的体验，可考虑本地部署(请联系GML-GX工作人员:guoxuan@gml.ac.cn)</p>
          <el-button type="primary" plain>Request Agent</el-button>
        </div>
        <el-form :model="form" ref="dataAssetFormRef" label-position="top" :rules="rules">
          <el-form-item label="数据源名称" prop="dataSourceName">
            <el-input v-model="form.dataSourceName" placeholder="例如:tax_data"></el-input>
          </el-form-item>
          <el-form-item label="连接URL" prop="dataBaseURL">
            <el-input v-model="form.dataBaseURL" type="password" show-password
              placeholder="例如:postgresql+psycopg2://postgres:123456@127.0.0.1:5432/postgres"></el-input>
            <small>URL的构成如: &lt数据库类型>://&lt 用户名>:&lt密码>@&ltip地址>:&lt端口号>/&lt数据库名称></small>
          </el-form-item>
          
          <!-- 新增：后端错误信息显示区域 -->
          <div v-if="connectionError" class="connection-error-display">
            {{ connectionError }}
          </div>
        </el-form>
      </div>

      <!-- 步骤 2: 添加数据集 -->
      <div v-if="currentStep === 2" class="form-content step2-content">
        <div class="step2-header">
          <span class="datasource-name">{{ connectedDataSourceName }}</span>
          <span class="datasource-type">{{ formattedDataSourceType }}</span>
        </div>
        <p class="step2-instruction">选择要作为数据资产导入的表</p>

        <el-input v-model="searchTerm" placeholder="搜索表名" clearable class="search-input">
        </el-input>

        <el-checkbox v-model="selectAllTables" @change="handleSelectAllTables" :indeterminate="isIndeterminate"
          class="select-all-checkbox" :disabled="filteredDataAssets.length === 0">
          选择所有 {{ filteredDataAssets.length }} 个匹配的表
        </el-checkbox>

        <div class="tables-list-container">
          <el-checkbox-group v-model="selectedTables" class="tables-checkbox-group">
            <el-checkbox v-for="asset in filteredDataAssets" :key="asset" :label="asset" class="table-checkbox-item">
              {{ asset }}
            </el-checkbox>
          </el-checkbox-group>
          <p v-if="filteredDataAssets.length === 0 && dataAssets.length > 0 && searchTerm" class="no-results">
            未找到匹配 "{{ searchTerm }}" 的表。
          </p>
          <p v-if="dataAssets.length === 0" class="no-results">
            此数据源中没有可用的数据资产。
          </p>
        </div>
      </div>

      <!-- 步骤 3: 监控策略 (占位) -->
      <div v-if="currentStep === 3" class="form-content">
        <h4>配置监控策略</h4>
        <p>为 "{{ connectedDataSourceName }}" 中的已选资产配置监控...</p>
        <p>选中的资产: {{ selectedTables.join(', ') }}</p>
        <!-- 此处添加步骤3的表单和逻辑 -->
      </div>


      <div class="form-footer">
        <el-button @click="handleBack" v-if="currentStep > 1">上一步</el-button>
        <el-button @click="closeForm" v-if="currentStep === 1">回退</el-button>

        <el-button type="primary" @click="connectDataSource" v-if="currentStep === 1">连接</el-button>
        <el-button type="primary" @click="handleAddAssets" v-if="currentStep === 2"
          :disabled="selectedTables.length === 0">添加资产</el-button>
        <el-button type="primary" @click="submitFinalForm" v-if="currentStep === 3">完成</el-button>
      </div>
    </div>
  </div>
</template>

<script setup name="NewDataAsset">

import { ref, computed, watch } from 'vue'; // 修改这里，添加 watch
import axios from 'axios'; // 导入 axios
import { API_URL } from '../config'
import { ElMessage } from 'element-plus';
const props = defineProps({
  dataSourceType: {
    type: String,
    required: true
  }
});

const rules = {
  dataSourceName: [
    { required: true, message: '请为数据源起个名字', trigger: 'blur' }
  ],
  dataBaseURL: [
    { required: true, message: '请输入数据URL', trigger: 'blur' }
  ]
};


const emit = defineEmits(['close', 'connect', 'assetsAdded', 'creationComplete']); // 添加 'creationComplete' 事件

const currentStep = ref(1); // 1: 连接数据源, 2: 添加数据集, 3: 监控策略
const dataAssetFormRef = ref(null);
const form = ref({ // Step 1 form
  dataSourceName: '',
  dataBaseURL: ''
});

const connectionError = ref(''); // 新增：用于存储连接错误信息

// --- 新增用于第二步的状态 ---
const connectedDataSourceName = ref(''); // 存储连接成功的数据源名称
const dataAssets = ref([]); // 存储从后端获取的数据资产列表 (例如表名)
const selectedTables = ref([]); // 存储用户在第二步选择的表
const searchTerm = ref(''); // 用于第二步的搜索功能
const selectAllTables = ref(false); // 第二步全选状态
const dataSourceId = ref(null); // 将在最终提交时填充
// --- 结束新增状态 ---

const formattedDataSourceType = computed(() => {
  if (!props.dataSourceType) return '';
  if (props.dataSourceType.toLowerCase() === 'csv') return 'CSV File';
  if (props.dataSourceType.toLowerCase() === 'spark') return 'Spark Streaming Data';
  return props.dataSourceType.charAt(0).toUpperCase() + props.dataSourceType.slice(1);
});

const closeForm = () => {
  emit('close');
  currentStep.value = 1;
  form.value.dataSourceName = '';
  form.value.dataBaseURL = '';
  dataAssets.value = [];
  selectedTables.value = [];
  connectedDataSourceName.value = '';
  searchTerm.value = '';
  dataSourceId.value = null; // 重置dataSourceId
  connectionError.value = ''; // 重置连接错误信息
};

const connectDataSource = () => {
  if (!dataAssetFormRef.value) return;
  connectionError.value = ''; // 每次尝试连接时，先清除旧的错误信息
  dataAssetFormRef.value.validate(async (valid) => {
    if (valid) {
      const userid = localStorage.getItem('userid');
      if (!userid) {
        ElMessage.error('用户未登录或会话已过期，请重新登录。');
        return;
      }
      try {
        const isexist = await axios.get(`${API_URL}/pg/${userid}/dataSource/${form.value.dataSourceName}`);
        if (isexist.data.dataSourceId) {
          connectionError.value = '已拥有相同的数据源，请使用其它名称。';
        } else {
          const responseTable = await axios.post(
            `${API_URL}/pg/tables`,
            { name: form.value.dataSourceName, url: form.value.dataBaseURL } );
          if ( responseTable.data.code === 200) {
            ElMessage.success('数据源连接成功，已获取表列表！');
            connectedDataSourceName.value = form.value.dataSourceName;
            dataAssets.value = responseTable.data.tablesName || [];
            currentStep.value = 2;
            connectionError.value = ''; 
          } else {
            connectionError.value = responseTable.data.message || '获取表列表失败或连接无效,请检查连接URL和凭据。';
          }
        }
      } catch (error) {
        console.error('请求数据源连接/获取表API失败:', error);
        let errMsg = '连接失败，请检查网络或联系管理员。';
        if (error.response && error.response.data && error.response.data.message) {
          errMsg = error.response.data.message;
        } else if (error.message) {
          // 捕获非HTTP错误，例如网络问题直接导致的错误
          errMsg = error.message;
        }
        ElMessage.error(errMsg);
        connectionError.value = errMsg;
      }
    } else {
      connectionError.value = '请填写所有必填项。'; 
    }
  });
};

// --- 第二步---
const filteredDataAssets = computed(() => {
  if (!searchTerm.value) {
    return dataAssets.value;
  }
  return dataAssets.value.filter(asset =>
    asset.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});

const isIndeterminate = computed(() => {
  return selectedTables.value.length > 0 && selectedTables.value.length < filteredDataAssets.value.length;
});


// 提交选中的表
const handleSelectAllTables = (value) => {
  if (value) {
    selectedTables.value = filteredDataAssets.value.slice();
    console.log("选择的数据资产是", selectedTables.value); // 注意: 'print' 不是标准JS函数
  }
  else {
    selectedTables.value = [];
  }
};

watch([selectedTables, filteredDataAssets], () => {
  if (filteredDataAssets.value.length === 0) {
    selectAllTables.value = false;
  } else {
    selectAllTables.value = selectedTables.value.length === filteredDataAssets.value.length && filteredDataAssets.value.length > 0;
  }
}, { deep: true });

const handleAddAssets = async () => {
  if (selectedTables.value.length === 0) {
    ElMessage.warning('请至少选择一个数据资产。');
    return;
  }

  // 仅记录选择并进入下一步，不在此处提交API
  emit('assetsAdded', {
    dataSourceName: connectedDataSourceName.value, // 这应该是 form.value.dataSourceName
    assets: selectedTables.value
  });

  console.log("数据资产已选择，准备进入监控策略步骤。");
  currentStep.value = 3;
};

const submitFinalForm = async () => {
  const userid = localStorage.getItem('userid');
  if (!userid) {
    ElMessage.error('用户未登录或会话已过期，请重新登录。');
    return;
  }
  if (selectedTables.value.length === 0 && currentStep.value > 1) { // 确保从第二步过来时有选中的表
    ElMessage.warning('请至少选择一个数据资产才能完成创建。');
    currentStep.value = 2; // 可以选择让用户返回第二步
    return;
  }

  try {
    const responseCreateDataSource = await axios.post(
      `${API_URL}/pg/${userid}/dataSource`,
      { name: form.value.dataSourceName, url: form.value.dataBaseURL }
    );
    if (responseCreateDataSource.data.code === 200) {
      dataSourceId.value = responseCreateDataSource.data.dataSourceId;
      if (selectedTables.value.length > 0) {
        const responseAddDataAsset = await axios.post(
          `${API_URL}/pg/${dataSourceId.value}/dataAsset`,
          selectedTables.value
        );
        if (responseAddDataAsset.data.code === 200) {
          ElMessage.success('数据资产添加成功！');
          window.location.reload();
        } else {
          ElMessage.error(responseAddDataAsset.data.message || '添加数据资产失败。');
          return;
        }
      }
      emit('creationComplete', {
        dataSourceId: dataSourceId.value,
        dataSourceName: form.value.dataSourceName,
        addedAssets: selectedTables.value
      });
      closeForm(); // 关闭表单
    } else {
      ElMessage.error(responseCreateDataSource.data.message || '创建数据源失败。');
    }
  } catch (error) {
    console.error('提交最终表单时发生错误:', error);
    if (error.response) {
      ElMessage.error(`操作失败: ${error.response.data.message || '服务器处理请求出错'}`);
    } else if (error.request) {
      ElMessage.error('无法连接到服务器，请检查网络或联系管理员。');
    } else {
      ElMessage.error('发起请求时发生内部错误。');
    }
  }
};

const handleBack = () => {
  if (currentStep.value === 2) {
    currentStep.value = 1;
    // 重置第二步的状态
    selectedTables.value = [];
    searchTerm.value = '';
    selectAllTables.value = false;
    // dataAssets.value 和 connectedDataSourceName.value 保留，因为它们来自上一步的成功连接
  } else if (currentStep.value === 3) {
    currentStep.value = 2;
    // 重置第三步的状态 (如果适用)
  }
};
</script>







































<style scoped>
.new-data-asset-form-overlay {
  position: fixed;
  /* 改为 fixed 以覆盖整个视口 */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: flex-end;
  z-index: 1001;
}

.new-data-asset-form {
  width: 500px;
  height: 100%;
  background-color: white;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-sizing: border-box;
  animation: slideInFromRight 0.3s ease-out;
}

@keyframes slideInFromRight {
  from {
    transform: translateX(100%);
  }

  to {
    transform: translateX(0);
  }
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.form-header h3 {
  margin: 0;
  font-size: 18px;
}

.close-button {
  font-size: 20px;
  /* 调整关闭按钮大小 */
  padding: 5px;
  /* 增加点击区域 */
  line-height: 1;
  /* 确保图标垂直居中 */
}

.form-steps {
  margin-bottom: 20px;
  font-size: 12px;
  color: #666;
}

.form-content {
  flex-grow: 1;
  overflow-y: auto;
}

.form-content h4 {
  font-size: 16px;
  margin-top: 0;
  margin-bottom: 15px;
}

.info-box {
  background-color: #eef6ff;
  border: 1px solid #d1e3ff;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
  font-size: 13px;
}

.info-box p {
  margin: 5px 0;
}

.el-form-item small {
  font-size: 12px;
  color: #999;
  display: block;
  margin-top: 5px;
}

.form-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid #eee;
  margin-top: auto;
}

.form-footer .el-button {
  margin-left: 10px;
}

/* 步骤指示器样式 */
.form-steps span {
  color: #909399;
  /* 默认颜色 */
}

.form-steps .active-step {
  color: #409EFF;
  /* 当前步骤颜色 */
  font-weight: bold;
}

.form-steps .completed-step {
  color: #67C23A;
  /* 已完成步骤颜色 */
}

/* 第二步特定样式 */
.step2-content {
  display: flex;
  flex-direction: column;
}

.step2-header {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.step2-header .datasource-name {
  font-weight: bold;
  font-size: 16px;
  margin-right: 8px;
}

.step2-header .datasource-type {
  font-size: 14px;
  color: #606266;
  background-color: #f0f2f5;
  padding: 2px 6px;
  border-radius: 4px;
}

.step2-instruction {
  font-size: 14px;
  color: #303133;
  margin-bottom: 15px;
}

.search-input {
  margin-bottom: 15px;
}

.select-all-checkbox {
  margin-bottom: 10px;
  display: block;
  /* 让它占据一行 */
}

.tables-list-container {
  flex-grow: 1;
  overflow-y: auto;
  /* 如果列表很长，允许滚动 */
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 10px;
}

.tables-checkbox-group {
  display: flex;
  flex-direction: column;
}

.table-checkbox-item {
  margin-bottom: 8px;
  /* 复选框之间的间距 */
  display: block;
  /* 确保每个复选框占一行 */
}

.table-checkbox-item:last-child {
  margin-bottom: 0;
}

.no-results {
  color: #909399;
  text-align: center;
  padding: 20px;
}

/* 新增：后端错误信息显示区域样式 */
.connection-error-display {
  border: 1px solid #f56c6c; /* 红色边框 */
  color: #f56c6c; /* 红色文本 */
  background-color: #fef0f0; /* 浅红色背景 */
  padding: 10px 15px;
  margin-top: 10px; /* 与上方元素的间距 */
  border-radius: 4px;
  font-size: 13px;
  line-height: 1.5;
  word-break: break-all; /* 长消息自动换行 */
}
</style>