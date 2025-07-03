import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useExpectationStore = defineStore('expectation', () => {
  const needsRefresh = ref(false)
  const triggerRefresh = () => {
    needsRefresh.value = true
  }
  
  const resetRefresh = () => {
    needsRefresh.value = false
  }
  
  return {
    needsRefresh,
    triggerRefresh,
    resetRefresh
  }
})