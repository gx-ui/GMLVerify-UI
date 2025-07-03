<template>
  <div class="value-set-container">
    <div class="value-set-header">
      <span class="required-mark">*</span>
      <span class="value-set-label">Value Set</span>
      <el-tooltip content="指定一组期望值" placement="top">
        <el-icon class="info-icon"><QuestionFilled /></el-icon>
      </el-tooltip>
    </div>
    
    <div class="type-selector">
      <el-button-group>
        <el-button 
          :type="selectedType === 'text' ? 'primary' : ''" 
          @click="selectedType = 'text'"
          class="type-button"
        >Text</el-button>
        <el-button 
          :type="selectedType === 'numbers' ? 'primary' : ''" 
          @click="selectedType = 'numbers'"
          class="type-button"
        >Numbers</el-button>
      </el-button-group>
    </div>

    <div class="type-label">{{ selectedType === 'text' ? 'Text' : 'Numbers' }}</div>
    <div v-if="selectedType === 'text'" class="values-editor">
      <div v-for="(value, index) in values" :key="index" class="value-item">
        <div class="move-buttons">
          <el-button 
            @click="moveItemUp(index)" 
            :disabled="index === 0"
            class="move-button"
          >
            <el-icon><ArrowUp /></el-icon>
          </el-button>
          <el-button 
            @click="moveItemDown(index)" 
            :disabled="index === values.length - 1"
            class="move-button"
          >
            <el-icon><ArrowDown /></el-icon>
          </el-button>
        </div>
        <el-input v-model="values[index]" placeholder="value" @input="emitUpdate" type="text" />
        <el-button @click="removeItem(index)" class="delete-button">
          <el-icon><Delete /></el-icon>
        </el-button>
      </div>
      <el-button @click="addItem" class="add-button">
        <el-icon><Plus /></el-icon> Add value
      </el-button>
    </div>

    <div v-if="selectedType === 'numbers'" class="values-editor">
      <div v-for="(value, index) in values" :key="index" class="value-item">
        <div class="move-buttons">
          <el-button 
            @click="moveItemUp(index)" 
            :disabled="index === 0"
            class="move-button"
          >
            <el-icon><ArrowUp /></el-icon>
          </el-button>
          <el-button 
            @click="moveItemDown(index)" 
            :disabled="index === values.length - 1"
            class="move-button"
          >
            <el-icon><ArrowDown /></el-icon>
          </el-button>
        </div>
    
        
        <el-input v-model="values[index]" placeholder="value" @input="emitUpdate" type="number" />
        <el-button @click="removeItem(index)" class="delete-button">
          <el-icon><Delete /></el-icon>
        </el-button>
      </div>
      <el-button @click="addItem" class="add-button">
        <el-icon><Plus /></el-icon> Add value
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { ElButton, ElButtonGroup, ElInput, ElIcon, ElTooltip } from 'element-plus';
import { Delete, Plus, QuestionFilled, ArrowUp, ArrowDown } from '@element-plus/icons-vue';

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({ type: 'text', values: [''] })
  }
});

const emit = defineEmits(['update:modelValue']);

const selectedType = ref('text');
const values = ref( ['']);

watch(() => props.modelValue, (newValue) => {
  if (newValue) { 

    if (typeof newValue === 'object' && !Array.isArray(newValue) && typeof newValue.type === 'string') {
      selectedType.value = newValue.type;
    } else {
      selectedType.value = 'text'; // Default if type is missing, not a string, or newValue is not a suitable object
    }

    if (typeof newValue === 'object' && !Array.isArray(newValue) && newValue.hasOwnProperty('values')) {
      if (Array.isArray(newValue.values)) {
        values.value = [...newValue.values]; 
      } else {

        values.value = ['']; 
        console.warn(`ValueSet: modelValue.values was expected to be an array, but received ${typeof newValue.values}. Resetting values.`);
      }
    } else {

      values.value = ['']; 
    }
  } else {
    selectedType.value = 'text';
    values.value = [''];
  }
}, { deep: true });

watch(selectedType, (newType) => {
  if (newType !== props.modelValue.type) {
    // 当类型改变时，重置值数组
    values.value = [''];
    emitUpdate();
  }
});

const emitUpdate = () => {
  let processedValues = values.value;
  if (selectedType.value === 'numbers') {
    processedValues = values.value.map(val => {
      const num = parseFloat(val);
      return isNaN(num) ? val : num; // 如果不是有效数字，则保留原值或根据需求处理
    });
  }
  emit('update:modelValue', {
    type: selectedType.value,
    values: processedValues
  });
};

const addItem = () => {
  values.value.push('');
  emitUpdate();
};

const removeItem = (index) => {
  values.value.splice(index, 1);
  if (values.value.length === 0) {
    values.value.push('');
  }
  emitUpdate();
};

const moveItemUp = (index) => {
  if (index > 0) {
    const temp = values.value[index];
    values.value[index] = values.value[index - 1];
    values.value[index - 1] = temp;
    emitUpdate();
  }
};

const moveItemDown = (index) => {
  if (index < values.value.length - 1) {
    const temp = values.value[index];
    values.value[index] = values.value[index + 1];
    values.value[index + 1] = temp;
    emitUpdate();
  }
};
</script>

<style scoped>
.value-set-container {
  width: 60%;
  margin-bottom: 20px;
}

.value-set-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.required-mark {
  color: #f56c6c;
  margin-right: 4px;
}

.value-set-label {
  font-size: 14px;
  font-weight: 500;
}

.info-icon {
  margin-left: 4px;
  color: #909399;
  cursor: pointer;
}

.type-selector {
  margin-bottom: 10px;
}

.type-button {
  border-radius: 0;
  padding: 8px 16px;
}

.type-button:first-child {
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
}

.type-button:last-child {
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
}

.type-label {
  font-size: 14px;
  margin-bottom: 10px;
}

.values-editor {
  width: 100%;
}

.value-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  width: 100%;
}

.move-buttons {
  display: flex;
  flex-direction: column;
  margin-right: 8px;
}

.move-button {
  padding: 2px;
  height: 20px;
  width: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #606266;
  background-color: transparent;
  border: none;
}

.move-button:disabled {
  color: #c0c4cc;
}

.move-button .el-icon {
  font-size: 12px;
}

.el-input {
  flex-grow: 1;
}

.delete-button {
  margin-left: 8px;
  padding: 8px;
  height: 32px;
  width: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: #606266;
  background-color: transparent;
  border: none;
}

.add-button {
  margin-top: 8px;
  border: 1px solid #dcdfe6;
  background-color: transparent;
  color: #606266;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
}

.add-button .el-icon {
  margin-right: 4px;
}

.values-editor :deep(.el-input__inner::-webkit-outer-spin-button),
        .values-editor :deep(.el-input__inner::-webkit-inner-spin-button) {
          -webkit-appearance: none;
         margin: 0;
}
        
</style>