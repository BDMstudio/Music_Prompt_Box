import { ref } from 'vue'

const showToast = ref(false)
const toastMessage = ref('')

let toastTimeout: ReturnType<typeof setTimeout> | null = null

export function useClipboard() {
  async function copy(text: string, message: string = '已复制') {
    try {
      await navigator.clipboard.writeText(text)
      toastMessage.value = message
      showToast.value = true
      
      if (toastTimeout) {
        clearTimeout(toastTimeout)
      }
      
      toastTimeout = setTimeout(() => {
        showToast.value = false
      }, 2000)
      
      return true
    } catch {
      return false
    }
  }

  return {
    showToast,
    toastMessage,
    copy,
  }
}
