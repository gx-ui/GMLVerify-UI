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
      <Column v-model="form.column" :columns="extractedColumns"/>

     

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

      <template v-if="showValue">
        <Value v-model="form.value" :id="form.expectation" />
      </template>

      <template v-if="showValueSet">
        <ValueSet v-model="form.valueSet" />
      </template>
      <template v-if="showMatchOn">
        <MatchOn v-model="form.matchOn" />
      </template>
      <template v-if="showMostly">
        <Mostly v-model="form.mostly" />
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
import {  RefreshLeft } from '@element-plus/icons-vue';
import { ElForm, ElFormItem, ElIcon, ElMessage } from 'element-plus';
import axios from 'axios';
import Expect from './common/Expect.vue';
import Column from './common/Column.vue';
import TypeList from './common/TypeList.vue';
import Mostly from './common/Mostly.vue';
import ToBeBetween from './common/ToBeBetween.vue';
import Value from './common/Value.vue';
import ValueSet from './common/ValueSet.vue';
import MatchOn from './common/MatchOn.vue';
import { API_URL } from '@/config';
import { useExpectationStore } from '@/stores/expectationStore';
const expectationStore = useExpectationStore()


const props = defineProps({
  expectationType: {
    type: String,
    required: true
  },
  typeDisplayName: {
    type: String,
    default: '有效性期望'
  },
  assetFields: {
    type: Object,
    default: () => ({})
  }
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
  { label: 'Column values to be in set', expectation_type: 'expect_column_values_to_be_in_set', type_id: 601},
  { label: 'Column most common value to be in set', expectation_type: 'expect_column_most_common_value_to_be_in_set', type_id: 602},
  { label: 'Column pair values to be equal', expectation_type: 'expect_column_pair_values_to_be_equal', type_id: 603},
  { label: 'Column value lengths to be between', expectation_type: 'expect_column_value_lengths_to_be_between', type_id: 604},
  { label: 'Column value lengths to equal', expectation_type: 'expect_column_value_lengths_to_equal', type_id: 605},
  { label: 'Column values to match like pattern', expectation_type: 'expect_column_values_to_match_like_pattern', type_id: 606},
  { label: 'Column values to match like pattern list', expectation_type: 'expect_column_values_to_match_like_pattern_list', type_id: 607},
  { label: 'Column values to match regex', expectation_type: 'expect_column_values_to_match_regex', type_id: 608},
  { label: 'Column values to match regex list', expectation_type: 'expect_column_values_to_match_regex_list', type_id: 609},
  { label: 'Column values to not be in set', expectation_type: 'expect_column_values_to_not_be_in_set', type_id: 610},
  { label: 'Column values to not match like pattern', expectation_type: 'expect_column_values_to_not_match_like_pattern', type_id: 611},
  { label: 'Column values to not match like pattern list', expectation_type: 'expect_column_values_to_not_match_like_pattern_list', type_id: 612},
  { label: 'Column values to not match regex', expectation_type: 'expect_column_values_to_not_match_regex', type_id: 613},
  { label: 'Column values to not match regex list', expectation_type: 'expect_column_values_to_not_match_regex_list', type_id: 614}
];

const form = ref({
  expectation: 601,
  column: null,
  valueSet: { type: 'text', values: [''] },
  typeList: [{ value: '' }],
  matchOn: 'any',
  mostly: 100,
  toBeBetween_minValue: null,
  toBeBetween_maxValue: null,
  toBeBetween_option: 'fixed',
  value: null,
  notes: ''
});

const setForm= ()=>{
    form.value.column = null;
    form.value.valueSet = { type: 'text', values: [''] };
    form.value.typeList = [{ value: '' }];
    form.value.matchOn = 'any';
    form.value.mostly = 100;
    form.value.toBeBetween_minValue = null;
    form.value.toBeBetween_maxValue = null;
    form.value.toBeBetween_option = 'fixed';
    form.value.value = null;
}


const formRef = ref(null);

// 根据组件规则定义计算属性
const showTypeList = computed(() => [607, 609, 612, 614].includes(form.value.expectation));
const showMatchOn = computed(() => [607,609].includes(form.value.expectation));
const showMostly = computed(() => [601, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614].includes(form.value.expectation));
const showToBeBetween = computed(() => [604].includes(form.value.expectation));
const showValue = computed(() => [605,606,608,611,613].includes(form.value.expectation));
const showValueSet = computed(() => [601, 602, 610].includes(form.value.expectation));

const rules = {
  column: [{ required: true, message: '请选择列', trigger: 'blur' }],
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
  ],
  typeList: [{ type: 'array', required: true, trigger: 'blur' }],
  toBeBetween_minValue: [{required: true, trigger: 'blur' }],
  toBeBetween_maxValue: [{ required: true, trigger: 'blur' }],
  value: [{ required: true,message:'值不能为空',trigger: 'blur'  }
],
};

watch(() => form.value.expectation, (newExpectation, oldExpectation) => {
  if (newExpectation !== oldExpectation) {
    formRef.value.clearValidate();
    setForm();
  }
});




const constructPayload = () => {
  const selectedExpectation = expectationOptions.find(opt => opt.type_id === form.value.expectation);
  const expectations = [];
  const kwargs = {};
  
  if (form.value.column) kwargs.column = form.value.column;
  
  switch (selectedExpectation.type_id) {
    case 601: 
    case 610: 
      if (form.value.valueSet && form.value.valueSet.values.length > 0) {
        kwargs.value_set = form.value.valueSet.values.filter(v => v !== '');
      }
      break; 
    case 602: 
      if (form.value.valueSet && form.value.valueSet.values.length > 0) {
        kwargs.value_set = form.value.valueSet.values.filter(v => v !== '');
      }
     
      break; 
    case 603: 
      break;
    case 604: 
      if (form.value.toBeBetween_minValue !== null) kwargs.min_value = form.value.toBeBetween_minValue;
      if (form.value.toBeBetween_maxValue !== null) kwargs.max_value = form.value.toBeBetween_maxValue;
      break;
      
    case 605: 
      if (form.value.value !== null) kwargs.value = form.value.value;
      break;
      
    case 606: 
    case 611: 
      if (form.value.value) kwargs.like_pattern= form.value.value;
      if (showMatchOn.value) kwargs.match_on = form.value.matchOn;
      break;
    case 607: 
    case 612: 
      if (form.value.typeList && form.value.typeList.length > 0) {
        kwargs.like_pattern_list = form.value.typeList.map(item => item.value).filter(v => v !== '');
      }
      if (form.value.matchOn) kwargs.match_on = form.value.matchOn;
      break;
      
    case 608: 
    case 613: 
      if (form.value.value) kwargs.regex = form.value.value;
      break;
    case 609: 
    case 614: 
      if (form.value.typeList && form.value.typeList.length > 0) {
        kwargs.regex_list = form.value.typeList.map(item => item.value).filter(v => v !== '');
      }
      break;
    default:
      console.warn('未处理的期望类型:', selectedExpectation.expectation_type);
      break;
  }

  if (selectedExpectation.type_id !== 602) {kwargs.mostly = form.value.mostly / 100; }
  
  if (form.value.notes) {  kwargs.meta = { notes: form.value.notes };}
  
  
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
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (valid) {
      const payload = constructPayload();
      console.log('准备发送的 payload:', payload);
      try {
        const response = await axios.post(`${API_URL}/dataasset/${props.assetFields.dataAssetId}/expectation`, payload);
        if(response.data){
          ElMessage.success('期望保存成功');
          if (isSaveAndAddMore) {setForm(); }
          expectationStore.triggerRefresh()
          emit('save', {isSaveAndAddMore,update:true});  
          }
      } catch (error) {
        console.error('保存失败:', error);
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
.el-form-item .info-icon {
  margin-left: 5px;
  color: #909399;
  cursor: help;
}

.el-select, .el-input, .el-slider {
  width: 100%;
}

.condition-builder {
  display: flex;
  align-items: center;
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