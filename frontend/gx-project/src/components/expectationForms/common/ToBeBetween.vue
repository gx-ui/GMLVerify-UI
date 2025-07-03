<template>
  <el-form-item label="To be between">
    <div class="to-be-between-container">
      <el-select v-model="selectedOption" placeholder="Select option" class="option-select" @change="handleOptionChange">
        <el-option label="the fixed values" value="fixed"></el-option>
        <el-option label="a dynamic range of" value="dynamic"></el-option>
      </el-select>

      <!-- Fixed Values Inputs -->
      <div v-if="selectedOption === 'fixed'" class="value-inputs fixed-values-inputs">
        <el-input
          :model-value="minValue"
          @update:modelValue="(val) => emit('update:minValue', val)"
          placeholder="Min value"
          class="value-input"
        />
        <span class="and-separator">AND</span>
        <el-input
          :model-value="maxValue"
          @update:modelValue="(val) => emit('update:maxValue', val)"
          placeholder="Max value"
          class="value-input"
        />
      </div>

      <!-- Dynamic Range Inputs -->
      <div v-if="selectedOption === 'dynamic'" class="value-inputs dynamic-range-inputs">
        <el-select v-model="localDynamicSign" class="dynamic-sign-select" @change="(val) => emit('update:dynamicSign', val)">
          <el-option label="+" value="+"></el-option>
          <el-option label="-" value="-"></el-option>
        </el-select>
        <el-input
          :model-value="dynamicPercentage"
          @update:modelValue="(val) => emit('update:dynamicPercentage', val)"
          placeholder="%"
          class="dynamic-percentage-input"
        />
        <span class="dynamic-text">% of the average of the last</span>
        <el-input
          :model-value="dynamicRuns"
          @update:modelValue="(val) => emit('update:dynamicRuns', val)"
          placeholder="runs"
          class="dynamic-runs-input"
        />
        <span class="dynamic-text">runs</span>
        <el-checkbox 
          :model-value="dynamicStrict" 
          @update:modelValue="(val) => emit('update:dynamicStrict', val)" 
          label="Strict" 
          class="dynamic-strict-checkbox"
        />
      </div>
    </div>
  </el-form-item>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue';
import { ElFormItem, ElSelect, ElOption, ElInput, ElCheckbox } from 'element-plus';

const props = defineProps({
  minValue: {
    type: [Number, String],
    default: null
  },
  maxValue: {
    type: [Number, String],
    default: null
  },
  option: {
    type: String,
    default: 'fixed'
  },
  dynamicSign: {
    type: String,
    default: '+'
  },
  dynamicPercentage: {
    type: [Number, String],
    default: null
  },
  dynamicRuns: {
    type: [Number, String],
    default: null
  },
  dynamicStrict: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits([
  'update:minValue',
  'update:maxValue',
  'update:option',
  'update:dynamicSign',
  'update:dynamicPercentage',
  'update:dynamicRuns',
  'update:dynamicStrict'
]);

const selectedOption = ref(props.option);
const localDynamicSign = ref(props.dynamicSign);
// No need for local refs for dynamicPercentage, dynamicRuns, dynamicStrict if directly binding to props in template
// and emitting update on input. If more complex local logic is needed, they can be added.

watch(selectedOption, (newVal) => {
  emit('update:option', newVal);
});

watch(() => props.option, (newVal) => {
  if (selectedOption.value !== newVal) {
    selectedOption.value = newVal;
  }
});

watch(() => props.dynamicSign, (newVal) => {
  if (localDynamicSign.value !== newVal) {
    localDynamicSign.value = newVal;
  }
});

// Optional: Clear other fields when option changes
const handleOptionChange = (newOption) => {
  if (newOption === 'fixed') {
    emit('update:dynamicSign', '+');
    emit('update:dynamicPercentage', null);
    emit('update:dynamicRuns', null);
    emit('update:dynamicStrict', false);
  } else if (newOption === 'dynamic') {
    emit('update:minValue', null);
    emit('update:maxValue', null);
  }
};

</script>

<style scoped>
.to-be-between-container {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.option-select {
  margin-bottom: 10px;
  width: 100%;
}

.value-inputs {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 10px; /* Adds space between elements */
}

.fixed-values-inputs .value-input {
  flex-grow: 1;
}

.fixed-values-inputs .and-separator {
  margin: 0 10px;
  color: #606266;
  white-space: nowrap;
}

.dynamic-range-inputs {
  display: flex;
  align-items: center;
  gap: 8px; /* Adjust gap as needed */
}

.dynamic-sign-select {
  width: 70px; /* Adjust width as needed */
}

.dynamic-percentage-input {
  width: 80px; /* Adjust width as needed */
}

.dynamic-runs-input {
  width: 80px; /* Adjust width as needed */
}

.dynamic-text {
  color: #606266;
  white-space: nowrap;
  font-size: 14px;
}

.dynamic-strict-checkbox {
  margin-left: auto; /* Pushes the checkbox to the right */
}
</style>