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
      <!-- 使用 Expect 组件 -->
      <Expect
        v-model="form.expectation"
        :options="expectationOptions"
      />

      <!-- 使用 Column 组件 -->
      <Column
        v-model="form.column"
        :columns="extractedColumns"
      />

      <!-- 使用 ToBeBetween 组件 -->
      <template v-if="showToBeBetween">
        <ToBeBetween
          v-model:minValue="form.minValue"
          v-model:maxValue="form.maxValue"
          v-model:strict_min="form.strict_min"
          v-model:strict_max="form.strict_max"
        />
      </template>

      <!-- 使用 TypeList 组件 -->
      <template v-if="showTypeList">
        <TypeList v-model="form.typeList" :id="form.expectation" />
      </template>

      <!-- 符合期望的比例 -->
      <el-form-item required v-if="showMostly">
        <template #label>
          <span>符合期望的比例</span>
          <el-tooltip content="期望有多少百分比的数据行符合此条件" placement="top">
            <el-icon class="info-icon"><InfoFilled /></el-icon>
          </el-tooltip>
        </template>
        <el-slider v-model="form.mostly" :min="0" :max="100" show-input />
      </el-form-item>



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
import { ElForm, ElFormItem, ElInput, ElButton, ElIcon ,ElSlider, ElTooltip, ElMessage } from 'element-plus';
import { RefreshLeft, InfoFilled } from '@element-plus/icons-vue';
import axios from 'axios';
import Expect from './common/Expect.vue';
import Column from './common/Column.vue';
import ToBeBetween from './common/ToBeBetween.vue';
import TypeList from './common/TypeList.vue'; 
import { API_URL } from '@/config';
import { useExpectationStore } from '@/stores/expectationStore';
const expectationStore = useExpectationStore()
const props = defineProps({
  typeDisplayName: {
    type: String,
    default: '数值型期望'
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
  { label: 'Column values to be between', expectation_type: 'expect_column_values_to_be_between' ,type_id: 501},
  { label: 'Column maximum to be between', expectation_type: 'expect_column_max_to_be_between',type_id: 502},
  { label: 'Column mean to be between', expectation_type: 'expect_column_mean_to_be_between',type_id: 503},
  { label: 'Column median to be between', expectation_type: 'expect_column_median_to_be_between',type_id: 504},
  { label: 'Column minimum to be between', expectation_type: 'expect_column_min_to_be_between',type_id: 505},
  { label: 'Column pair values a to be greater than b', expectation_type: 'expect_column_pair_values_a_to_be_greater_than_b',type_id: 506},
  { label: 'Column standard deviation to be between', expectation_type: 'expect_column_stdev_to_be_between',type_id: 507},
  { label: 'Column sum to be between', expectation_type: 'expect_column_sum_to_be_between',type_id: 508},
  { label: 'Column value z - scores to be less than', expectation_type: 'expect_column_value_z_scores_to_be_less_than',type_id: 509},
  { label: 'Multicolumn sum to equal', expectation_type: 'expect_multicolumn_sum_to_equal',type_id: 510}
];

const form = ref({
  expectation: 501, 
  column: null,
  minValue: null,
  maxValue: null,
  strict_min: true,
  strict_max: true,
  mostly: 100,
  typeList: [{ value: '' }], 
  notes: ''
});

const showToBeBetween = computed(() => [ 501, 502, 503, 504, 505, 507, 508].includes(form.value.expectation));
const showTypeList = computed(() => [510].includes(form.value.expectation));
const showMostly = computed(() => [501, 506, 509, 510].includes(form.value.expectation));


const setForm = () => {
  form.value.column = null;
  form.value.minValue = null;
  form.value.maxValue = null;
  form.value.strict_min = true;
  form.value.strict_max = true;
  form.value.typeList = [{ value: '' }];
  form.value.mostly = 100;
  form.value.notes = '';
};

// 在 watch 函数中替换为：
watch(() => form.value.expectation, (newExpectation, oldExpectation) => {
  if (newExpectation !== oldExpectation) {
    formRef.value.clearValidate();
    setForm();
  }
});

const formRef = ref(null);
const rules = {
  column: [{ required: true, message: '请选择列', trigger: 'blur' }],
  mostly: [{ required: true, message: '符合度不能为空', trigger: 'blur' }],
  typeList: [
    { 
      required: computed(() => showTypeList.value), 
      validator: (rule, value, callback) => {
        if (showTypeList.value && (!value || value.length === 0 || value.some(item => !item.value))) {
          callback(new Error('列表不能为空'));
        } else {
          callback();
        }
      },
      trigger: 'blur' 
    }
  ]
};

const constructPayload = () => {
  const selectedExpectation = expectationOptions.find(opt => opt.type_id === form.value.expectation);
  const expectations = [];
  const kwargs = {};
  if (showToBeBetween.value) {
    if (form.value.column) kwargs.column = form.value.column;
    if (form.value.minValue !== null) kwargs.min_value = form.value.minValue;
    if (form.value.maxValue !== null) kwargs.max_value = form.value.maxValue;
    if (form.value.strict_min !== null) kwargs.strict_min = form.value.strict_min;
    if (form.value.strict_max !== null) kwargs.strict_max = form.value.strict_max;
  } else if (showTypeList.value) { 
     if (form.value.typeList && form.value.typeList.length > 0) {
        kwargs.column_list = form.value.typeList.map(item => item.value).filter(v => v !== '');
      }
  } else {
    switch (selectedExpectation.type_id) {
      case 506:
        if (form.value.column) kwargs.column_A = form.value.column; 
        break;
      case 509:
         if (form.value.column) kwargs.column = form.value.column;
        break;
      default:
        console.warn('未处理的期望类型:', selectedExpectation.expectation_type);
        break;
    }
  }

  if (showMostly.value) {kwargs.mostly = form.value.mostly / 100; }
  if (form.value.notes) { kwargs.meta = { notes: form.value.notes };}

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
        console.log('返回的结果:', response.data);
        if(response.data){
          ElMessage.success('期望保存成功');
          if (isSaveAndAddMore) {
            setForm();
          }
          expectationStore.triggerRefresh()
          emit('save', isSaveAndAddMore);  
    }
      } catch (error) {
        console.error('保存失败:', error);
      }

    } else {
      console.log('表单校验失败!');
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
  padding-right: 10px; /* for scrollbar */
  margin-right: -10px; /* for scrollbar */
}

.el-form-item {
  margin-bottom: 20px;
}
.el-form-item .info-icon {
  margin-left: 5px;
  color: #909399;
  cursor: help;
}

.el-select, .el-input, .el-input-number, .el-slider {
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