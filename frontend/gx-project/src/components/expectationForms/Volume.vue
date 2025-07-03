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
      <Expect v-model="form.expectation" :options="expectationOptions" />

      <template v-if="showToBeBetween">
        <ToBeBetween 
          v-model:minValue="form.toBeBetween_minValue" 
          v-model:maxValue="form.toBeBetween_maxValue"
          v-model:option="form.toBeBetween_option"
        />
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
import { RefreshLeft } from '@element-plus/icons-vue';
import { ElForm, ElFormItem, ElInput, ElButton, ElIcon, ElMessage } from 'element-plus';
import axios from 'axios';
import Expect from './common/Expect.vue';
import ToBeBetween from './common/ToBeBetween.vue';
import Value from './common/Value.vue';
import { API_URL } from '@/config';
import { useExpectationStore } from '@/stores/expectationStore';
const expectationStore = useExpectationStore()

const props = defineProps({
  typeDisplayName: {
    type: String,
    default: 'Volume'
  },
  assetFields: {
    type: Object,
    default: () => ({})
  },

});

const emit = defineEmits(['back', 'save', 'save-and-add-more', 'need-different']);

const extractedColumns = computed(() => {
  if (props.assetFields && props.assetFields.column_info) {
    return props.assetFields.column_info.map(col => {
      const columnName = Object.keys(col)[0];
      return columnName !== undefined ? columnName : null; 
    }).filter(col => col !== null); 
  }
  return [];
});

const expectationOptions = [
  { label: 'Table row count to be between', expectation_type: 'expect_table_row_count_to_be_between', type_id: 201},
  { label: 'Table row count to equal', expectation_type: 'expect_table_row_count_to_equal', type_id: 202},
  { label: 'Table row count to equal other table', expectation_type: 'expect_table_row_count_to_equal_other_table', type_id: 203}
];

const formRef = ref(null);

const form = ref({
  expectation: 201,
  toBeBetween_minValue: null, 
  toBeBetween_maxValue: null, 
  toBeBetween_option: 'fixed',
  value: null,
  other_table_name: '', 
  notes: ''
});

const showToBeBetween = computed(() => form.value.expectation === 201);
const showValue = computed(() => form.value.expectation === 202);


const showOtherTableNameInput = computed(() => form.value.expectation === 203);

const setForm = () => {
  form.value.toBeBetween_minValue = null;
  form.value.toBeBetween_maxValue = null;
  form.value.toBeBetween_option = 'fixed';
  form.value.value = null;
  form.value.other_table_name = '';
  form.value.notes = '';
};

// 在 watch 函数中替换为：
watch(() => form.value.expectation, (newExpectation, oldExpectation) => {
  if (newExpectation !== oldExpectation) {
    formRef.value.clearValidate();
    setForm();
  }
});



const rules = ref({
  toBeBetween_minValue: [{ required: true, message: '最小值不能为空', trigger: 'blur' }],
  toBeBetween_maxValue: [{ required: true, message: '最大值不能为空', trigger: 'blur' }],
  value: [{ required: true, message: '值不能为空', trigger: 'blur' }],
  other_table_name: [ { required: true, message: '其他表名不能为空', trigger: 'blur' }]
});



const constructPayload = () => {
  const selectedExpectation = expectationOptions.find(opt => opt.type_id === form.value.expectation);

  const expectations = [];
  const kwargs = {};
  switch (selectedExpectation.type_id) {
    case 201: 
      if (form.value.toBeBetween_minValue !== null) kwargs.min_value = form.value.toBeBetween_minValue;
      if (form.value.toBeBetween_maxValue !== null) kwargs.max_value = form.value.toBeBetween_maxValue;
      break;
    case 202: 
      if (form.value.value !== null) kwargs.value = form.value.value;
      break;
    case 203:
      if (form.value.other_table_name) kwargs.other_table_name = form.value.other_table_name;
      break;
    default:
      console.warn('未处理的期望类型:', selectedExpectation.expectation_type);
      break;
  }
  
  if (form.value.notes) { kwargs.meta = { notes: form.value.notes };  }
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

.el-select,
.el-input-number,
.el-input {
  width: 100%;
}

.form-section {
  margin-bottom: 24px;
}
.form-text {
  margin: 12px 0 8px 0;
  color: #606266;
  font-size: 15px;
}
.condition-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.info-icon {
  margin-left: 4px;
  color: #909399;
  cursor: help;
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