import { ref } from 'vue'

const showToast = ref(false)
const toastMessage = ref('')

let toastTimeout: ReturnType<typeof setTimeout> | null = null

export function useClipboard() {
  async function copy(text: string, message: string = '已复制') {
    const showSuccess = () => {
      toastMessage.value = message
      showToast.value = true
      if (toastTimeout) clearTimeout(toastTimeout)
      toastTimeout = setTimeout(() => { showToast.value = false }, 2000)
    }

    try {
      await navigator.clipboard.writeText(text)
      showSuccess()
      return true
    } catch {
      // Clipboard API not available (non-secure context e.g. LAN HTTP).
      // Fallback to execCommand approach.
      return copyFallback(text, message)
    }
  }

  function copyFallback(text: string, message: string): boolean {
    try {
      const textarea = document.createElement('textarea')
      textarea.value = text
      textarea.style.position = 'fixed'
      textarea.style.opacity = '0'
      document.body.appendChild(textarea)
      textarea.select()
      const ok = document.execCommand('copy')
      document.body.removeChild(textarea)
      if (ok) {
        toastMessage.value = message
        showToast.value = true
        if (toastTimeout) clearTimeout(toastTimeout)
        toastTimeout = setTimeout(() => { showToast.value = false }, 2000)
        return true
      }
      return false
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
