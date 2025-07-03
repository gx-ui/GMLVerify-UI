import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../components/Login.vue')
    },
    {
      path: '/home',  
      name: 'zhuye',
      component: () => import('@/views/Home.vue'),
      children:[
        {
          path: 'new-assets',
          name: 'creat-assets',
          component: ()=>import('@/views/CreateDataAssets.vue')
        },
        {
          path: 'assets', 
          name: 'existing-assets',
          component: ()=>import('@/views/ExistingDataAssets.vue'),
    
        },
        {
          path: 'asset/:assetId/:dataSourceName/:assetName',
          name: 'assetDetail',  
          component: () => import('@/views/AssetDetail.vue'),
          props: true, 
          children:[
            {
              path: 'expectations', 
              redirect: 'expectations'
            },
            {
              path: 'expectations',
              name: 'AssetExpectations',
              component: () => import('@/views/detail/Expectations.vue'),
              props: true 
            },
            {
              path: 'validation',
              name: 'AssetValidations',
              component: () => import('@/views/detail/Validation.vue'),
              props: true 
            },
            {
              path: 'metric',
              name: 'AssetMetrics',
              component: () => import('@/views/detail/Metric.vue'),
              props: true 
            }
          ]
        }   
      ]
     
    },
    {
      // 默认重定向到登录页
      path: '/:pathMatch(.*)*',
      redirect: '/login'
    }
  ]
})

// 路由守卫，检查用户是否已登录
// router.beforeEach((to, from, next) => {
//   const token = localStorage.getItem('token')
  
//   // 如果用户访问的不是登录页且没有token，则重定向到登录页
//   if (to.path !== '/login' && !token) {
//     next('/login')
//   } else {
//     next()
//   }
// })

export default router