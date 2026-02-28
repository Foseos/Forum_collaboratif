import { ref, watchEffect } from 'vue'

const theme = ref(localStorage.getItem('theme') || 'light')

function applyTheme() {
  document.documentElement.classList.toggle('dark', theme.value === 'dark')
}

watchEffect(applyTheme)

export function useTheme() {
  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    localStorage.setItem('theme', theme.value)
  }

  return { theme, toggleTheme }
}
