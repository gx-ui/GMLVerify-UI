<template>
  <div class="login-container">
    <el-card class="login-card" shadow="always">
      <div class="login-header">
        <img src="../assets/logo.png" alt="GMLVerify Logo" class="logo" />
        <h1 class="company-name">GMLVerify</h1>
      </div>
      <el-form :model="loginForm" :rules="rules" class="login-form" ref="loginFormRef" :hide-required-asterisk="true" :show-message="false" status-icon scroll-to-error @submit.prevent="handleSubmit">
        <el-form-item prop="username" :show-message="true">
          <el-input v-model.lazy="loginForm.username" placeholder="请输入用户名" prefix-icon="User" clearable size="large"></el-input>
        </el-form-item>
        <el-form-item prop="password" :show-message="true">
          <el-input v-model.lazy="loginForm.password" type="password" placeholder="请输入密码" prefix-icon="Lock" show-password clearable size="large" aria-autocomplete="new-password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-button" @click="handleSubmit" :loading="isLoading" native-type="submit">
            {{ isLoading ? '登录中...' : '登 入' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup name="Login">
import { ref,reactive } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { API_URL } from '../config'

   
   
   const router = useRouter()
   const loginFormRef = ref(null)
   let loginForm = reactive({
     username: '',
     password: ''
   })
   const isLoading = ref(false)
   
   const rules = {
     username: [
       { required: true, message: '请输入用户名', trigger: 'blur' },
       {  max: 10, message: '最多为10个字符', trigger: 'change' }   
     ],
     password: [
       { required: true, message: '请输入密码', trigger: 'blur' },
       { min: 1, message: '密码长度至少为6个字符', trigger: 'change' }
     ]
   }
   
   function handleSubmit() {
     loginFormRef.value.validate(async (valid) => {
       if (valid) {
         try {
           isLoading.value = true
           const response = await axios.post(`${API_URL}/login`, {
             username: loginForm.username,
             password: loginForm.password
           })

           if (response.data.code === 200) {
               ElMessage.success(response.data.message)
                  localStorage.setItem('username',response.data.username)
                  localStorage.setItem('userid',response.data.userid)
                router.push( {name: 'zhuye'})
           } else {
             ElMessage.error(response.data.message)  
             loginForm.password=''
           }
         } catch (error) {
           ElMessage.error('登录失败: ' + (error.response.data.message || '网络错误，请稍后重试'))
         } finally {
           isLoading.value = false
         }
       }
     })
   }
   
  
   
   </script>
   
   <style scoped>
   .login-container {
     display: flex;
     justify-content: center;
     align-items: center;
     min-height: 100vh;
     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 


     padding: 20px;
     box-sizing: border-box;
     overflow: hidden; /* 防止卡片过大时出现滚动条 */
   }
   
   .login-card {
     width: 100%;
     max-width: 420px; /* 稍微增加宽度 */
     padding: 30px; /* 调整内边距 */
     border-radius: 16px; /* 更大的圆角 */
     box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1), 0 4px 12px rgba(0,0,0,0.05); /* 更柔和的阴影 */
     text-align: center;
     background-color: #ffffff;
     overflow: hidden; /* 确保子元素不会溢出圆角 */
     transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
   }
   
   .login-card:hover {
     transform: translateY(-5px);
     box-shadow: 0 18px 40px rgba(0, 0, 0, 0.15), 0 6px 18px rgba(0,0,0,0.08);
   }
   
   .login-header {
     display: flex;
     flex-direction: column; /* Logo 和公司名垂直排列 */
     align-items: center;
     margin-bottom: 30px;
   }
   
   .logo {
     width: 100px; 
     height: 100px;
     margin-bottom: 15px; 
   }
   
   .company-name {
     font-size: 24px; /* 增大字体 */
     font-weight: 700; /* 加粗 */
     color: #303133; /* 深色，更稳重 */
     margin: 0;
   }
   
   .login-form {
     width: 100%;
   }
   
   .login-form .el-form-item {
     margin-bottom: 25px; /* 增加表单项间距 */
   }
   
   /* 使用 Element Plus 的变量或直接覆盖 */
   .login-form :deep(.el-input__wrapper) {
     border-radius: 8px; /* 输入框圆角 */
     box-shadow: 0 2px 4px rgba(0,0,0,0.03) inset; /* 轻微内阴影 */
   }
   
   .login-form :deep(.el-input__inner) {
     height: 48px; /* 增加输入框高度 */
     line-height: 48px;
     font-size: 16px;
   }
   
   .login-button {
     width: 100%; /* 按钮宽度充满 */
     height: 50px; /* 增加按钮高度 */
     font-size: 18px; /* 增大字体 */
     border-radius: 8px; /* 按钮圆角 */
     background: linear-gradient(135deg, #5a78f0 0%, #7a52cc 100%); /* 按钮渐变 */
     border: none;
     font-weight: 500;
     transition: background 0.3s ease, transform 0.2s ease;
     margin-top: 10px; /* 与上方表单项的间距 */
   }
   
   .login-button:hover {
     background: linear-gradient(135deg, #4e67d4 0%, #6c46b0 100%);
     transform: translateY(-2px);
   }
   
   .login-button:active {
     transform: translateY(0px);
   }
   
   /* 移除第二个 style 块中不再需要的样式，或者合并 */
   /* 如果有其他全局或特定组件的样式，可以保留，但 Login.vue 相关的建议合并 */
   
   /* 以下是原第二个 style 块的内容，根据需要保留或移除 */
   /* .item { ... } */
   /* .details { ... } */
   /* i { ... } */
   /* h3 { ... } */
   /* @media (min-width: 1024px) { ... } */
   </style>
   
   <style scoped>
   .item {
     margin-top: 2rem;
     display: flex;
     position: relative;
   }
   
   .details {
     flex: 1;
     margin-left: 1rem;
   }
   
   i {
     display: flex;
     place-items: center;
     place-content: center;
     width: 32px;
     height: 32px;
     color: var(--color-text);
   }
   
   h3 {
     font-size: 1.2rem;
     font-weight: 500;
     margin-bottom: 0.4rem;
     color: var(--color-heading);
   }
   
   @media (min-width: 1024px) {
     .item {
       margin-top: 0;
       padding: 0.4rem 0 1rem calc(var(--section-gap) / 2);
     }
   
     i {
       top: calc(50% - 25px);
       left: -26px;
       position: absolute;
       border: 1px solid var(--color-border);
       background: var(--color-background);
       border-radius: 8px;
       width: 50px;
       height: 50px;
     }
   
     .item:before {
       content: ' ';
       border-left: 1px solid var(--color-border);
       position: absolute;
       left: 0;
       bottom: calc(50% + 25px);
       height: calc(50% - 25px);
     }
   
     .item:after {
       content: ' ';
       border-left: 1px solid var(--color-border);
       position: absolute;
       left: 0;
       top: calc(50% + 25px);
       height: calc(50% - 25px);
     }
   
     .item:first-of-type:before {
       display: none;
     }
   
     .item:last-of-type:after {
       display: none;
     }
   }
   .login-form :deep(.el-form-item.is-error .el-input__wrapper) {
     box-shadow: 0 0 0 1px var(--el-color-danger) inset; /* 仅在错误时显示红色边框 */
   }
   
   .login-form :deep(.el-form-item__error) {
     padding-top: 2px; /* 调整错误信息位置 */
     font-size: 12px;
   }
   
   /* 隐藏el-input自带的校验成功和失败的图标 */
   .login-form :deep(.el-input__suffix .el-input__validateIcon) {
     display: none !important;
   }
   </style>
   
  
