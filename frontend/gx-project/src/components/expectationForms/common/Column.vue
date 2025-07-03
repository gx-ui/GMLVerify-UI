<template>
  <el-form-item label="列" prop="column">
    <el-select
      :model-value="modelValue"
      placeholder="选择一个列"
      @update:modelValue="(value) => $emit('update:modelValue', value)"
    >
      <el-option
        v-for="col in columns"
        :key="col"
        :label="col"
        :value="col"
      ></el-option>
    </el-select>
  </el-form-item>
</template>

<script setup>
import { ElFormItem, ElSelect, ElOption } from 'element-plus';

const props = defineProps({
  modelValue: {
    type: [String, Number, null],
    required: true
  },
  columns: {
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