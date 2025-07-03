<template>
  <div class="data-assets-section">
    <div class="section-header">
      <h2>{{ title }}</h2>
      <div class="section-stats">
        <span>{{ dataSourceCount }} 数据源</span>
        <span class="divider"></span>
        <span>{{ dataAssetCount }} 数据资产</span>
      </div>
    </div>

    <div class="connection-section">
      <h3>连接到数据源以开始</h3>
      <div class="data-sources">
        <div class="data-source-card" @click="connectToSource('postgresql')">
          <img src="../assets/pgsql_logo.svg" alt="PostgreSQL" class="data-source-icon"/>
          <span>PostgreSQL</span>
        </div>
        <div class="data-source-card" @click="connectToSource('csv')">
          <img src="../assets/csv_logo.svg" alt="csv文件" class="data-source-icon"/>
          <span>csv文件</span>
        </div>
        <div class="data-source-card" @click="connectToSource('spark')">
          <img src="../assets/spark_Logo.svg" alt="spark流式数据" class="data-source-icon"/>
          <span>spark流式数据</span>
        </div>
      </div>
    </div>

    <div class="not-ready-section">
      <h3>还没准备好连接到您的数据？</h3>
      <div class="demo-options">
        <div class="demo-option" @click="useDemo">
          <el-icon><Service /></el-icon>
          <span>使用演示数据</span>
        </div>
        <div class="demo-option" @click="requestDemoFromContent">
          <el-icon><Service /></el-icon>
          <span>请求演示</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue';
import { 
  Service
} from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

const props = defineProps({
  title: {
    type: String,
    default: '数据资产'
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

const emit = defineEmits(['connect-to-source', 'use-demo', 'request-demo']);

const connectToSource = (source) => {
  emit('connect-to-source', source);
};

const useDemo = () => {
  emit('use-demo');
};

const requestDemoFromContent = () => {
  ElMessage({
    message: '(From Dynamic Content) 已发送演示请求',
    type: 'success'
  });
  emit('request-demo');
};
</script>

<style scoped>
.data-assets-section {
  background-color: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.section-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.section-stats {
  margin-left: 20px;
  font-size: 14px;
  color: #909399;
  display: flex;
  align-items: center;
}

.divider {
  height: 12px;
  width: 1px;
  background-color: #dcdfe6;
  margin: 0 10px;
}

.connection-section {
  margin-bottom: 30px;
  padding: 20px 0;
  text-align: center;
}

.connection-section h3 {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 24px;
}

.data-sources {
  display: flex;
  justify-content: center;
  gap: 24px;
  flex-wrap: wrap;
}

.data-source-card {
  width: 180px;
  height: 120px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.data-source-card:hover {
  border-color: #409eff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.data-source-card img.data-source-icon {
  width: 35px;
  height: 35px;
  margin-bottom: 10px;
}

.not-ready-section {
  margin-top: 40px;
  padding: 20px 0;
  text-align: center;
}

.not-ready-section h3 {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 24px;
}

.demo-options {
  display: flex;
  justify-content: center;
  gap: 24px;
}

.demo-option {
  width: 180px;
  height: 80px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  gap: 10px;
}

.demo-option:hover {
  border-color: #409eff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.demo-option .el-icon {
  font-size: 24px;
  color: #409eff;
}
</style>