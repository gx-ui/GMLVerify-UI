<template>
  <el-form-item label="Match On">
    <template #label>
      <span>Match On</span>
      <el-tooltip content="any：值应匹配列表中的至少一个正则表达式；all：值应匹配列表中的每个正则表达式" placement="top">
        <el-icon class="info-icon"><InfoFilled /></el-icon>
      </el-tooltip>
    </template>
    <el-radio-group
      :model-value="modelValue"
      @update:modelValue="(value) => emit('update:modelValue', value)"
      class="match-on-group"
    >
      <el-radio value="any" size="large">any</el-radio>
      <el-radio value="all" size="large">all</el-radio>
    </el-radio-group>
  </el-form-item>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import { ElFormItem, ElRadioGroup, ElRadio, ElTooltip, ElIcon } from 'element-plus';
import { InfoFilled } from '@element-plus/icons-vue';

const props = defineProps({
  modelValue: {
    type: String,
    default: 'any'
  }
});

const emit = defineEmits(['update:modelValue']);
</script>

<style scoped>
.match-on-group {
  width: 100%;
}

.match-on-group .el-radio {
  margin-right: 30px;
  font-weight: 500;
}

.info-icon {
  margin-left: 5px;
  color: #909399;
  cursor: help;
}
</style>