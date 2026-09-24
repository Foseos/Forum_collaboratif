import { ref, watchEffect } from 'vue'

const theme = ref(localStorage.getItem('theme') || 'dark')

function applyTheme() {
  const html = document.documentElement
  html.classList.remove('dark', 'light')
  html.classList.add(theme.value)
}

watchEffect(applyTheme)

export function useTheme() {
  function toggleTheme() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
    localStorage.setItem('theme', theme.value)
  }

  return { theme, toggleTheme }
}
