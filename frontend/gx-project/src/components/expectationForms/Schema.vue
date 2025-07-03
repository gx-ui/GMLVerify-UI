<template>
  <div class="expectation-form-container">
    <div class="form-header">
      <h3>创建期望 | {{ typeDisplayName }}</h3>
      <el-button @click="$emit('need-different')" text>
        <el-icon><RefreshLeft /></el-icon>
        需要其他期望?
      </el-button>
    </div>
    <el-form :model="form" :rules="rules" ref="formRef" label-position="top" class="expectation-form">

      <Expect v-model="form.expectation" :options="expectationOptions"/>

      <template v-if="showColumn">
        <Column v-model="form.column"  :columns="extractedColumns"/>
      </template>

      <template v-if="showType">  
        <Type v-model="form.columnType" /> 
      </template>
      
      <template v-if="showTypeList">
        <TypeList v-model="form.typeList" :id="form.expectation" />
      </template>

      <template v-if="showToBeBetween">
        <ToBeBetween 
          v-model:minValue="form.toBeBetween_minValue" 
          v-model:maxValue="form.toBeBetween_maxValue"
          v-model:option="form.toBeBetween_option"
        />
      </template>

      <template v-if="showMostly">
        <Mostly v-model="form.mostly" />
      </template>

      <template v-if="showValue">
        <Value v-model="form.value" />
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
import Type from './common/Type.vue'; 
import Value from './common/Value.vue';
import { API_URL } from '@/config'
import { useExpectationStore } from '@/stores/expectationStore';
const expectationStore = useExpectationStore()
const props = defineProps({
  expectationType: {
    type: String,
    required: true
  },
  typeDisplayName: {
    type: String,
    default: '期望'
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
  {label: 'Column to exist', expectation_type: 'expect_column_to_exist', type_id: 101},
  {label: 'Column values to be in type list', expectation_type: 'expect_column_values_to_be_in_type_list', type_id: 102},
  {label: 'Column values to be of type', expectation_type: 'expect_column_values_to_be_of_type', type_id: 103 },
  {label: 'Table column count to be between', expectation_type: 'expect_table_column_count_to_be_between', type_id: 104}, 
  {label: 'Table column count to equal', expectation_type: 'expect_table_column_count_to_equal', type_id: 105},
  {label: 'Table columns to match ordered list', expectation_type: 'expect_table_columns_to_match_ordered_list', type_id: 106},
  {label: 'Table columns to match set', expectation_type: 'expect_table_columns_to_match_set', type_id: 107}
];
const showColumn = computed(() => [101, 102, 103].includes(form.value.expectation));
const showTypeList = computed(() => [102, 106, 107].includes(form.value.expectation));
const showMostly = computed(() => [102, 103].includes(form.value.expectation));
const showToBeBetween = computed(() => [104].includes(form.value.expectation));
const showType = computed(() => [103].includes(form.value.expectation)); 
const showValue = computed(() => [105].includes(form.value.expectation));
const formRef = ref(null);

const  rules = {
  column: [{required: true,message: '请选择列',trigger: 'blur'}],
  columnType: [{ required: true, message: '类型不能为空', trigger: 'blur' }],
  toBeBetween_minValue: [{ required: true, message: '最小值不能为空', trigger: 'blur' }],
  toBeBetween_maxValue: [{ required: true, message: '最大值不能为空', trigger: 'blur' } ],
  value: [ { required: true, message: '值不能为空', trigger: 'blur' }]
};
const form = ref({
  expectation: 101,
  column: null, 
  columnType: '', 
  typeList: [{ value: '' }],
  mostly: 100,
  toBeBetween_minValue: null, 
  toBeBetween_maxValue: null, 
  toBeBetween_option: 'fixed', 
  value: null, 
  notes: ''
});

//选择不同期望时，重置表单
const setForm = () => {
  form.value.column = null;
  form.value.columnType = '';
  form.value.typeList = [{ value: '' }];
  form.value.mostly = 100;
  form.value.toBeBetween_minValue = null;
  form.value.toBeBetween_maxValue = null;
  form.value.toBeBetween_option = 'fixed';
  form.value.value = null;
  form.value.notes = '';
};

// 在 watch 函数中替换为：
watch(() => form.value.expectation, (newExpectation, oldExpectation) => {
  if (newExpectation !== oldExpectation) {
    formRef.value.clearValidate();
    setForm();
  }
});


watch(() => form.value.column, (newColumn) => {
    const columnInfo = props.assetFields.column_info.find(col => Object.keys(col)[0] === newColumn);
    form.value.columnType = columnInfo ? columnInfo[newColumn] : '';
}, { immediate: true });


const constructPayload = () => {
  const selectedExpectation = expectationOptions.find(opt => opt.type_id === form.value.expectation);
  const expectations = [];
  const kwargs = {};

  switch (selectedExpectation.type_id) { 
    case 101:
      if (form.value.column) kwargs.column = form.value.column;
      break;
    case 102:
      if (form.value.column) kwargs.column = form.value.column;
      if (form.value.typeList && form.value.typeList.length > 0) {
        kwargs.type_list = form.value.typeList.map(item => item.value).filter(v => v !== '');
      }
      if (form.value.mostly !== null) kwargs.mostly = form.value.mostly / 100;
      break;
    case 103:
      if (form.value.column) kwargs.column = form.value.column;
      if (form.value.columnType) kwargs.type_ = form.value.columnType;
      if (form.value.mostly !== null) kwargs.mostly = form.value.mostly / 100;
      break;
    case 104:
      if (form.value.toBeBetween_minValue !== null) kwargs.min_value = form.value.toBeBetween_minValue;
      if (form.value.toBeBetween_maxValue !== null) kwargs.max_value = form.value.toBeBetween_maxValue;
      break;
    case 105:
      if (form.value.value !== null) kwargs.value = form.value.value;
      break;
    case 107: 
    case 106: 
      if (form.value.typeList && form.value.typeList.length > 0) {
        kwargs.column_list = form.value.typeList.map(item => item.value).filter(v => v !== '');
      }
      break;
    default:
      console.warn('未处理的期望类型:', selectedExpectation.expectation_type);
      break;
  }
  
  if (form.value.notes) {
    kwargs.meta = { notes: form.value.notes }; 
  }
  expectations.push({
    expectation_type: selectedExpectation.expectation_type,
    kwargs: kwargs
  });
  return {
    suite_json: {
      expectations: expectations
    },
    type_id: selectedExpectation.type_id
  };
};


const handleSave = async (isSaveAndAddMore = false) => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      const payload = constructPayload();
      console.log('准备发送的 payload:', payload);
        try {
          const response = await axios.post(`${API_URL}/dataasset/${props.assetFields.dataAssetId }/expectation`, payload);
          console.log('返回的结果:', response.data);
          if(response.data){
          ElMessage.success('期望保存成功');
          if (isSaveAndAddMore) {
            setForm();
          }
          expectationStore.triggerRefresh()
          emit('save', isSaveAndAddMore);  
          }
        }
        catch (error) {
          console.error('保存期望时出错:', error);
        } 
    } else {
      ElMessage.error('表单校验失败，请检查输入',error);
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
</style>