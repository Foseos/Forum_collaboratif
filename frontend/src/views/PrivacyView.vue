<template>
  <div class="page privacy-page"><div class="container privacy-wrap">
    <h1>Vos données sur Nexus Arcana</h1>
    <div class="card privacy-content">
      <p>Le forum utilise les informations nécessaires à votre compte : nom d’utilisateur, adresse e-mail, profil, messages et activité du personnage. L’adresse e-mail sert à la connexion, aux confirmations et aux notifications que vous avez choisies.</p>
      <p>Le forum ne constitue plus d’historique des adresses IP lors de l’inscription ou de la connexion. Comme pour tout site, les services qui acheminent la connexion peuvent néanmoins traiter des informations techniques nécessaires à son fonctionnement.</p>
      <p>Les photos et GIF ajoutés par adresse externe sont chargés depuis le site qui les héberge. Ce site peut alors recevoir votre adresse IP et les informations techniques de votre navigateur. Privilégiez les fichiers dont l’utilisation est autorisée.</p>
      <p>Votre profil et vos publications restent disponibles tant que le compte est actif, sous réserve des demandes de suppression et des besoins légitimes liés aux échanges déjà publiés. Les durées de conservation et les prestataires d’hébergement et d’e-mail seront précisés avant l’ouverture publique.</p>
      <p>Pour demander l’accès, la correction ou la suppression de vos données, <router-link to="/contact">contactez l’administration</router-link>. Vous pouvez aussi y signaler un contenu qui vous concerne.</p>
    </div>
  </div></div>
</template>

<style scoped>
.privacy-page { padding: 2.5rem 0; }
.privacy-wrap { max-width: 820px; }
.privacy-wrap h1 { color: var(--accent); }
.privacy-content { padding: 1.5rem; line-height: 1.75; }
.privacy-content p { margin: 0 0 1rem; }
.privacy-content p:last-child { margin-bottom: 0; }
</style>
