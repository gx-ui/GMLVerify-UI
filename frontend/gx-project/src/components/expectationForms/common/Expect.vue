<template>
  <el-form-item label="期望类型">
    <el-select
      :model-value="modelValue"
      placeholder="选择期望"
      @update:modelValue="(value) => $emit('update:modelValue', value)"
    >
      <el-option
        v-for="item in options"
        :key="item.type_id"
        :label="item.label"
        :value="item.type_id"
      ></el-option>
    </el-select>
  </el-form-item>
</template>

<script setup>
import { ElFormItem, ElSelect, ElOption } from 'element-plus';

const props = defineProps({
  modelValue: {
    type: [String, Number],
    required: true
  },
  options: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue']);
</script>

<style scoped>
.el-select {
  width: 100%;
}
</style>