import { ref, watch } from 'vue'

// Each draft belongs to one account and one editor on this browser.
export function useLocalDraft(key, read, restore, empty) {
  const status = ref('')
  let restoring = false
  watch(key, (current) => {
    restoring = true
    restore(empty())
    status.value = ''
    if (current) {
      try {
        const saved = JSON.parse(localStorage.getItem(current) || 'null')
        if (saved && saved.value && typeof saved.value === 'object' &&
            Object.keys(empty()).every(name => typeof saved.value[name] === 'string')) {
          restore(saved.value)
          status.value = 'Brouillon restauré sur cet appareil'
        }
      } catch { status.value = 'Sauvegarde locale indisponible' }
    }
    restoring = false
  }, { immediate: true, flush: 'sync' })
  watch(read, (value) => {
    if (restoring || !key.value) return
    try {
      if (Object.values(value).some(text => text.trim())) {
        localStorage.setItem(key.value, JSON.stringify({ value, savedAt: Date.now() }))
        status.value = 'Brouillon sauvegardé sur cet appareil'
      } else {
        localStorage.removeItem(key.value)
        status.value = ''
      }
    } catch { status.value = 'Sauvegarde impossible : gardez une copie de votre texte' }
  }, { deep: true, flush: 'sync' })
  function clear(savedKey = key.value) {
    if (!savedKey) return
    try {
      localStorage.removeItem(savedKey)
      if (savedKey === key.value) status.value = ''
    } catch { status.value = 'Impossible d’effacer le brouillon local' }
  }
  return { status, clear }
}
