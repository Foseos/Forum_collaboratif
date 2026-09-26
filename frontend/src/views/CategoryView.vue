<template>
  <div class="page">
    <div class="container">
    <div class="category-header">
      <div>
        <router-link to="/" class="text-sm text-secondary">&larr; Catégories</router-link>
        <h1 class="page-title" style="margin-bottom: 0.25rem">
          {{ forum.currentCategory?.name || fallbackCategoryName }}
        </h1>
        <p v-if="forum.currentCategory?.description" class="text-secondary">
          {{ forum.currentCategory.description }}
        </p>
      </div>
      <router-link
        v-if="auth.isAuthenticated && props.slug === 'demande-double-compte'"
        to="/demande-double-compte/nouvelle"
        class="btn btn-primary"
      >
        ✉ Faire ma demande
      </router-link>
      <router-link
        v-else-if="auth.isAuthenticated && auth.user?.fiche_status !== 'validated' && props.slug === 'fiches-de-presentation-terminees'"
        to="/fiches/nouvelle"
        class="btn btn-primary"
      >
        + Créer ma fiche
      </router-link>
      <button v-else-if="props.slug === 'demande-de-partenariats'" class="btn btn-primary" @click="showPartnershipForm = !showPartnershipForm">
        {{ showPartnershipForm ? 'Fermer le formulaire' : '+ Proposer un partenariat' }}
      </button>
      <button
        v-else-if="auth.isAuthenticated && !isParentCategory && !['demande-de-partenariats', 'nos-partenaires'].includes(props.slug) && props.slug !== 'fiches-de-presentation-terminees' && props.slug !== 'agence-immobiliere' && props.slug !== 'recherche-de-rp' && (props.slug !== 'parrainage' || isAdminOrFondatrice) && (!isCharacterSheetCategory || (canCreateRecap && !ownRecapTopic))"
        class="btn btn-primary"
        @click="openNewTopic"
      >
        {{ isCharacterSheetCategory ? '+ Créer mon récapitulatif' : props.slug === 'parrainage' ? '+ Ouvrir un parrainage' : '+ Nouveau sujet' }}
      </button>
    </div>

    <section v-if="props.slug === 'demande-de-partenariats'" class="recap-guide card">
      <p class="recap-eyebrow">✦ Rencontres entre univers</p>
      <h2>Faisons connaissance</h2>
      <p>Un partenariat peut prendre la forme d’un échange de fiches, de boutons, ou des deux. Chaque forum ouvre une demande à son nom et le staff lui répond dans son sujet. Les invités peuvent aussi proposer leur forum, sans inscription.</p>
      <p>Aucun minimum de membres ou d’ancienneté n’est demandé. Nous apprécions surtout une présentation claire et un échange suivi.</p>
      <div class="recap-guide-actions">
        <router-link to="/topics/proposer-un-partenariat" class="btn btn-secondary btn-sm">Lire le guide et copier le modèle</router-link>
        <router-link to="/categories/nos-partenaires" class="btn btn-secondary btn-sm">Voir nos partenaires</router-link>
      </div>
    </section>

    <section v-if="props.slug === 'nos-partenaires'" class="recap-guide card">
      <p class="recap-eyebrow">✦ Les mondes qui nous entourent</p>
      <h2>Nos partenaires</h2>
      <p>Retrouvez ici les forums avec lesquels Nexus Arcana échange. Chaque fiche ouvre le sujet du partenaire et ses liens.</p>
      <router-link to="/categories/demande-de-partenariats" class="btn btn-secondary btn-sm">Proposer un partenariat</router-link>
    </section>

    <form v-if="props.slug === 'demande-de-partenariats' && showPartnershipForm" class="recap-guide card partnership-form" @submit.prevent="submitPartnership">
      <h2>Présenter mon forum</h2>
      <p class="text-secondary">Les informations envoyées seront visibles dans un sujet public. Revenez sur ce sujet pour lire la réponse du staff.</p>
      <label>Nom du forum <input v-model="partnership.forum_name" class="form-input" maxlength="120" required></label>
      <label>Adresse du forum <input v-model="partnership.forum_url" class="form-input" type="url" placeholder="https://…" required></label>
      <label>Univers et concept <textarea v-model="partnership.concept" class="form-input" maxlength="2000" rows="3" required></textarea></label>
      <label>Date d’ouverture <input v-model="partnership.opened_at" class="form-input" maxlength="100" placeholder="Facultatif"></label>
      <label>Échange souhaité <select v-model="partnership.partnership_type" class="form-input"><option value="fiches">Échange de fiches</option><option value="boutons">Échange de boutons</option><option value="les deux">Fiches et boutons</option></select></label>
      <label>Lien vers notre affichage chez vous <input v-model="partnership.reciprocal_url" class="form-input" type="url" placeholder="Facultatif"></label>
      <label>Votre fiche de partenariat <textarea v-model="partnership.presentation" class="form-input" maxlength="3000" rows="3" placeholder="Texte de présentation ou lien vers votre fiche"></textarea></label>
      <label>Adresse de votre bouton <input v-model="partnership.button_url" class="form-input" type="url" placeholder="Facultatif"></label>
      <label>Un mot pour le staff <textarea v-model="partnership.message" class="form-input" maxlength="2000" rows="3" placeholder="Facultatif"></textarea></label>
      <input v-model="partnership.website" class="partnership-honeypot" tabindex="-1" autocomplete="off" aria-hidden="true">
      <p v-if="partnershipError" role="alert" class="create-error">{{ partnershipError }}</p>
      <button type="submit" class="btn btn-primary" :disabled="submittingPartnership">{{ submittingPartnership ? 'Envoi…' : 'Publier ma demande' }}</button>
    </form>

    <section v-if="isCharacterSheetCategory" class="recap-guide card">
      <p class="recap-eyebrow">✦ Après la validation</p>
      <h2>Le carnet de votre personnage</h2>
      <p>Cette rubrique rassemble des portraits faciles à consulter. Votre fiche de présentation validée reste la référence pour l’histoire et les pouvoirs ; ici, résumez ce qui aide les autres joueurs à vous retrouver et faites évoluer votre carnet au fil des RP.</p>
      <p><strong>Un sujet par personnage.</strong> Vous pourrez modifier votre premier message pour actualiser les liens, les relations et les événements importants.</p>
      <div class="recap-guide-actions">
        <router-link v-if="ownRecapTopic" :to="`/topics/${ownRecapTopic.slug}`" class="btn btn-primary btn-sm">Voir mon carnet</router-link>
        <span v-else-if="auth.isAuthenticated && !canCreateRecap" class="text-secondary text-sm">Votre présentation doit d’abord être validée.</span>
      </div>
    </section>

    <section v-if="props.slug === 'demande-double-compte'" class="recap-guide card">
      <p class="recap-eyebrow">✦ Un nouveau personnage</p>
      <h2>Demander un double compte</h2>
      <p>Présentez votre idée de personnage, sa nature et l’avatar envisagé. Le staff pourra échanger avec vous dans le sujet créé par le formulaire avant de vous donner sa réponse.</p>
      <router-link v-if="auth.isAuthenticated" to="/demande-double-compte/nouvelle" class="btn btn-primary btn-sm">Remplir le formulaire</router-link>
      <router-link v-else to="/login" class="btn btn-secondary btn-sm">Se connecter pour faire une demande</router-link>
    </section>

    <section v-if="props.slug === 'parrainage'" class="recap-guide card">
      <p class="recap-eyebrow">✦ Bienvenue à Nexus Arcana</p>
      <h2>Un premier repère dans le Nexus</h2>
      <p>Un membre expérimenté peut accompagner un nouveau joueur dans ses premiers pas : découvrir les rubriques, poser des questions et trouver des pistes de RP. Le parrainage est libre et se construit à deux.</p>
      <p><strong>Un sujet par binôme.</strong> Après votre accord, contactez l’administration : elle ouvrira un sujet portant vos deux noms. Vous pourrez y échanger au fil de l’accompagnement ; les autres membres pourront consulter les échanges.</p>
      <router-link to="/topics/guide-du-parrainage" class="btn btn-secondary btn-sm">Lire le guide du parrainage</router-link>
    </section>

    <!-- Sous-catégories Bienvenue à Nexus Arcana -->
    <router-link v-if="props.slug === 'bienvenue-san-francisco'" to="/bienvenue/parcours-arrivee" class="recap-guide card arrival-guide-link">
      <p class="recap-eyebrow">✦ Nouveau sur le forum ?</p>
      <h2>Suivre le parcours d’arrivée →</h2>
      <p>Du contexte à ton premier RP, retrouve les étapes et les liens utiles au même endroit.</p>
    </router-link>
    <div v-if="props.slug === 'bienvenue-san-francisco'" class="sub-list">
      <!-- CTA Créer ma fiche -->
      <div class="sub-cta">
        <p class="sub-cta-text">Prêt à rejoindre l'aventure ?</p>
        <router-link
          v-if="auth.isAuthenticated && auth.user?.fiche_status !== 'validated'"
          to="/fiches/nouvelle"
          class="btn btn-primary btn-sm"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Créer ma fiche
        </router-link>
        <router-link v-else-if="!auth.isAuthenticated" to="/register" class="btn btn-primary btn-sm">
          Rejoindre Nexus Arcana
        </router-link>
      </div>

      <router-link
        v-for="sub in bienvenueSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Ma situation magique -->
    <div v-if="props.slug === 'ma-situation-magique'" class="sub-list">
      <router-link
        v-for="sub in situationSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Une question ? -->
    <div v-if="props.slug === 'une-question'" class="sub-list">
      <router-link
        v-for="sub in questionSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Quartiers résidentiels -->
    <div v-if="cityDistricts.length" class="sub-list">
      <router-link
        v-for="district in cityDistricts"
        :key="district.slug"
        :to="`/categories/${district.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ district.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ district.name }}</span>
          <span class="sub-desc">{{ district.desc }}</span>
        </div>
        <div class="sub-stats"><span class="sub-stat-label">Lieu de RP →</span></div>
      </router-link>
    </div>

    <!-- Sous-catégories Quartiers résidentiels -->
    <div v-if="props.slug === 'quartiers-residentiels'" class="sub-list">
      <router-link
        v-for="sub in quartiersSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Rues commerçantes -->
    <div v-if="props.slug === 'rues-commercantes'" class="sub-list">
      <router-link
        v-for="sub in ruesCommercantesSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Centre ville -->
    <div v-if="props.slug === 'centre-ville'" class="sub-list">
      <router-link
        v-for="sub in centreVilleSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Civic Center -->
    <div v-if="props.slug === 'civic-center'" class="sub-list">
      <router-link
        v-for="sub in civicCenterSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Quartier culturel et d'enseignement -->
    <div v-if="props.slug === 'quartier-culturel-et-enseignement'" class="sub-list">
      <router-link
        v-for="sub in quartierCulturelSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Quartier des affaires -->
    <div v-if="props.slug === 'quartier-des-affaires'" class="sub-list">
      <router-link
        v-for="sub in quartierAffairesSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Fisherman's Wharf -->
    <div v-if="props.slug === 'fishermans-wharf'" class="sub-list">
      <router-link
        v-for="sub in fishermansWharfSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Cimetière -->
    <div v-if="props.slug === 'cimetiere'" class="sub-list">
      <router-link
        v-for="sub in cimetiereSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories École de magie -->
    <div v-if="props.slug === 'ecole-de-magie'" class="sub-list">
      <router-link
        v-for="sub in ecoleMagieSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Les Enfers -->
    <!-- Sous-catégories Continents -->
    <div v-if="props.slug === 'continents'" class="sub-list">
      <router-link
        v-for="sub in continentsSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Les Cieux -->
    <div v-if="props.slug === 'les-cieux'" class="sub-list">
      <router-link
        v-for="sub in lesCieuxSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Dimensions alternatives -->
    <div v-if="props.slug === 'dimensions-alternatives'" class="sub-list">
      <router-link
        v-for="sub in dimensionsAlternativesSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Les Enfers -->
    <div v-if="props.slug === 'les-enfers'" class="sub-list">
      <router-link
        v-for="sub in lesEnfersSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Presidio of San Francisco -->
    <div v-if="props.slug === 'presidio-of-san-francisco'" class="sub-list">
      <router-link
        v-for="sub in presidioSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Glen Park -->
    <div v-if="props.slug === 'glen-park'" class="sub-list">
      <router-link
        v-for="sub in glenParkSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Ocean Beach -->
    <div v-if="props.slug === 'ocean-beach'" class="sub-list">
      <router-link
        v-for="sub in oceanBeachSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories Liens magiques -->
    <div v-if="props.slug === 'liens-magiques'" class="sub-list">
      <router-link
        v-for="sub in liensSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>
        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>
        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>
        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Sous-catégories (uniquement pour le Règlement magique) -->
    <div v-if="props.slug === 'reglement-magique'" class="sub-list">
      <router-link
        v-for="sub in grimoireSubCategories"
        :key="sub.slug"
        :to="`/categories/${sub.slug}`"
        class="sub-row card"
      >
        <div class="sub-icon">{{ sub.icon }}</div>

        <div class="sub-info">
          <span class="sub-name">{{ sub.name }}</span>
          <span class="sub-desc">{{ sub.desc }}</span>
        </div>

        <div class="sub-stats">
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.topic_count ?? 0 }}</span>
            <span class="sub-stat-label">sujets</span>
          </div>
          <div class="sub-stat">
            <span class="sub-stat-value">{{ categoryStats[sub.slug]?.post_count ?? 0 }}</span>
            <span class="sub-stat-label">messages</span>
          </div>
        </div>

        <div class="sub-last">
          <div class="sub-last-avatar-wrap">
            <img v-if="lastPostMap[sub.slug]?.author_avatar" :src="lastPostMap[sub.slug].author_avatar" class="sub-last-avatar" />
            <div v-else class="sub-last-avatar-fallback">{{ (lastPostMap[sub.slug]?.author_pseudo || '?')[0].toUpperCase() }}</div>
          </div>
          <div class="sub-last-body">
            <span class="sub-last-title">{{ lastPostMap[sub.slug]?.topic_title || sub.lastPost.title }}</span>
            <span class="sub-last-meta">{{ lastPostMap[sub.slug]?.author_pseudo || sub.lastPost.author }} · {{ lastPostMap[sub.slug] ? formatSubDate(lastPostMap[sub.slug].created_at) : sub.lastPost.date }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Formulaire nouveau sujet -->
    <div v-if="showNewTopic" class="card mb-2">
      <h3 style="margin-bottom: 0.75rem">{{ isCharacterSheetCategory ? 'Créer le carnet de mon personnage' : 'Créer un sujet' }}</h3>
      <p v-if="isCharacterSheetCategory" class="text-secondary" style="margin: -0.25rem 0 0.9rem; font-size: 0.85rem">
        Le modèle est déjà inséré. Remplace les indications entre crochets et ajoute un lien vers ta fiche validée.
      </p>
      <div class="form-group">
        <label>Titre</label>
        <input v-model="newTopic.title" class="form-input" :placeholder="isCharacterSheetCategory ? 'Ex : Prénom Nom — carnet de personnage' : 'Titre du sujet'" />
      </div>
      <div class="form-group" style="margin-bottom: 0">
        <label>Premier message</label>
        <!-- Onglets Écrire / Prévisualiser -->
        <div class="editor-tabs">
          <button
            class="editor-tab"
            :class="{ active: !showPreview }"
            @click="showPreview = false"
          >
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            Écrire
          </button>
          <button
            class="editor-tab"
            :class="{ active: showPreview }"
            :disabled="!newTopic.content.trim()"
            @click="showPreview = true"
          >
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            Prévisualiser
          </button>
        </div>
        <!-- Zone d'écriture -->
        <RichTextField v-if="!showPreview" v-model="newTopic.content" label="Premier message du sujet" placeholder="Écrivez votre premier message…" />
        <!-- Panneau de prévisualisation -->
        <div v-else class="preview-panel">
          <div class="preview-bar">
            <span class="preview-label">Aperçu</span>
            <span class="preview-hint">Rendu tel qu'il apparaîtra sur le forum</span>
          </div>
          <div class="preview-body" v-html="newTopic.content"></div>
        </div>
      </div>
      <p v-if="createError" class="create-error">{{ createError }}</p>
      <div class="flex gap-1" style="justify-content: flex-end; margin-top: 1rem">
        <span v-if="draftStatus" class="text-sm text-secondary" role="status">{{ draftStatus }}</span>
        <button class="btn btn-secondary btn-sm" @click="cancelNewTopic" :disabled="creating">Fermer</button>
        <button class="btn btn-primary btn-sm" :disabled="!newTopic.title.trim() || !newTopic.content.trim() || creating" @click="handleCreateTopic">
          {{ creating ? 'Création…' : 'Créer' }}
        </button>
      </div>
    </div>


    <!-- ── Modèle de fiche de présentation ────────────────────────────── -->
    <template v-if="props.slug === 'modele-fiche-de-presentation'">
      <!-- Post verrouillé de l'admin -->
      <div class="card fiche-post">
        <!-- En-tête : auteur + verrou -->
        <div class="fiche-post-meta">
          <div class="fiche-post-author">
            <div class="fiche-author-avatar">
              <img
                v-if="ficheAuthor?.avatar"
                :src="ficheAuthor.avatar"
                :alt="ficheAuthor.username"
                class="fiche-avatar-img"
              />
              <span v-else>{{ ficheAuthor?.username?.[0]?.toUpperCase() || 'AB' }}</span>
            </div>
            <div class="fiche-author-info">
              <span class="fiche-author-name">{{ ficheAuthor?.username || 'Ava Bartholomé' }}</span>
              <span class="fiche-author-badge">✦ Administration de Nexus Arcana</span>
            </div>
          </div>
          <div class="fiche-lock-tag">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            Verrouillé
          </div>
        </div>

        <div class="fiche-post-divider"></div>

        <!-- Corps : aperçu visuel du modèle -->
        <div class="fiche-post-body" v-html="FICHE_HTML_TEMPLATE"></div>

        <!-- Bloc code copiable -->
        <div class="fiche-code-block">
          <div class="fiche-code-header">
            <div class="fiche-code-label">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
              Code à copier dans votre éditeur
            </div>
            <button class="btn btn-primary btn-sm" @click="copyFicheTemplate">
              <svg v-if="!ficheCopied" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="flex-shrink:0"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
              {{ ficheCopied ? '✓ Copié !' : 'Copier le code' }}
            </button>
          </div>
          <textarea
            class="fiche-code-area"
            readonly
            :value="FICHE_HTML_TEMPLATE"
            @click="$event.target.select()"
          ></textarea>
        </div>
      </div>

      <!-- Notice bas de page -->
      <div class="fiche-locked-notice">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        Sujet verrouillé — seule l'équipe de modération peut le modifier.
        Copiez le code, puis rendez-vous dans
        <router-link to="/categories/fiches-de-presentation-terminees" class="fiche-link">Fiches en attente de validation</router-link>
        pour soumettre votre fiche.
      </div>
    </template>


    <LoadingSpinner v-if="forum.loading && props.slug !== 'modele-fiche-de-presentation'" />

    <div v-else-if="isCharacterSheetCategory" class="recap-directory">
      <section class="recap-directory-section">
        <h2>Modèle officiel</h2>
        <router-link to="/topics/modele-fiche-personnage" class="recap-model-link card">
          <span aria-hidden="true">📋</span>
          <span><strong>Modèle fiche personnage</strong><small>Consulter et copier le modèle pour créer votre carnet.</small></span>
          <span class="recap-arrow" aria-hidden="true">→</span>
        </router-link>
      </section>

      <section class="recap-directory-section">
        <h2>Carnets des personnages</h2>
        <p class="text-secondary">Les récapitulatifs publiés par les joueurs validés sont accessibles à tous.</p>
        <div v-if="characterRecaps.length" class="recap-cards">
          <router-link v-for="topic in characterRecaps" :key="topic.id" :to="`/topics/${topic.slug}`" class="recap-card card">
            <img v-if="topic.author?.avatar" :src="topic.author.avatar" :alt="topic.author?.username" class="recap-avatar">
            <span v-else class="recap-avatar recap-avatar-fallback">{{ (topic.author?.username || '?')[0].toUpperCase() }}</span>
            <span class="recap-card-info"><strong>{{ topic.title }}</strong><small>par {{ topic.author?.username }}</small></span>
            <span class="recap-arrow" aria-hidden="true">→</span>
          </router-link>
        </div>
        <p v-else class="recap-empty card">Aucun carnet publié pour le moment. Le premier personnage validé peut ouvrir le sien.</p>
      </section>
      <PaginationBar :page="forum.pagination.page" :count="forum.pagination.count" @change="loadPage" />
    </div>

    <div v-else-if="props.slug !== 'modele-fiche-de-presentation'" class="topics-list">
      <TopicCard
        v-for="topic in forum.topics"
        :key="topic.id"
        :topic="topic"
      />

      <div v-if="forum.topics.length === 0" class="text-center text-secondary" style="padding: 3rem">
        Aucun sujet dans cette catégorie.
      </div>

      <PaginationBar
        :page="forum.pagination.page"
        :count="forum.pagination.count"
        @change="loadPage"
      />
    </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useForumStore } from '../stores/forum'
import { useAuthStore } from '../stores/auth'
import TopicCard from '../components/TopicCard.vue'
import PaginationBar from '../components/PaginationBar.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import RichTextField from '../components/RichTextField.vue'
import subData from '../data/subcategories.json'
import { crossoverCities } from '../data/crossoverCities'
import api from '../composables/useApi'
import { useLocalDraft } from '../composables/useLocalDraft'

const props = defineProps({
  slug: { type: String, required: true },
})

const bienvenueSubCategories  = subData.bienvenue
const grimoireSubCategories   = subData.grimoire
const liensSubCategories      = subData.liens
const situationSubCategories  = subData.situation
const questionSubCategories   = subData.question
const quartiersSubCategories  = subData.quartiers
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
const lesCieuxSubCategories = subData.lesCieux
const continentsSubCategories = subData.continents
const cityDistricts = computed(() => crossoverCities.find(city => city.slug === props.slug)?.districts || [])
const dimensionsAlternativesSubCategories = subData.dimensionsAlternatives
const ruesCommercantesSubCategories = subData.ruesCommercantes
const centreVilleSubCategories = subData.centreVille

// Pages sans bouton "Nouveau sujet" :
// - pages parent (sous-listes uniquement)
// - recensement : les joueurs répondent au sujet épinglé, ils ne créent pas de nouveaux sujets
const isParentCategory = computed(() => {
  const fixed = [
    'bienvenue-san-francisco',
    'fiches-validees-et-archivees',
    'reglement-magique',
    'modele-fiche-de-presentation',
    'liens-magiques',
    'une-question',
    'ma-situation-magique',
    'quartiers-residentiels',
    'centre-ville',
    'rues-commercantes',
    'quartier-des-affaires',
    'quartier-culturel-et-enseignement',
    'civic-center',
    'ocean-beach',
    'glen-park',
    'presidio-of-san-francisco',
    'fishermans-wharf',
    'cimetiere',
    'ecole-de-magie',
    'les-enfers',
    'dimensions-alternatives',
    'les-cieux',
    'continents',
    ...crossoverCities.map(city => city.slug),
  ]
  // La sous-catégorie du grimoire des pouvoirs est une fiche officielle : pas de nouveau sujet
  fixed.push('grimoire-des-pouvoirs')
  // Les sous-catégories du grimoire sont des fiches officielles : pas de nouveau sujet
  const grimoireSlugs = grimoireSubCategories.map(s => s.slug)
  return [...fixed, ...grimoireSlugs].includes(props.slug)
})


const fallbackCategoryName = computed(() => {
  const all = [...bienvenueSubCategories, ...grimoireSubCategories, ...liensSubCategories, ...questionSubCategories, ...situationSubCategories, ...quartiersSubCategories, ...centreVilleSubCategories, ...ruesCommercantesSubCategories, ...quartierAffairesSubCategories, ...quartierCulturelSubCategories, ...civicCenterSubCategories, ...oceanBeachSubCategories, ...glenParkSubCategories, ...presidioSubCategories, ...fishermansWharfSubCategories, ...cimetiereSubCategories, ...ecoleMagieSubCategories, ...lesEnfersSubCategories, ...dimensionsAlternativesSubCategories, ...lesCieuxSubCategories, ...continentsSubCategories]
  return all.find(s => s.slug === props.slug)?.name || crossoverCities.find(city => city.slug === props.slug)?.name || props.slug
})

const forum = useForumStore()
const auth = useAuthStore()
const router = useRouter()
const showPartnershipForm = ref(false)
const submittingPartnership = ref(false)
const partnershipError = ref('')
const partnership = reactive({ forum_name: '', forum_url: '', concept: '', opened_at: '', partnership_type: 'les deux', reciprocal_url: '', presentation: '', button_url: '', message: '', website: '' })

async function submitPartnership() {
  partnershipError.value = ''
  submittingPartnership.value = true
  try {
    const { data } = await api.post('/partnership-requests/', partnership)
    router.push(`/topics/${data.slug}`)
  } catch (error) {
    const details = error.response?.data
    partnershipError.value = details?.detail || Object.values(details || {})[0]?.[0] || 'Impossible de publier la demande. Réessayez.'
  } finally {
    submittingPartnership.value = false
  }
}

const isAdminOrFondatrice = computed(() =>
  auth.user?.role === 'admin' || auth.user?.role === 'fondatrice'
)
const isCharacterSheetCategory = computed(() => props.slug === 'fiche-personnage')
const characterRecaps = computed(() => forum.topics.filter(topic => topic.slug !== 'modele-fiche-personnage'))
const canCreateRecap = computed(() => auth.user?.fiche_status === 'validated' || isAdminOrFondatrice.value)
const ownRecapTopic = ref(null)
const isScenarioCategory = computed(() => props.slug === 'scenarios-a-prendre')

// ── Règlement éditable ────────────────────────────────────────────────────
const reglContent = ref('')
const reglEditMode = ref(false)
const reglEditContent = ref('')
const reglSaving = ref(false)

async function loadReglement() {
  if (props.slug !== 'reglement-du-forum') return
  try {
    const { data } = await api.get('/pages/reglement-du-forum/')
    reglContent.value = data.content
  } catch { /* silencieux */ }
}

async function saveReglement() {
  reglSaving.value = true
  try {
    const { data } = await api.patch('/pages/reglement-du-forum/', { content: reglEditContent.value })
    reglContent.value = data.content
    reglEditMode.value = false
  } finally {
    reglSaving.value = false
  }
}

const showNewTopic = ref(false)
const showPreview = ref(false)
const newTopic = reactive({ title: '', content: '' })
const topicDraftKey = computed(() => auth.user?.id ? `nexus:draft:${auth.user.id}:topic:${props.slug}` : null)
const { status: draftStatus, clear: clearTopicDraft } = useLocalDraft(
  topicDraftKey, () => ({ ...newTopic }), value => Object.assign(newTopic, value),
  () => ({ title: '', content: '' }),
)
const createError = ref('')
const creating = ref(false)

function cancelNewTopic() {
  showNewTopic.value = false
  showPreview.value = false
  createError.value = ''
}

function openNewTopic() {
  showNewTopic.value = true
  showPreview.value = false
  createError.value = ''
  if (isCharacterSheetCategory.value && !newTopic.content) {
    newTopic.title = '[Prénom Nom] — carnet de personnage'
    newTopic.content = RECAP_HTML_TEMPLATE
  }
  if (isScenarioCategory.value && !newTopic.content) {
    newTopic.title = 'Scénario — [Prénom Nom]'
    newTopic.content = SCENARIO_HTML_TEMPLATE
  }
  if (props.slug === 'parrainage' && !newTopic.content) {
    newTopic.title = 'Parrainage — [Nouveau membre] & [Parrain ou marraine]'
    newTopic.content = PARRAINAGE_TEMPLATE
  }
}

const PARRAINAGE_TEMPLATE = `<h2>Notre parrainage</h2>
<p><strong>Nouveau membre :</strong> [Nom d'utilisateur]</p>
<p><strong>Parrain ou marraine :</strong> [Nom d'utilisateur]</p>
<p><strong>Ce que j'aimerais découvrir :</strong> [Univers, rubriques, création de personnage, recherche de RP…]</p>
<p><strong>Nos premières pistes de jeu :</strong> [Facultatif]</p>
<p>Nous pourrons poursuivre la discussion en répondant à ce sujet.</p>`

// Carnet évolutif publié après validation, distinct de la fiche de présentation.
const RECAP_HTML_TEMPLATE = `<div style="font-family:Georgia,'Times New Roman',serif;background:#0d0a1a;color:#e2d9f3;padding:1.8rem;border:1px solid rgba(124,58,237,.35);border-radius:10px;max-width:720px;margin:auto;line-height:1.7">
  <p style="margin:0;text-align:center;color:#a78bfa;font-size:.7rem;letter-spacing:.24em;text-transform:uppercase">✦ Nexus Arcana · Carnet de personnage ✦</p>
  <h1 style="margin:.4rem 0 .2rem;text-align:center;color:#f5d76e;font-size:1.8rem;font-weight:normal;font-style:italic">[Prénom Nom]</h1>
  <p style="margin:0 0 1.5rem;text-align:center;color:#c4b5d4">[Race] · [Camp] · [Ville]</p>
  <div style="border:1px solid rgba(124,58,237,.3);border-radius:7px;padding:1rem;margin-bottom:1rem"><h2 style="margin:0 0 .5rem;color:#a78bfa;font-size:1rem;font-weight:normal">En quelques mots</h2><p style="margin:0">[Qui est votre personnage aujourd’hui ? Son tempérament, son activité, ce qui le préoccupe ou le fait avancer. Quelques phrases suffisent.]</p></div>
  <div style="border:1px solid rgba(124,58,237,.3);border-radius:7px;padding:1rem;margin-bottom:1rem"><h2 style="margin:0 0 .5rem;color:#a78bfa;font-size:1rem;font-weight:normal">Repères</h2><p style="margin:0"><strong>Fiche validée :</strong> [Lien vers votre fiche validée]<br><strong>Ville / quartier :</strong> [Lieu de vie]<br><strong>Faction ou coven :</strong> [Si concerné]<br><strong>Capacités :</strong> [Résumé des pouvoirs déjà validés, sans en ajouter]</p></div>
  <div style="border:1px solid rgba(124,58,237,.3);border-radius:7px;padding:1rem;margin-bottom:1rem"><h2 style="margin:0 0 .5rem;color:#a78bfa;font-size:1rem;font-weight:normal">Liens &amp; relations</h2><p style="margin:0">[Personnes importantes, alliances, tensions et liens que vous aimeriez développer. Ajoutez des liens vers leurs sujets si vous en avez.]</p></div>
  <div style="border:1px solid rgba(124,58,237,.3);border-radius:7px;padding:1rem;margin-bottom:1rem"><h2 style="margin:0 0 .5rem;color:#a78bfa;font-size:1rem;font-weight:normal">Parcours en jeu</h2><p style="margin:0"><strong>Événements marquants :</strong> [Ce qui a changé pour le personnage depuis sa validation]<br><strong>RP en cours :</strong> [Titres et liens]<br><strong>RP terminés :</strong> [Titres et liens]</p></div>
  <p style="margin:1rem 0 0;text-align:center;color:#a78bfa;font-size:.8rem;font-style:italic">Ce carnet peut être enrichi après chaque RP important.</p>
</div>`

// ── Modèle de fiche ───────────────────────────────────────────────────────
const FICHE_HTML_TEMPLATE = `<div style="font-family: Georgia, 'Times New Roman', serif; background: #0d0a1a; color: #e2d9f3; padding: 2rem; border-radius: 10px; border: 1px solid rgba(124,58,237,0.3); max-width: 720px; margin: 0 auto;">

<!-- EN-TÊTE : nom à gauche, image à droite -->
<table style="width: 100%; border-collapse: collapse; margin-bottom: 1.75rem; padding-bottom: 1.5rem; border-bottom: 1px solid rgba(124,58,237,0.2);">
<tr>
  <td style="vertical-align: top; padding-right: 1.5rem;">
    <p style="margin: 0 0 0.5rem; font-size: 0.58rem; letter-spacing: 0.38em; text-transform: uppercase; color: #6d28d9;">✦ Nexus Arcana · Livre des Ombres ✦</p>
    <h1 style="margin: 0 0 0.6rem; font-size: 2rem; font-weight: normal; font-style: italic; color: #f5d76e; letter-spacing: 0.04em; line-height: 1.2;">Prénom(s)<br>Nom</h1>
    <p style="margin: 0 0 1rem; font-size: 0.82rem; color: #a78bfa; font-style: italic; letter-spacing: 0.06em;">Race · Camp</p>
    <p style="margin: 0; font-size: 0.75rem; color: #4b3a6b; font-style: italic; line-height: 1.7;">"Une citation ou accroche qui définit votre personnage en quelques mots."</p>
  </td>
  <td style="vertical-align: top; width: 210px; text-align: center;">
    <!-- Remplacez src par l'URL de votre image de personnage -->
    <img src="/Image_de_base_photo_de_profil.jpg" alt="Prénom NOM" style="width:200px;height:320px;object-fit:cover;border-radius:6px;border:2px solid rgba(124,58,237,0.35);display:block;margin:0 auto;">
    <p style="margin: 0.35rem 0 0; font-size: 0.6rem; color: #3d2d5e; font-style: italic;">Prénom NOM — célébrité jouée</p>
  </td>
</tr>
</table>

<!-- BOX I : IDENTITÉ -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ I. Identité</h2>
  </div>
  <div style="padding: 0.6rem 1rem;">
    <table style="width: 100%; border-collapse: collapse;">
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; width: 42%; border-bottom: 1px solid rgba(124,58,237,0.08);">Âge</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">XX ans</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Date de naissance</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">JJ Mois AAAA</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Sexe</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Féminin / Masculin / Autre</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Orientation sexuelle</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">...</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Situation familiale</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Célibataire / Marié(e) / Veuf(ve) / ...</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Race</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Sorcière / Démon / ...</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Camp</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Bien / Neutre / Mal</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0;">Métier</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3;">...</td></tr>
    </table>
  </div>
</div>

<!-- DÉMONS UNIQUEMENT : supprimez cet encart entier pour les autres races. -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(185,120,139,0.45); border-radius: 7px; overflow: hidden; background: #17101f;">
  <div style="padding: 0.5rem 1rem; border-bottom: 1px solid rgba(185,120,139,0.3); background: rgba(185,120,139,0.1);">
    <h2 style="margin: 0; font-size: 0.65rem; letter-spacing: 0.22em; text-transform: uppercase; color: #d3aab6; font-weight: normal;">◈ Forme démoniaque · si Démon</h2>
  </div>
  <div style="padding: 1rem; text-align: center;">
    <p style="margin: 0 0 0.35rem; color: #f5d76e; font-size: 1rem;">[Nom de la forme]</p>
    <p style="margin: 0 0 0.85rem; color: #c4b5d4; font-size: 0.82rem; line-height: 1.6;">[Décrivez son apparence. Elle doit aussi être déclarée au bottin des formes démoniaques.]</p>
    <!-- Remplacez uniquement l'adresse src par celle de votre image ou de votre GIF ; supprimez l'image si vous n'en souhaitez pas. -->
    <img src="/demon-form-placeholder.svg" alt="Image ou GIF de la forme démoniaque" style="display: block; width: 180px; max-width: 100%; height: 110px; object-fit: cover; border-radius: 6px; margin: 0 auto; border: 1px solid rgba(185,120,139,0.4);">
  </div>
</div>

<!-- BOX II : POUVOIRS -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ II. Pouvoirs Magiques &amp; Aptitudes</h2>
  </div>
  <div style="padding: 0.85rem 1rem 0.75rem;">
    <p style="margin: 0 0 0.4rem; font-size: 0.78rem; font-weight: 600; color: #c4b5fd;">⚡ Pouvoirs actifs :</p>
    <ul style="margin: 0; padding-left: 1.3rem; line-height: 1.85; font-size: 0.87rem; color: #c4b5d4;">
      <li><strong style="color: #e2d9f3;">Nom du pouvoir</strong> — Description et limites du pouvoir</li>
      <li><strong style="color: #e2d9f3;">Nom du pouvoir</strong> — Description et limites du pouvoir</li>
      <li><strong style="color: #e2d9f3;">Nom du pouvoir</strong> — Description et limites du pouvoir</li>
      <li><strong style="color: #e2d9f3;">Nom du pouvoir</strong> — Description et limites du pouvoir</li>
      <li><strong style="color: #e2d9f3;">Nom du pouvoir</strong> — Description et limites du pouvoir</li>
    </ul>
  </div>
</div>

<!-- BOX III : CARACTÈRE -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ III. Âme &amp; Caractère</h2>
  </div>
  <div style="padding: 1rem;">
    <p style="margin: 0; line-height: 1.9; color: #c4b5d4; text-align: justify; font-size: 0.9rem;">[Décrivez la personnalité de votre personnage : ses traits dominants, ses habitudes, ses valeurs, ses peurs, ses forces et faiblesses. Comment se comporte-t-il face aux autres ? Quel est son rapport à la magie, au destin, à la trahison ? Comment réagit-il sous pression ? <em>Minimum 15 lignes.</em>]</p>
  </div>
</div>

<!-- BOX IV : HISTOIRE -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ IV. Mémoire des Âges · Histoire</h2>
  </div>
  <div style="padding: 1rem;">
    <p style="margin: 0; line-height: 1.9; color: #c4b5d4; text-align: justify; font-size: 0.9rem;">[Racontez l'histoire complète de votre personnage : ses origines, les événements qui l'ont façonné, les épreuves traversées, et ce qui l'a conduit dans l'une des villes du Nexus. Comment a-t-il découvert le monde magique ? Quels secrets porte-t-il ? Quelles cicatrices l'invisible lui a-t-il laissées ? <em>Minimum 30 lignes.</em>]</p>
  </div>
</div>

<!-- BOX V : HORS PERSONNAGE -->
<div style="border: 1px solid rgba(245,215,110,0.22); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(245,215,110,0.12), rgba(245,215,110,0.03)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(245,215,110,0.2);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #f5d76e; font-weight: normal;">◈ V. Hors Personnage</h2>
  </div>
  <div style="padding: 0.6rem 1rem;">
    <table style="width: 100%; border-collapse: collapse;">
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; width: 50%; border-bottom: 1px solid rgba(245,215,110,0.07);">Pseudonyme sur le forum</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(245,215,110,0.07);">...</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(245,215,110,0.07);">Âge</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(245,215,110,0.07);">...</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(245,215,110,0.07);">Comment avez-vous connu le forum ?</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(245,215,110,0.07);">...</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(245,215,110,0.07);">Crédits</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(245,215,110,0.07);">Avatar, images, GIFs…</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0;">Souhaitez-vous un parrain / une marraine ?</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3;">Oui / Non</td></tr>
    </table>
  </div>
</div>

<p style="text-align: center; margin: 1.25rem 0 0; font-size: 0.58rem; color: #2d1f4a; font-style: italic; letter-spacing: 0.18em;">✦ Fiche soumise à la validation de Nexus Arcana ✦</p>
</div>`

const SCENARIO_HTML_TEMPLATE = `<div style="font-family: Georgia, 'Times New Roman', serif; background:#0d0a1a; color:#e2d9f3; padding:2rem; border:1px solid rgba(124,58,237,.3); border-radius:10px; max-width:720px; margin:auto;">
  <p style="margin:0 0 .45rem;text-align:center;color:#a78bfa;font-size:.62rem;letter-spacing:.22em;">✦ NEXUS ARCANA · SCÉNARIO ✦</p>
  <h1 style="margin:0 0 .4rem;text-align:center;color:#f5d76e;font-weight:normal;font-style:italic;">PRÉNOM NOM — LIBRE</h1>
  <p style="margin:0 0 1.4rem;text-align:center;color:#c4b5d4;font-style:italic;">ft. Célébrité jouée · conditions éventuelles</p>
  <div style="padding:1rem;margin-bottom:1rem;border:1px solid rgba(124,58,237,.25);border-radius:7px;"><h2 style="margin:0 0 .65rem;color:#a78bfa;font-size:.78rem;letter-spacing:.15em;">I. IDENTITÉ</h2><p><strong>Âge :</strong> …<br><strong>Race / groupe :</strong> …<br><strong>Ville / quartier :</strong> …<br><strong>Métier / statut :</strong> …</p></div>
  <div style="padding:1rem;margin-bottom:1rem;border:1px solid rgba(124,58,237,.25);border-radius:7px;"><h2 style="margin:0 0 .65rem;color:#a78bfa;font-size:.78rem;letter-spacing:.15em;">II. CE QU’IL FAUT SAVOIR</h2><p>Caractère, histoire, éléments non négociables et éléments laissés libres…</p></div>
  <div style="padding:1rem;margin-bottom:1rem;border:1px solid rgba(124,58,237,.25);border-radius:7px;"><h2 style="margin:0 0 .65rem;color:#a78bfa;font-size:.78rem;letter-spacing:.15em;">III. POUVOIRS &amp; LIENS</h2><p><strong>Pouvoirs / limites :</strong> …<br><strong>Liens recherchés :</strong> …</p></div>
  <p style="margin:0;text-align:right;color:#8b7aa8;font-size:.7rem;"><strong>Crédits :</strong> avatar, images, GIFs et ressources…</p>
</div>`

// ── Dernier post par sous-catégorie ──────────────────────────────────────────
const lastPostMap = ref({})
const categoryStats = ref({})

async function loadSubLastPosts() {
  try {
    const { data } = await api.get('/categories/?page_size=200')
    const list = data.results || data
    const map = {}
    for (const cat of list) {
      if (cat.last_post) map[cat.slug] = cat.last_post
    }
    lastPostMap.value = map
    categoryStats.value = Object.fromEntries(list.map(cat => [cat.slug, cat]))
  } catch { /* silencieux */ }
}

function formatSubDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diffDays = Math.floor((now - date) / 86400000)
  if (diffDays === 0) return 'aujourd\'hui'
  if (diffDays === 1) return 'hier'
  return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' })
}

const ficheCopied = ref(false)
async function copyFicheTemplate() {
  await navigator.clipboard.writeText(FICHE_HTML_TEMPLATE)
  ficheCopied.value = true
  setTimeout(() => { ficheCopied.value = false }, 2000)
}

const ficheAuthor = ref(null)
async function loadFicheAuthor() {
  try {
    const { data } = await api.get('/users/?role=fondatrice')
    const list = data.results || data
    if (list.length > 0) ficheAuthor.value = list[0]
  } catch { /* silencieux */ }
}

async function load() {
  await forum.fetchCategory(props.slug)
  ownRecapTopic.value = null
  if (props.slug !== 'modele-fiche-de-presentation') {
    await forum.fetchTopics(props.slug)
    if (isCharacterSheetCategory.value && auth.user?.id) {
      try {
        const { data } = await api.get(`/categories/fiche-personnage/topics/?author=${auth.user.id}`)
        ownRecapTopic.value = (data.results || data).find(topic => topic.slug !== 'modele-fiche-personnage') || null
      } catch { /* la liste reste consultable */ }
    }
  } else {
    loadFicheAuthor()
  }
  loadReglement()
  loadSubLastPosts()
}

onMounted(load)
watch(() => props.slug, load)

function loadPage(page) {
  forum.fetchTopics(props.slug, page)
}

async function handleCreateTopic() {
  createError.value = ''
  creating.value = true
  try {
    const data = await forum.createTopic(props.slug, {
      title: newTopic.title,
      first_post_content: newTopic.content,
    })
    clearTopicDraft()
    showNewTopic.value = false
    showPreview.value = false
    newTopic.title = ''
    newTopic.content = ''
    router.push(`/topics/${data.slug}`)
  } catch (err) {
    const msg = err?.response?.data?.detail
      || err?.response?.data?.title?.[0]
      || err?.response?.data?.first_post_content?.[0]
      || 'Une erreur est survenue. Veuillez réessayer.'
    createError.value = msg
  } finally {
    creating.value = false
  }
}

</script>

<style scoped>
.recap-guide {
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.25rem;
  border-color: rgba(139, 92, 246, .3);
}
.partnership-form { display: grid; gap: .85rem; }
.partnership-form label { display: grid; gap: .35rem; color: var(--text-secondary); font-size: .9rem; }
.partnership-honeypot { position: absolute; left: -9999px; opacity: 0; pointer-events: none; }
.recap-eyebrow { margin: 0 0 .25rem; color: #a78bfa; font-size: .72rem; letter-spacing: .15em; text-transform: uppercase; }
.recap-guide h2 { margin: 0 0 .65rem; color: var(--text-primary); font-size: 1.3rem; }
.recap-guide p { line-height: 1.7; }
.recap-guide-actions { display: flex; flex-wrap: wrap; align-items: center; gap: .75rem; margin-top: 1rem; }
.recap-directory { display: grid; gap: 1.5rem; }
.recap-directory-section h2 { margin: 0 0 .65rem; color: var(--text-primary); font-size: 1.15rem; }
.recap-directory-section > p { margin: 0 0 1rem; }
.recap-model-link, .recap-card { display: flex; align-items: center; gap: .8rem; padding: .9rem 1rem; color: var(--text-primary); text-decoration: none; }
.recap-model-link:hover, .recap-card:hover { border-color: var(--primary); transform: translateY(-1px); }
.recap-model-link > span:first-child { font-size: 1.5rem; }
.recap-model-link > span:nth-child(2), .recap-card-info { display: flex; flex: 1; min-width: 0; flex-direction: column; gap: .2rem; }
.recap-model-link small, .recap-card small { color: var(--text-secondary); font-size: .78rem; }
.recap-arrow { color: var(--primary); font-size: 1.2rem; }
.recap-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 290px), 1fr)); gap: .8rem; }
.recap-card-info strong { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.recap-avatar { width: 43px; height: 43px; flex-shrink: 0; border-radius: 50%; object-fit: cover; }
.recap-avatar-fallback { display: grid; place-items: center; background: rgba(139, 92, 246, .15); color: var(--primary); font-weight: 700; }
.recap-empty { padding: 1.25rem; color: var(--text-secondary); }
.create-error {
  color: #ef4444;
  font-size: 0.8rem;
  margin: 0.75rem 0 0;
  padding: 0.4rem 0.75rem;
  background: rgba(239,68,68,0.08);
  border: 1px solid rgba(239,68,68,0.25);
  border-radius: 6px;
}

/* ── Anciens styles recensement (supprimés) ──────────────────────────────── */
.recensement-desc {
  font-size: 0.78rem;
  color: var(--text-secondary);
  margin: 0;
  font-style: italic;
}

/* ── Category header ─────────────────────────────────────────────────────── */
.category-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.topics-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* === CTA Bienvenue === */
.sub-cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.875rem 1.25rem;
  border-radius: var(--radius);
  background: linear-gradient(135deg, rgba(52, 211, 153, 0.06), rgba(134, 239, 172, 0.04));
  border: 1px dashed rgba(52, 211, 153, 0.3);
  margin-bottom: 0.25rem;
}

.sub-cta-text {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin: 0;
  font-style: italic;
}

/* === Sous-catégories Règlement === */
.sub-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.sub-row {
  display: grid;
  grid-template-columns: 3rem 1fr auto auto;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  text-decoration: none;
  color: var(--text);
  transition: all var(--transition);
  border-left: 3px solid transparent;
}

.sub-row:hover {
  border-left-color: var(--accent);
  box-shadow: var(--shadow), 0 0 16px rgba(139, 92, 246, 0.15);
  transform: translateX(3px);
}

.sub-icon {
  font-size: 1.6rem;
  text-align: center;
  line-height: 1;
  transition: transform var(--transition);
}

.sub-row:hover .sub-icon {
  transform: scale(1.15);
}

.sub-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
}

.sub-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text);
  transition: color var(--transition);
}

.sub-row:hover .sub-name {
  color: var(--accent);
}

.sub-desc {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.sub-stats {
  display: flex;
  gap: 1.25rem;
  flex-shrink: 0;
}

.sub-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.1rem;
  min-width: 3rem;
}

.sub-stat-value {
  font-size: 1rem;
  font-weight: 700;
  color: var(--gold);
}

.sub-stat-label {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--text-muted);
}

.sub-last {
  display: flex;
  align-items: flex-start;
  gap: 0.45rem;
  flex-shrink: 0;
  min-width: 180px;
  max-width: 220px;
  border-left: 1px solid var(--border);
  padding-left: 1rem;
}

.sub-last-avatar-wrap {
  flex-shrink: 0;
}

.sub-last-avatar {
  width: 44px;
  height: 56px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid var(--border);
}

.sub-last-avatar-fallback {
  width: 44px;
  height: 56px;
  border-radius: 6px;
  background: var(--primary-light);
  color: var(--accent);
  font-size: 0.85rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sub-last-body {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  min-width: 0;
}

.sub-last-title {
  font-size: 0.78rem;
  color: var(--text);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sub-last-meta {
  font-size: 0.68rem;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sub-last-meta strong {
  color: var(--accent-light, #a78bfa);
  font-weight: 600;
}

/* ── Modèle fiche de présentation ───────────────────────────────────────── */
.fiche-post {
  padding: 0;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.fiche-post-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  gap: 1rem;
}

.fiche-post-author {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.fiche-author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent, #7c3aed), var(--gold, #d4af37));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  flex-shrink: 0;
  overflow: hidden;
}
.fiche-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
}

.fiche-author-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.fiche-author-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text);
}

.fiche-author-badge {
  font-size: 0.7rem;
  color: var(--gold, #d4af37);
  letter-spacing: 0.04em;
}

.fiche-lock-tag {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.72rem;
  color: var(--text-muted);
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border);
  flex-shrink: 0;
}

.fiche-post-divider {
  height: 1px;
  background: var(--border);
}

.fiche-post-body {
  padding: 1.5rem;
  overflow-x: auto;
}

.fiche-code-block {
  border-top: 1px solid var(--border);
}

.fiche-code-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.65rem 1.25rem;
  border-bottom: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.02);
  flex-wrap: wrap;
}

.fiche-code-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.fiche-code-area {
  display: block;
  width: 100%;
  height: 200px;
  padding: 0.85rem 1.25rem;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.72rem;
  line-height: 1.6;
  color: var(--text-secondary);
  background: transparent;
  border: none;
  resize: vertical;
  outline: none;
  cursor: text;
  box-sizing: border-box;
}

.fiche-code-area:focus {
  background: rgba(167, 139, 250, 0.03);
}

.fiche-locked-notice {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.4rem;
  padding: 0.7rem 1rem;
  font-size: 0.78rem;
  color: var(--text-muted);
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 1rem;
}

.fiche-link {
  color: var(--accent-light, #a78bfa);
  text-decoration: underline;
  text-underline-offset: 2px;
}

/* ── Bannière Créer ma fiche personnage ──────────────────────────────────── */
.fiche-cta-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.25rem;
  border-radius: var(--radius);
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.08), rgba(109, 40, 217, 0.04));
  border: 1px solid rgba(139, 92, 246, 0.25);
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.fiche-cta-left {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  min-width: 0;
}

.fiche-cta-icon {
  font-size: 1.4rem;
  line-height: 1;
  flex-shrink: 0;
}

.fiche-cta-text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
}

.fiche-cta-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: 0.01em;
}

.fiche-cta-desc {
  margin: 0;
  font-size: 0.78rem;
  color: var(--text-secondary);
  font-style: italic;
}

.fiche-cta-btn {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

/* ── Éditeur onglets ─────────────────────────────────────────────────────── */
.editor-tabs {
  display: flex;
  border-bottom: 1px solid var(--border);
  margin-bottom: 0;
}

.editor-tab {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-secondary);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  cursor: pointer;
  transition: color var(--transition), border-color var(--transition);
}

.editor-tab:hover:not(:disabled) {
  color: var(--text);
}

.editor-tab.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

.editor-tab:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.editor-textarea {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
  border-top: none;
  resize: vertical;
  min-height: 120px;
}

/* ── Panneau de prévisualisation ─────────────────────────────────────────── */
.preview-panel {
  border: 1px solid var(--border);
  border-top: none;
  border-radius: 0 0 var(--radius) var(--radius);
  min-height: 120px;
  overflow: hidden;
}

.preview-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.4rem 0.875rem;
  background: rgba(139, 92, 246, 0.05);
  border-bottom: 1px solid var(--border);
}

.preview-label {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent);
}

.preview-hint {
  font-size: 0.7rem;
  color: var(--text-muted);
  font-style: italic;
}

.preview-body {
  padding: 1rem 1.25rem;
  color: var(--text);
  font-size: 0.9rem;
  line-height: 1.75;
  min-height: 80px;
  word-break: break-word;
  overflow-x: auto;
}

@media (max-width: 768px) {
  .category-header {
    flex-direction: column;
  }

  .sub-row {
    grid-template-columns: 2.5rem 1fr;
  }

  .sub-stats,
  .sub-last {
    display: none;
  }

  .fiche-section-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

/* ── Règlement éditable ───────────────────────────────────────────────────── */
.reglement-block {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--glass-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.reglement-content {
  line-height: 1.8;
  color: var(--text);
  font-size: 0.9rem;
}

.reglement-content :deep(h1),
.reglement-content :deep(h2),
.reglement-content :deep(h3) {
  color: var(--gold);
  margin: 1.25rem 0 0.5rem;
}

.reglement-content :deep(a) { color: var(--accent); }
.reglement-content :deep(ul), .reglement-content :deep(ol) { padding-left: 1.5rem; margin: 0.5rem 0; }
.reglement-content :deep(li) { margin: 0.3rem 0; }

.reglement-empty {
  color: var(--text-secondary);
  font-style: italic;
  text-align: center;
  padding: 2rem 0;
  margin: 0;
}

.reglement-edit-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.25rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.reglement-hint {
  font-size: 0.78rem;
  color: var(--text-secondary);
  font-style: italic;
  margin: 0 0 0.75rem;
}

.reglement-textarea {
  width: 100%;
  padding: 0.75rem;
  background: var(--bg-deep);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  font-family: monospace;
  font-size: 0.85rem;
  resize: vertical;
  box-sizing: border-box;
}

.reglement-textarea:focus {
  outline: none;
  border-color: var(--accent);
}

.reglement-preview-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-secondary);
  margin: 1rem 0 0.4rem;
}

.reglement-preview {
  padding: 1rem;
  background: var(--bg-deep);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  min-height: 80px;
  font-size: 0.88rem;
  line-height: 1.7;
  color: var(--text);
  margin-bottom: 1rem;
}

.reglement-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}
</style>
