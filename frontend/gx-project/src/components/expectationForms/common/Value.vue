<template>
  <el-form-item :label="dynamicLabel" required prop="value">
    <template #label>
      <span>{{ dynamicLabel }}</span>
      <el-tooltip content="请输入正则表达式" placement="top">
        <el-icon class="info-icon"><InfoFilled /></el-icon>
      </el-tooltip>
    </template>
    <el-input
      v-model="inputValue"
      placeholder="请输入值"
      @blur="handleBlur"
    ></el-input>
  </el-form-item>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { ElFormItem, ElInput, ElIcon, ElTooltip } from 'element-plus';
import { InfoFilled } from '@element-plus/icons-vue';

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  id: {
    type: [String, Number], 
    default: ''
  }
});

const emit = defineEmits(['update:modelValue', 'blur']);

const inputValue = ref(props.modelValue);

const dynamicLabel = computed(() => {
  switch (props.id) {
    case 606:
    case 611:
      return 'Like_Pattern';
    case 608:
    case 613:
      return 'Regex';  
    default:
      return 'Value';
  }
});


watch(() => props.id, (newId) => {
  if (newId === 608 && (!inputValue.value || inputValue.value === '')) {
    inputValue.value = '(?s).*';
    emit('update:modelValue', inputValue.value);
  }
}, { immediate: true });

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
.el-form-item {
  width: 100%; 
}
.el-input {
  width: 100%;
}
</style>