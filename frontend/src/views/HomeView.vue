<template>
  <div class="home">
    <!-- Hero Banner -->
    <section class="hero">
      <div class="hero-bg">
        <img :src="heroBanner" alt="" class="hero-image" />
        <div class="hero-overlay"></div>
      </div>
      <div class="hero-content animate-fade-in-up">
        <div class="hero-triquetra">
          <svg viewBox="0 0 80 80" width="43" height="43">
            <path d="M40 4C40 4 16 28 16 44c0 10 6 16 12 18c-4-4-6-10-6-16c0-12 18-32 18-32s18 20 18 32c0 6-2 12-6 16c6-2 12-8 12-18c0-16-24-40-24-40z" fill="url(#hero-triquetra-grad)" opacity="0.9"/>
            <path d="M40 76c-8 0-16-6-18-14c4 4 10 6 18 6s14-2 18-6c-2 8-10 14-18 14z" fill="url(#hero-triquetra-grad)" opacity="0.7"/>
            <circle cx="40" cy="44" r="6" fill="url(#hero-triquetra-grad)" opacity="0.8"/>
            <defs>
              <linearGradient id="hero-triquetra-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#c084fc" />
                <stop offset="50%" stop-color="#f0c674" />
                <stop offset="100%" stop-color="#c084fc" />
              </linearGradient>
            </defs>
          </svg>
        </div>
        <h1 class="hero-title">Nexus Arcana</h1>
        <p class="hero-eyebrow">Charmed · The Vampire Diaries · The Originals · Legacies · Teen Wolf</p>
        <p class="hero-subtitle">Un crossover surnaturel où les mondes ne sont plus séparés.</p>
        <div v-if="!auth.isAuthenticated" class="hero-actions">
          <router-link to="/register" class="btn btn-primary btn-lg">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
            Rejoindre Nexus Arcana
          </router-link>
          <router-link to="/login" class="btn btn-secondary btn-lg">
            Connexion
          </router-link>
        </div>
      </div>
      <!-- Floating particles -->
      <div class="hero-particles" aria-hidden="true">
        <span v-for="n in 12" :key="n" class="particle" :style="particleStyle(n)"></span>
      </div>
    </section>

    <!-- Stats Bar -->
    <section class="stats-bar">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-icon">🔮</span>
            <div class="stat-content">
              <span class="stat-value">{{ forum.categories?.length || 0 }}</span>
              <span class="stat-label">Univers reliés</span>
            </div>
          </div>
          <div class="stat-item">
            <span class="stat-icon">📜</span>
            <div class="stat-content">
              <span class="stat-value">{{ totalTopics }}</span>
              <span class="stat-label">Sujets</span>
            </div>
          </div>
          <div class="stat-item">
            <span class="stat-icon">✨</span>
            <div class="stat-content">
              <span class="stat-value">{{ totalPosts }}</span>
              <span class="stat-label">Messages</span>
            </div>
          </div>
          <div class="stat-item">
            <span class="stat-icon">🌙</span>
            <div class="stat-content">
              <span class="stat-value">—</span>
              <span class="stat-label">En ligne</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Quick Nav Bar -->
    <section class="quick-nav-bar">
      <div class="container">
        <nav class="qnav-links">
          <router-link to="/groupes" class="qnav-item">
            <span class="qnav-icon">⚜</span>
            <span>Groupes</span>
          </router-link>
          <router-link to="/membres" class="qnav-item">
            <span class="qnav-icon">🧙</span>
            <span>Membres</span>
          </router-link>
          <router-link to="/messageries" class="qnav-item">
            <span class="qnav-icon">💬</span>
            <span>Messageries</span>
          </router-link>
          <router-link v-if="!auth.isAuthenticated" to="/register" class="qnav-item qnav-cta">
            <span class="qnav-icon">✦</span>
            <span>Rejoindre</span>
          </router-link>
        </nav>
      </div>
    </section>

    <!-- Crossover : manifeste et points d'ancrage narratifs -->
    <section class="crossover-section">
      <div class="container">
        <div class="crossover-intro card">
          <div class="crossover-copy">
            <p class="intro-tag">L'INTRIGUE EN COURS</p>
            <h2 class="crossover-title">La Faille a ouvert les portes.</h2>
            <p>
              Une onde ancienne a relié San Francisco, Mystic Falls, La Nouvelle-Orléans et Beacon Hills.
              Les grimoires, les lignées et les meutes sentent tous le même appel : les frontières du monde
              surnaturel se fissurent.
            </p>
          </div>
          <div class="crossover-seal" aria-hidden="true">
            <span>✦</span>
            <span class="crossover-seal-ring"></span>
          </div>
        </div>

        <div class="crossover-worlds" aria-label="Les univers du crossover">
          <article class="crossover-world crossover-world--charmed">
            <span class="crossover-world-kicker">LE CŒUR MAGIQUE</span>
            <h3>San Francisco</h3>
            <p>Le Manoir, les Enfers et les forces qui veillent sur l'équilibre.</p>
            <span class="crossover-world-source">Charmed</span>
          </article>
          <article class="crossover-world crossover-world--mystic">
            <span class="crossover-world-kicker">LES LIGNÉES</span>
            <h3>Mystic Falls</h3>
            <p>Des secrets de famille, des pactes anciens et des héritages impossibles à fuir.</p>
            <span class="crossover-world-source">The Vampire Diaries</span>
          </article>
          <article class="crossover-world crossover-world--orleans">
            <span class="crossover-world-kicker">LES ALLIANCES</span>
            <h3>La Nouvelle-Orléans</h3>
            <p>Une ville de promesses, de pouvoir et de rivalités qui traversent les siècles.</p>
            <span class="crossover-world-source">The Originals · Legacies</span>
          </article>
          <article class="crossover-world crossover-world--beacon">
            <span class="crossover-world-kicker">L'APPEL SAUVAGE</span>
            <h3>Beacon Hills</h3>
            <p>Le Nemeton résonne de nouveau, attirant les secrets et les présences oubliées.</p>
            <span class="crossover-world-source">Teen Wolf</span>
          </article>
        </div>

        <p class="crossover-note">
          Les groupes et créatures déjà présents sur le forum restent inchangés : le crossover ouvre de nouvelles histoires,
          sans effacer celles qui existent déjà.
        </p>
      </div>
    </section>

    <!-- Forum Presentation -->
    <section class="forum-intro">
      <div class="container">
        <div class="intro-grid">

          <!-- Lore / Context -->
          <div class="intro-lore card" :class="{ 'intro-lore--editing': contextEditMode }">
            <h3 class="intro-tag intro-lore-title">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3 3 7l9 4 9-4-9-4Z"/><path d="m3 12 9 4 9-4"/><path d="m3 17 9 4 9-4"/></svg>
              Contexte de la saison 1
            </h3>
            <!-- Mode lecture -->
            <template v-if="!contextEditMode">
              <div class="intro-lore-scroll" tabindex="0" aria-label="Contexte de la saison 1, faire défiler pour lire la suite">
                <div v-if="contextContent" class="context-html" v-html="contextContent" />
                <template v-else>
                <h2 class="intro-title">Les mondes se sont rejoints</h2>
                <p class="intro-text">
                  San Francisco n'est plus seule. Une faille relie désormais la ville à Mystic Falls,
                  La Nouvelle-Orléans et Beacon Hills. Les <em>Charmed Ones</em> veillent toujours sur l'équilibre,
                  mais les forces anciennes répondent désormais depuis bien plus loin.
                </p>
                <p class="intro-text">
                  Ici, chaque personnage écrit son propre destin. Alliances fragiles, secrets de famille,
                  meutes et covens se croisent sans que les histoires déjà écrites ne soient effacées.
                </p>
                </template>
              </div>
              <p class="intro-lore-hint">Faire défiler pour lire le contexte ↓</p>
              <button
                v-if="isAdmin"
                class="context-edit-btn"
                @click="contextEditContent = contextContent; contextEditMode = true"
              >✏️ Modifier</button>
            </template>

            <!-- Mode édition (admin) -->
            <template v-else>
              <p class="context-hint">HTML accepté. Prévisualisation ci-dessous.</p>
              <textarea v-model="contextEditContent" class="context-textarea" rows="12" />
              <div class="context-preview" v-html="contextEditContent" />
              <div class="context-actions">
                <button class="btn btn-primary" @click="saveContext" :disabled="contextSaving">
                  {{ contextSaving ? 'Enregistrement…' : '💾 Enregistrer' }}
                </button>
                <button class="btn btn-ghost" @click="contextEditMode = false">Annuler</button>
              </div>
            </template>
          </div>

          <!-- Personnages Attendus (scénarios admin) -->
          <div class="intro-members card">
            <h3 class="intro-members-title">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              Personnages Attendus
            </h3>

            <!-- Grille de scénarios -->
            <div v-if="featuredScenarios.length > 0" class="intro-scenarios-container">
              <div class="intro-scenarios">
                <router-link
                  v-for="scenario in featuredScenarios"
                  :key="scenario.id"
                  :to="`/topics/${scenario.slug}`"
                  class="intro-scenario-card"
                  :title="scenario.title"
                >
                  <div v-if="scenario.first_image" class="intro-scenario-img-wrap">
                    <img :src="scenario.first_image" :alt="scenario.title" class="intro-scenario-img" />
                  </div>
                  <span v-else class="intro-scenario-icon">🎭</span>
                  <span class="intro-scenario-name">{{ scenario.title }}</span>
                </router-link>

                <!-- Carte "Voir tout" (swipe up metaphor) -->
                <router-link
                  v-if="featuredScenarios.length > 4"
                  to="/categories/scenarios-a-prendre"
                  class="intro-scenario-card intro-scenario-more"
                  title="Voir tous les scénarios"
                >
                  <span class="intro-scenario-icon">➡</span>
                  <span class="intro-scenario-name">Voir tout</span>
                </router-link>
              </div>
              <div class="intro-scenarios-hint" v-if="featuredScenarios.length > 4">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
                Glisser pour voir plus
              </div>
            </div>

            <!-- État vide -->
            <div v-else class="intro-scenarios-empty">
              <span class="intro-scenarios-empty-icon">🎭</span>
              <p>Aucun personnage attendu pour le moment.</p>
              <p class="intro-scenarios-empty-sub">Les administrateurs publieront prochainement des scénarios à incarner.</p>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- Staff Section -->
    <section class="staff-section">
      <div class="container">
        <div class="staff-section-head">
          <h2 class="section-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            Team du Staff
          </h2>
          <!-- Bouton visible uniquement pour les admins -->
          <button v-if="isAdmin" @click="isEditing = !isEditing" class="staff-edit-btn" :class="{ active: isEditing }">
            <svg v-if="!isEditing" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            {{ isEditing ? 'Terminer' : 'Modifier' }}
          </button>
        </div>

        <div v-if="isEditing && isAdmin" class="staff-promote card">
          <span>Ajouter un membre à l’administration</span>
          <select v-model="staffCandidateId" class="staff-edit-select">
            <option value="">Choisir un membre…</option>
            <option v-for="member in staffCandidates" :key="member.id" :value="member.id">
              {{ member.username }}<template v-if="member.pseudo"> — pseudo RP : {{ member.pseudo }}</template>
            </option>
          </select>
          <button class="btn btn-primary btn-sm" :disabled="!staffCandidateId || staffPromoting" @click="promoteStaffMember">
            {{ staffPromoting ? 'Ajout…' : 'Ajouter comme administrateur' }}
          </button>
        </div>

        <div class="staff-grid">
          <div
            v-for="(member, index) in staffSlots"
            :key="index"
            class="staff-card card"
            :class="{ 'staff-card--empty': !member }"
          >
            <!-- Slot rempli -->
            <template v-if="member">
              <div
                class="staff-avatar-wrap"
                :class="{ 'staff-avatar-wrap--editable': isAdmin }"
                @click="isAdmin && triggerAvatarUpload(index)"
              >
                <img
                  v-if="(localAvatars[index] || member.avatar) && !brokenAvatars[index]"
                  :src="localAvatars[index] || member.avatar"
                  :alt="member.username"
                  class="staff-avatar-img"
                  @error="markAvatarBroken(index)"
                />
                <div v-else class="staff-avatar-placeholder">
                  {{ member.username?.[0]?.toUpperCase() }}
                </div>
                <div v-if="isAdmin" class="staff-avatar-edit-overlay" aria-hidden="true">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
                </div>
                <input
                  v-if="isAdmin"
                  :id="`staff-upload-${index}`"
                  type="file"
                  accept="image/*"
                  class="staff-upload-input"
                  @change="handleAvatarChange($event, index)"
                />
              </div>

              <!-- Mode édition : champs texte -->
              <div v-if="isEditing" class="staff-info">
                <input v-model="member.pseudo"    class="staff-edit-input" placeholder="Pseudo RP du joueur" />
                <input v-model="member.username"  class="staff-edit-input" placeholder="Compte" />
                <select v-model="member.role" class="staff-edit-select">
                  <option value="admin">Administrateur</option>
                  <option value="moderator">Modérateur</option>
                  <option value="fondatrice">Fondatrice</option>
                </select>
              </div>

              <!-- Mode affichage normal -->
              <div v-else class="staff-info">
                <span class="staff-pseudo">{{ member.username }}</span>
                <span v-if="member.pseudo" class="staff-username">Pseudo RP : {{ member.pseudo }}</span>
                <span class="staff-role-badge" :class="`staff-role-${member.role}`">
                  {{ staffRoleLabel(member.role) }}
                </span>
              </div>
            </template>

            <!-- Slot vide -->
            <template v-else>
              <!-- Mode édition : label du poste + bouton ajouter -->
              <div v-if="isEditing" class="staff-add-slot">
                <input
                  v-model="slotLabels[index]"
                  class="staff-edit-input staff-edit-input--slot"
                  placeholder="Intitulé du poste"
                />
                <div class="staff-add-btn" @click="fillSlot">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                  <span>Ajouter un membre</span>
                </div>
              </div>
              <!-- Mode affichage : intitulé du poste -->
              <template v-else>
                <div class="staff-avatar-wrap">
                  <div class="staff-avatar-placeholder staff-avatar-placeholder--empty">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  </div>
                </div>
                <div class="staff-info">
                  <span class="staff-pseudo staff-pseudo--empty">{{ slotLabels[index] || 'Poste vacant' }}</span>
                </div>
              </template>
            </template>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ BIENVENUE À TOI ═══ -->
    <section class="bienvenue-group">
      <div class="container">

        <div class="bgroup-banner">
          <svg class="bgroup-banner-icon" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
          <div>
            <h2 class="bgroup-title">Bienvenue à toi</h2>
            <p class="bgroup-subtitle">Découvre Nexus Arcana, présente-toi et commence ton histoire dans la ville de ton choix</p>
          </div>
        </div>

        <div class="bgroup-grid">

          <!-- Règlement magique -->
          <div class="bgroup-card card">
            <router-link to="/categories/reglement-magique" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">📚</span>
              <span class="bgroup-cat-title">Règlement magique et grimoires ancestraux</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in grimoireSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Bienvenue à Nexus Arcana -->
          <div class="bgroup-card card">
            <router-link to="/categories/bienvenue-san-francisco" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🌁</span>
              <span class="bgroup-cat-title">Bienvenue à Nexus Arcana</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in bienvenueSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Ma situation magique -->
          <div class="bgroup-card card">
            <router-link to="/categories/ma-situation-magique" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🏡</span>
              <span class="bgroup-cat-title">Ma situation magique</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in situationSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Une question ? -->
          <div class="bgroup-card card">
            <router-link to="/categories/une-question" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">❓</span>
              <span class="bgroup-cat-title">Une question ?</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in questionSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Liens magiques -->
          <div class="bgroup-card card">
            <router-link to="/categories/liens-magiques" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🔗</span>
              <span class="bgroup-cat-title">Liens magiques</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in liensSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- Rues commerçantes -->
    <!-- ═══ SAN FRANCISCO ═══ -->
    <section class="bienvenue-group sf-group" :class="{ 'guest-locked': isGuest }">
      <div class="container">

        <div class="bgroup-banner sf-banner">
          <svg class="bgroup-banner-icon" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
          <div>
            <h2 class="bgroup-title">San Francisco</h2>
            <p class="bgroup-subtitle">Explorez les quartiers de la ville et jouez vos scènes de RP</p>
          </div>
        </div>

        <div class="bgroup-grid sf-grid">

          <!-- Rues commerçantes -->
          <div class="bgroup-card card">
            <router-link to="/categories/rues-commercantes" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🛍️</span>
              <span class="bgroup-cat-title">Rues commerçantes</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in ruesCommercantesSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Centre ville -->
          <div class="bgroup-card card">
            <router-link to="/categories/centre-ville" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🏙️</span>
              <span class="bgroup-cat-title">Centre-ville</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in centreVilleSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Civic Center -->
          <div class="bgroup-card card">
            <router-link to="/categories/civic-center" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🏛️</span>
              <span class="bgroup-cat-title">Civic Center</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in civicCenterSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Quartier culturel -->
          <div class="bgroup-card card">
            <router-link to="/categories/quartier-culturel-et-enseignement" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🎓</span>
              <span class="bgroup-cat-title">Quartier culturel et d'enseignement</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in quartierCulturelSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Quartier des affaires -->
          <div class="bgroup-card card">
            <router-link to="/categories/quartier-des-affaires" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">💼</span>
              <span class="bgroup-cat-title">Quartier des affaires</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in quartierAffairesSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Fisherman's Wharf -->
          <div class="bgroup-card card">
            <router-link to="/categories/fishermans-wharf" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🍫</span>
              <span class="bgroup-cat-title">Fisherman's Wharf</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in fishermansWharfSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Presidio of San Francisco -->
          <div class="bgroup-card card">
            <router-link to="/categories/presidio-of-san-francisco" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🌉</span>
              <span class="bgroup-cat-title">Presidio of San Francisco</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in presidioSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Glen Park -->
          <div class="bgroup-card card">
            <router-link to="/categories/glen-park" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🌿</span>
              <span class="bgroup-cat-title">Glen Park</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in glenParkSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Ocean Beach -->
          <div class="bgroup-card card">
            <router-link to="/categories/ocean-beach" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🏖️</span>
              <span class="bgroup-cat-title">Ocean Beach</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in oceanBeachSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Cimetière -->
          <div class="bgroup-card card">
            <router-link to="/categories/cimetiere" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🪦</span>
              <span class="bgroup-cat-title">Cimetière</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in cimetiereSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Quartiers résidentiels -->
          <div class="bgroup-card card">
            <router-link to="/categories/quartiers-residentiels" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🏡</span>
              <span class="bgroup-cat-title">Quartiers résidentiels</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in quartiersSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- ═══ AUTRES VILLES DU CROSSOVER ═══ -->
    <section
      v-for="city in crossoverCities"
      :key="city.slug"
      class="bienvenue-group crossover-city-group"
      :class="[`crossover-city--${city.slug}`, { 'guest-locked': isGuest }]"
    >
      <div class="container">
        <div class="bgroup-banner crossover-city-banner">
          <span class="crossover-city-symbol" aria-hidden="true">{{ city.icon }}</span>
          <div>
            <p class="crossover-city-universe">{{ city.universe }}</p>
            <h2 class="bgroup-title">{{ city.name }}</h2>
            <p class="bgroup-subtitle">{{ city.description }}</p>
          </div>
        </div>

        <div class="bgroup-grid sf-grid">
          <div v-for="district in city.districts" :key="district.slug" class="bgroup-card card">
            <router-link :to="`/categories/${district.slug}`" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">{{ district.icon }}</span>
              <span class="bgroup-cat-title">{{ district.name }}</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="place in district.places" :key="place" class="bgroup-chip">{{ place }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ LIEUX MAGIQUES ═══ -->
    <section class="bienvenue-group lieux-magiques-group" :class="{ 'guest-locked': isGuest }">
      <div class="container">

        <div class="bgroup-banner lieux-magiques-banner">
          <svg class="bgroup-banner-icon" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
            <path d="M12 6 Q14 10 12 14 Q10 10 12 6Z" fill="currentColor" opacity="0.3"/>
          </svg>
          <div>
            <h2 class="bgroup-title">Lieux magiques</h2>
            <p class="bgroup-subtitle">Les endroits imprégnés de magie, refuges et nexus de pouvoir à San Francisco</p>
          </div>
        </div>

        <div class="bgroup-grid sf-grid">

          <!-- L'école de magie -->
          <div class="bgroup-card card">
            <router-link to="/categories/ecole-de-magie" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🏫</span>
              <span class="bgroup-cat-title">L'école de magie</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in ecoleMagieSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Les Enfers -->
          <div class="bgroup-card card">
            <router-link to="/categories/les-enfers" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🔥</span>
              <span class="bgroup-cat-title">Les Enfers</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in lesEnfersSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Dimensions alternatives -->
          <div class="bgroup-card card">
            <router-link to="/categories/dimensions-alternatives" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🪞</span>
              <span class="bgroup-cat-title">Dimensions alternatives</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in dimensionsAlternativesSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

          <!-- Les Cieux -->
          <div class="bgroup-card card">
            <router-link to="/categories/les-cieux" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">☁️</span>
              <span class="bgroup-cat-title">Les Cieux</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in lesCieuxSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- ══════════════ LE MONDE ══════════════ -->
    <section class="bienvenue-group monde-group" :class="{ 'guest-locked': isGuest }">
      <div class="container">

        <div class="bgroup-banner monde-banner">
          <svg class="bgroup-banner-icon" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
            <circle cx="12" cy="12" r="10"/>
            <line x1="2" y1="12" x2="22" y2="12"/>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
          </svg>
          <div>
            <h2 class="bgroup-title">Le monde</h2>
            <p class="bgroup-subtitle">Explorez les quatre coins du globe et jouez hors des frontières de San Francisco</p>
          </div>
        </div>

        <div class="bgroup-grid sf-grid">

          <!-- Continents -->
          <div class="bgroup-card card">
            <router-link to="/categories/continents" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🌍</span>
              <span class="bgroup-cat-title">Continents</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span v-for="sub in continentsSubCategories" :key="sub.slug" class="bgroup-chip" :title="sub.desc">
                <span>{{ sub.icon }}</span> {{ sub.name }}
              </span>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- ══════════════ PARTENARIATS ET ARCADES ══════════════ -->
    <section class="bienvenue-group partenariats-group">
      <div class="container">

        <div class="bgroup-banner partenariats-banner">
          <svg class="bgroup-banner-icon" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
          <div>
            <h2 class="bgroup-title">Partenariat et arcades</h2>
            <p class="bgroup-subtitle">Échanges de partenariat, jeux et animations communautaires</p>
          </div>
        </div>

        <div class="bgroup-grid sf-grid">

          <div class="bgroup-card card">
            <router-link to="/categories/jeu-des-prenoms" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🎮</span>
              <span class="bgroup-cat-title">Jeux</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <span class="bgroup-chip" title="Participez au jeu des prénoms">
                <span>🎯</span> Participer
              </span>
            </div>
          </div>

          <div class="bgroup-card card">
            <router-link to="/categories/demande-de-partenariats" class="bgroup-cat-header">
              <span class="bgroup-cat-icon">🤝</span>
              <span class="bgroup-cat-title">Demande de partenariat</span>
              <svg class="bgroup-cat-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </router-link>
            <div class="bgroup-chips">
              <router-link to="/categories/demande-de-partenariats" class="bgroup-chip" title="Proposez un partenariat avec votre forum">
                <span>📋</span> Proposer
              </router-link>
              <router-link to="/categories/nos-partenaires" class="bgroup-chip" title="Découvrir les forums partenaires">
                <span>✦</span> Nos partenaires
              </router-link>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- ══════════════ TABLEAU DE BORD ══════════════ -->
    <section class="dashboard-section">
      <div class="container">
        <div class="dashboard-header">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
          <h2 class="dashboard-title">Nos habitants</h2>
        </div>

        <div class="dashboard-grid">

          <!-- Compteurs -->
          <div class="dash-card dash-counters">
            <div class="dash-counter-item">
              <span class="dash-counter-icon">🧙</span>
              <div class="dash-counter-body">
                <span class="dash-counter-value">{{ stats?.member_count ?? '—' }}</span>
                <span class="dash-counter-label">Membres inscrits</span>
              </div>
            </div>
            <div class="dash-divider"></div>
            <div class="dash-counter-item">
              <span class="dash-counter-icon">📜</span>
              <div class="dash-counter-body">
                <span class="dash-counter-value">{{ stats?.message_count ?? '—' }}</span>
                <span class="dash-counter-label">Messages postés</span>
              </div>
            </div>
          </div>

          <!-- Dernier inscrit -->
          <div class="dash-card dash-newest">
            <p class="dash-card-label">✦ Bienvenue parmi nous</p>
            <template v-if="stats?.newest_member">
              <router-link :to="`/membres`" class="dash-member-row">
                <img
                  v-if="toRelativeAvatar(stats.newest_member.avatar)"
                  :src="toRelativeAvatar(stats.newest_member.avatar)"
                  class="dash-avatar"
                  :alt="stats.newest_member.pseudo"
                />
                <span v-else class="dash-avatar dash-avatar-placeholder">✦</span>
                <div>
                  <span class="dash-member-name">{{ stats.newest_member.pseudo }}</span>
                  <span class="dash-member-date">Inscrit le {{ formatDate(stats.newest_member.date_joined) }}</span>
                </div>
              </router-link>
            </template>
            <p v-else class="dash-empty">Aucun membre encore.</p>
          </div>

          <!-- Membres connectés dernières 48h -->
          <div class="dash-card dash-online">
            <p class="dash-card-label">🌙 Vus ces dernières 48h</p>
            <template v-if="stats?.recent_members?.length">
              <div class="dash-online-list">
                <router-link
                  v-for="m in stats.recent_members"
                  :key="m.username"
                  to="/membres"
                  class="dash-online-item"
                  :title="m.pseudo"
                >
                  <img
                    v-if="toRelativeAvatar(m.avatar)"
                    :src="toRelativeAvatar(m.avatar)"
                    class="dash-avatar dash-avatar-sm"
                    :alt="m.pseudo"
                  />
                  <span v-else class="dash-avatar dash-avatar-sm dash-avatar-placeholder">✦</span>
                  <span class="dash-online-name">{{ m.pseudo }}</span>
                </router-link>
              </div>
            </template>
            <p v-else class="dash-empty">Aucun membre actif récemment.</p>
          </div>

        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useForumStore } from '../stores/forum'
import { useAuthStore } from '../stores/auth'
import api from '../composables/useApi'
import heroBanner from '../assets/nexus-world-hero.png'
import { crossoverCities } from '../data/crossoverCities'

const forum = useForumStore()
const auth = useAuthStore()

// Scénarios à prendre — topics de la catégorie scenarios-a-prendre
const featuredScenarios = ref([])
const hiddenFeaturedScenarioTitles = new Set(['Nyméa Argent', 'Briséis Argent'])
async function fetchFeaturedScenarios() {
  try {
    const { data } = await api.get('/categories/scenarios-a-prendre/topics/?page_size=100')
    featuredScenarios.value = (data.results || data).filter(
      (scenario) => !hiddenFeaturedScenarioTitles.has(scenario.title) && scenario.scenario_status !== 'played',
    )
  } catch { /* silent */ }
}

// --- Staff ---
const isEditing = ref(false)
const staffMembers = ref([])
const staffCandidates = ref([])
const staffCandidateId = ref('')
const staffPromoting = ref(false)

// Intitulé de chaque slot (affiché quand le slot est vide, éditable par l'admin)
const slotLabels = ref([
  'Fondatrice',
  'Administrateur',
  'Modérateur',
  'Modérateur',
])

function fillSlot() {
  if (staffMembers.value.length >= 4) return
  staffMembers.value.push({ id: Date.now(), username: '', pseudo: '', role: 'moderator', avatar: null })
}

// Convertit une URL avatar absolue (http://host/media/...) en URL relative (/media/...)
// pour qu'elle passe par le proxy Vite et évite les problèmes cross-origin
function toRelativeUrl(url) {
  if (!url) return null
  try { return new URL(url).pathname } catch { return url }
}

async function fetchStaff() {
  try {
    const [r1, r2, r3, r4] = await Promise.all([
      api.get('/users/?role=fondatrice'),
      api.get('/users/?role=admin'),
      api.get('/users/?role=moderator'),
      api.get('/users/'),
    ])
    const list = [
      ...(r1.data.results || r1.data),
      ...(r2.data.results || r2.data),
      ...(r3.data.results || r3.data),
    ]
      .filter(member => member.show_in_staff_team !== false)
      .slice(0, 4)
      .map(m => ({ ...m, avatar: toRelativeUrl(m.avatar) }))
    // N'écrase les données de test que si l'API renvoie des vrais membres
    staffMembers.value = list
    staffCandidates.value = (r4.data.results || r4.data)
      .filter(member => !['admin', 'fondatrice'].includes(member.role))
  } catch { /* silent */ }
}

async function promoteStaffMember() {
  if (!staffCandidateId.value) return
  staffPromoting.value = true
  try {
    await api.patch(`/users/${staffCandidateId.value}/`, { role: 'admin' })
    staffCandidateId.value = ''
    await fetchStaff()
  } finally {
    staffPromoting.value = false
  }
}

// Avatars remplacés localement (index → dataURL) — non persisté côté serveur
const localAvatars = ref({})
// Avatars dont le chargement a échoué (URL cassée) → affiche le placeholder
const brokenAvatars = ref({})

function markAvatarBroken(index) {
  brokenAvatars.value = { ...brokenAvatars.value, [index]: true }
}

function triggerAvatarUpload(index) {
  document.getElementById(`staff-upload-${index}`)?.click()
}

async function handleAvatarChange(event, index) {
  const file = event.target.files?.[0]
  if (!file) return

  // Aperçu immédiat via DataURL (avant que le serveur réponde)
  const reader = new FileReader()
  reader.onload = (e) => {
    localAvatars.value = { ...localAvatars.value, [index]: e.target.result }
  }
  reader.readAsDataURL(file)

  // Persistance côté serveur
  const member = staffSlots.value[index]
  if (!member?.id) return

  const formData = new FormData()
  formData.append('avatar', file)

  try {
    const { data } = await api.patch(`/users/${member.id}/`, formData)
    if (data.avatar) {
      // Remplace le DataURL local par l'URL serveur définitive
      member.avatar = data.avatar
      const next = { ...localAvatars.value }
      delete next[index]
      localAvatars.value = next
    }
  } catch {
    // En mode test (IDs fictifs) l'upload échoue silencieusement,
    // le DataURL reste affiché en attendant les vrais comptes
  }
}

// Toujours 4 slots — complétés par des cases vides si besoin
const staffSlots = computed(() => {
  const slots = [...staffMembers.value]
  while (slots.length < 4) slots.push(null)
  return slots
})

function staffRoleLabel(role) {
  if (role === 'admin') return 'Administrateur'
  if (role === 'fondatrice') return 'Fondatrice'
  return 'Modérateur'
}

// --- Bienvenue à Nexus Arcana ---
const bienvenueSubCategories = [
  {
    slug: 'scenarios-a-prendre', icon: '🎭',
    name: 'Scénarios à prendre', desc: 'Personnages et histoires disponibles à incarner',
    topics: 8, posts: 24,
    lastPost: { title: 'Cherche partenaire — Sorcière Bien', author: 'Modo1', date: '28 fév. 2026' },
  },
  {
    slug: 'modele-fiche-de-presentation', icon: '📋',
    name: 'Modèle de fiche de présentation', desc: 'Modèle officiel pour créer votre personnage',
    topics: 1, posts: 1,
    lastPost: { title: 'Fiche type — version 3', author: 'AvaBartholomé', date: '1 janv. 2026' },
  },
  {
    slug: 'fiches-de-presentation-terminees', icon: '✨',
    name: 'Fiches en attente de validation', desc: 'Présentations à découvrir et messages de bienvenue',
  },
  {
    slug: 'demande-double-compte', icon: '👥',
    name: 'Demande de double compte', desc: 'Formulaire pour proposer un second personnage',
  },
]

// --- Règlement magique & Grimoires ---
const grimoireSubCategories = [
  {
    slug: 'reglement-du-forum', icon: '⚖️',
    name: 'Règlement du forum', desc: 'Les lois fondamentales de Nexus Arcana',
    topics: 5, posts: 18,
    lastPost: { title: 'Charte des membres v2', author: 'AvaBartholomé', date: '28 fév. 2026' },
  },
  {
    slug: 'creatures-et-races', icon: '🐉',
    name: 'Créatures et races', desc: 'Encyclopédie des êtres magiques',
    topics: 14, posts: 62,
    lastPost: { title: 'Fiche : Traqueurs de Sombres', author: 'Modo1', date: '25 fév. 2026' },
  },
  {
    slug: 'factions', icon: '⚜️',
    name: 'Factions', desc: 'Alliances, clans et ordres secrets',
    topics: 8, posts: 34,
    lastPost: { title: 'Les Vengeances du Nexus', author: 'AdminPrincipal', date: '22 fév. 2026' },
  },
  {
    slug: 'bottin-des-avatars', icon: '📸',
    name: 'Bottin des avatars', desc: 'Registre officiel des célébrités',
    topics: 27, posts: 109,
    lastPost: { title: 'Réservation : Alyssa Milano', author: 'Modo2', date: '27 fév. 2026' },
  },
  {
    slug: 'bottin-des-formes-demoniaques', icon: '👹',
    name: 'Bottin des formes démoniaques', desc: 'Répertoire des apparences démoniaques',
    topics: 11, posts: 43,
    lastPost: { title: 'Nouvelle forme : Ombre du Chaos', author: 'Modo1', date: '20 fév. 2026' },
  },
  {
    slug: 'contextes-et-animations', icon: '🎭',
    name: 'Contextes et animations', desc: 'Événements et fils narratifs actifs',
    topics: 6, posts: 29,
    lastPost: { title: 'Événement : Nuit de Samhain', author: 'AvaBartholomé', date: '1 mars 2026' },
  },
]


// --- Liens magiques ---
const liensSubCategories = [
  {
    slug: 'recherche-de-rp', icon: '🔍',
    name: 'Recherche de RP', desc: 'Trouvez des partenaires pour vos aventures roleplay',
  },
  {
    slug: 'fiche-personnage', icon: '📋',
    name: 'Fiche personnage', desc: 'Carnets récapitulatifs des personnages validés',
  },
]

// --- Ma situation magique ---
const situationSubCategories = [
  {
    slug: 'agence-immobiliere', icon: '🏠',
    name: 'Agence immobilière', desc: 'Choisissez votre lieu de vie dans les villes du Nexus',
  },
  {
    slug: 'boutique-magique', icon: '🔮',
    name: 'La boutique magique', desc: 'Achetez des objets magiques, potions et cristaux',
  },
]

// --- Centre ville & Quartiers résidentiels ---
import subData from '../data/subcategories.json'
const ruesCommercantesSubCategories = subData.ruesCommercantes
const centreVilleSubCategories = subData.centreVille
const quartierAffairesSubCategories = subData.quartierAffaires
const quartierCulturelSubCategories = subData.quartierCulturel
const civicCenterSubCategories = subData.civicCenter
const oceanBeachSubCategories = subData.oceanBeach
const glenParkSubCategories = subData.glenPark
const presidioSubCategories = subData.presidio
const fishermansWharfSubCategories = subData.fishermansWharf
const cimetiereSubCategories = subData.cimetiere
const ecoleMagieSubCategories = subData.ecoleMagie
const lesEnfersSubCategories = subData.lesEnfers
const dimensionsAlternativesSubCategories = subData.dimensionsAlternatives
const lesCieuxSubCategories = subData.lesCieux
const continentsSubCategories = subData.continents
const quartiersSubCategories = subData.quartiers

// --- Une question ? ---
const questionSubCategories = [
  {
    slug: 'questions-invites', icon: '👤',
    name: 'Questions des invités', desc: 'Vous n\'êtes pas encore membre ? Posez vos questions ici',
  },
  {
    slug: 'questions-membres', icon: '💬',
    name: 'Questions des membres', desc: 'Vous êtes membre de Nexus Arcana ? Posez vos questions à l\'équipe',
  },
  {
    slug: 'signaler-absence', icon: '🌙',
    name: 'Signaler une absence', desc: 'Prévenez l\'équipe de votre absence ou retour',
  },
]

const totalTopics = computed(() => {
  return forum.categories?.reduce((sum, cat) => sum + (cat.topic_count || 0), 0) || 0
})

const totalPosts = computed(() => {
  return forum.categories?.reduce((sum, cat) => sum + (cat.post_count || 0), 0) || 0
})

function particleStyle(n) {
  const left = Math.random() * 100
  const delay = Math.random() * 8
  const duration = 6 + Math.random() * 8
  const size = 2 + Math.random() * 4
  return {
    left: `${left}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`,
    width: `${size}px`,
    height: `${size}px`,
  }
}

const isGuest = computed(() => !auth.isAuthenticated)
const isAdmin = computed(() => ['admin', 'fondatrice'].includes(auth.user?.role))

// --- Contexte éditable ---
const contextContent = ref('')
const contextEditMode = ref(false)
const contextEditContent = ref('')
const contextSaving = ref(false)

async function loadContext() {
  try {
    const { data } = await api.get('/pages/home-context/')
    contextContent.value = data.content || ''
  } catch { /* silencieux */ }
}

async function saveContext() {
  contextSaving.value = true
  try {
    const { data } = await api.patch('/pages/home-context/', { content: contextEditContent.value })
    contextContent.value = data.content
    contextEditMode.value = false
  } finally {
    contextSaving.value = false
  }
}

// --- Tableau de bord ---
const stats = ref(null)

async function fetchStats() {
  try {
    const { data } = await api.get('/stats/')
    stats.value = data
  } catch { /* silent */ }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

function toRelativeAvatar(url) {
  if (!url) return null
  try { return new URL(url).pathname } catch { return url }
}

onMounted(() => {
  forum.fetchCategories()
  fetchStaff()
  fetchFeaturedScenarios()
  fetchStats()
  loadContext()
})
</script>

<style scoped>
/* === Hero === */
.hero {
  position: relative;
  min-height: 540px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  margin-top: 0;
}

.hero-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(5, 8, 19, 0.62) 0%, rgba(7, 12, 28, 0.28) 48%, rgba(5, 8, 19, 0.56) 100%),
    linear-gradient(180deg, transparent 38%, var(--bg) 100%);
}

.hero-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    linear-gradient(115deg, transparent 20%, rgba(124, 92, 255, 0.18) 49%, transparent 72%),
    radial-gradient(circle at 50% 42%, rgba(143, 229, 223, 0.14), transparent 28%);
  mix-blend-mode: screen;
}

html.light .hero-overlay {
  background:
    linear-gradient(180deg, rgba(245, 243, 250, 0.3) 0%, rgba(245, 243, 250, 0.5) 50%, var(--bg) 100%),
    linear-gradient(0deg, var(--bg) 0%, transparent 30%);
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 3rem 1.5rem;
  max-width: 700px;
}

.hero-triquetra {
  margin-bottom: 1.5rem;
  filter: drop-shadow(0 0 18px rgba(143, 229, 223, 0.42)) drop-shadow(0 0 34px rgba(124, 92, 255, 0.38));
  animation: float 4s ease-in-out infinite;
}

.hero-title {
  font-family: var(--font-display);
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(110deg, #f1f5ff 8%, var(--accent) 48%, var(--gold) 94%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  letter-spacing: 0.04em;
  line-height: 1.2;
  text-shadow: none;
}

.hero-tagline {
  font-family: var(--font-display);
  font-size: 1.1rem;
  color: var(--gold);
  font-style: italic;
  margin-bottom: 0.5rem;
  opacity: 0.9;
}

.hero-subtitle {
  font-size: 1.05rem;
  color: #d8e3f1;
  margin-bottom: 2rem;
}

.hero-eyebrow {
  color: var(--accent);
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  line-height: 1.6;
  margin: 0 auto 0.65rem;
  max-width: 610px;
  text-transform: uppercase;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-lg {
  padding: 0.75rem 2rem;
  font-size: 0.95rem;
  border-radius: var(--radius-lg);
}

/* Hero Particles */
.hero-particles {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

.particle {
  position: absolute;
  bottom: -10px;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent);
  border-radius: 50%;
  opacity: 0;
  animation: rise-particle linear infinite;
}

@keyframes rise-particle {
  0% {
    opacity: 0;
    transform: translateY(0) scale(0);
  }
  20% {
    opacity: 0.8;
    transform: translateY(-60px) scale(1);
  }
  80% {
    opacity: 0.3;
  }
  100% {
    opacity: 0;
    transform: translateY(-480px) scale(0.5);
  }
}

/* === Quick Nav Bar === */
.quick-nav-bar {
  position: relative;
  z-index: 2;
  padding: 0.75rem 0;
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--glass-border);
}

.qnav-links {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.qnav-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1.25rem;
  border-radius: 2rem;
  border: 1px solid var(--border);
  background: var(--bg-secondary);
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: all var(--transition);
}

.qnav-item:hover,
.qnav-item.router-link-active {
  background: var(--primary-light);
  border-color: var(--accent);
  color: var(--accent);
}

.qnav-cta {
  background: linear-gradient(135deg, var(--primary-light), rgba(139, 92, 246, 0.15));
  border-color: rgba(139, 92, 246, 0.4);
  color: var(--accent);
}

.qnav-cta:hover {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}

.qnav-icon {
  font-size: 1rem;
}

/* === Crossover === */
.crossover-section {
  padding: 3.25rem 0 0;
  position: relative;
  z-index: 1;
}

.crossover-intro {
  align-items: center;
  background:
    radial-gradient(circle at 88% 50%, rgba(245, 215, 110, 0.15), transparent 20rem),
    linear-gradient(120deg, rgba(47, 22, 82, 0.92), rgba(14, 11, 28, 0.98));
  display: flex;
  gap: 2rem;
  justify-content: space-between;
  overflow: hidden;
  padding: 2rem 2.25rem;
}

.crossover-copy {
  max-width: 700px;
}

.crossover-copy .intro-tag {
  margin-bottom: 0.85rem;
}

.crossover-title {
  color: var(--text);
  font-family: var(--font-display);
  font-size: clamp(1.45rem, 3vw, 2.1rem);
  margin: 0 0 0.75rem;
}

.crossover-copy > p:last-child {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.75;
  margin: 0;
}

.crossover-seal {
  align-items: center;
  color: var(--gold);
  display: flex;
  flex: 0 0 92px;
  font-size: 1.7rem;
  height: 92px;
  justify-content: center;
  position: relative;
}

.crossover-seal::before,
.crossover-seal-ring {
  border: 1px solid rgba(245, 215, 110, 0.65);
  border-radius: 50%;
  inset: 4px;
  position: absolute;
}

.crossover-seal::before {
  content: '';
  transform: rotate(45deg);
}

.crossover-seal-ring {
  inset: 15px;
}

.crossover-seal > span:first-child {
  filter: drop-shadow(0 0 8px rgba(245, 215, 110, 0.7));
  position: relative;
  z-index: 1;
}

.crossover-worlds {
  display: grid;
  gap: 0.9rem;
  grid-template-columns: repeat(4, 1fr);
  margin-top: 1rem;
}

.crossover-world {
  background: linear-gradient(155deg, rgba(29, 24, 50, 0.95), rgba(12, 10, 24, 0.98));
  border: 1px solid rgba(167, 139, 250, 0.2);
  border-top: 2px solid var(--world-color, var(--accent));
  border-radius: var(--radius-lg);
  min-height: 200px;
  padding: 1.3rem;
  position: relative;
  transition: transform var(--transition), border-color var(--transition), box-shadow var(--transition);
}

.crossover-world:hover {
  border-color: var(--world-color, var(--accent));
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.25);
  transform: translateY(-3px);
}

.crossover-world--charmed { --world-color: #c084fc; }
.crossover-world--mystic { --world-color: #c95f72; }
.crossover-world--orleans { --world-color: #d3a24c; }
.crossover-world--beacon { --world-color: #67ad83; }

.crossover-world-kicker,
.crossover-world-source {
  color: var(--world-color, var(--accent));
  display: block;
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.13em;
  text-transform: uppercase;
}

.crossover-world h3 {
  color: var(--text);
  font-family: var(--font-display);
  font-size: 1.1rem;
  margin: 0.65rem 0 0.55rem;
}

.crossover-world p {
  color: var(--text-secondary);
  font-size: 0.8rem;
  line-height: 1.6;
  margin: 0;
}

.crossover-world-source {
  bottom: 1.15rem;
  left: 1.3rem;
  position: absolute;
}

.crossover-note {
  color: var(--text-muted);
  font-size: 0.78rem;
  font-style: italic;
  margin: 1rem 0 0;
  text-align: center;
}

/* === Forum Presentation === */
.forum-intro {
  position: relative;
  z-index: 1;
  padding: 3rem 0 2rem;
}

.intro-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  align-items: stretch;
}

/* Lore block */
.intro-lore {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 460px;
  min-height: 0;
  box-sizing: border-box;
}

.intro-lore--editing { height: auto; min-height: 460px; }

.intro-lore-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-left: 0;
  padding-left: 0;
  color: var(--text);
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 600;
  letter-spacing: 0;
  text-transform: none;
}

.intro-lore-title svg { color: var(--accent); flex-shrink: 0; }

.intro-lore-scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding-right: 0.75rem;
  scrollbar-width: thin;
  scrollbar-color: var(--accent) rgba(0, 0, 0, 0.2);
}

.intro-lore-scroll::-webkit-scrollbar { width: 5px; }
.intro-lore-scroll::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.2); border-radius: 4px; }
.intro-lore-scroll::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 4px; }
.intro-lore-scroll:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }
.intro-lore-hint { color: var(--text-muted); font-size: 0.65rem; text-align: right; margin: 0; }

.intro-tag {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--gold);
  border-left: 2px solid var(--gold);
  padding-left: 0.625rem;
  margin: 0;
}

.intro-title {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--text), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.intro-text {
  font-size: 0.9rem;
  line-height: 1.75;
  color: var(--text-secondary);
  margin: 0;
}

/* Context editor */
.context-html {
  font-size: 0.9rem;
  line-height: 1.75;
  color: var(--text-secondary);
}
.context-html h1, .context-html h2, .context-html h3 {
  font-family: var(--font-display);
  color: var(--text);
  margin: 0.5rem 0;
}
.context-html em { color: var(--accent); font-style: italic; }
.context-html strong { color: var(--text); }
.context-html p { margin: 0 0 0.75rem; }

.context-edit-btn {
  align-self: flex-end;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text-secondary);
  font-size: 0.72rem;
  padding: 0.3rem 0.65rem;
  cursor: pointer;
  transition: border-color var(--transition), color var(--transition);
}
.context-edit-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.context-hint {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-style: italic;
  margin: 0;
}

.context-textarea {
  width: 100%;
  min-height: 200px;
  background: rgba(0,0,0,0.3);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  font-family: monospace;
  font-size: 0.8rem;
  padding: 0.75rem;
  resize: vertical;
  box-sizing: border-box;
}
.context-textarea:focus {
  outline: none;
  border-color: var(--accent);
}

.context-preview {
  background: rgba(0,0,0,0.2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem;
  font-size: 0.85rem;
  line-height: 1.7;
  color: var(--text-secondary);
  min-height: 60px;
}
.context-preview h1, .context-preview h2, .context-preview h3 {
  font-family: var(--font-display);
  color: var(--text);
  margin: 0.5rem 0;
}
.context-preview em { color: var(--accent); }
.context-preview strong { color: var(--text); }
.context-preview p { margin: 0 0 0.5rem; }

.context-actions {
  display: flex;
  gap: 0.75rem;
}

.intro-text em {
  color: var(--accent);
  font-style: normal;
  font-weight: 500;
}

.intro-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
}

/* Members block */
.intro-members {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow: visible;
  align-self: stretch;
}

.intro-members-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.intro-members-title svg {
  color: var(--accent);
  flex-shrink: 0;
}

/* Container for scenarios */
.intro-scenarios-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Grille de scénarios (personnages attendus) — transformed to 2-row horizontal slider */
.intro-scenarios {
  display: grid;
  grid-template-rows: 1fr 1fr;
  grid-auto-flow: column;
  grid-auto-columns: min(130px, calc(100% / 3.5 - 0.6rem));
  gap: 0.6rem;
  overflow-x: auto;
  scroll-behavior: smooth;
  scroll-snap-type: x mandatory;
  padding-bottom: 0.5rem;
  /* Scrollbar hiding for cleaner look, especially on mobile */
  scrollbar-width: thin;
  scrollbar-color: var(--accent) rgba(0, 0, 0, 0.2);
}

.intro-scenarios::-webkit-scrollbar {
  height: 4px;
}
.intro-scenarios::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}
.intro-scenarios::-webkit-scrollbar-thumb {
  background: var(--accent);
  border-radius: 4px;
}

.intro-scenarios-hint {
  font-size: 0.65rem;
  color: var(--text-muted);
  text-align: right;
  margin-top: 0.2rem;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.3rem;
  opacity: 0.8;
}

.intro-scenario-card {
  scroll-snap-align: start;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  aspect-ratio: 2 / 3;
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid rgba(124,58,237,0.3);
  text-decoration: none;
  transition: all var(--transition);
  background: linear-gradient(160deg, rgba(109,40,217,0.18) 0%, rgba(13,10,26,0.97) 100%);
  text-align: center;
}

.intro-scenario-card:hover {
  border-color: var(--accent);
  box-shadow: 0 0 14px rgba(139, 92, 246, 0.45);
  transform: translateY(-2px);
}

.intro-scenario-more {
  background: linear-gradient(160deg, rgba(139, 92, 246, 0.15) 0%, rgba(13, 10, 26, 0.95) 100%);
  border-color: rgba(139, 92, 246, 0.4);
}
.intro-scenario-more:hover {
  background: linear-gradient(160deg, rgba(139, 92, 246, 0.25) 0%, rgba(245, 215, 110, 0.1) 100%);
}

/* Image de couverture */
.intro-scenario-img-wrap {
  position: absolute;
  inset: 0;
}

.intro-scenario-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
  transition: transform 0.4s ease;
}

.intro-scenario-card:hover .intro-scenario-img {
  transform: scale(1.06);
}

/* Icône fallback (sans image) */
.intro-scenario-icon {
  font-size: 1.4rem;
  display: block;
  margin-bottom: 0.3rem;
  filter: drop-shadow(0 0 6px rgba(167,139,250,0.5));
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Titre — centré au milieu de la carte */
.intro-scenario-name {
  position: absolute;
  z-index: 1;
  left: 0;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  padding: 0.4rem 0.3rem;
  background: rgba(7,7,14,0.65);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-size: 0.6rem;
  font-weight: 600;
  color: #e2d9f3;
  line-height: 1.35;
  text-align: center;
}

/* État vide */
.intro-scenarios-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 2rem 1rem;
  color: var(--text-secondary);
  text-align: center;
  font-size: 0.875rem;
}

.intro-scenarios-empty-icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 0.25rem;
  animation: float 4s ease-in-out infinite;
}

.intro-scenarios-empty-sub {
  font-size: 0.75rem;
  color: var(--text-muted);
  max-width: 220px;
}

/* === Stats Bar === */
.stats-bar {
  position: relative;
  z-index: 1;
  margin-top: -2rem;
  padding: 0 1.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  background: var(--card-bg);
  backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  padding: 1.5rem 2rem;
  box-shadow: var(--shadow-lg), var(--shadow-glow);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  justify-content: center;
}

.stat-icon {
  font-size: 1.5rem;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text);
}

.stat-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* === Categories Section === */
.categories-section {
  position: relative;
  z-index: 1;
  padding: 3rem 0 4rem;
}

.section-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: linear-gradient(135deg, var(--accent), var(--gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-title svg {
  flex-shrink: 0;
  color: var(--accent);
}

/* === Category Cards === */
.category-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  text-decoration: none;
  color: var(--text);
  cursor: pointer;
  animation: fade-in-up 0.6s ease-out both;
}

.category-icon {
  width: 52px;
  height: 52px;
  border-radius: var(--radius);
  background: var(--primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
  transition: all var(--transition);
}

.category-card:hover .category-icon {
  background: var(--primary);
  box-shadow: 0 0 16px var(--primary-glow);
  transform: scale(1.05);
}

.category-info {
  flex: 1;
  min-width: 0;
}

.category-name {
  font-family: var(--font-display);
  font-size: 1.05rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  transition: color var(--transition);
}

.category-card:hover .category-name {
  color: var(--accent);
}

.category-desc {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.category-stats {
  display: flex;
  gap: 0.5rem;
}

.category-arrow {
  flex-shrink: 0;
  color: var(--text-muted);
  transition: all var(--transition);
}

.category-card:hover .category-arrow {
  color: var(--accent);
  transform: translateX(4px);
}

/* === Empty State === */
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
  animation: float 3s ease-in-out infinite;
}

/* === Staff Section === */
.staff-section {
  padding: 0 0 2rem;
  position: relative;
  z-index: 1;
}

.staff-section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.staff-section-head .section-title {
  margin-bottom: 0;
}

.staff-edit-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.875rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: var(--bg-secondary);
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 500;
  font-family: var(--font-body);
  cursor: pointer;
  transition: all var(--transition);
  white-space: nowrap;
}

.staff-edit-btn:hover,
.staff-edit-btn.active {
  background: var(--primary-light);
  border-color: var(--accent);
  color: var(--accent);
}

.staff-edit-input {
  width: 100%;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  padding: 0.35rem 0.5rem;
  font-size: 0.8rem;
  font-family: var(--font-body);
  color: var(--text);
  outline: none;
  transition: border-color var(--transition);
  text-align: center;
}

.staff-edit-input:focus {
  border-color: var(--accent);
}

.staff-edit-input::placeholder {
  color: var(--text-muted);
}

.staff-edit-select {
  width: 100%;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  padding: 0.35rem 0.5rem;
  font-size: 0.75rem;
  font-family: var(--font-body);
  color: var(--accent);
  outline: none;
  cursor: pointer;
  text-align: center;
}

.staff-add-slot {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  width: 100%;
  height: 100%;
  min-height: 160px;
  color: var(--text-muted);
  font-size: 0.75rem;
}

.staff-add-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  padding: 0.5rem 0.875rem;
  border-radius: var(--radius);
  border: 1px dashed var(--border);
  color: var(--text-muted);
  font-size: 0.72rem;
  cursor: pointer;
  transition: all var(--transition);
  text-align: center;
}

.staff-add-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--primary-light);
}

.staff-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.staff-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.875rem;
  padding: 1.5rem 1rem;
  text-align: center;
  transition: all var(--transition);
}

.staff-card--empty {
  opacity: 0.35;
  border-style: dashed;
}

.staff-avatar-wrap {
  width: 90px;
  height: 120px;
  border-radius: var(--radius);
  overflow: hidden;
  border: 2px solid var(--border-strong);
  box-shadow: var(--shadow), 0 0 12px rgba(240, 198, 116, 0.15);
  transition: all var(--transition);
  flex-shrink: 0;
  position: relative;
  cursor: default;
}

.staff-avatar-wrap--editable {
  cursor: pointer;
}

.staff-avatar-edit-overlay {
  position: absolute;
  inset: 0;
  background: rgba(7, 7, 14, 0.6);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  opacity: 0;
  transition: opacity var(--transition);
}

.staff-avatar-wrap:hover .staff-avatar-edit-overlay {
  opacity: 1;
}

.staff-upload-input {
  display: none;
}

.staff-card:not(.staff-card--empty):hover .staff-avatar-wrap {
  border-color: var(--gold);
  box-shadow: var(--shadow-lg), 0 0 22px rgba(240, 198, 116, 0.4);
}

.staff-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.staff-card:hover .staff-avatar-img {
  transform: scale(1.06);
}

.staff-avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--bg-elevated), var(--bg-secondary));
  font-family: var(--font-display);
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--gold);
}

.staff-avatar-placeholder--empty {
  color: var(--text-muted);
  font-size: inherit;
}

.staff-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}

.staff-pseudo {
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text);
}

.staff-pseudo--empty {
  color: var(--text-muted);
  font-style: italic;
  font-weight: 400;
}

.staff-username {
  font-size: 0.72rem;
  color: var(--text-secondary);
}

.staff-role-badge {
  display: inline-block;
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: 0.2rem 0.625rem;
  border-radius: 999px;
  border: 1px solid;
  margin-top: 0.15rem;
}

.staff-role-admin {
  background: rgba(240, 198, 116, 0.12);
  color: var(--gold);
  border-color: rgba(240, 198, 116, 0.4);
}

.staff-role-fondatrice {
  background: linear-gradient(135deg, rgba(240, 198, 116, 0.2), rgba(192, 132, 252, 0.15));
  color: var(--gold);
  border-color: rgba(240, 198, 116, 0.55);
  text-shadow: 0 0 8px rgba(240, 198, 116, 0.35);
  box-shadow: 0 0 8px rgba(240, 198, 116, 0.12);
}

.staff-role-moderator {
  background: rgba(139, 92, 246, 0.12);
  color: var(--accent);
  border-color: rgba(139, 92, 246, 0.35);
}

/* === Bienvenue Section (variante verte) === */
.bienvenue-section {
  padding-bottom: 0 !important;
}

.bienvenue-header {
  background: linear-gradient(
    135deg,
    rgba(52, 211, 153, 0.06) 0%,
    var(--card-bg) 50%,
    rgba(134, 239, 172, 0.04) 100%
  ) !important;
  border-color: rgba(52, 211, 153, 0.22) !important;
}

.bienvenue-header:hover {
  border-color: rgba(52, 211, 153, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(52, 211, 153, 0.14) !important;
}

.liens-header {
  background: linear-gradient(
    135deg,
    rgba(244, 114, 182, 0.06) 0%,
    rgba(251, 191, 36, 0.04) 100%
  ) !important;
  border-color: rgba(244, 114, 182, 0.22) !important;
}

.liens-header:hover {
  border-color: rgba(244, 114, 182, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(244, 114, 182, 0.14) !important;
}

.situation-header {
  background: linear-gradient(
    135deg,
    rgba(52, 211, 153, 0.08) 0%,
    rgba(16, 185, 129, 0.04) 100%
  ) !important;
  border-color: rgba(52, 211, 153, 0.22) !important;
}

.situation-header:hover {
  border-color: rgba(52, 211, 153, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(52, 211, 153, 0.14) !important;
}

.question-header {
  background: linear-gradient(
    135deg,
    rgba(56, 189, 248, 0.08) 0%,
    rgba(14, 165, 233, 0.04) 100%
  ) !important;
  border-color: rgba(56, 189, 248, 0.22) !important;
}

.question-header:hover {
  border-color: rgba(56, 189, 248, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(56, 189, 248, 0.14) !important;
}

.rues-commercantes-header {
  background: linear-gradient(
    135deg,
    rgba(251, 191, 36, 0.08) 0%,
    rgba(245, 158, 11, 0.04) 100%
  ) !important;
  border-color: rgba(251, 191, 36, 0.22) !important;
}

.rues-commercantes-header:hover {
  border-color: rgba(251, 191, 36, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(251, 191, 36, 0.14) !important;
}

.centre-ville-header {
  background: linear-gradient(
    135deg,
    rgba(99, 202, 183, 0.08) 0%,
    rgba(20, 184, 166, 0.04) 100%
  ) !important;
  border-color: rgba(99, 202, 183, 0.22) !important;
}

.centre-ville-header:hover {
  border-color: rgba(99, 202, 183, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(99, 202, 183, 0.14) !important;
}

.civic-center-header {
  background: linear-gradient(
    135deg,
    rgba(6, 182, 212, 0.08) 0%,
    rgba(8, 145, 178, 0.04) 100%
  ) !important;
  border-color: rgba(6, 182, 212, 0.22) !important;
}

.civic-center-header:hover {
  border-color: rgba(6, 182, 212, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(6, 182, 212, 0.14) !important;
}

.quartier-culturel-header {
  background: linear-gradient(
    135deg,
    rgba(244, 63, 94, 0.08) 0%,
    rgba(225, 29, 72, 0.04) 100%
  ) !important;
  border-color: rgba(244, 63, 94, 0.22) !important;
}

.quartier-culturel-header:hover {
  border-color: rgba(244, 63, 94, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(244, 63, 94, 0.14) !important;
}

.quartier-affaires-header {
  background: linear-gradient(
    135deg,
    rgba(99, 102, 241, 0.08) 0%,
    rgba(79, 70, 229, 0.04) 100%
  ) !important;
  border-color: rgba(99, 102, 241, 0.22) !important;
}

.quartier-affaires-header:hover {
  border-color: rgba(99, 102, 241, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(99, 102, 241, 0.14) !important;
}

.fishermans-wharf-header {
  background: linear-gradient(
    135deg,
    rgba(245, 158, 11, 0.08) 0%,
    rgba(217, 119, 6, 0.04) 100%
  ) !important;
  border-color: rgba(245, 158, 11, 0.22) !important;
}

.fishermans-wharf-header:hover {
  border-color: rgba(245, 158, 11, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(245, 158, 11, 0.14) !important;
}

.presidio-header {
  background: linear-gradient(
    135deg,
    rgba(239, 68, 68, 0.08) 0%,
    rgba(220, 38, 38, 0.04) 100%
  ) !important;
  border-color: rgba(239, 68, 68, 0.22) !important;
}

.presidio-header:hover {
  border-color: rgba(239, 68, 68, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(239, 68, 68, 0.14) !important;
}

.glen-park-header {
  background: linear-gradient(
    135deg,
    rgba(34, 197, 94, 0.08) 0%,
    rgba(22, 163, 74, 0.04) 100%
  ) !important;
  border-color: rgba(34, 197, 94, 0.22) !important;
}

.glen-park-header:hover {
  border-color: rgba(34, 197, 94, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(34, 197, 94, 0.14) !important;
}

.ocean-beach-header {
  background: linear-gradient(
    135deg,
    rgba(59, 130, 246, 0.08) 0%,
    rgba(37, 99, 235, 0.04) 100%
  ) !important;
  border-color: rgba(59, 130, 246, 0.22) !important;
}

.ocean-beach-header:hover {
  border-color: rgba(59, 130, 246, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(59, 130, 246, 0.14) !important;
}

.cimetiere-header {
  background: linear-gradient(
    135deg,
    rgba(107, 114, 128, 0.08) 0%,
    rgba(75, 85, 99, 0.04) 100%
  ) !important;
  border-color: rgba(107, 114, 128, 0.22) !important;
}

.cimetiere-header:hover {
  border-color: rgba(107, 114, 128, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(107, 114, 128, 0.14) !important;
}

.quartiers-header {
  background: linear-gradient(
    135deg,
    rgba(251, 146, 60, 0.08) 0%,
    rgba(234, 88, 12, 0.04) 100%
  ) !important;
  border-color: rgba(251, 146, 60, 0.22) !important;
}

.quartiers-header:hover {
  border-color: rgba(251, 146, 60, 0.6) !important;
  box-shadow: var(--shadow-lg), 0 0 28px rgba(251, 146, 60, 0.14) !important;
}

/* === Bienvenue à toi — groupe compact === */
.bienvenue-group {
  padding: 0 0 2rem;
  position: relative;
  z-index: 1;
}

.bgroup-banner {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem 1.75rem;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, rgba(240,198,116,0.08) 0%, rgba(192,132,252,0.06) 100%);
  border: 1px solid rgba(240,198,116,0.18);
  border-radius: var(--radius);
}

.bgroup-banner-icon {
  color: var(--accent-gold, #f0c674);
  flex-shrink: 0;
  opacity: 0.85;
}

.bgroup-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text);
  margin: 0 0 0.15rem;
  letter-spacing: 0.01em;
}

.bgroup-subtitle {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin: 0;
}

.bgroup-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.bgroup-card {
  padding: 1rem 1.1rem 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.bgroup-cat-header {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  text-decoration: none;
  color: var(--text);
  transition: color var(--transition);
}

.bgroup-cat-header:hover {
  color: var(--accent);
}

.bgroup-cat-icon {
  font-size: 1rem;
  flex-shrink: 0;
}

.bgroup-cat-title {
  font-size: 0.85rem;
  font-weight: 600;
  flex: 1;
  line-height: 1.3;
}

.bgroup-cat-arrow {
  flex-shrink: 0;
  opacity: 0.4;
  transition: opacity var(--transition);
}

.bgroup-cat-header:hover .bgroup-cat-arrow {
  opacity: 0.9;
}

.bgroup-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.bgroup-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.2rem 0.5rem;
  background: rgba(139,92,246,0.07);
  border: 1px solid rgba(139,92,246,0.12);
  border-radius: 999px;
  font-size: 0.7rem;
  color: var(--text-secondary);
  white-space: nowrap;
  cursor: default;
}

.sf-banner {
  background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(59,130,246,0.06) 100%);
  border-color: rgba(99,102,241,0.18);
}

.sf-banner .bgroup-banner-icon {
  color: rgba(99,102,241,0.8);
}

.staff-promote {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin: 0 0 1rem;
  padding: 0.75rem 1rem;
  color: var(--text-secondary);
  font-size: 0.82rem;
}
.staff-promote .staff-edit-select { flex: 1; }

.crossover-city-group {
  padding-top: 1.5rem;
}

.crossover-city-banner {
  background: linear-gradient(135deg, color-mix(in srgb, var(--city-color) 16%, transparent), rgba(8, 13, 28, 0.82));
  border-color: color-mix(in srgb, var(--city-color) 42%, transparent);
}

.crossover-city-symbol {
  align-items: center;
  background: color-mix(in srgb, var(--city-color) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--city-color) 35%, transparent);
  border-radius: 50%;
  color: var(--city-color);
  display: flex;
  flex: 0 0 46px;
  font-size: 1.35rem;
  height: 46px;
  justify-content: center;
}

.crossover-city-universe {
  color: var(--city-color);
  font-size: 0.61rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  margin: 0 0 0.25rem;
}

.crossover-city--mystic-falls { --city-color: #d9839a; }
.crossover-city--la-nouvelle-orleans { --city-color: #e8bc6b; }
.crossover-city--beacon-hills { --city-color: #84cba5; }

.lieux-magiques-banner {
  background: linear-gradient(135deg, rgba(192,132,252,0.1) 0%, rgba(139,92,246,0.07) 100%);
  border-color: rgba(192,132,252,0.22);
}

.lieux-magiques-banner .bgroup-banner-icon {
  color: rgba(192,132,252,0.85);
}

.monde-banner {
  background: linear-gradient(135deg, rgba(56,189,248,0.1) 0%, rgba(14,165,233,0.07) 100%);
  border-color: rgba(56,189,248,0.22);
}

.partenariats-banner {
  background: linear-gradient(135deg, rgba(52,211,153,0.1) 0%, rgba(16,185,129,0.07) 100%);
  border-color: rgba(52,211,153,0.22);
}

.partenariats-banner .bgroup-banner-icon {
  color: rgba(52,211,153,0.85);
}

.sf-grid {
  grid-template-columns: 1fr 1fr 1fr;
}

@media (max-width: 900px) {
  .sf-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .bgroup-grid,
  .sf-grid {
    grid-template-columns: 1fr;
  }
}

/* === Grimoire Section === */
.grimoire-section {
  padding: 0 0 2.5rem;
  position: relative;
  z-index: 1;
}

/* En-tête grande catégorie */
.grimoire-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.75rem 2rem;
  margin-bottom: 1rem;
  text-decoration: none;
  color: var(--text);
  background: linear-gradient(
    135deg,
    rgba(240, 198, 116, 0.07) 0%,
    var(--card-bg) 50%,
    rgba(192, 132, 252, 0.06) 100%
  );
  border: 1px solid rgba(240, 198, 116, 0.25);
  transition: all var(--transition);
  position: relative;
  overflow: hidden;
}

.grimoire-header:hover {
  border-color: var(--gold);
  box-shadow: var(--shadow-lg), 0 0 28px rgba(240, 198, 116, 0.18);
  transform: translateY(-2px);
}

.grimoire-header-deco {
  flex-shrink: 0;
  opacity: 0.7;
  transition: opacity var(--transition);
}

.grimoire-header:hover .grimoire-header-deco {
  opacity: 1;
}

.grimoire-header-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}


.grimoire-title {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: linear-gradient(135deg, var(--text) 40%, var(--gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.grimoire-title svg {
  flex-shrink: 0;
  color: var(--gold);
  -webkit-text-fill-color: unset;
}

.grimoire-desc {
  font-size: 0.82rem;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.grimoire-header-arrow {
  flex-shrink: 0;
  color: var(--gold);
  opacity: 0.5;
  transition: all var(--transition);
}

.grimoire-header:hover .grimoire-header-arrow {
  opacity: 1;
  transform: translateX(4px);
}

/* === Mini-répertoire compact === */
.grimoire-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.75rem 0 0.25rem;
}

.grimoire-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--bg-secondary);
  font-size: 0.78rem;
  color: var(--text-secondary);
  cursor: default;
  transition: all var(--transition);
  white-space: nowrap;
}

.grimoire-chip:hover {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--primary-light);
}

.grimoire-chip-icon {
  font-size: 0.95rem;
  line-height: 1;
}

.grimoire-chip-name {
  font-weight: 500;
}

/* === Responsive === */
@media (max-width: 768px) {
  .crossover-intro {
    align-items: flex-start;
    padding: 1.5rem;
  }

  .crossover-seal {
    flex-basis: 66px;
    height: 66px;
  }

  .crossover-worlds {
    grid-template-columns: repeat(2, 1fr);
  }

  .intro-grid {
    grid-template-columns: 1fr;
  }

  .intro-scenarios {
    grid-template-columns: repeat(4, 1fr);
  }

  .hero {
    min-height: 400px;
  }

  .hero-title {
    font-size: 2rem;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
    padding: 1.25rem;
  }

  .grid-categories {
    grid-template-columns: 1fr;
  }

  .staff-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .grimoire-header {
    flex-wrap: wrap;
    gap: 1rem;
  }

  .grimoire-header-deco {
    display: none;
  }

  .grimoire-preview {
    gap: 0.375rem;
  }
}

@media (max-width: 480px) {
  .hero-eyebrow {
    font-size: 0.56rem;
    letter-spacing: 0.09em;
  }
  .staff-promote { align-items: stretch; flex-direction: column; }

  .crossover-section {
    padding-top: 2.25rem;
  }

  .crossover-intro {
    gap: 1rem;
  }

  .crossover-title {
    font-size: 1.3rem;
  }

  .crossover-seal {
    display: none;
  }

  .crossover-worlds {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: 1.6rem;
  }

  .hero-tagline {
    font-size: 0.95rem;
  }
}

/* === Sections verrouillées pour les invités === */
.guest-locked .bgroup-cat-header {
  pointer-events: none;
  cursor: default;
}

.no-link {
  pointer-events: none;
  cursor: default;
}

/* === Tableau de bord === */
.dashboard-section {
  padding: 3rem 0 4rem;
}

.dashboard-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 1.5rem;
  color: var(--accent);
}

.dashboard-title {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text);
  margin: 0;
  letter-spacing: 0.06em;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 2fr;
  gap: 1rem;
}

@media (max-width: 900px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

.dash-card {
  background: var(--surface);
  border: 1px solid rgba(124, 58, 237, 0.2);
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
}

.dash-card-label {
  font-size: 0.65rem;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 0 0 1rem;
}

/* Compteurs */
.dash-counters {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
}

.dash-counter-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.dash-counter-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.dash-counter-body {
  display: flex;
  flex-direction: column;
}

.dash-counter-value {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--gold);
  line-height: 1;
}

.dash-counter-label {
  font-size: 0.78rem;
  color: var(--text-secondary);
  margin-top: 0.2rem;
}

.dash-divider {
  height: 1px;
  background: rgba(124, 58, 237, 0.15);
}

/* Dernier inscrit */
.dash-newest {
  display: flex;
  flex-direction: column;
}

.dash-member-row {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  text-decoration: none;
  color: inherit;
  border-radius: 8px;
  padding: 0.4rem;
  transition: background var(--transition);
}

.dash-member-row:hover {
  background: rgba(124, 58, 237, 0.08);
}

.dash-member-name {
  display: block;
  font-size: 0.92rem;
  color: var(--text);
  font-weight: 500;
}

.dash-member-date {
  display: block;
  font-size: 0.72rem;
  color: var(--text-secondary);
  margin-top: 0.15rem;
  font-style: italic;
}

/* En ligne */
.dash-online-list {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  max-height: 220px;
  overflow-y: auto;
}

.dash-online-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  color: var(--text);
  border-radius: 6px;
  padding: 0.25rem 0.4rem;
  transition: background var(--transition);
}

.dash-online-item:hover {
  background: rgba(124, 58, 237, 0.08);
}

.dash-online-name {
  font-size: 0.85rem;
}

/* Avatars */
.dash-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid rgba(124, 58, 237, 0.3);
  flex-shrink: 0;
}

.dash-avatar-sm {
  width: 28px;
  height: 28px;
}

.dash-avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(124, 58, 237, 0.15);
  font-size: 0.7rem;
  color: var(--accent);
}

.dash-empty {
  font-size: 0.82rem;
  color: var(--text-secondary);
  font-style: italic;
  margin: 0;
}
</style>
