<template>
  <div class="header">
    <div class="notification">
      <el-alert type="info" :closable="false" show-icon>
        <div class="notification-content">
          <span>您已验证{{ validatedCount }}个（共{{ totalCount }}个）数据资产。此计划将于20xx年x月x日重置。</span>
          <el-button type="primary" link>升级获取更多覆盖范围</el-button>
        </div>
      </el-alert>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  validatedCount: {
    type: Number,
    default: 0
  },
  totalCount: {
    type: Number,
    default: 0
  }
});
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 1000;
  background-color: #ffffff;
  padding: 0 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  transition: left 0.3s ease;
  height: 60px;
  left: 10px;
  margin-left: 10px;
  display: flex;
  align-items: center;
}

.notification {
  width: 100%;
}

.notification-content {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>