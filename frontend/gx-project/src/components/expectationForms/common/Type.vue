<template>

  <el-form-item label="类型" required prop="columnType">
    <template #label>
      <span>类型</span>
      <el-tooltip content="期望的数据类型，可自定义" placement="top"> 
        <el-icon class="info-icon"><InfoFilled /></el-icon>
      </el-tooltip>
    </template>
    <el-input  
      v-model="inputValue" 
      placeholder="输入期望的类型" 
      @blur="handleBlur"
    ></el-input>
  </el-form-item>

</template>

<script setup>
import { ref, watch } from 'vue';
import { ElFormItem, ElInput, ElIcon, ElTooltip } from 'element-plus';
import { InfoFilled } from '@element-plus/icons-vue';

const props = defineProps({
  modelValue: { 
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue', 'blur']); 

const inputValue = ref(props.modelValue);

watch(() => props.modelValue, (newValue) => {
  inputValue.value = newValue;
});

const handleBlur = (event) => {
  if (inputValue.value !== props.modelValue) {
    emit('update:modelValue', inputValue.value);
  }
  emit('blur', event); 
};
</script>

<style scoped>
.info-icon {
  margin-left: 4px;
  cursor: pointer;
}

</style>