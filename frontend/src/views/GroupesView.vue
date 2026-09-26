<template>
  <div class="page">
    <div class="container">

    <!-- ── Page Header ─────────────────────────────────────────── -->
    <div class="pg-header animate-fade-in-up">
      <div class="pg-header-icon">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
          <circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
      </div>
      <div>
        <h1 class="page-title text-gradient">Factions & Espèces</h1>
        <p class="page-subtitle">Les forces qui façonnent les univers de Nexus Arcana</p>
      </div>
    </div>

    <!-- ── Section Factions ────────────────────────────────────── -->
    <section class="gs-section">
      <div class="gs-section-head">
        <span class="gs-label">⚔️ Organisations</span>
        <h2 class="gs-section-title">Factions & Alliances</h2>
      </div>

      <div class="factions-grid">
        <button
          v-for="(g, i) in factions"
          :key="g.id"
          class="faction-card animate-fade-in-up"
          :class="{ 'faction-card--four': g.id === 'pouvoir-des-quatre' }"
          :style="{ '--glow': g.theme.glow, '--tc': g.theme.accent, animationDelay: `${i * 0.08}s` }"
          @click="openModal(g)"
        >
          <!-- Background -->
          <div class="fc-bg">
            <img v-if="g.imageUrl" :src="g.imageUrl" class="fc-bg-img" :alt="g.name" />
            <div
              class="fc-overlay"
              :class="{ 'fc-overlay-img': g.imageUrl }"
              :style="!g.imageUrl ? { background: g.theme.gradient } : {}"
            ></div>
          </div>

          <!-- Emoji top-left (only for non-image cards) -->
          <span v-if="!g.imageUrl" class="fc-emoji">{{ g.emoji }}</span>

          <!-- Content anchored to bottom -->
          <div class="fc-body">
            <h3 class="fc-name">{{ g.name }}</h3>
            <p class="fc-desc">{{ g.description }}</p>
            <div class="fc-footer">
              <span v-if="g.members != null" class="fc-count">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
                {{ g.members }}
              </span>
              <span class="fc-cta">Découvrir →</span>
            </div>
          </div>
        </button>
      </div>
    </section>

    <!-- ── Section Espèces ─────────────────────────────────────── -->
    <section class="gs-section">
      <div class="gs-section-head">
        <span class="gs-label">📖 Les archives du Nexus</span>
        <h2 class="gs-section-title">Codex des espèces</h2>
      </div>
      <p class="codex-intro">Parcourez les espèces des quatre villes. Chaque fiche présente leur nature, leurs dons et leurs limites dans l'univers de Nexus Arcana.</p>
      <router-link class="codex-official-link" to="/topics/encyclopedie-des-creatures-et-races">Consulter le bottin complet des créatures et des profils →</router-link>

      <div class="codex-layout">
        <nav class="codex-index" aria-label="Sommaire des espèces">
          <div v-for="family in codexFamilies" :key="family.title" class="codex-family">
            <h3>{{ family.title }}</h3>
            <p>{{ family.subtitle }}</p>
            <div class="codex-links">
              <button
                v-for="g in family.groups"
                :key="g.id"
                type="button"
                class="codex-link"
                :class="{ 'codex-link--active': selectedRace?.id === g.id }"
                :aria-current="selectedRace?.id === g.id ? 'true' : undefined"
                @click="selectedRace = g"
              >{{ g.emoji || '◈' }} {{ g.name }}<span v-if="raceSpecialties[g.id]?.length" class="codex-link-count">{{ raceSpecialties[g.id].length }}</span></button>
            </div>
          </div>
        </nav>

        <article v-if="selectedRace" class="codex-entry" :style="{ '--codex-accent': selectedRace.theme.accent }">
          <div class="codex-entry-head" :style="{ background: selectedRace.theme.gradient }">
            <span class="codex-entry-icon">{{ selectedRace.emoji || '◈' }}</span>
            <div>
              <span class="codex-eyebrow">Fiche du codex</span>
              <h3>{{ selectedRace.name }}</h3>
              <p>{{ raceCodex[selectedRace.id]?.origine }}</p>
            </div>
          </div>
          <div class="codex-entry-body">
            <section class="codex-chapter">
              <h4>Nature</h4>
              <p>{{ selectedRace.description }}</p>
            </section>
            <section class="codex-chapter">
              <h4>Dons et capacités</h4>
              <p>{{ raceCodex[selectedRace.id]?.dons }}</p>
            </section>
            <section v-if="raceCodex[selectedRace.id]?.baguesDeJour" class="codex-chapter">
              <h4>Bagues de jour</h4>
              <p>{{ raceCodex[selectedRace.id].baguesDeJour }}</p>
            </section>
            <section v-if="raceSpecialties[selectedRace.id]?.length" class="codex-chapter">
              <h4>Branches, affinités et profils</h4>
              <p class="codex-specialty-intro">Ces choix orientent la fiche du personnage. Ils ne donnent pas automatiquement tous les pouvoirs cités.</p>
              <ul class="codex-specialties">
                <li v-for="specialty in raceSpecialties[selectedRace.id]" :key="specialty.name">
                  <strong>{{ specialty.name }}</strong>
                  <p>{{ specialty.description }}</p>
                </li>
              </ul>
            </section>
            <section class="codex-chapter">
              <h4>Limites</h4>
              <p>{{ raceCodex[selectedRace.id]?.limites }}</p>
            </section>
            <section class="codex-chapter codex-chapter--note">
              <h4>Dans la Convergence</h4>
              <p>Les personnages de cette espèce peuvent désormais croiser les habitants des quatre villes. Leur histoire, leurs pouvoirs précis et leurs éventuelles hybridations sont définis dans leur fiche de personnage validée.</p>
            </section>
            <button type="button" class="codex-members-btn" @click="openModal(selectedRace)">Voir les membres de cette espèce →</button>
          </div>
        </article>
      </div>
    </section>

    <!-- ── Modal ───────────────────────────────────────────────── -->
    <Teleport to="body">
      <Transition name="modal-anim">
        <div
          v-if="selectedGroup"
          class="modal-overlay"
          @click.self="closeModal"
          role="dialog"
          aria-modal="true"
          :aria-label="selectedGroup.name"
        >
          <div
            class="modal-panel"
            :style="{ '--mglow': selectedGroup.theme.glow, '--maccent': selectedGroup.theme.accent }"
          >
            <!-- Modal Header -->
            <div class="modal-head" :style="{ background: selectedGroup.theme.gradient }">

              <!-- Floating particles -->
              <div class="mp-wrap" aria-hidden="true">
                <span v-for="n in 10" :key="n" class="mp" :style="mpStyle(n)">
                  {{ selectedGroup.theme.particle }}
                </span>
              </div>

              <!-- Icon -->
              <div class="mh-icon">
                <img v-if="selectedGroup.imageUrl" :src="selectedGroup.imageUrl" class="mh-img" :alt="selectedGroup.name" />
                <span v-else class="mh-emoji">{{ selectedGroup.emoji }}</span>
              </div>

              <!-- Texts -->
              <div class="mh-text">
                <h2 class="mh-title">{{ selectedGroup.name }}</h2>
                <p class="mh-mood">{{ selectedGroup.theme.mood }}</p>
              </div>

              <!-- Close -->
              <button class="mh-close" @click="closeModal" aria-label="Fermer">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>

            <!-- Modal Body -->
            <div class="modal-body">
              <div v-if="selectedGroup.id === 'pouvoir-des-quatre' && selectedGroup.imageUrl" class="four-portrait-preview">
                <img :src="selectedGroup.imageUrl" alt="Les quatre visages du Pouvoir des Quatre" />
              </div>
              <p class="modal-lore">{{ selectedGroup.description }}</p>
              <router-link
                v-if="selectedGroup.scenario"
                class="modal-scenario-link"
                :to="{ name: 'topic', params: { slug: selectedGroup.scenario.slug } }"
              >Voir le scénario de {{ selectedGroup.scenario.nom }} →</router-link>
              <section v-if="selectedGroup.type === 'race' && raceSpecialties[selectedGroup.id]?.length" class="modal-specialties">
                <h3>Branches, affinités et profils</h3>
                <p>{{ raceSpecialties[selectedGroup.id].map(item => item.name).join(' · ') }}</p>
              </section>
              <section v-if="factionRoles[selectedGroup.id]" class="modal-role-powers">
                <h3>Pouvoirs selon le rôle</h3>
                <p class="modal-role-note">Le rôle impose quatre facultés qui occupent les quatre emplacements de base. Elles ne s’ajoutent pas aux pouvoirs de base. <span v-if="selectedGroup.id === 'Les cavaliers de l\'apocalypse'">Chaque Cavalier possède quatre facultés définies ; aucune ne provoque automatiquement la mort.</span> Les effets sur autrui se jouent avec les personnes concernées.</p>
                <div v-for="role in factionRoles[selectedGroup.id]" :key="role.name" class="modal-role-card">
                  <h4>{{ role.symbol }} {{ role.name }}<span v-if="role.element"> — {{ role.element }}</span></h4>
                  <ul>
                    <li v-for="power in role.powers" :key="power.name"><strong>{{ power.name }}</strong> — {{ power.description }}</li>
                  </ul>
                </div>
              </section>

              <div
                class="modal-sep"
                :style="{ background: `linear-gradient(90deg, transparent, ${selectedGroup.theme.accent}, transparent)` }"
              ></div>

              <!-- Members section -->
              <div class="modal-members">
                <div class="mm-header">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                    <circle cx="9" cy="7" r="4"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                  </svg>
                  <h3 class="mm-title">Membres du groupe</h3>
                  <span class="mm-count" :style="{ color: selectedGroup.theme.accent }">
                    {{ loadingMembers ? '…' : groupMembers.length }}
                  </span>
                  <button
                    v-if="isAdmin"
                    class="mm-admin-btn"
                    :style="{ '--maccent': selectedGroup.theme.accent }"
                    @click="showAddMember = !showAddMember"
                  >
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                    Ajouter
                  </button>
                </div>

                <!-- Admin : formulaire d'ajout -->
                <div v-if="isAdmin && showAddMember" class="admin-add">
                  <label v-if="selectedGroup.type === 'race' && raceSpecialties[selectedGroup.id]?.length" class="admin-specialty-label">
                    Spécialité du membre
                    <select v-model="selectedSpecialty" class="admin-specialty-select">
                      <option value="">Sans spécialité précisée</option>
                      <option v-for="specialty in raceSpecialties[selectedGroup.id]" :key="specialty.name" :value="profileRaceName(specialty.name, selectedGroup.id)">{{ profileRaceName(specialty.name, selectedGroup.id) }}</option>
                    </select>
                  </label>
                  <div class="admin-add-row">
                    <input
                      v-model="addMemberSearch"
                      class="admin-add-input"
                      placeholder="Nom du membre…"
                      :style="{ '--maccent': selectedGroup.theme.accent }"
                      @keyup.enter="searchUser"
                    />
                    <button
                      class="admin-add-search-btn"
                      :style="{ '--maccent': selectedGroup.theme.accent }"
                      :disabled="addMemberLoading"
                      @click="searchUser"
                    >
                      {{ addMemberLoading ? '…' : 'Chercher' }}
                    </button>
                  </div>
                  <p v-if="addMemberSuccess" class="admin-msg admin-msg--ok">✓ {{ addMemberSuccess }}</p>
                  <p v-if="addMemberError"   class="admin-msg admin-msg--err">{{ addMemberError }}</p>
                  <div v-if="addMemberResults.length > 0" class="admin-results">
                    <button
                      v-for="u in addMemberResults"
                      :key="u.id"
                      class="admin-result"
                      :disabled="addMemberLoading"
                      @click="confirmAddMember(u)"
                    >
                      <div class="admin-av">{{ u.username?.[0]?.toUpperCase() }}</div>
                      <div class="admin-info">
                        <span class="admin-pseudo">{{ u.username }}</span>
                        <span v-if="u.pseudo" class="admin-login">Pseudo RP : {{ u.pseudo }}</span>
                      </div>
                      <span class="admin-cta" :style="{ color: selectedGroup.theme.accent }">+ Ajouter</span>
                    </button>
                  </div>
                </div>

                <!-- Loading -->
                <div v-if="loadingMembers" class="mm-loading">
                  <span class="mm-spinner" :style="{ borderTopColor: selectedGroup.theme.accent }"></span>
                  <span>Invocation des membres...</span>
                </div>

                <!-- Empty (aucun membre dans ce groupe) -->
                <div v-else-if="groupMembers.length === 0 && !memberSearch" class="mm-empty">
                  <span class="mm-empty-icon">{{ selectedGroup.theme.particle }}</span>
                  <p>Aucun membre n'a rejoint ce groupe pour le moment.</p>
                </div>

                <!-- Search -->
                <div v-if="groupMembers.length > 5" class="mm-search-wrap">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                  </svg>
                  <input
                    v-model="memberSearch"
                    class="mm-search"
                    placeholder="Rechercher un membre..."
                    :style="{ '--maccent': selectedGroup.theme.accent }"
                  />
                </div>

                <!-- No search results -->
                <div v-if="filteredMembers.length === 0 && memberSearch" class="mm-empty">
                  <span class="mm-empty-icon">🔍</span>
                  <p>Aucun membre ne correspond à "{{ memberSearch }}".</p>
                </div>

                <!-- Grid -->
                <div v-else class="mm-grid" :class="{ 'mm-grid--many': groupMembers.length > 10 }">
                  <div
                    v-for="m in filteredMembers"
                    :key="m.id"
                    class="mm-member"
                    :class="{ 'mm-member--compact': groupMembers.length > 10 }"
                  >
                    <div class="mm-av" :style="{ boxShadow: `0 0 12px ${selectedGroup.theme.glow}` }">
                      <img v-if="m.avatar" :src="m.avatar" :alt="m.username" />
                      <span v-else>{{ m.username?.[0]?.toUpperCase() }}</span>
                    </div>
                    <div class="mm-info">
                      <span class="mm-pseudo">{{ m.username }}</span>
                      <span v-if="m.pseudo && m.pseudo !== m.username" class="mm-login">Pseudo RP : {{ m.pseudo }}</span>
                      <span
                        v-if="m.race"
                        class="mm-race"
                        :style="{ borderColor: selectedGroup.theme.accent, color: selectedGroup.theme.accent }"
                      >{{ m.race }}</span>
                    </div>
                    <button
                      v-if="isAdmin"
                      class="mm-remove-btn"
                      :disabled="removing[m.id]"
                      title="Retirer du groupe"
                      @click.stop="removeMember(m)"
                    >
                      <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                      </svg>
                    </button>
                  </div>
                </div>

              </div>
            </div>

          </div>
        </div>
      </Transition>
    </Teleport>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import api from '../composables/useApi'
import groupesData from '../data/groupes.json'
import { raceCodex, raceFamilies } from '../data/raceCodex'
import raceSpecialties from '../data/raceSpecialties.json'
import factionRoles from '../data/factionRoles.json'
import { useAuthStore } from '../stores/auth'

// ── Thèmes par groupe ──────────────────────────────────────────────────────
const THEMES = {
  'pouvoir-des-quatre': {
    gradient: 'linear-gradient(135deg,#4c1d95,#7c3aed,#c084fc)',
    glow: 'rgba(139,92,246,0.55)', accent: '#c084fc', particle: '✨',
    mood: 'Unis par le sang, liés par la destinée',
  },
  'etre-de-lumiere': {
    gradient: 'linear-gradient(135deg,#78350f,#d97706,#f0c674)',
    glow: 'rgba(240,198,116,0.5)', accent: '#f0c674', particle: '🕊️',
    mood: 'Gardiens célestes des âmes innocentes',
  },
  'la-triade': {
    gradient: 'linear-gradient(135deg,#450a0a,#7f1d1d,#ef4444)',
    glow: 'rgba(239,68,68,0.6)', accent: '#f87171', particle: '🔥',
    mood: "Le mal absolu régit l'Inframonde",
  },
  'fondateurs': {
    gradient: 'linear-gradient(135deg,#1e3a5f,#1d4ed8,#60a5fa)',
    glow: 'rgba(96,165,250,0.5)', accent: '#60a5fa', particle: '⚖️',
    mood: 'La justice divine préside le cosmos',
  },
  'demon': {
    gradient: 'linear-gradient(135deg,#0a0014,#1e1b4b,#4c1d95)',
    glow: 'rgba(76,29,149,0.55)', accent: '#a78bfa', particle: '💀',
    mood: "Depuis les abysses, les ténèbres surgissent",
  },
  "Les veilleurs de l'aube": {
    gradient: 'linear-gradient(135deg,#713f12,#b45309,#f0c674)',
    glow: 'rgba(202,138,4,0.5)', accent: '#fbbf24', particle: '🌅',
    mood: "À l'aube, les veilleurs ouvrent les yeux",
  },
  'Les cavaliers de l\'apocalypse': {
    gradient: 'linear-gradient(135deg,#1a0a2e,#3b0764,#7e22ce)',
    glow: 'rgba(126,34,206,0.6)', accent: '#c084fc', particle: '🌑',
    mood: "La fin des temps chevauche à l'horizon",
  },
  'Les gardiens des sceaux primordiaux': {
    gradient: 'linear-gradient(135deg,#0c1445,#1e3a8a,#2563eb)',
    glow: 'rgba(37,99,235,0.5)', accent: '#93c5fd', particle: '🔒',
    mood: 'Les sceaux éternels ne doivent jamais briser',
  },
  'meute-beacon-hills': {
    gradient: 'linear-gradient(135deg,#10251c,#166534,#65a30d)',
    glow: 'rgba(101,163,13,0.45)', accent: '#bef264', particle: '🐺',
    mood: 'Unis pour protéger Beacon Hills et le Nemeton',
  },
  'gardiens-mystic-falls': {
    gradient: 'linear-gradient(135deg,#172554,#1e40af,#3b82f6)',
    glow: 'rgba(59,130,246,0.45)', accent: '#93c5fd', particle: '🔍',
    mood: 'Les secrets de Mystic Falls ne restent jamais enfouis',
  },
  'maison-seconde-soif': {
    gradient: 'linear-gradient(135deg,#290b18,#651b3b,#a33762)',
    glow: 'rgba(163,55,98,0.5)', accent: '#f9a8c5', particle: '🩸',
    mood: 'Deux soifs, une famille choisie',
  },
  'chambre-murmures': {
    gradient: 'linear-gradient(135deg,#1b1238,#4c1d95,#7c3aed)',
    glow: 'rgba(124,58,237,0.5)', accent: '#c4b5fd', particle: '🗝️',
    mood: "L'Expression ouvre des chemins à explorer avec prudence",
  },
  'heritiers-vide': {
    gradient: 'linear-gradient(135deg,#101e38,#1e3a5f,#3975a3)',
    glow: 'rgba(57,117,163,0.45)', accent: '#a5d8f2', particle: '✧',
    mood: 'La magie se cherche, se partage et se négocie',
  },
  'veilleurs-voile': {
    gradient: 'linear-gradient(135deg,#3b1d0b,#92400e,#d97706)',
    glow: 'rgba(217,119,6,0.45)', accent: '#fcd34d', particle: '🕯️',
    mood: 'Écouter les ancêtres sans renoncer à choisir',
  },
  'cercle-terres-perdues': {
    gradient: 'linear-gradient(135deg,#153324,#166534,#3f8a62)',
    glow: 'rgba(63,138,98,0.45)', accent: '#a7f3d0', particle: '🧭',
    mood: 'Leur chemin relie les terres et les traditions',
  },
  'Sorcier Charmed': {
    gradient: 'linear-gradient(135deg,#2e1065,#6d28d9,#a78bfa)',
    glow: 'rgba(109,40,217,0.5)', accent: '#a78bfa', particle: '🔮',
    mood: "La magie coule dans leurs veines depuis l'aube des temps",
  },
  'Elfe': {
    gradient: 'linear-gradient(135deg,#052e16,#166534,#4ade80)',
    glow: 'rgba(74,222,128,0.4)', accent: '#86efac', particle: '🌿',
    mood: "Gardiens millénaires de l'équilibre naturel",
  },
  'Cupidon': {
    gradient: 'linear-gradient(135deg,#831843,#be185d,#f9a8d4)',
    glow: 'rgba(190,24,93,0.5)', accent: '#f9a8d4', particle: '💘',
    mood: "L'amour est la magie la plus puissante qui soit",
  },
  'Phoenix': {
    gradient: 'linear-gradient(135deg,#7c2d12,#ea580c,#fb923c)',
    glow: 'rgba(234,88,12,0.5)', accent: '#fdba74', particle: '🔥',
    mood: "Des cendres, ils renaissent plus forts qu'avant",
  },
  'Valkyrie': {
    gradient: 'linear-gradient(135deg,#1a1a2e,#374151,#d4af37)',
    glow: 'rgba(212,175,55,0.5)', accent: '#fbbf24', particle: '⚔️',
    mood: "Seules les plus vaillantes sont choisies par les dieux",
  },
  'Nymphe/Satyre': {
    gradient: 'linear-gradient(135deg,#052e16,#14532d,#65a30d)',
    glow: 'rgba(101,163,13,0.45)', accent: '#a3e635', particle: '🌿',
    mood: "La forêt respire, et ils respirent avec elle",
  },
  'Humain': {
    gradient: 'linear-gradient(135deg,#1e293b,#475569,#94a3b8)',
    glow: 'rgba(148,163,184,0.3)', accent: '#cbd5e1', particle: '🌟',
    mood: 'Leur force réside dans leur humanité même',
  },
  'Sirène/Triton Charmed': {
    gradient: 'linear-gradient(135deg,#0c4a6e,#0284c7,#38bdf8)',
    glow: 'rgba(56,189,248,0.5)', accent: '#7dd3fc', particle: '🌊',
    mood: "Les profondeurs n'ont aucun secret pour eux",
  },
  'Sorcier': {
    gradient: 'linear-gradient(135deg,#20104a,#4c1d95,#c084fc)',
    glow: 'rgba(192,132,252,0.48)', accent: '#ddd6fe', particle: '🕯️',
    mood: "Les lignées, les covens et les ancêtres guident leur magie",
  },
  'Sirène': {
    gradient: 'linear-gradient(135deg,#0f172a,#164e63,#22d3ee)',
    glow: 'rgba(34,211,238,0.46)', accent: '#a5f3fc', particle: '🎶',
    mood: "Leur appel traverse les esprits et les frontières de l'au-delà",
  },
  'Vampire': {
    gradient: 'linear-gradient(135deg,#1c0000,#7f1d1d,#b91c1c)',
    glow: 'rgba(185,28,28,0.55)', accent: '#fca5a5', particle: '🩸',
    mood: "L'éternité est leur malédiction et leur don",
  },
  'Loup-garou': {
    gradient: 'linear-gradient(135deg,#1c1917,#44403c,#78716c)',
    glow: 'rgba(120,113,108,0.4)', accent: '#d6d3d1', particle: '🌕',
    mood: 'La pleine lune éveille la bête qui sommeille',
  },
  'Fée': {
    gradient: 'linear-gradient(135deg,#14532d,#15803d,#86efac)',
    glow: 'rgba(134,239,172,0.4)', accent: '#bbf7d0', particle: '🌸',
    mood: 'La magie des fleurs et des forêts les guide',
  },
  'Muse': {
    gradient: 'linear-gradient(135deg,#1e1040,#6b21a8,#e879f9)',
    glow: 'rgba(232,121,249,0.45)', accent: '#f0abfc', particle: '🎨',
    mood: "Là où elles passent, l'art et la vie s'éveillent",
  },
  'Hybride': {
    gradient: 'linear-gradient(135deg,#312e81,#7c3aed,#ec4899)',
    glow: 'rgba(236,72,153,0.4)', accent: '#f0abfc', particle: '⚡',
    mood: 'Entre deux mondes, leur puissance est sans limite',
  },
}

const DEFAULT_THEME = {
  gradient: 'linear-gradient(135deg,#1e1b4b,#4c1d95)',
  glow: 'rgba(139,92,246,0.4)', accent: '#c084fc', particle: '✨',
  mood: 'Un mystère plane sur ce groupe...',
}


const auth = useAuthStore()
const isAdmin = computed(() => auth.user?.role === 'fondatrice')

// ── Helpers ────────────────────────────────────────────────────────────────
function getIconUrl(icon) {
  if (icon && icon.includes('.')) {
    return new URL(`../assets/${icon}`, import.meta.url).href
  }
  return null
}

function buildGroup(g) {
  const isImage = g.icone && g.icone.includes('.')
  return {
    id: g.id,
    name: g.nom,
    description: g.description,
    emoji: isImage ? null : (g.icone || '◈'),
    imageUrl: isImage ? getIconUrl(g.icone) : null,
    members: g.membres_count ?? null,
    theme: THEMES[g.id] || DEFAULT_THEME,
    type: g.type || 'race',
    scenario: g.scenario || null,
  }
}

// ── Data ───────────────────────────────────────────────────────────────────
const allGroups = groupesData.map(buildGroup)
const factions  = computed(() => allGroups.filter(g => g.type === 'faction'))
const species   = computed(() => allGroups.filter(g => g.type === 'race'))
const codexFamilies = computed(() => raceFamilies.map(family => ({
  ...family,
  groups: family.ids.map(id => species.value.find(group => group.id === id)).filter(Boolean),
})))
const selectedRace = ref(species.value[0] || null)

// ── Fetch paginé des membres d'un groupe ──────────────────────────────────
async function fetchGroupMembers(group) {
  const filterKey = group.type === 'faction' ? 'groupe' : null
  const members = []
  let page = 1
  let hasMore = true

  while (hasMore) {
    const query = filterKey ? `${filterKey}=${encodeURIComponent(group.name)}&` : ''
    const { data } = await api.get(`/users/?${query}page=${page}`)
    if (data.results) {
      members.push(...data.results)
      hasMore = !!data.next
      page++
    } else {
      members.push(...(Array.isArray(data) ? data : []))
      hasMore = false
    }
  }
  if (group.type === 'faction') return members
  return members.filter(member => matchesRaceGroup(member.race, group))
}

function normalizeRace(value) {
  return (value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim()
}

function profileRaceName(name, raceId) {
  if (raceId === 'Fée') {
    return name.replace(/^Fées /, 'Fée ')
      .replace('sylvestres', 'sylvestre').replace('lumineuses', 'lumineuse').replace('noires', 'noire')
  }
  if (raceId === 'Kitsune') {
    return name.replace(/^Kitsunes /, 'Kitsune ').replace('soniques', 'sonique')
  }
  return name
}

function matchesRaceGroup(value, group) {
  const race = normalizeRace(value)
  if (!race) return false
  const name = normalizeRace(group.name)
  if (race === name || race.startsWith(`${name} `)) return true
  return (raceSpecialties[group.id] || []).some(specialty => {
    const branch = normalizeRace(specialty.name)
    return race === branch || race.startsWith(`${branch} `)
  })
}

// ── Admin : Ajouter un membre ──────────────────────────────────────────────
const showAddMember    = ref(false)
const addMemberSearch  = ref('')
const addMemberResults = ref([])
const addMemberLoading = ref(false)
const addMemberSuccess = ref('')
const addMemberError   = ref('')
const selectedSpecialty = ref('')

async function searchUser() {
  if (!addMemberSearch.value.trim()) return
  addMemberLoading.value = true
  addMemberSuccess.value = ''
  addMemberError.value   = ''
  try {
    const { data } = await api.get(`/users/?search=${encodeURIComponent(addMemberSearch.value)}`)
    addMemberResults.value = data.results || data
  } catch {
    addMemberError.value = 'Erreur lors de la recherche.'
  } finally {
    addMemberLoading.value = false
  }
}

async function confirmAddMember(user) {
  const group   = selectedGroup.value
  const payload = group.type === 'faction' ? { groupe: group.name } : { race: selectedSpecialty.value || group.name }
  addMemberLoading.value = true
  addMemberSuccess.value = ''
  addMemberError.value   = ''
  try {
    await api.patch(`/users/${user.id}/`, payload)
    addMemberSuccess.value = `${user.username} a été ajouté(e) à ${group.name}.`
    addMemberResults.value = []
    addMemberSearch.value  = ''
    groupMembers.value = await fetchGroupMembers(group)
  } catch {
    addMemberError.value = "Erreur lors de l'ajout du membre."
  } finally {
    addMemberLoading.value = false
  }
}

// ── Admin : Retirer un membre ──────────────────────────────────────────────
const removing = ref({})

async function removeMember(member) {
  const group = selectedGroup.value
  const payload = group.type === 'faction' ? { groupe: '' } : { race: '' }
  removing.value[member.id] = true
  try {
    await api.patch(`/users/${member.id}/`, payload)
    groupMembers.value = groupMembers.value.filter(m => m.id !== member.id)
  } finally {
    delete removing.value[member.id]
  }
}

// ── Modal ──────────────────────────────────────────────────────────────────
const selectedGroup  = ref(null)
const loadingMembers = ref(false)
const groupMembers   = ref([])
const memberSearch   = ref('')

const filteredMembers = computed(() => {
  if (!memberSearch.value.trim()) return groupMembers.value
  const q = memberSearch.value.toLowerCase()
  return groupMembers.value.filter(m =>
    (m.pseudo || '').toLowerCase().includes(q) ||
    m.username.toLowerCase().includes(q) ||
    (m.race || '').toLowerCase().includes(q)
  )
})

async function openModal(group) {
  selectedGroup.value    = group
  groupMembers.value     = []
  memberSearch.value     = ''
  loadingMembers.value   = true
  showAddMember.value    = false
  addMemberSearch.value  = ''
  addMemberResults.value = []
  addMemberSuccess.value = ''
  addMemberError.value   = ''
  selectedSpecialty.value = ''
  document.body.style.overflow = 'hidden'

  try {
    groupMembers.value = await fetchGroupMembers(group)
  } catch {
    groupMembers.value = []
  } finally {
    loadingMembers.value = false
  }
}

function closeModal() {
  selectedGroup.value    = null
  groupMembers.value     = []
  memberSearch.value     = ''
  showAddMember.value    = false
  addMemberSearch.value  = ''
  addMemberResults.value = []
  addMemberSuccess.value = ''
  addMemberError.value   = ''
  selectedSpecialty.value = ''
  document.body.style.overflow = ''
}

function handleKey(e) {
  if (e.key === 'Escape') closeModal()
}

// ── Positions particules (déterministes) ───────────────────────────────────
const PARTICLE_POS = [
  { left: 8,  top: 18 }, { left: 22, top: 65 }, { left: 42, top: 22 },
  { left: 58, top: 72 }, { left: 72, top: 28 }, { left: 85, top: 58 },
  { left: 15, top: 82 }, { left: 50, top: 42 }, { left: 90, top: 15 },
  { left: 35, top: 88 },
]

function mpStyle(n) {
  const p = PARTICLE_POS[(n - 1) % PARTICLE_POS.length]
  return {
    left: `${p.left}%`,
    top:  `${p.top}%`,
    animationDelay:    `${((n - 1) * 0.55) % 3}s`,
    animationDuration: `${2.5 + ((n - 1) % 4) * 0.6}s`,
    fontSize: `${0.6 + ((n - 1) % 3) * 0.22}rem`,
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKey)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKey)
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* ── Page Header ────────────────────────────────────────────────────────── */
.pg-header {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin-bottom: 3rem;
}

.pg-header-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-lg);
  background: var(--primary-light);
  border: 1px solid var(--glass-border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  flex-shrink: 0;
  box-shadow: 0 0 24px var(--primary-glow);
}

/* ── Section ────────────────────────────────────────────────────────────── */
.gs-section {
  margin-bottom: 3.5rem;
}

.gs-section-head {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.gs-label {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  background: var(--primary-light);
  border: 1px solid var(--glass-border);
  border-radius: 999px;
  padding: 0.25rem 0.75rem;
  white-space: nowrap;
}

.gs-section-title {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent), var(--gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ── Codex des espèces ──────────────────────────────────────────────────── */
.codex-intro { color: var(--text-secondary); line-height: 1.7; margin: 0 0 1.5rem; }
.codex-official-link { display: inline-block; color: var(--accent); margin: 0 0 1.5rem; font-weight: 700; text-decoration: none; }
.codex-official-link:hover { text-decoration: underline; }
.codex-layout { display: grid; grid-template-columns: minmax(240px, 300px) minmax(0, 1fr); gap: 1.4rem; align-items: start; }
.codex-index, .codex-entry { background: var(--glass-bg); border: 1px solid var(--border); border-radius: var(--radius-xl); overflow: hidden; }
.codex-index { padding: 1.25rem; max-height: 75vh; overflow-y: auto; }
.codex-family + .codex-family { border-top: 1px solid var(--border); margin-top: 1.2rem; padding-top: 1.2rem; }
.codex-family h3 { font-family: var(--font-display); font-size: 1rem; color: var(--text); margin: 0 0 .25rem; }
.codex-family p { color: var(--text-secondary); font-size: .75rem; line-height: 1.5; margin: 0 0 .7rem; }
.codex-links { display: flex; flex-direction: column; gap: .2rem; }
.codex-link { border: 0; border-radius: .55rem; background: transparent; color: var(--text-secondary); text-align: left; padding: .5rem .6rem; font: inherit; font-size: .82rem; cursor: pointer; }
.codex-link:hover, .codex-link--active { background: rgba(139,92,246,.16); color: var(--text); }
.codex-link--active { box-shadow: inset 3px 0 0 var(--accent); }
.codex-link-count { float: right; min-width: 1.3rem; margin-left: .5rem; padding: 0 .3rem; border-radius: 999px; background: rgba(139,92,246,.2); text-align: center; font-size: .7rem; }
.codex-entry-head { display: flex; align-items: center; gap: 1rem; padding: 2rem; color: #fff; }
.codex-entry-icon { font-size: 2.7rem; }
.codex-eyebrow { font-size: .68rem; text-transform: uppercase; letter-spacing: .16em; opacity: .85; }
.codex-entry-head h3 { font-family: var(--font-display); font-size: clamp(1.5rem, 3vw, 2.2rem); margin: .3rem 0; }
.codex-entry-head p { margin: 0; opacity: .88; }
.codex-entry-body { padding: 1.5rem 2rem 2rem; }
.codex-chapter { margin-bottom: 1.4rem; }
.codex-chapter h4 { color: var(--codex-accent); font-family: var(--font-display); font-size: 1rem; margin: 0 0 .45rem; }
.codex-chapter p { color: var(--text-secondary); line-height: 1.8; margin: 0; }
.codex-chapter .codex-specialty-intro { margin-bottom: .7rem; font-size: .84rem; }
.codex-specialties { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: .65rem; margin: 0; padding: 0; list-style: none; }
.codex-specialties li { padding: .75rem; border: 1px solid var(--border); border-radius: .65rem; background: rgba(139,92,246,.07); }
.codex-specialties strong { display: block; margin-bottom: .25rem; color: var(--codex-accent); font-size: .84rem; }
.codex-specialties li p { font-size: .77rem; line-height: 1.55; }
.codex-chapter--note { border-top: 1px solid var(--border); padding-top: 1.25rem; }
.codex-members-btn { border: 1px solid var(--codex-accent); border-radius: var(--radius); background: transparent; color: var(--codex-accent); padding: .7rem 1rem; font: inherit; cursor: pointer; }
.codex-members-btn:hover { background: rgba(139,92,246,.12); }

/* ── Factions Grid ──────────────────────────────────────────────────────── */
.factions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.25rem;
}

.faction-card {
  position: relative;
  height: 230px;
  border-radius: var(--radius-xl);
  overflow: hidden;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.07);
  transition: all var(--transition);
  text-align: left;
  background: none;
  color: #fff;
  padding: 0;
  box-shadow: var(--shadow);
}

.faction-card:hover {
  transform: translateY(-5px) scale(1.01);
  border-color: rgba(255, 255, 255, 0.14);
  box-shadow:
    var(--shadow-lg),
    0 0 32px var(--glow, rgba(139,92,246,0.4)),
    inset 0 1px 0 rgba(255,255,255,0.1);
}

/* Background layer */
.fc-bg {
  position: absolute;
  inset: 0;
}

.fc-bg-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(0.75) brightness(0.55);
  transition: transform var(--transition-slow), filter var(--transition);
}

.faction-card:hover .fc-bg-img {
  transform: scale(1.06);
  filter: saturate(0.9) brightness(0.65);
}

.fc-overlay {
  position: absolute;
  inset: 0;
  opacity: 0.8;
  transition: opacity var(--transition);
}

/* Gradient overlay for image cards */
.fc-overlay-img {
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.92) 0%,
    rgba(0, 0, 0, 0.52) 45%,
    rgba(0, 0, 0, 0.1) 100%
  ) !important;
  opacity: 1 !important;
}

/* Emoji (top-left, non-image cards) */
.fc-emoji {
  position: absolute;
  top: 1.5rem;
  left: 1.75rem;
  font-size: 2.25rem;
  filter: drop-shadow(0 0 14px rgba(255, 255, 255, 0.35));
  transition: transform var(--transition);
  z-index: 2;
}

.faction-card:hover .fc-emoji {
  transform: scale(1.15) rotate(-6deg);
}

/* Content block — anchored to bottom */
.fc-body {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 2;
  padding: 0 1.75rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.fc-name {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 700;
  color: #fff;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
  line-height: 1.2;
}

.fc-desc {
  font-size: 0.78rem;
  color: rgba(255, 255, 255, 0.72);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.fc-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.fc-count {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.76rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.82);
  background: rgba(0, 0, 0, 0.38);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 999px;
  padding: 0.22rem 0.625rem;
}

.fc-cta {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--tc, #c084fc);
  letter-spacing: 0.02em;
  transition: transform var(--transition);
  text-shadow: 0 0 12px var(--glow, rgba(192,132,252,0.5));
}

.faction-card:hover .fc-cta {
  transform: translateX(5px);
}

/* ── Species Grid ───────────────────────────────────────────────────────── */
.species-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 0.75rem;
}

.species-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.125rem;
  background: var(--card-bg);
  backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  text-align: left;
  color: var(--text);
  transition: all var(--transition);
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow);
}

.species-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 12%;
  bottom: 12%;
  width: 3px;
  background: var(--tc, var(--accent));
  border-radius: 0 2px 2px 0;
  opacity: 0;
  transition: opacity var(--transition);
}

.species-card:hover {
  border-color: var(--tc, var(--accent));
  box-shadow: var(--shadow), 0 0 18px var(--glow, rgba(139,92,246,0.25));
  transform: translateX(4px);
}

.species-card:hover::before {
  opacity: 1;
}

.sc-orb {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 1.45rem;
  box-shadow: 0 0 18px var(--glow, rgba(139,92,246,0.3));
  transition: transform var(--transition), box-shadow var(--transition);
}

.species-card:hover .sc-orb {
  transform: scale(1.12) rotate(8deg);
  box-shadow: 0 0 28px var(--glow, rgba(139,92,246,0.5));
}

.sc-emoji {
  filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.4));
}

.sc-body {
  flex: 1;
  min-width: 0;
}

.sc-name {
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 0.2rem;
  transition: color var(--transition);
}

.species-card:hover .sc-name {
  color: var(--tc, var(--accent));
}

.sc-desc {
  font-size: 0.74rem;
  color: var(--text-secondary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.sc-arrow {
  flex-shrink: 0;
  color: var(--text-muted);
  transition: all var(--transition);
}

.species-card:hover .sc-arrow {
  color: var(--tc, var(--accent));
  transform: translateX(4px);
}

/* ── MODAL ──────────────────────────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.78);
  backdrop-filter: blur(10px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal-panel {
  background: var(--bg-elevated);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 560px;
  max-height: 88vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow:
    0 32px 80px rgba(0, 0, 0, 0.65),
    0 0 0 1px rgba(255,255,255,0.04),
    0 0 60px var(--mglow, rgba(139,92,246,0.25));
}

/* Modal Header */
.modal-head {
  position: relative;
  padding: 2rem 1.75rem 1.5rem;
  display: flex;
  align-items: flex-end;
  gap: 1.25rem;
  min-height: 145px;
  overflow: hidden;
  flex-shrink: 0;
}

/* Floating particles */
.mp-wrap {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.mp {
  position: absolute;
  animation: mp-float linear infinite;
  user-select: none;
  line-height: 1;
}

@keyframes mp-float {
  0%   { transform: translateY(0) scale(0.7); opacity: 0; }
  15%  { opacity: 0.85; }
  85%  { opacity: 0.35; }
  100% { transform: translateY(-65px) scale(1.3); opacity: 0; }
}

/* Icon */
.mh-icon {
  width: 76px;
  height: 76px;
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  border: 2px solid rgba(255, 255, 255, 0.22);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.45);
  position: relative;
  z-index: 2;
}

.mh-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mh-emoji {
  font-size: 2.2rem;
  filter: drop-shadow(0 0 14px rgba(255, 255, 255, 0.5));
}

/* Title block */
.mh-text {
  flex: 1;
  position: relative;
  z-index: 2;
  min-width: 0;
}

.mh-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 800;
  color: #fff;
  text-shadow: 0 2px 14px rgba(0, 0, 0, 0.55);
  margin-bottom: 0.3rem;
  line-height: 1.2;
}

.mh-mood {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.72);
  font-style: italic;
  line-height: 1.4;
}

/* Close button */
.mh-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: rgba(255, 255, 255, 0.75);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
  z-index: 5;
}

.mh-close:hover {
  background: rgba(239, 68, 68, 0.5);
  color: #fff;
  border-color: rgba(239, 68, 68, 0.6);
  transform: scale(1.1) rotate(90deg);
}

/* Modal Body */
.modal-body {
  padding: 1.75rem;
  overflow-y: auto;
  flex: 1;
}

.modal-body::-webkit-scrollbar { width: 4px; }
.modal-body::-webkit-scrollbar-track { background: transparent; }
.modal-body::-webkit-scrollbar-thumb {
  background: var(--maccent, var(--accent));
  border-radius: 4px;
  opacity: 0.5;
}

.modal-lore {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.75;
}

.modal-scenario-link {
  display: inline-flex;
  margin-top: .35rem;
  padding: .65rem .9rem;
  border: 1px solid var(--maccent, var(--accent));
  border-radius: var(--radius);
  color: var(--maccent, var(--accent));
  font-size: .85rem;
  font-weight: 700;
  text-decoration: none;
}
.modal-scenario-link:hover,
.modal-scenario-link:focus-visible {
  background: color-mix(in srgb, var(--maccent, var(--accent)) 14%, transparent);
}

.modal-sep {
  height: 1px;
  margin: 1.5rem 0;
  opacity: 0.5;
}

/* Members header */
.mm-header {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  margin-bottom: 1.25rem;
  color: var(--text-secondary);
}

.mm-title {
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text);
  flex: 1;
}

.mm-count {
  font-size: 0.78rem;
  font-weight: 700;
  padding: 0.2rem 0.625rem;
  border-radius: 999px;
  background: var(--primary-light);
  min-width: 28px;
  text-align: center;
}

/* Loading */
.mm-loading {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
  padding: 1.5rem 0;
}

.mm-spinner {
  width: 22px;
  height: 22px;
  border: 2px solid rgba(255, 255, 255, 0.08);
  border-top-color: var(--maccent, var(--accent));
  border-radius: 50%;
  animation: mm-spin 0.8s linear infinite;
  flex-shrink: 0;
}

@keyframes mm-spin {
  to { transform: rotate(360deg); }
}

/* Empty */
.mm-empty {
  text-align: center;
  padding: 2.5rem 1rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.mm-empty-icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 0.75rem;
  animation: float 3s ease-in-out infinite;
}

/* Search bar */
.mm-search-wrap {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.875rem;
  transition: border-color var(--transition);
}

.mm-search-wrap:focus-within {
  border-color: var(--maccent, var(--accent));
  box-shadow: 0 0 0 2px rgba(255,255,255,0.04);
}

.mm-search-wrap svg {
  flex-shrink: 0;
  color: var(--text-muted);
}

.mm-search {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  font-family: var(--font-body);
  font-size: 0.85rem;
  color: var(--text);
}

.mm-search::placeholder {
  color: var(--text-muted);
}

/* Member grid */
.mm-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.5rem;
}

/* 2 colonnes à partir de 10 membres */
.mm-grid--many {
  grid-template-columns: 1fr 1fr;
}

.mm-member {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.7rem 0.875rem;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  transition: all var(--transition);
}

.mm-member:hover {
  border-color: var(--maccent, var(--accent));
  background: rgba(255,255,255,0.03);
  box-shadow: 0 0 12px var(--mglow, rgba(139,92,246,0.15));
}

/* Compact variant (>10 membres) */
.mm-member--compact {
  padding: 0.5rem 0.75rem;
  gap: 0.625rem;
}

/* Avatar */
.mm-av {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.1);
  transition: box-shadow var(--transition);
}

.mm-member--compact .mm-av {
  width: 34px;
  height: 34px;
  font-size: 0.85rem;
}

.mm-av img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mm-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  min-width: 0;
}

.mm-pseudo {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mm-member--compact .mm-pseudo {
  font-size: 0.8rem;
}

/* Bouton retirer (admin) */
.mm-remove-btn {
  margin-left: auto;
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid rgba(239,68,68,0.3);
  background: rgba(239,68,68,0.07);
  color: #f87171;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: opacity var(--transition), background var(--transition);
}
.mm-member:hover .mm-remove-btn { opacity: 1; }
.mm-remove-btn:hover:not(:disabled) { background: rgba(239,68,68,0.25); }
.mm-remove-btn:disabled { opacity: 0.4; cursor: not-allowed; }

.mm-login {
  font-size: 0.7rem;
  color: var(--text-muted);
}

.mm-race {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  padding: 0.15rem 0.45rem;
  border-radius: 999px;
  border: 1px solid;
  white-space: nowrap;
  align-self: flex-start;
}

/* ── Modal Transition ───────────────────────────────────────────────────── */
.modal-anim-enter-active {
  transition: all 0.38s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.modal-anim-leave-active {
  transition: all 0.2s ease-in;
}
.modal-anim-enter-from {
  opacity: 0;
  transform: scale(0.86) translateY(20px);
}
.modal-anim-leave-to {
  opacity: 0;
  transform: scale(0.94) translateY(8px);
}

/* ── Responsive ─────────────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .codex-layout { grid-template-columns: 1fr; }
  .codex-index { max-height: none; }
  .codex-entry-body { padding: 1.25rem; }
  .factions-grid {
    grid-template-columns: 1fr;
  }

  .faction-card {
    height: 200px;
  }

  .species-grid {
    grid-template-columns: 1fr;
  }

  .modal-panel {
    max-height: 92vh;
  }

  .mh-title {
    font-size: 1.2rem;
  }

  .mh-icon {
    width: 60px;
    height: 60px;
  }
}

@media (max-width: 480px) {
  .modal-head {
    padding: 1.5rem 1.25rem 1.25rem;
    min-height: 120px;
    gap: 1rem;
  }

  .modal-body {
    padding: 1.25rem;
  }

  .mh-emoji {
    font-size: 1.8rem;
  }
}

/* ── Admin : Ajouter un membre ──────────────────────────────────────────── */
.mm-admin-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.72rem;
  font-weight: 600;
  font-family: var(--font-body);
  padding: 0.28rem 0.7rem;
  border-radius: 999px;
  border: 1px solid var(--maccent, var(--accent));
  color: var(--maccent, var(--accent));
  background: transparent;
  cursor: pointer;
  transition: all var(--transition);
  flex-shrink: 0;
}
.mm-admin-btn:hover {
  background: rgba(255,255,255,0.08);
}

.admin-add {
  margin-bottom: 1rem;
  padding: 0.875rem;
  background: rgba(255,255,255,0.03);
  border: 1px dashed rgba(255,255,255,0.1);
  border-radius: var(--radius);
}

/* Portraits du Pouvoir des Quatre : l'image entière reste visible et le texte
   se place sous les visages, sans les masquer. */
.faction-card--four { height: 270px; background: #100b19; }
.faction-card--four .fc-bg-img { object-fit: contain; filter: saturate(.9) brightness(.8); }
.faction-card--four:hover .fc-bg-img { transform: none; filter: saturate(1) brightness(.9); }
.faction-card--four .fc-overlay-img { background: linear-gradient(to top, rgba(6,3,12,.95), rgba(6,3,12,.3) 22%, transparent 48%) !important; }
.faction-card--four .fc-body { padding: .5rem 1rem .8rem; gap: .2rem; }
.faction-card--four .fc-desc { display: none; }
.faction-card--four .fc-name { font-size: 1.1rem; }

.four-portrait-preview { display: grid; place-items: center; margin-bottom: 1rem; border-radius: var(--radius-lg); overflow: hidden; background: #100b19; border: 1px solid rgba(245,215,110,.28); }
.four-portrait-preview img { display: block; width: min(100%, 500px); max-height: 420px; object-fit: contain; }
.admin-specialty-label { display: grid; gap: .35rem; margin-bottom: .7rem; color: var(--text-secondary); font-size: .8rem; }
.admin-specialty-select { width: 100%; padding: .55rem .65rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--bg-secondary); color: var(--text); font: inherit; }
.admin-specialty-select:focus { outline: 2px solid var(--accent); outline-offset: 2px; }
.modal-specialties { margin: .7rem 0 1rem; padding: .8rem 1rem; border: 1px solid var(--border); border-radius: var(--radius); background: rgba(139,92,246,.06); }
.modal-specialties h3 { margin: 0 0 .35rem; color: var(--text); font-size: .88rem; }
.modal-specialties p { margin: 0; color: var(--text-secondary); font-size: .8rem; line-height: 1.6; }
.modal-role-powers { margin: 1rem 0; }
.modal-role-powers > h3 { margin: 0 0 .4rem; color: var(--maccent); font-size: 1rem; }
.modal-role-note { margin: 0 0 .7rem; color: var(--text-secondary); font-size: .8rem; line-height: 1.6; }
.modal-role-card { margin: .65rem 0; padding: .75rem .9rem; border: 1px solid var(--border); border-radius: var(--radius); background: rgba(139,92,246,.06); }
.modal-role-card h4 { margin: 0 0 .45rem; color: var(--text); font-size: .88rem; }
.modal-role-card ul { margin: 0; padding-left: 1.2rem; color: var(--text-secondary); font-size: .8rem; line-height: 1.6; }
.modal-role-card li + li { margin-top: .35rem; }
.modal-role-card strong { color: var(--text); }

.admin-add-row {
  display: flex;
  gap: 0.5rem;
}

.admin-add-input {
  flex: 1;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: var(--radius);
  padding: 0.45rem 0.75rem;
  font-size: 0.84rem;
  font-family: var(--font-body);
  color: var(--text);
  outline: none;
  transition: border-color var(--transition);
}
.admin-add-input:focus {
  border-color: var(--maccent, var(--accent));
}
.admin-add-input::placeholder {
  color: var(--text-muted);
}

.admin-add-search-btn {
  padding: 0.45rem 1rem;
  font-size: 0.8rem;
  font-weight: 600;
  font-family: var(--font-body);
  border-radius: var(--radius);
  border: 1px solid var(--maccent, var(--accent));
  color: var(--maccent, var(--accent));
  background: transparent;
  cursor: pointer;
  transition: all var(--transition);
  white-space: nowrap;
}
.admin-add-search-btn:hover:not(:disabled) {
  background: var(--maccent, var(--accent));
  color: #000;
}
.admin-add-search-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.admin-msg {
  font-size: 0.78rem;
  margin: 0.5rem 0 0;
  padding: 0.35rem 0.625rem;
  border-radius: var(--radius);
}
.admin-msg--ok  { color: #4ade80; background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); }
.admin-msg--err { color: #f87171; background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.2); }

.admin-results {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  margin-top: 0.625rem;
}

.admin-result {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.5rem 0.75rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: var(--radius);
  cursor: pointer;
  text-align: left;
  color: var(--text);
  font-family: var(--font-body);
  transition: all var(--transition);
}
.admin-result:hover:not(:disabled) {
  background: rgba(255,255,255,0.08);
  border-color: var(--maccent, var(--accent));
}
.admin-result:disabled { opacity: 0.5; cursor: not-allowed; }

.admin-av {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.8rem;
  color: #fff;
  flex-shrink: 0;
}

.admin-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.05rem;
  min-width: 0;
}
.admin-pseudo {
  font-size: 0.84rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.admin-login {
  font-size: 0.68rem;
  color: var(--text-muted);
}
.admin-cta {
  font-size: 0.72rem;
  font-weight: 700;
  flex-shrink: 0;
}
</style>
