<template>
  <div class="expectation-form">
    <div class="drawer-header">
      <h3>New Expectation | {{ typeDisplayName }}</h3>
      <el-button @click="$emit('need-different')" class="need-different" type="default" size="small">
        Need a different Expectation?
      </el-button>
    </div>

    <el-form :model="form" :rules="rules" ref="formRef" label-position="top" class="form-content">
      <div class="form-section">
        <h4>Expect</h4>
        <Expect
          v-model="form.expectation"
          :options="expectationOptions"
        />
      </div>
      <div class="form-section">
        <Column
          v-model="form.column"
          :columns="extractedColumns"
        />
      </div>

      <div class="form-section">
        <Mostly v-model="form.mostly" />
      </div>

      <div class="form-section">
        <h4>Notes</h4>
        <el-form-item label="备注">
          <el-input
            v-model="form.notes"
            type="textarea"
            :rows="4"
            placeholder="Example notes about this Expectation. **Markdown** `supported`."
          />
        </el-form-item>
      </div>
    </el-form>

    <div class="form-footer">
      <el-button @click="handleBack">Back</el-button>
      <el-button @click="onSave">Save</el-button>
      <el-button type="primary" @click="onSaveAndAddMore">Save & add more</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { ElForm, ElFormItem, ElInput, ElButton, ElMessage } from 'element-plus';
import Expect from './common/Expect.vue';
import Column from './common/Column.vue';
import Mostly from './common/Mostly.vue';
import axios from 'axios';
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
  }
});
const emit = defineEmits(['back', 'save', 'save-and-add-more', 'need-different']);

const formRef = ref(null);

const extractedColumns = computed(() => {
  if (props.assetFields && props.assetFields.column_info) { 
    return props.assetFields.column_info.map(col => {
      const columnName = Object.keys(col)[0];
      return columnName !== undefined ? columnName : null; 
    }).filter(col => col !== null); 
  }
  return [];
});

const form = ref({
  expectation: 301, 
  column: null, 
  mostly: 100, 
  notes: '' 
});

const setForm = () => {
        form.value.column = null;
        form.value.mostly = 100;
        form.value.notes = '';
      };


const rules = ref({
  column: [{required: true,message: '请选择列',trigger: ['blur',],}]
});

const expectationOptions = [
  { type_id: 301, label: 'Column values to not be null', expectation_type: 'expect_column_values_to_not_be_null' },
  { type_id: 302, label: 'Column values to be null', expectation_type: 'expect_column_values_to_be_null' }
];

const constructPayload = () => {
  const selectedExpectation = expectationOptions.find(opt => opt.type_id === form.value.expectation);
  const expectations = [];
  const kwargs = {}; 
  if (form.value.column) kwargs.column = form.value.column;
  if (form.value.mostly !== null) { kwargs.mostly = form.value.mostly / 100;}
  if (form.value.notes) {kwargs.meta = { notes: form.value.notes }; }
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
  const valid = await formRef.value.validate();
  if (valid) {
    const payload = constructPayload();
    console.log('准备发送的 payload (Completeness):', payload);
    try {
      const response = await axios.post(`${API_URL}/dataasset/${props.assetFields.dataAssetId}/expectation`, payload);
      console.log('返回的结果 (Completeness):', response.data);
      if(response.data){
          ElMessage.success('期望保存成功');
          if (isSaveAndAddMore) {
            setForm();
          }
          expectationStore.triggerRefresh()
          emit('save', isSaveAndAddMore);  
    }
    } catch (error) {
      console.error('保存期望时出错:', error);
    }
  } else {
    ElMessage.error('表单校验失败，请检查输入');
  }
};

const onSave = () => handleSave(false);
const onSaveAndAddMore = () => handleSave(true);

const handleBack = () => {
  emit('back');
};

</script>

<style scoped>
.expectation-form {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.drawer-header h3 {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
}

.need-different {
  font-size: 14px;
}

.form-content {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 10px; 
  margin-right: -10px; 
}

.form-section {
  margin-bottom: 24px;
}

.form-section h4 {
  margin: 0 0 16px;
  font-size: 16px;
  font-weight: 500;
}

.form-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #e4e7ed;
}

:deep(.el-select) {
  width: 100%;
}

.el-form-item {
  margin-bottom: 20px; 
}

.el-select, .el-input, .el-input-number {
  width: 100%; 
}
</style>