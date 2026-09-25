<template>
  <div class="page">
    <div class="container">
    <div v-if="forum.currentTopic">
      <router-link
        v-if="forum.currentTopic.category"
        :to="`/categories/${forum.currentTopic.category_slug}`"
        class="text-sm text-secondary"
      >
        &larr; Retour
      </router-link>

      <div class="topic-header">
        <h1 class="page-title" style="margin-bottom: 0.25rem">{{ forum.currentTopic.title }}</h1>
        <button v-if="canEditTitle && !editingTitle" class="btn-admin-edit" @click="startTitleEdit">✏️ Modifier le titre</button>
        <form v-if="canEditTitle && editingTitle" class="topic-title-editor" @submit.prevent="saveTitle">
          <label for="topic-title-input">Titre du sujet</label>
          <input id="topic-title-input" ref="titleInput" v-model="titleDraft" maxlength="200" required :disabled="savingTitle" @keydown.esc.prevent="cancelTitleEdit">
          <div class="flex gap-1">
            <button type="submit" class="btn-admin-edit" :disabled="savingTitle || !titleDraft.trim()">{{ savingTitle ? 'Enregistrement…' : 'Enregistrer' }}</button>
            <button type="button" class="btn-admin-cancel" :disabled="savingTitle" @click="cancelTitleEdit">Annuler</button>
          </div>
        </form>
        <p v-if="titleError" role="alert">{{ titleError }}</p>
        <p v-if="titleSaved" role="status">Titre modifié.</p>
        <div class="flex gap-1 items-center">
          <span v-if="forum.currentTopic.is_pinned" class="badge badge-warning">📌 Épinglé</span>
          <span v-if="forum.currentTopic.is_locked" class="badge badge-danger">🔒 Verrouillé</span>
          <span v-if="isScenario" class="scenario-status" :class="`scenario-status--${forum.currentTopic.scenario_status}`">
            {{ scenarioStatusLabels[forum.currentTopic.scenario_status] || '✦ Libre' }}
          </span>
          <span class="text-sm text-secondary">
            par <strong>{{ forum.currentTopic.author?.username }}</strong>
            &middot; {{ formatDate(forum.currentTopic.created_at) }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="isScenario && isAdminOrFondatrice" class="scenario-admin-bar card">
      <label for="scenario-status">Statut du scénario</label>
      <select id="scenario-status" v-model="scenarioStatus" :disabled="savingScenarioStatus" @change="saveScenarioStatus">
        <option value="free">Libre</option>
        <option value="reserved">Réservé</option>
        <option value="played">Joué</option>
      </select>
      <span class="scenario-admin-help">Un scénario joué reste accessible ici, mais disparaît des Personnages attendus de l’accueil.</span>
    </div>

    <div v-if="isPendingPartnership && auth.isModerator" class="scenario-admin-bar card">
      <strong>Demande de partenariat</strong>
      <button class="btn btn-primary btn-sm" :disabled="approvingPartnership" @click="approvePartnership">{{ approvingPartnership ? 'Validation…' : 'Accepter et afficher dans Nos partenaires' }}</button>
      <span v-if="partnershipApprovalError" role="alert">{{ partnershipApprovalError }}</span>
    </div>

    <!-- Bouton admin : modifier le contenu (topics verrouillés, hors règlement) -->
    <div
      v-if="auth.isModerator && (forum.currentTopic?.is_locked || isHtmlEditableTopic || (isScenario && isAdminOrFondatrice)) && forum.posts[0]?.id === forum.currentTopic?.first_post_id"
      class="admin-edit-bar"
    >
      <button v-if="!editingPost" class="btn-admin-edit" @click="startEdit(forum.posts[0])">
        {{ isScenario ? '✏️ Modifier le code de la fiche' : '✏️ Modifier la fiche' }}
      </button>
      <button v-else class="btn-admin-cancel" @click="editingPost = null">
        ✕ Annuler la modification
      </button>
    </div>

    <div v-if="isScenario && editingPost?.id === forum.currentTopic?.first_post_id" ref="scenarioEditorRef" class="mt-2">
      <p v-if="editError" role="alert">{{ editError }}</p>
      <p class="text-secondary">Le code complet de la fiche est affiché ci-dessous. Modifiez les adresses des images, puis enregistrez la fiche.</p>
      <PostEditor :edit-post="editingPost" :start-in-source-mode="true" :loading="posting" @submit="handleEditSubmit" @cancel="editingPost = null" />
    </div>

    <LoadingSpinner v-if="forum.loading && forum.posts.length === 0" />

    <div v-else>
      <!-- ── Fiche modèle : rendu HTML + zone de copie ── -->
      <template v-if="isFicheModele && forum.posts.length > 0">

        <!-- En-tête auteur (pleine largeur) -->
        <div class="card fiche-post-header">
          <div class="fiche-post-meta">
            <div class="fiche-post-author">
              <div class="fiche-author-avatar">
                <img
                  v-if="forum.posts[0].author?.avatar"
                  :src="forum.posts[0].author.avatar"
                  :alt="forum.posts[0].author.username"
                  class="fiche-avatar-img"
                />
                <span v-else>{{ forum.posts[0].author?.username?.[0]?.toUpperCase() || 'MJ' }}</span>
              </div>
              <div class="fiche-author-info">
                <span class="fiche-author-name">{{ forum.posts[0].author?.username }}</span>
                <span class="fiche-author-badge">✦ Administration de Nexus Arcana</span>
              </div>
            </div>
            <div class="fiche-lock-tag">🔒 Verrouillé</div>
          </div>
        </div>

        <!-- Layout deux colonnes -->
        <div class="fiche-layout">

          <!-- Colonne gauche : aperçu visuel -->
          <div class="fiche-preview-col">
            <div class="fiche-col-label">Aperçu de la fiche</div>
            <div class="fiche-post-body" v-html="forum.posts[0].content"></div>
          </div>

          <!-- Colonne droite : code copiable -->
          <div class="fiche-code-col">
            <div class="fiche-col-label">Code à copier</div>
            <div class="card fiche-code-card">
              <div class="fiche-code-header">
                <span class="fiche-code-label">Code :</span>
                <button class="fiche-select-btn" @click="selectAndCopy">
                  {{ topicCopied ? '✓ Copié !' : 'Sélectionner' }}
                </button>
              </div>
              <textarea
                ref="codeAreaRef"
                class="fiche-code-area"
                readonly
                :value="forum.posts[0].content"
                @click="$event.target.select()"
              ></textarea>
            </div>
            <div class="fiche-notice">
              🔒 Verrouillé — seule l'équipe peut modifier ce modèle.<br>
              Copiez, remplissez et postez dans
              <router-link to="/categories/fiches-de-presentation-terminees">
                Fiches en attente de validation
              </router-link>.
            </div>
          </div>
        </div>

        <!-- Admin : éditeur de la fiche modèle -->
        <div v-if="editingPost" class="mt-2">
          <PostEditor
            :edit-post="editingPost"
            :loading="posting"
            @submit="handleEditSubmit"
            @cancel="editingPost = null"
          />
        </div>
      </template>

      <!-- ── Sujets normaux ── -->
      <template v-else>

        <div v-if="isRecapModel && forum.posts.length" class="partner-copy-bar card">
          <div>
            <strong>Modèle du carnet de personnage</strong>
            <p>Après validation, copiez ce code puis créez votre sujet dans la rubrique Fiche personnage.</p>
          </div>
          <button type="button" class="btn btn-primary" @click="copyRecapModel">{{ recapModelCopied ? '✓ Modèle copié' : '📋 Copier le modèle' }}</button>
          <span v-if="recapCopyError" role="alert">{{ recapCopyError }}</span>
        </div>

        <div v-if="isPartnerRequest" class="partner-copy-bar card">
          <div>
            <strong>Prêt à publier votre recherche ?</strong>
            <p>Copiez le modèle, puis collez-le dans votre réponse et remplacez les indications entre crochets.</p>
          </div>
          <button type="button" class="btn btn-primary" @click="copyPartnerTemplate">
            {{ partnerTemplateCopied ? '✓ Modèle copié' : '📋 Copier le modèle' }}
          </button>
          <span v-if="partnerCopyError" role="alert">{{ partnerCopyError }}</span>
        </div>

        <div v-if="isPartnershipGuide" class="partner-copy-bar card">
          <div><strong>Modèle de demande de partenariat</strong><p>Copiez ce modèle si vous préférez rédiger votre présentation librement. Le formulaire de la rubrique est également accessible aux invités.</p></div>
          <button type="button" class="btn btn-primary" @click="copyPartnershipModel">{{ partnershipModelCopied ? '✓ Modèle copié' : '📋 Copier le modèle' }}</button>
          <span v-if="partnershipModelError" role="alert">{{ partnershipModelError }}</span>
        </div>

        <!-- Barre admin règlement -->
        <div
          v-if="isHtmlEditableTopic && isAdminOrFondatrice && forum.posts.length > 0"
          class="admin-edit-bar"
        >
          <button v-if="!reglementEditMode" class="btn-admin-edit" @click="startReglementEdit">
            ✏️ Modifier le règlement
          </button>
          <button v-else class="btn-admin-cancel" @click="reglementEditMode = false">
            ✕ Annuler la modification
          </button>
        </div>

        <!-- Éditeur HTML inline règlement -->
        <div v-if="isHtmlEditableTopic && reglementEditMode" class="reglement-html-editor card">
          <p class="reglement-editor-hint">HTML accepté — prévisualisation en temps réel ci-dessous.</p>
          <textarea v-model="reglementEditContent" class="reglement-textarea" rows="22" />
          <div class="reglement-editor-actions">
            <button class="btn btn-primary" @click="saveReglementEdit" :disabled="savingReglement">
              {{ savingReglement ? 'Enregistrement…' : '💾 Enregistrer' }}
            </button>
            <button class="btn btn-ghost" @click="reglementEditMode = false">Annuler</button>
          </div>
          <div class="reglement-preview-label">Prévisualisation</div>
          <div class="reglement-preview" v-html="reglementEditContent" />
        </div>

        <TransitionGroup name="slide" tag="div">
          <PostCard
            v-for="post in forum.posts"
            :key="post.id"
            :post="post"
            :locked="forum.currentTopic?.is_locked"
            :scenario-first-post="isScenario && post.id === forum.currentTopic?.first_post_id"
            :grimoire="slug === 'liste-des-pouvoirs-magiques'"
            @edit="startEdit"
            @delete="handleDelete"
            @react="handleReaction"
            @avatarUpdated="load"
          />
        </TransitionGroup>

        <section v-if="slug === 'loterie-des-arcana-flouz'" class="card" style="padding:1.25rem;margin:1.5rem 0">
          <h2 style="margin:0 0 .5rem">✦ Tenter ma chance</h2>
          <p class="text-secondary">Un message de RP de plus de 100 mots publié ces sept derniers jours vous donne droit à un tirage.</p>
          <template v-if="auth.isAuthenticated">
            <p v-if="lotteryStatus" role="status">{{ lotteryStatus.reason }} <span v-if="lotteryStatus.next_at">Prochain tirage : {{ formatDate(lotteryStatus.next_at) }}.</span></p>
            <button type="button" class="btn btn-primary" :disabled="drawingLottery || !lotteryStatus?.available" @click="drawLottery">{{ drawingLottery ? 'Tirage en cours…' : 'Tenter ma chance' }}</button>
          </template>
          <p v-else><router-link to="/login">Connectez-vous</router-link> pour participer.</p>
          <p v-if="lotteryResult" role="status">Vous gagnez <strong>{{ lotteryResult.prize }} Arcana Flouz</strong> grâce à votre RP « {{ lotteryResult.qualifying_topic }} » !</p>
          <p v-if="lotteryError" role="alert">{{ lotteryError }}</p>
        </section>

        <section v-if="showDiceRoller" class="card" style="padding:1.25rem;margin:1.5rem 0">
          <h2 style="margin:0 0 .5rem">🎲 Dé du destin</h2>
          <p class="text-secondary">Décrivez une action incertaine. Le résultat est publié dans ce sujet et ne peut plus être modifié. Il guide la scène sans décider des actions ou blessures d'un autre personnage.</p>
          <div v-if="auth.isAuthenticated" class="form-group">
            <label for="dice-intention">Action tentée</label>
            <input id="dice-intention" v-model.trim="diceIntention" class="form-input" maxlength="280" placeholder="Ex. : Je cherche un indice près du Nemeton" />
            <button type="button" class="btn btn-primary" style="margin-top:.75rem" :disabled="rollingDice || !diceIntention" @click="rollDice">{{ rollingDice ? 'Lancer en cours…' : 'Lancer le dé à six faces' }}</button>
          </div>
          <p v-else><router-link to="/login">Connectez-vous</router-link> pour lancer le dé.</p>
          <p v-if="diceError" role="alert">{{ diceError }}</p>
        </section>

        <section v-if="isScenario" class="scenario-links-board card">
          <div class="scenario-links-heading">
            <span aria-hidden="true">🔗</span>
            <div>
              <p>LES CONNEXIONS</p>
              <h2>Liens du personnage</h2>
            </div>
          </div>

          <div v-if="scenarioLinkCards.length" class="scenario-link-grid">
            <article v-for="(link, index) in scenarioLinkCards" :key="`${link.gif}-${index}`" class="scenario-link-card">
              <img v-if="link.gif" :src="link.gif" :alt="link.title || 'Lien du personnage'" />
              <div v-else class="scenario-link-placeholder">✦</div>
              <div class="scenario-link-overlay" tabindex="0" role="region" :aria-label="link.title || 'Lien important'">
                <strong>{{ link.title || 'Lien important' }}</strong>
                <p>{{ link.text || 'Description à compléter.' }}</p>
              </div>
            </article>
          </div>
          <p v-else class="scenario-links-empty">Les liens de ce personnage seront bientôt renseignés.</p>

          <div v-if="isAdminOrFondatrice" class="scenario-link-editor">
            <div v-for="(link, index) in scenarioLinkCards" :key="`edit-${index}`" class="scenario-link-edit-row">
              <input v-model="link.gif" type="text" placeholder="Adresse de l’image ou du GIF" :aria-label="`Image du lien ${index + 1}`" />
              <label class="btn btn-ghost btn-sm">Choisir une image ou un GIF
                <input type="file" accept="image/png,image/jpeg,image/gif,image/webp" hidden :disabled="uploadingScenarioImage" @change="uploadScenarioLinkImage($event, index)" />
              </label>
              <input v-model="link.title" type="text" placeholder="Nom du lien" />
              <textarea v-model="link.text" rows="2" placeholder="Texte qui apparaît au survol" />
              <button type="button" class="scenario-link-remove" @click="removeScenarioLink(index)">Retirer</button>
            </div>
            <div class="scenario-link-editor-actions">
              <button type="button" class="btn btn-ghost" @click="addScenarioLink">+ Ajouter un lien</button>
              <button class="btn btn-primary" :disabled="savingScenarioLinks" @click="saveScenarioLinks">
                {{ savingScenarioLinks ? 'Enregistrement…' : 'Enregistrer les liens' }}
              </button>
            </div>
            <p v-if="scenarioLinksError" role="alert">{{ scenarioLinksError }}</p>
            <p v-if="scenarioLinksSaved" role="status">Images et liens enregistrés.</p>
          </div>
        </section>

        <PaginationBar
          :page="forum.pagination.page"
          :count="forum.pagination.count"
          @change="loadPage"
        />

        <!-- Post Editor -->
        <div v-if="editingPost && (!isScenario || editingPost.id !== forum.currentTopic?.first_post_id)" ref="postEditorRef" class="mt-2">
          <p v-if="editError" role="alert">{{ editError }}</p>
          <PostEditor
            :edit-post="editingPost"
            :loading="posting"
            @submit="handleEditSubmit"
            @cancel="editingPost = null"
          />
        </div>

        <div v-else-if="canReply" class="mt-2">
          <p v-if="postError" role="alert" class="text-sm">{{ postError }}</p>
          <PostEditor :loading="posting" @submit="handleNewPost" />
        </div>

        <div
          v-else-if="forum.currentTopic?.is_locked"
          class="card text-center text-secondary mt-2"
          style="padding: 1.5rem"
        >
          🔒 Ce sujet est verrouillé. Vous ne pouvez plus y répondre.
        </div>

        <div
          v-else-if="!auth.isAuthenticated"
          class="card text-center text-secondary mt-2"
          style="padding: 1.5rem"
        >
          <router-link to="/login">Connectez-vous</router-link> pour répondre.
        </div>
      </template>
    </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useForumStore } from '../stores/forum'
import { useAuthStore } from '../stores/auth'
import api from '../composables/useApi'
import PostCard from '../components/PostCard.vue'
import PostEditor from '../components/PostEditor.vue'
import { useRoute } from 'vue-router'
import PaginationBar from '../components/PaginationBar.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'

const props = defineProps({
  slug: { type: String, required: true },
})

const forum = useForumStore()
const auth = useAuthStore()
const diceIntention = ref('')
const diceError = ref('')
const rollingDice = ref(false)
const drawingLottery = ref(false)
const lotteryResult = ref(null)
const lotteryError = ref('')
const lotteryStatus = ref(null)
const isAnimationTopic = computed(() => forum.currentTopic?.category_name === 'Contextes et animations')
const showDiceRoller = computed(() => isAnimationTopic.value
  && props.slug !== 'loterie-des-arcana-flouz'
  && forum.currentTopic?.slug !== 'loterie-des-arcana-flouz'
  && !forum.currentTopic?.is_locked)

async function drawLottery() {
  if (drawingLottery.value) return
  drawingLottery.value = true
  lotteryError.value = ''
  lotteryResult.value = null
  try {
    const { data } = await api.post('/lottery/draw/')
    lotteryResult.value = data
    await auth.fetchProfile()
    await fetchLotteryStatus()
  } catch (e) {
    lotteryError.value = e.response?.data?.detail || 'Le tirage a échoué.'
  } finally {
    drawingLottery.value = false
  }
}

async function fetchLotteryStatus() {
  if (props.slug !== 'loterie-des-arcana-flouz' || !auth.isAuthenticated) return
  try {
    const { data } = await api.get('/lottery/draw/')
    lotteryStatus.value = data
  } catch {
    lotteryStatus.value = null
    lotteryError.value = 'Impossible de vérifier la disponibilité du tirage.'
  }
}

async function rollDice() {
  if (!diceIntention.value || rollingDice.value) return
  diceError.value = ''
  rollingDice.value = true
  try {
    await api.post(`/topics/${props.slug}/roll/`, { intention: diceIntention.value })
    diceIntention.value = ''
    const lastPage = Math.ceil((forum.pagination.count + 1) / 20)
    await forum.fetchPosts(props.slug, lastPage)
  } catch (e) {
    diceError.value = e.response?.data?.detail || e.response?.data?.intention?.[0] || 'Le lancer a échoué.'
  } finally {
    rollingDice.value = false
  }
}
const editingPost = ref(null)
const posting = ref(false)
const postError = ref('')
const editError = ref('')
const scenarioEditorRef = ref(null)
const postEditorRef = ref(null)
const route = useRoute()
const editingTitle = ref(false)
const titleDraft = ref('')
const titleInput = ref(null)
const savingTitle = ref(false)
const titleError = ref('')
const titleSaved = ref(false)
const canEditTitle = computed(() => Boolean(auth.user && forum.currentTopic && (
  (!isScenario.value || ['admin', 'fondatrice'].includes(auth.user.role)) &&
  (!forum.currentTopic.is_locked || ['admin', 'fondatrice'].includes(auth.user.role)) &&
  (auth.user.id === forum.currentTopic.author?.id || ['admin', 'fondatrice', 'moderator'].includes(auth.user.role))
)))

async function startTitleEdit() {
  titleDraft.value = forum.currentTopic.title
  titleError.value = ''
  titleSaved.value = false
  editingTitle.value = true
  await nextTick()
  titleInput.value?.focus()
}

function cancelTitleEdit() {
  if (savingTitle.value) return
  editingTitle.value = false
  titleError.value = ''
}

watch(() => props.slug, () => {
  editingTitle.value = false
  titleError.value = ''
  titleSaved.value = false
})

async function saveTitle() {
  const title = titleDraft.value.trim()
  if (!title || savingTitle.value || !canEditTitle.value) return
  const slug = forum.currentTopic.slug
  savingTitle.value = true
  titleError.value = ''
  try {
    const { data } = await api.patch(`/topics/${slug}/`, { title })
    if (forum.currentTopic?.slug === slug) {
      forum.currentTopic.title = data.title
      editingTitle.value = false
      titleSaved.value = true
    }
  } catch (error) {
    if (props.slug === slug) titleError.value = error.response?.data?.title?.[0] || error.response?.data?.detail || 'Impossible de modifier le titre. Réessaie.'
  } finally {
    savingTitle.value = false
  }
}

const HTML_EDITABLE_SLUGS = ['reglement-officiel-du-forum', 'encyclopedie-des-creatures-et-races', 'reglement-et-reservations-avatars', 'reglement-et-reservations-formes-demoniaques', 'agence-immobiliere-demande-de-logement']

const isFicheModele = computed(() => props.slug === 'modele-de-fiche-de-presentation')
const isRecapModel = computed(() => props.slug === 'modele-fiche-personnage')
const recapModelCopied = ref(false)
const recapCopyError = ref('')

async function copyRecapModel() {
  recapCopyError.value = ''
  try {
    await navigator.clipboard.writeText(forum.posts[0].content)
    recapModelCopied.value = true
  } catch {
    recapCopyError.value = 'Copie impossible dans ce navigateur.'
  }
}

const isPartnerRequest = computed(() => props.slug === 'demande-de-partenaire-de-rp')
const isPartnershipGuide = computed(() => props.slug === 'proposer-un-partenariat')
const isPendingPartnership = computed(() => forum.currentTopic?.category_name === 'Demande de partenariats' && !isPartnershipGuide.value)
const approvingPartnership = ref(false)
const partnershipApprovalError = ref('')
const partnershipModelCopied = ref(false)
const partnershipModelError = ref('')
const PARTNERSHIP_MODEL = `Nom du forum :
Adresse du forum :
Univers et concept :
Date d’ouverture :
Type de partenariat souhaité : échange de fiches, affichage de boutons ou les deux
Lien vers notre fiche ou notre bouton sur votre forum :
Votre fiche de partenariat :
Votre bouton :
Un mot pour présenter votre communauté :`

async function copyPartnershipModel() {
  partnershipModelError.value = ''
  try {
    await navigator.clipboard.writeText(PARTNERSHIP_MODEL)
    partnershipModelCopied.value = true
  } catch {
    partnershipModelError.value = 'Copie impossible dans ce navigateur.'
  }
}

async function approvePartnership() {
  approvingPartnership.value = true
  partnershipApprovalError.value = ''
  try {
    await api.post(`/partnership-requests/${props.slug}/approve/`)
    await forum.fetchTopic(props.slug)
  } catch (error) {
    partnershipApprovalError.value = error.response?.data?.detail || 'Impossible de valider ce partenariat.'
  } finally {
    approvingPartnership.value = false
  }
}
const partnerTemplateCopied = ref(false)
const partnerCopyError = ref('')
const PARTNER_TEMPLATE = `Statut : Ouvert
Mon personnage : [Nom et lien vers sa fiche, si vous le souhaitez]
Ville et lieu : [San Francisco, Beacon Hills, Mystic Falls, La Nouvelle-Orléans ou lieu à définir]
Idée de départ : [La situation qui lance la scène et ce que vous aimeriez explorer]
Partenaire(s) recherché(s) : [Libre à tous, lien particulier, faction, nombre de joueurs…]
Ambiance : [Enquête, action, quotidien, tension, romance… selon vos envies]
Rythme de réponse : [Votre disponibilité approximative]
Pour me contacter : [Réponse dans ce sujet ou message privé]`

async function copyPartnerTemplate() {
  partnerCopyError.value = ''
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(PARTNER_TEMPLATE)
    } else {
      const area = document.createElement('textarea')
      area.value = PARTNER_TEMPLATE
      area.style.position = 'fixed'
      area.style.opacity = '0'
      document.body.appendChild(area)
      area.select()
      const copied = document.execCommand('copy')
      area.remove()
      if (!copied) throw new Error('copy failed')
    }
    partnerTemplateCopied.value = true
  } catch {
    partnerCopyError.value = 'Copie impossible dans ce navigateur. Sélectionnez le modèle dans le message ci-dessous.'
  }
}

const isHtmlEditableTopic = computed(() => HTML_EDITABLE_SLUGS.includes(props.slug))
const isAdminOrFondatrice = computed(() =>
  auth.user?.role === 'admin' || auth.user?.role === 'fondatrice'
)
const isScenario = computed(() => forum.currentTopic?.category_name === 'Scénarios à prendre')
const scenarioStatus = ref('free')
const savingScenarioStatus = ref(false)
const scenarioLinkCards = ref([])
const savingScenarioLinks = ref(false)
const uploadingScenarioImage = ref(false)
const scenarioLinksError = ref('')
const scenarioLinksSaved = ref(false)
const scenarioStatusLabels = { free: '✦ Libre', reserved: '⏳ Réservé', played: '✓ Joué' }
watch(() => forum.currentTopic?.scenario_status, (status) => {
  scenarioStatus.value = status || 'free'
}, { immediate: true })

watch(() => forum.currentTopic?.scenario_link_cards, (links) => {
  scenarioLinkCards.value = Array.isArray(links)
    ? links.map((link) => ({ gif: link.gif || '', title: link.title || '', text: link.text || '' }))
    : []
}, { immediate: true })

async function saveScenarioStatus() {
  if (!forum.currentTopic?.slug) return
  savingScenarioStatus.value = true
  try {
    const { data } = await api.patch(`/topics/${forum.currentTopic.slug}/`, {
      scenario_status: scenarioStatus.value,
    })
    forum.currentTopic = data
  } finally {
    savingScenarioStatus.value = false
  }
}

async function saveScenarioLinks() {
  if (!forum.currentTopic?.slug) return
  scenarioLinksError.value = ''
  scenarioLinksSaved.value = false
  savingScenarioLinks.value = true
  try {
    const { data } = await api.patch(`/topics/${forum.currentTopic.slug}/`, {
      scenario_link_cards: scenarioLinkCards.value,
    })
    forum.currentTopic = data
    scenarioLinksSaved.value = true
  } catch (error) {
    scenarioLinksError.value = error?.response?.data?.detail || 'Impossible d’enregistrer les images et les liens.'
  } finally {
    savingScenarioLinks.value = false
  }
}

async function uploadScenarioLinkImage(event, index) {
  const file = event.target.files?.[0]
  if (!file) return
  scenarioLinksError.value = ''
  scenarioLinksSaved.value = false
  if (file.size > 5 * 1024 * 1024) {
    scenarioLinksError.value = 'L’image doit peser moins de 5 Mo.'
    event.target.value = ''
    return
  }
  uploadingScenarioImage.value = true
  try {
    const form = new FormData()
    form.append('image', file)
    const { data } = await api.post('/posts/images/', form)
    scenarioLinkCards.value[index].gif = data.url
  } catch (error) {
    scenarioLinksError.value = error?.response?.data?.detail || 'Impossible d’ajouter cette image.'
  } finally {
    uploadingScenarioImage.value = false
    event.target.value = ''
  }
}

function addScenarioLink() {
  scenarioLinkCards.value.push({ gif: '', title: '', text: '' })
}

function removeScenarioLink(index) {
  scenarioLinkCards.value.splice(index, 1)
}

// Éditeur HTML inline pour le règlement
const reglementEditMode = ref(false)
const reglementEditContent = ref('')
const savingReglement = ref(false)

function startReglementEdit() {
  reglementEditContent.value = forum.posts[0]?.content || ''
  reglementEditMode.value = true
}

async function saveReglementEdit() {
  if (!forum.posts[0]?.id) return
  savingReglement.value = true
  try {
    await api.patch(`/posts/${forum.posts[0].id}/`, { content: reglementEditContent.value })
    await forum.fetchPosts(props.slug)
    reglementEditMode.value = false
  } finally {
    savingReglement.value = false
  }
}
const topicCopied = ref(false)
const codeAreaRef = ref(null)

async function selectAndCopy() {
  const content = forum.posts[0]?.content
  if (!content) return
  codeAreaRef.value?.select()
  await navigator.clipboard.writeText(content)
  topicCopied.value = true
  setTimeout(() => { topicCopied.value = false }, 2000)
}

const canReply = computed(() => {
  return auth.isAuthenticated && !forum.currentTopic?.is_locked
})

async function load() {
  await forum.fetchTopic(props.slug)
  const requestedPage = Number(route.query.page)
  await forum.fetchPosts(props.slug, Number.isInteger(requestedPage) && requestedPage > 0 ? requestedPage : 1)
  await fetchLotteryStatus()
}

onMounted(load)
watch(() => props.slug, load)

function loadPage(page) {
  forum.fetchPosts(props.slug, page)
}

async function handleNewPost(content, onPublished) {
  postError.value = ''
  let published = false
  posting.value = true
  try {
    await forum.createPost(props.slug, content)
    published = true
    onPublished?.()
    // Go to last page to see the new post
    const lastPage = Math.ceil((forum.pagination.count + 1) / 20)
    await forum.fetchPosts(props.slug, lastPage)
    // Rafraîchir le profil pour mettre à jour le compte bancaire si RP crédité
    await auth.fetchProfile()
  } catch (error) {
    postError.value = published ? 'Message publié. Rechargez la page pour actualiser l’affichage.' : (error?.response?.data?.detail || 'Envoi impossible. Votre texte est conservé ; vous pouvez réessayer.')
  } finally {
    posting.value = false
  }
}

async function startEdit(post) {
  editError.value = ''
  editingPost.value = post
  await nextTick()
  ;(isScenario.value && post.id === forum.currentTopic?.first_post_id ? scenarioEditorRef.value : postEditorRef.value)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

async function handleEditSubmit(content, onPublished) {
  editError.value = ''
  posting.value = true
  try {
    await forum.updatePost(editingPost.value.id, content)
    onPublished?.()
    editingPost.value = null
  } catch (error) {
    editError.value = error?.response?.data?.detail || 'Impossible d’enregistrer la fiche. Votre contenu reste dans l’éditeur.'
  } finally {
    posting.value = false
  }
}

async function handleDelete(postId) {
  if (!confirm('Supprimer ce message ?')) return
  await forum.deletePost(postId)
}

async function handleReaction(postId, reactionType) {
  if (!auth.isAuthenticated) return
  await forum.toggleReaction(postId, reactionType)
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}
</script>

<style scoped>
.partner-copy-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem 1.25rem;
}

.partner-copy-bar strong { color: var(--text-primary); }
.partner-copy-bar p { margin: .3rem 0 0; color: var(--text-secondary); font-size: .85rem; }
.partner-copy-bar [role="alert"] { width: 100%; color: var(--text-secondary); font-size: .8rem; }

.topic-title-editor { display: grid; gap: .65rem; max-width: 650px; margin: .75rem 0; }
.topic-title-editor input { width: 100%; box-sizing: border-box; padding: .7rem; border: 1px solid var(--border); border-radius: 6px; background: var(--bg-secondary); color: var(--text-primary); font: inherit; }
.topic-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

/* ── Barre d'édition admin ── */
.admin-edit-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.scenario-admin-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding: 0.8rem 1rem;
}

.scenario-admin-bar label {
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 700;
}

.scenario-admin-bar select {
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--bg-input, var(--bg-secondary));
  color: var(--text-primary);
  padding: 0.4rem 0.55rem;
}

.scenario-admin-help {
  color: var(--text-muted);
  font-size: 0.75rem;
}

.scenario-status {
  border-radius: 999px;
  padding: 0.2rem 0.5rem;
  font-size: 0.72rem;
  font-weight: 700;
}

.scenario-status--free { background: rgba(74, 222, 128, 0.16); color: #65d99b; }
.scenario-status--reserved { background: rgba(245, 215, 110, 0.16); color: #f5d76e; }
.scenario-status--played { background: rgba(148, 163, 184, 0.16); color: #b7c0cf; }


.scenario-links-board {
  margin: 1.25rem 0;
  padding: 1.15rem;
  border-color: rgba(139, 92, 246, 0.28);
}

.scenario-links-heading { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.9rem; }
.scenario-links-heading > span { font-size: 1.3rem; }
.scenario-links-heading p { margin: 0 0 0.12rem; color: var(--accent); font-size: 0.62rem; font-weight: 800; letter-spacing: 0.15em; }
.scenario-links-heading h2 { margin: 0; color: var(--text-primary); font-family: var(--font-heading); font-size: 1.15rem; }
.scenario-links-empty { margin: 0 0 1rem; color: var(--text-muted); font-size: 0.88rem; font-style: italic; }
.scenario-link-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(155px, 1fr)); gap: 0.75rem; }
.scenario-link-card { position: relative; min-height: 150px; overflow: hidden; border: 1px solid rgba(139, 92, 246, 0.25); border-radius: 9px; background: #10172c; }
.scenario-link-card img { width: 100%; height: 150px; display: block; object-fit: cover; transition: transform 0.35s ease; }
.scenario-link-card:hover img { transform: scale(1.08); }
.scenario-link-placeholder { height: 150px; display: grid; place-items: center; color: var(--accent); font-size: 2rem; background: radial-gradient(circle, rgba(139, 92, 246, 0.22), transparent 70%); }
.scenario-link-overlay { position: absolute; inset: 0; display: flex; flex-direction: column; gap: 0.3rem; padding: 0.75rem; overflow-y: auto; overflow-x: hidden; scrollbar-width: thin; scrollbar-color: #a78bfa #10172c; color: #fff; background: linear-gradient(rgba(5, 8, 20, 0.65), rgba(5, 8, 20, 0.94)); opacity: 0; transform: translateY(8px); transition: opacity 0.25s ease, transform 0.25s ease; }
.scenario-link-card:hover .scenario-link-overlay, .scenario-link-card:focus-within .scenario-link-overlay { opacity: 1; transform: translateY(0); }
.scenario-link-overlay strong { flex-shrink: 0; margin-top: auto; overflow-wrap: anywhere; font-size: 0.85rem; }
.scenario-link-overlay p { flex-shrink: 0; margin: 0; overflow-wrap: anywhere; white-space: pre-wrap; font-size: 0.73rem; line-height: 1.35; }
.scenario-link-overlay:focus-visible { outline: 2px solid #a78bfa; outline-offset: -2px; }
@media (hover: none) {
  .scenario-link-overlay { opacity: 1; transform: none; }
}
.scenario-link-editor { margin-top: 1rem; border-top: 1px solid var(--border); padding-top: 0.9rem; }
.scenario-link-edit-row { display: grid; grid-template-columns: 1.2fr 0.8fr 1.4fr auto; gap: 0.45rem; align-items: start; margin-bottom: 0.55rem; }
.scenario-link-edit-row input, .scenario-link-edit-row textarea { box-sizing: border-box; width: 100%; border: 1px solid var(--border); border-radius: 6px; background: var(--bg-input, var(--bg-secondary)); color: var(--text-primary); padding: 0.5rem; font: inherit; font-size: 0.78rem; }
.scenario-link-edit-row textarea { resize: vertical; }
.scenario-link-remove { border: 0; border-radius: 6px; background: rgba(248, 113, 113, 0.15); color: #fca5a5; cursor: pointer; padding: 0.48rem 0.6rem; }
.scenario-link-editor-actions { display: flex; justify-content: space-between; gap: 0.6rem; margin-top: 0.65rem; }

@media (max-width: 700px) {
  .scenario-admin-bar { align-items: flex-start; flex-direction: column; gap: 0.45rem; }
  .scenario-link-edit-row { grid-template-columns: 1fr; }
}

.btn-admin-edit,
.btn-admin-cancel {
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  padding: 0.35rem 0.9rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-admin-edit {
  background: rgba(234, 179, 8, 0.12);
  color: #eab308;
  border: 1px solid rgba(234, 179, 8, 0.35);
}
.btn-admin-edit:hover { background: rgba(234, 179, 8, 0.22); }

.btn-admin-cancel {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
}
.btn-admin-cancel:hover { background: rgba(239, 68, 68, 0.2); }

/* ── Fiche modèle ── */

/* En-tête auteur (pleine largeur) */
.fiche-post-header {
  margin-bottom: 1.25rem;
}

.fiche-post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.fiche-post-author {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.fiche-author-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
  overflow: hidden;
}

.fiche-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.fiche-author-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.fiche-author-name {
  font-weight: 600;
  font-size: 0.9375rem;
}

.fiche-author-badge {
  font-size: 0.7rem;
  color: var(--accent, #a78bfa);
  font-style: italic;
}

.fiche-lock-tag {
  font-size: 0.75rem;
  color: var(--text-secondary);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 0.2rem 0.65rem;
}

/* Layout deux colonnes */
.fiche-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 1.5rem;
  align-items: start;
}

/* Label de colonne */
.fiche-col-label {
  font-size: 0.68rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-secondary);
  margin-bottom: 0.75rem;
}

/* Colonne gauche : aperçu */
.fiche-preview-col {
  min-width: 0;
}

.fiche-post-body {
  overflow-x: auto;
}

/* Colonne droite : code */
.fiche-code-col {
  position: sticky;
  top: 1rem;
}

.fiche-code-card {
  padding: 0 !important;
  overflow: hidden;
  margin-bottom: 0.75rem;
}

.fiche-code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.55rem 0.9rem;
  background: rgba(109, 40, 217, 0.1);
  border-bottom: 1px solid var(--border);
}

.fiche-code-label {
  font-weight: 600;
  font-size: 0.88rem;
  color: var(--text-primary, #e2d9f3);
}

.fiche-select-btn {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--accent, #a78bfa);
  background: transparent;
  border: 1px solid rgba(167, 139, 250, 0.35);
  border-radius: 4px;
  padding: 0.2rem 0.7rem;
  cursor: pointer;
  transition: background 0.15s;
}

.fiche-select-btn:hover {
  background: rgba(167, 139, 250, 0.12);
}

.fiche-code-area {
  display: block;
  width: 100%;
  height: 420px;
  padding: 0.85rem;
  background: rgba(0, 0, 0, 0.25);
  border: none;
  color: var(--text-secondary);
  font-family: 'Courier New', monospace;
  font-size: 0.72rem;
  line-height: 1.55;
  resize: vertical;
  box-sizing: border-box;
  cursor: text;
  outline: none;
}

.fiche-notice {
  font-size: 0.78rem;
  color: var(--text-secondary);
  line-height: 1.6;
  padding: 0.75rem;
  border: 1px dashed var(--border);
  border-radius: 8px;
}

.fiche-notice a {
  color: var(--accent, #a78bfa);
}

/* Responsive : empiler sur mobile */
@media (max-width: 900px) {
  .fiche-layout {
    grid-template-columns: 1fr;
  }
  .fiche-code-col {
    position: static;
  }
}

/* ── Éditeur HTML règlement ── */
.reglement-html-editor {
  margin-bottom: 1.5rem;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.reglement-editor-hint {
  font-size: 0.8rem;
  color: var(--text-muted, #8b8ba7);
  font-style: italic;
  margin: 0;
}

.reglement-textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 0.85rem;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--glass-border, rgba(255,255,255,0.08));
  border-radius: 8px;
  color: var(--text, #e2d9f3);
  font-family: 'Courier New', monospace;
  font-size: 0.78rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s;
}
.reglement-textarea:focus {
  border-color: var(--accent, #a78bfa);
}

.reglement-editor-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.reglement-preview-label {
  font-size: 0.68rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-secondary, #8b8ba7);
}

.reglement-preview {
  padding: 1rem 1.25rem;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--glass-border, rgba(255,255,255,0.06));
  border-radius: 8px;
  line-height: 1.75;
  overflow-x: auto;
  min-height: 80px;
}
</style>
