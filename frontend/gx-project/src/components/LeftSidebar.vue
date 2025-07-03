<template>
  <div class="sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
    <div class="logo-section">
      <img src="../assets/logo.png" alt="User logo" class="avatar">
      <span class="username" v-show="!isSidebarCollapsed">{{ username }}</span>
    </div>
    <el-menu default-active="1" class="el-menu-vertical-custom" :collapse="isSidebarCollapsed" :collapse-transition="false">
      <el-menu-item index="1">
        <el-icon><Coin /></el-icon>
        <template #title><span>Data Assets</span></template>
      </el-menu-item>
      <el-menu-item index="2">
        <el-icon><Odometer /></el-icon>
        <template #title><span>Logs</span></template>
      </el-menu-item>

      <el-sub-menu index="3" >
        <template #title>
          <el-icon><Setting /></el-icon>
          <span>Settings</span>
        </template>
        <el-menu-item index="3-1">
          <el-icon><User /></el-icon>
          <template #title><span>Users</span></template>
        </el-menu-item>
        <el-menu-item index="3-2">
          <el-icon><Key /></el-icon>
          <template #title><span>Tokens</span></template>
        </el-menu-item>
      </el-sub-menu>
    </el-menu>

    <div class="sidebar-bottom">
      <div class="sidebar-item-group" v-show="!isSidebarCollapsed">
        <div class="sidebar-item">Request a demo</div>
        <div class="sidebar-item">Documentation</div>
        <div class="sidebar-item">Support</div>
      </div>
      <div class="toggle-button-wrapper">
        <div class="sidebar-item toggle-button" @click="toggleSidebar">
          <el-icon v-if="!isSidebarCollapsed"><ArrowLeftBold /></el-icon>
          <el-icon v-else><ArrowRightBold /></el-icon>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import {
  Coin,
  Odometer,
  User,
  Key,
  Setting,
  ArrowLeftBold,
  ArrowRightBold
} from '@element-plus/icons-vue';

const props = defineProps({
  username: {
    type: String,
    default: ''
  },
  isSidebarCollapsed: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:isSidebarCollapsed']);

const toggleSidebar = () => {
  emit('update:isSidebarCollapsed', !props.isSidebarCollapsed);
};
</script>

<style scoped>


.sidebar {
  width: 230px;
  background: linear-gradient(180deg, #497bc7 0%, #a1b6dc 50%, #4692ea 100%);
  color: #f8fafc;
  display: flex;
  flex-direction: column;
  height: 100vh;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  pointer-events: none;
}

.sidebar-collapsed {
  width: 64px;
}

.logo-section {
  display: flex;
  align-items: center;
  padding: 24px 20px;
  margin-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 1;
}

.sidebar-collapsed .logo-section {
  padding: 24px 0;
  justify-content: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
  object-fit: cover;
  border: 3px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease;
}

.avatar:hover {
  transform: scale(1.05);
}

.sidebar-collapsed .avatar {
  margin-right: 0;
}

.username {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.el-menu-vertical-custom {
  border-right: none;
  background-color: transparent !important;
  flex-grow: 1;
  position: relative;
  z-index: 1;
}

.el-menu-vertical-custom:not(.el-menu--collapse) {
  width: 100%;
}

.el-menu-item, 
.el-sub-menu__title {
  color: #e2e8f0 !important;
  height: 52px;
  line-height: 52px;
  padding-left: 20px !important;
  margin: 4px 12px;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.el-menu-item::before,
.el-sub-menu__title::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.el-menu-item .el-icon,
.el-sub-menu__title .el-icon {
  margin-right: 12px;
  font-size: 20px;
  color: #cbd5e1;
  transition: color 0.3s ease;
}

.el-menu-item:hover,
.el-sub-menu__title:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08)) !important;
  color: #ffffff !important;
  transform: translateX(4px);
}

.el-menu-item:hover::before,
.el-sub-menu__title:hover::before {
  opacity: 1;
}

.el-menu-item:hover .el-icon,
.el-sub-menu__title:hover .el-icon {
  color: #ffffff;
}

.el-menu-item.is-active {
  background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
  color: #ffffff !important;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  transform: translateX(4px);
}

.el-menu-item.is-active .el-icon {
  color: #ffffff;
}

.el-menu-item.is-active::after {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 24px;
  background: #ffffff;
  border-radius: 0 2px 2px 0;
}
/* 使用CSS变量覆盖Element Plus菜单样式，实现背景统一 */
.sidebar {
  --el-menu-bg-color: #6b93d0;
  --el-menu-item-bg-color: transparent;
  --el-menu-item-hover-bg-color: #6b93d0;
  --el-menu-item-active-bg-color: #6b93d0;
  --el-sub-menu-bg-color: #6b93d0;
}

/* 强制覆盖Element Plus子菜单的默认样式 */
.el-menu--inline {
  background: rgba(30, 58, 138, 0.3) !important;
  border-radius: 8px;
  margin: 4px 12px;
  padding: 8px 0;
  backdrop-filter: blur(10px);
}

/* 更具体的选择器来覆盖Element Plus默认样式 */
.el-menu.el-menu--inline {
  background-color: rgba(30, 58, 138, 0.3) !important;
  background: rgba(30, 58, 138, 0.3) !important;
}

/* 确保子菜单容器背景统一 */
.el-sub-menu .el-menu {
  background: rgba(30, 58, 138, 0.3) !important;
  background-color: rgba(30, 58, 138, 0.3) !important;
}

/* 子菜单项样式 */
.el-menu--inline .el-menu-item {
  background-color: transparent !important;
  background: transparent !important;
  padding-left: 48px !important;
  margin: 2px 8px;
  height: 44px;
  line-height: 44px;
  color: #e2e8f0 !important;
}

.el-menu--inline .el-menu-item:hover {
  background: rgba(255, 255, 255, 0.15) !important;
  background-color: rgba(255, 255, 255, 0.15) !important;
  transform: translateX(2px);
  color: #ffffff !important;
}

.el-menu--inline .el-menu-item.is-active {
  background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
  background-color: #3b82f6 !important;
  color: #ffffff !important;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

/* 确保子菜单图标颜色一致 */
.el-menu--inline .el-menu-item .el-icon {
  color: #cbd5e1 !important;
}

.el-menu--inline .el-menu-item:hover .el-icon {
  color: #ffffff !important;
}

.el-menu--inline .el-menu-item.is-active .el-icon {
  color: #ffffff !important;
}

.sidebar-collapsed .el-menu-item,
.sidebar-collapsed .el-sub-menu__title {
  justify-content: center;
  padding-left: 0 !important;
  margin: 4px 8px;
}

.sidebar-collapsed .el-menu-item .el-icon,
.sidebar-collapsed .el-sub-menu__title .el-icon {
  margin-right: 0 !important;
  margin-left: 0 !important;
}

.sidebar-collapsed .el-sub-menu .el-menu-item {
  padding-left: 0 !important;
  justify-content: center;
}

.sidebar-collapsed .el-sub-menu .el-menu-item .el-icon {
  margin-right: 0 !important;
  margin-left: 0 !important;
}

.sidebar-bottom {
  margin-top: auto;
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 1;
}

.sidebar-item-group {
  margin-bottom: 16px;
}

.sidebar-item {
  padding: 10px 0;
  cursor: pointer;
  font-size: 14px;
  color: #cbd5e1;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  border-radius: 8px;
  padding-left: 8px;
  padding-right: 8px;
}

.sidebar-item:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(2px);
}

.toggle-button-wrapper {
  display: flex;
  justify-content: flex-end;
}

.sidebar-collapsed .toggle-button-wrapper {
  justify-content: center;
}

.toggle-button {
  cursor: pointer;
  padding: 12px;
  border-radius: 50%;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.toggle-button .el-icon {
  font-size: 18px;
  color: #e2e8f0;
}

.toggle-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.toggle-button:hover .el-icon {
  color: #ffffff;
}
</style>