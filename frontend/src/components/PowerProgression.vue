<template>
  <section class="power-tracker" aria-label="Progression des pouvoirs validés">
    <h3>Progression des pouvoirs</h3>
    <p>4 pouvoirs de base à la création · 5e à l’achat · 2 évolutions maximum par pouvoir.</p>
    <p v-if="!powers.length">Le suivi détaillé sera renseigné par l’administration à partir de la fiche validée.</p>
    <div class="power-grid">
      <div v-for="(power, index) in slots" :key="index" class="power-slot">
        <div class="slot-heading">
          <span>{{ index === 4 ? '5e pouvoir · achat' : `Pouvoir ${index + 1}` }}</span>
          <strong>{{ power?.name || 'Emplacement libre' }}</strong>
        </div>
        <ol class="evolutions">
          <li v-for="level in 2" :key="level" :class="{ empty: !power?.evolutions?.[level - 1] }">
            Évolution {{ level }} : {{ power?.evolutions?.[level - 1] || 'À débloquer' }}
          </li>
        </ol>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ powers: { type: Array, default: () => [] } })
const slots = computed(() => Array.from({ length: 5 }, (_, index) => props.powers[index] || null))
</script>

<style scoped>
.power-tracker { border: 1px solid rgba(245, 215, 110, .3); border-radius: 9px; padding: 1rem; margin: 1rem 0; background: rgba(245, 215, 110, .04); }
.power-tracker h3 { color: var(--gold); margin: 0 0 .35rem; font-size: 1rem; }
.power-tracker p { margin: 0 0 .8rem; color: var(--text-muted); font-size: .8rem; }
.power-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: .6rem; }
.power-slot { border: 1px solid rgba(167, 139, 250, .25); border-radius: 7px; padding: .65rem; background: rgba(13, 10, 26, .3); }
.slot-heading { display: grid; gap: .2rem; }
.slot-heading span { color: #a78bfa; font-size: .72rem; }
.slot-heading strong { color: var(--text); font-size: .86rem; }
.evolutions { list-style: none; padding: 0; margin: .55rem 0 0; font-size: .75rem; line-height: 1.55; }
.evolutions li { color: var(--text); }
.evolutions li.empty { color: var(--text-muted); }
</style>
