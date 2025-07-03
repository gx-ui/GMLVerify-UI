<template>
  <el-form-item label="Mostly">
    <template #label>
      <span>Mostly</span>
      <el-tooltip content="期望在多大比例上成立" placement="top">
        <el-icon class="info-icon"><InfoFilled /></el-icon>
      </el-tooltip>
    </template>
    <div class="mostly-container">
      <el-slider
        :model-value="modelValue"
        @update:modelValue="(value) => emit('update:modelValue', value)"
        :min="0"
        :max="100"
        show-input
        :input-size="'small'"
        class="mostly-slider"
      />
      <span class="percentage-sign">%</span>
    </div>
  </el-form-item>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import { ElFormItem, ElSlider, ElTooltip, ElIcon } from 'element-plus';
import { InfoFilled } from '@element-plus/icons-vue';

const props = defineProps({
  modelValue: {
    type: Number,
    default: 100
  }
});

const emit = defineEmits(['update:modelValue']);

</script>

<style scoped>
.mostly-container {
  display: flex;
  align-items: center;
  width: 100%;
}

.mostly-slider {
  flex-grow: 1;
  margin-right: 15px; /* 给百分号留出空间 */
  margin-left: 15px;
}

.info-icon {
  margin-left: 4px;
  color: #909399;
}

.percentage-sign {
  font-size: 14px;
  color: #606266;
}

/* 调整 el-slider 内部 input 的宽度 */
:deep(.el-slider__input.el-input-number--small) {
  width: 100px; /* 根据需要调整宽度 */
}
</style>