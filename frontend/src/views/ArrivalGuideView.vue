<template>
  <main class="arrival-page container">
    <router-link to="/categories/bienvenue-san-francisco" class="arrival-back">← Bienvenue à Nexus Arcana</router-link>
    <header class="arrival-hero">
      <span class="arrival-eyebrow">✦ Tes premiers pas</span>
      <h1>Bienvenue dans le Nexus</h1>
      <p>Tu découvres le forum ? Voici un chemin simple pour comprendre l’univers, créer ton personnage et trouver ton premier RP. Avance à ton rythme.</p>
    </header>

    <div class="arrival-steps">
      <section v-for="(step, index) in steps" :key="step.title" class="arrival-step card">
        <span class="arrival-number">{{ String(index + 1).padStart(2, '0') }}</span>
        <div class="arrival-content">
          <p class="arrival-phase">{{ step.phase }}</p>
          <h2>{{ step.title }}</h2>
          <p>{{ step.description }}</p>
          <div class="arrival-links">
            <router-link v-for="link in step.links" :key="link.to" :to="link.to" class="btn btn-secondary btn-sm">{{ link.label }} →</router-link>
          </div>
        </div>
      </section>
    </div>

    <aside class="arrival-help card">
      <h2>Besoin d’un coup de main ?</h2>
      <p>Tu peux poser une question ou demander un parrainage. L’équipe du staff reste disponible pour t’aider à trouver ta place.</p>
      <div class="arrival-links">
        <router-link to="/categories/une-question" class="btn btn-secondary btn-sm">Poser une question</router-link>
        <router-link to="/categories/parrainage" class="btn btn-secondary btn-sm">Découvrir le parrainage</router-link>
      </div>
    </aside>
  </main>
</template>

<script setup>
const steps = [
  {
    phase: 'Découvrir',
    title: 'Comprendre le monde et ses règles',
    description: 'Commence par le contexte de la saison 1 et le règlement. Le grimoire t’aidera ensuite à situer ton personnage parmi les espèces et les factions.',
    links: [
      { label: 'Contexte et animations', to: '/categories/contextes-et-animations' },
      { label: 'Règlement', to: '/categories/reglement-du-forum' },
      { label: 'Créatures et races', to: '/categories/creatures-et-races' },
    ],
  },
  {
    phase: 'Imaginer',
    title: 'Choisir ton personnage',
    description: 'Tu peux inventer un personnage ou adopter un scénario. Vérifie l’avatar envisagé avant de préparer ta présentation.',
    links: [
      { label: 'Scénarios à prendre', to: '/categories/scenarios-a-prendre' },
      { label: 'Bottin des avatars', to: '/categories/bottin-des-avatars' },
      { label: 'Groupes et factions', to: '/groupes' },
    ],
  },
  {
    phase: 'Se présenter',
    title: 'Créer ta fiche',
    description: 'Une fois inscrit, utilise le modèle de présentation pour raconter ton personnage. Ta fiche sera visible par les autres membres pendant son examen, puis archivée après validation par l’administration.',
    links: [
      { label: 'Modèle de présentation', to: '/categories/modele-fiche-de-presentation' },
      { label: 'Créer ma fiche', to: '/fiches/nouvelle' },
    ],
  },
  {
    phase: 'Après validation',
    title: 'Installer ton personnage dans le jeu',
    description: 'Publie son carnet récapitulatif, choisis où il habite et propose un RP. Ces étapes peuvent se faire dans l’ordre qui te convient.',
    links: [
      { label: 'Carnets des personnages', to: '/categories/fiche-personnage' },
      { label: 'Agence immobilière', to: '/topics/agence-immobiliere-demande-de-logement' },
      { label: 'Recherche de RP', to: '/topics/demande-de-partenaire-de-rp' },
    ],
  },
]
</script>

<style scoped>
.arrival-page { padding-top: 2rem; padding-bottom: 5rem; max-width: 1040px; }
.arrival-back { color: var(--color-text-secondary, #b9aacb); font-size: .9rem; }
.arrival-hero { margin: 1.4rem 0 2rem; padding: 2.5rem; border: 1px solid #b99b55; border-radius: 16px; background: linear-gradient(125deg, #211b38, #111627 70%); box-shadow: 0 12px 40px #0003; }
.arrival-eyebrow, .arrival-phase { color: #d8bc70; font-size: .8rem; text-transform: uppercase; letter-spacing: .16em; font-weight: 700; }
.arrival-hero h1 { margin: .65rem 0; color: #f1d997; font-family: Georgia, serif; font-size: clamp(2rem, 5vw, 3.5rem); }
.arrival-hero p { max-width: 680px; line-height: 1.7; margin-bottom: 0; }
.arrival-steps { display: grid; gap: 1rem; }
.arrival-step { display: flex; gap: 1.5rem; padding: 1.6rem; border: 1px solid #716088; background: #17152a; }
.arrival-number { color: #d8bc70; font: 2rem Georgia, serif; min-width: 2.5rem; }
.arrival-content h2, .arrival-help h2 { margin: .3rem 0 .6rem; color: #f1d997; font-family: Georgia, serif; }
.arrival-content > p:not(.arrival-phase), .arrival-help p { line-height: 1.65; color: #ddd5e8; }
.arrival-phase { margin: 0; }
.arrival-links { display: flex; flex-wrap: wrap; gap: .6rem; margin-top: 1.2rem; }
.arrival-help { margin-top: 1.5rem; padding: 1.6rem; border: 1px solid #9f8557; background: #211c30; }
@media (max-width: 600px) { .arrival-hero { padding: 1.5rem; } .arrival-step { gap: .8rem; padding: 1.2rem; } .arrival-number { font-size: 1.45rem; min-width: 1.8rem; } }
</style>
