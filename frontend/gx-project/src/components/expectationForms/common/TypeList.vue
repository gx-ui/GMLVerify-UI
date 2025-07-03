<template>
  <el-form-item :label="dynamicLabel">
    <div v-for="(item, index) in localList" :key="index" class="type-list-item">
      <el-input v-model="localList[index].value" placeholder="value" @blur="handleInputBlur(index)" />
      <el-button @click="removeItem(index)" :icon="Delete" circle text type="danger" />
    </div>
    <el-button @click="addItem" :icon="Plus" type="primary" plain>添加项</el-button>
  </el-form-item>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits, computed } from 'vue';
import { ElFormItem, ElInput, ElButton } from 'element-plus';
import { Delete, Plus } from '@element-plus/icons-vue';


const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  id: {
    type: [String, Number], 
    default: ''
  }
});

const emit = defineEmits(['update:modelValue']);

const localList = ref(JSON.parse(JSON.stringify(props.modelValue)));

watch(() => props.modelValue, (newValue) => {
  localList.value = JSON.parse(JSON.stringify(newValue));
}, { deep: true });

const dynamicLabel = computed(() => {
  switch (props.id) {
    case 102:
      return 'Type List';
    case 106:
    case 107:
    case 408: 
    case 409: 
    case 510:
      return 'Column List';
    case 607:
    case 612:
      return "Like Pattern List";
    case 609:
    case 614:
      return "Regex List";
    default:
      return 'Type List'; 
  }
});

const addItem = () => {
  localList.value.push({ value: '' });
  emit('update:modelValue', JSON.parse(JSON.stringify(localList.value)));
};

const removeItem = (index) => {
  localList.value.splice(index, 1);
  emit('update:modelValue', JSON.parse(JSON.stringify(localList.value)));
};

const handleInputBlur = (index) => {
  const currentItem = localList.value[index];
  if (currentItem && typeof currentItem.value === 'string') {
    const parentItem = props.modelValue[index];
    const parentValue = parentItem ? parentItem.value : undefined;
    if (currentItem.value !== parentValue) {
        emit('update:modelValue', JSON.parse(JSON.stringify(localList.value)));
    }
  }
};

</script>

<style scoped>
.type-list-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.type-list-item .el-input {
  margin-right: 8px;
}
</style>