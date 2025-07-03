<template>
  <div class="expectation-form-container">
    <div class="form-header">
      <h3>创建期望 | {{ typeDisplayName }}</h3>
      <el-button @click="$emit('need-different')" text>
        <el-icon><RefreshLeft /></el-icon>
        需要其他期望?
      </el-button>
    </div>

    <el-form :model="form" :rules="rules" ref="formRef" label-position="top" class="expectation-form" >
      <Expect v-model="form.expectation" :options="expectationOptions"/>
      
      <template v-if="showColumn">
        <Column v-model="form.column" :columns="extractedColumns"/>
      </template>

      <template v-if="showTypeList">
        <TypeList v-model="form.typeList" :id="form.expectation" />
      </template>

      <template v-if="showMostly">
        <Mostly v-model="form.mostly" />
      </template>

      <template v-if="showToBeBetween">
        <ToBeBetween 
          v-model:minValue="form.toBeBetween_minValue" 
          v-model:maxValue="form.toBeBetween_maxValue"
          v-model:option="form.toBeBetween_option"
        />
      </template>

      <template v-if="showValueSet">
        <ValueSet v-model="form.valueSet" />
      </template>
      
      <el-form-item label="备注 (可选)">
        <el-input
          v-model="form.notes"
          type="textarea"
          :rows="3"
          placeholder="关于此期望的备注。支持 **Markdown**。">
        </el-input>
      </el-form-item>
    </el-form>

    <div class="form-footer">
      <el-button @click="$emit('back')">返回</el-button>
      <el-button @click="onSave">保存</el-button>
      <el-button type="primary" @click="onSaveAndAddMore">保存并继续添加</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { ElForm, ElFormItem, ElInput, ElButton, ElIcon, ElMessage } from 'element-plus';
import { RefreshLeft } from '@element-plus/icons-vue';
import axios from 'axios'; 
import Expect from './common/Expect.vue';
import Column from './common/Column.vue';
import TypeList from './common/TypeList.vue';
import Mostly from './common/Mostly.vue';
import ToBeBetween from './common/ToBeBetween.vue'; 
import ValueSet from './common/ValueSet.vue'; 
import { API_URL } from '@/config';
import { useExpectationStore } from '@/stores/expectationStore';
const expectationStore = useExpectationStore()
const props = defineProps({
  typeDisplayName: {
    type: String,
    required: true
  },
  assetFields: {
    type: Object,
    default: () => ({})
  },
});
const emit = defineEmits(['back', 'save', 'save-and-add-more', 'need-different']);
const extractedColumns = computed(() => {
  if (props.assetFields) {
    return props.assetFields.column_info.map(col => {
      const columnName = Object.keys(col)[0];
      return columnName !== undefined ? columnName : null; 
    }).filter(col => col !== null); 
  }
  return [];
});

const expectationOptions = [
  {label: 'Column values to be unique', expectation_type: 'expect_column_values_to_be_unique', type_id:401},
  {label: 'Column distinct values to be in set', expectation_type: 'expect_column_distinct_values_to_be_in_set' , type_id:402},
  {label: 'Column distinct values to contain set', expectation_type: 'expect_column_distinct_values_to_contain_set', type_id:403},
  {label: 'Column distinct values to equal set', expectation_type: 'expect_column_distinct_values_to_equal_set' , type_id:405},
  {label: 'Column proportion of unique values to be between', expectation_type: 'expect_column_proportion_of_unique_values_to_be_between' , type_id:406},
  {label: 'Column unique value count to be between', expectation_type: 'expect_column_unique_value_count_to_be_between' , type_id:407},
  {label: 'Compound columns to be unique', expectation_type: 'expect_compound_columns_to_be_unique' , type_id:408},
  {label: 'Select column values to be unique within record', expectation_type: 'expect_select_column_values_to_be_unique_within_record' , type_id:409}
];

const form = ref({
  expectation: 401, 
  column: null, 
  typeList: [{ value: '' }],
  mostly: 100, 
  toBeBetween_minValue: null, 
  toBeBetween_maxValue: null, 
  toBeBetween_option: 'fixed', 
  valueSet: { type: 'text', values: [''] },
  notes: ''
});
const showColumn = computed(() => [401, 402, 403, 405, 406, 407].includes(form.value.expectation));
const showTypeList = computed(() => [408, 409].includes(form.value.expectation));
const showMostly = computed(() => [401, 408, 409].includes(form.value.expectation));
const showToBeBetween = computed(() => [406, 407].includes(form.value.expectation)); 
const showValueSet = computed(() => [402, 403, 405].includes(form.value.expectation));
const formRef = ref(null);


const rules = {
  column: [{ required:true, message: '请选择列', trigger: 'blur'}],
  typeList: [
    {  type: 'array', required: true, trigger: 'blur' }],
  toBeBetween_minValue: [
    { required: true, message: '最小值不能为空', trigger: 'blur' }
  ],
  toBeBetween_maxValue: [
    { required: true, message: '最大值不能为空', trigger: 'blur' }
  ],
  valueSet: [
    {
      required: true,
      validator: (rule, value, callback) => {
        if (showValueSet.value && (!value || !value.values || value.values.length === 0 || value.values.some(v => v === ''))) {
          callback(new Error('值集合不能为空'));
        } else {
          callback();
        }
      },
      trigger: 'blur'
    }
  ]
};






const setForm = () => {
  form.value.column = null;
  form.value.typeList = [{ value: '' }];
  form.value.mostly = 100;
  form.value.toBeBetween_minValue = null;
  form.value.toBeBetween_maxValue = null;
  form.value.toBeBetween_option = 'fixed';
  form.value.valueSet = { type: 'text', values: [''] };
  form.value.notes = '';
};

// 在 watch 函数中替换为：
watch(() => form.value.expectation, (newExpectation, oldExpectation) => {
  if (newExpectation !== oldExpectation) {
    formRef.value.clearValidate();
    setForm();
  }
});






const constructPayload = () => {
  const selectedExpectation = expectationOptions.find(opt => opt.type_id === form.value.expectation);
  const kwargs = {};
  if (form.value.column && showColumn.value) kwargs.column = form.value.column;
  
  if (showTypeList.value && form.value.typeList && form.value.typeList.length > 0) {
    kwargs.column_list = form.value.typeList.map(item => item.value).filter(v => v !== '');
  }
  
  if (showMostly.value && form.value.mostly !== null) {
    kwargs.mostly = form.value.mostly / 100; 
  }

  if (showToBeBetween.value) {
    if (form.value.toBeBetween_minValue !== null) kwargs.min_value = form.value.toBeBetween_minValue;
    if (form.value.toBeBetween_maxValue !== null) kwargs.max_value = form.value.toBeBetween_maxValue;
    if(form.value.expectation=== 406)   {kwargs.strict_min=true, kwargs.strict_max=true}  
  }

  if (showValueSet.value && form.value.valueSet && form.value.valueSet.values.length > 0) {
    kwargs.value_set = form.value.valueSet.values.filter(v => v !== ''); 
  }
  
  if (form.value.notes) {kwargs.meta = { notes: form.value.notes }; }
  return {
    suite_json: {
      expectations: [{
        expectation_type: selectedExpectation.expectation_type,
        kwargs: kwargs
      }]
    },
    type_id: selectedExpectation.type_id
  };
};


const handleSave = async (isSaveAndAddMore = false) => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (valid) {
      const payload = constructPayload();
      if (!payload) {
        ElMessage.error('无法构建请求数据');
        return;
      }
      console.log('准备发送的 payload (Uniqueness):', payload);
        try {
          const response = await axios.post(`${API_URL}/dataasset/${props.assetFields.dataAssetId}/expectation`, payload);
          if(response.data){
          ElMessage.success('期望保存成功');
          if (isSaveAndAddMore) {
            setForm();
          }
          expectationStore.triggerRefresh()
          emit('save', isSaveAndAddMore);  
      }
        } catch (error) {
          console.error('保存失败 (Uniqueness):', error);
        }
    } else {
      ElMessage.error('表单校验失败，请检查输入');
      return false;
    }
  });
};

const onSave = () => handleSave(false);
const onSaveAndAddMore = () => handleSave(true);

</script>

<style scoped>
.expectation-form-container {
  display: flex;
  flex-direction: column;
  height: 100%; 
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-shrink: 0;
}

.form-header h3 {
  margin: 0;
  font-size: 20px; 
  font-weight: 600;
}

.form-header .el-button {
  font-size: 13px;
}
.form-header .el-icon {
  margin-right: 4px;
}

.expectation-form {
  flex-grow: 1; 
  overflow-y: auto; 
  padding-right: 10px; 
  margin-right: -10px; 
}

.el-form-item {
  margin-bottom: 20px;
}

.el-select, .el-input {
  width: 100%;
}

.form-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
  flex-shrink: 0; 
}

.form-section {
  margin-bottom: 24px;
}

.form-section h4 {
  margin: 0 0 16px;
  font-size: 16px;
  font-weight: 500;
}

.condition-builder {
  display: flex;
  gap: 10px;
  align-items: center;
}

.condition-column-select {
  flex-grow: 1;
}
.condition-operator-select {
  width: 100px !important; /* Override default width */
  flex-shrink: 0;
}
.condition-value-input {
  flex-grow: 1;
}
.condition-clear-button {
  flex-shrink: 0;
}

.info-icon {
  margin-left: 4px;
  color: #909399;
}

.condition-form-item .el-form-item__label {
  display: flex; /* Allow custom layout for label */
  justify-content: space-between; /* If you want title and icon spread */
  width: 100%; /* Ensure label takes full width */
  line-height: normal; /* Override default line-height if needed */
}

.condition-label-header {
  display: flex;
  align-items: center;
}

.condition-label-header h4 {
  margin: 0 8px 0 0; /* Adjust spacing as needed */
  font-size: 14px; /* Match ElFormItem label size or customize */
  font-weight: normal; /* Match ElFormItem label weight or customize */
}

.condition-builder {
  display: flex;
  gap: 10px;
  align-items: center;
  width: 100%; /* Ensure builder takes full width within form item */
}

/* Optional: If Column component has its own label that you want to hide when used here */
.condition-builder :deep(.condition-column-select .el-form-item__label) {
  display: none;
}
</style>