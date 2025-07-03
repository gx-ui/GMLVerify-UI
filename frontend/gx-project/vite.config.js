import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import cdn from 'vite-plugin-cdn-import';

export default defineConfig({
  plugins: [
    cdn({
      modules: [
        {
          name: 'vue',
          var: 'Vue',
          path: 'https://unpkg.com/vue@3.5.13/dist/vue.global.js',
        },
        {
          name: 'element-plus',
          var: 'ElementPlus',
          path: 'https://unpkg.com/element-plus@2.9.9/dist/index.full.js',
          css: 'https://unpkg.com/element-plus@2.9.9/dist/index.css'
        },
      ],
    }),
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: { 
    host: '0.0.0.0',
    allowedHosts: ['39dl416aa932.vicp.fun']
  }
})
