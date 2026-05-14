import { ref, watch } from 'vue'

type Theme = 'light' | 'dark'

const STORAGE_KEY = 'mpb-theme'

// Module-level singleton — shared across all consumers
const current = ref<Theme>(loadTheme())

function loadTheme(): Theme {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored === 'dark' || stored === 'light') return stored
  // Respect system preference
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) return 'dark'
  return 'light'
}

function applyTheme(theme: Theme) {
  const html = document.documentElement
  if (theme === 'dark') {
    html.classList.add('dark')
  } else {
    html.classList.remove('dark')
  }
}

// Apply on import
applyTheme(current.value)

watch(current, (val) => {
  applyTheme(val)
  localStorage.setItem(STORAGE_KEY, val)
})

export function useTheme() {
  const isDark = ref(current.value === 'dark')

  watch(current, (val) => {
    isDark.value = val === 'dark'
  })

  function toggle() {
    current.value = current.value === 'dark' ? 'light' : 'dark'
  }

  function setTheme(theme: Theme) {
    current.value = theme
  }

  return {
    theme: current,
    isDark,
    toggle,
    setTheme,
  }
}
