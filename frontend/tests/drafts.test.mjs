import { test } from 'node:test'
import assert from 'node:assert/strict'
import { effectScope, ref } from 'vue'
import { useLocalDraft } from '../src/composables/useLocalDraft.js'

test('drafts survive remount and stay separate by account and topic', () => {
  const storage = new Map()
  globalThis.localStorage = { getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value), removeItem: key => storage.delete(key) }
  const key = ref('user:1:topic:1')
  const content = ref('')
  let draft
  function mount() {
    const scope = effectScope()
    scope.run(() => { draft = useLocalDraft(key, () => ({ content: content.value }), value => { content.value = value.content }, () => ({ content: '' })) })
    return scope
  }
  let scope = mount()
  content.value = 'Mon long RP'
  scope.stop()
  content.value = ''
  scope = mount()
  assert.equal(content.value, 'Mon long RP')
  key.value = 'user:2:topic:1'
  assert.equal(content.value, '')
  content.value = 'Autre compte'
  key.value = 'user:1:topic:2'
  assert.equal(content.value, '')
  key.value = 'user:1:topic:1'
  assert.equal(content.value, 'Mon long RP')
  draft.clear()
  content.value = ''
  assert.equal(storage.has(key.value), false)
  assert.equal(JSON.parse(storage.get('user:2:topic:1')).value.content, 'Autre compte')
  scope.stop()
})

test('unavailable storage keeps entered text and reports the problem', () => {
  globalThis.localStorage = { getItem() { throw Error('blocked') }, setItem() { throw Error('full') } }
  const scope = effectScope()
  scope.run(() => {
    const key = ref('draft')
    const content = ref('')
    const draft = useLocalDraft(key, () => ({ content: content.value }), value => { content.value = value.content }, () => ({ content: '' }))
    content.value = 'Texte à conserver'
    assert.equal(content.value, 'Texte à conserver')
    assert.match(draft.status.value, /impossible/)
  })
  scope.stop()
})
