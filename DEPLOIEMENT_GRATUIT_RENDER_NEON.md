# Option gratuite : Render + Neon

Cette option évite la pénurie de machines Oracle. Elle utilise **un seul service Web Render Free** pour Django et Vue, et **un projet Neon Free** pour PostgreSQL et les images. Le domaine reste chez OVHcloud. Les e-mails partent par l'API Resend, car Render Free bloque les ports SMTP.

## État au 7 octobre 2026

- Le projet Neon **Nexus Arcana** est créé dans la région de Francfort, sur le plan Free.
- Le bucket public `nexus-arcana-media` est créé. Les 64 images locales ont été transférées et vérifiées ; un accès public à une image a répondu HTTP 200.
- Une sauvegarde locale de PostgreSQL et des images se trouve dans `migration-backups/`, ignoré par Git. La base Neon contenait 0 table avant transfert. Après transfert, les comptes, sujets et messages correspondent à la base locale : **2 / 110 / 178**.
- Les informations de connexion Neon sont dans `.env.neon.database` et `.env.neon.storage`, ignorés par Git. Ne pas les copier dans un message.
- Le domaine Resend `nexus-arcana.fr` est vérifié. La clé d'envoi limitée à ce domaine est conservée dans `.env.resend`, ignoré par Git. L'adresse d'envoi retenue est `Nexus Arcana <noreply@nexus-arcana.fr>`.
- Le forum local continue de fonctionner. Si son contenu change avant la publication, refaire une dernière synchronisation avant de pointer le domaine vers Render.

## Ce qui est déjà prêt dans le dépôt

- `render.yaml` décrit un service Web `free`. Aucun PostgreSQL Render n'est créé : sa version gratuite expire après 30 jours.
- `Dockerfile.render` construit Vue et Django dans un seul service. Les fichiers du forum ne sont pas inclus dans l'image.
- `backend/config/settings/render.py` utilise `DATABASE_URL` pour Neon et un stockage S3 compatible pour les images. Le bucket Neon doit être **public_read** pour que les avatars et les images des messages puissent s'afficher.
- Les anciens liens `/media/...` redirigent vers les images migrées.
- La clé Resend passe par l'API HTTPS. Les secrets sont saisis uniquement dans les tableaux de bord Neon et Render, jamais dans Git ni dans une conversation.

## Limites à connaître avant d'ouvrir le forum

- Render Free met le serveur en veille après 15 minutes sans visite. Le premier visiteur peut attendre environ une minute. Le service a 512 Mo de mémoire et ne convient pas à un forum très fréquenté.
- Le système de fichiers Render est temporaire. **Ne pas créer la base SQLite ni enregistrer les images sur Render.**
- Neon Free annonce 1 Go de base PostgreSQL et 5 Go de stockage d'objets par projet en octobre 2026. Vérifier les limites affichées lors de l'inscription.
- Render peut suspendre le service lorsque les limites gratuites sont atteintes. Pour éviter une facture, ne pas ajouter de moyen de paiement à Render et garder le plan `Free`.
- Les comptes, sujets, messages et images présents localement doivent être migrés avant de diriger `nexus-arcana.fr` vers Render. GitHub ne contient pas ces données.
- Mesure locale du 6 octobre 2026 : environ **11 Mo** de base PostgreSQL et **6,8 Mo** d'images. Ces volumes sont inférieurs aux quotas Neon Free actuels, mais la taille peut croître après l'ouverture.

## Ordre de mise en ligne

1. Créer un projet **Free** dans Neon. Créer un bucket d'images `public_read` et obtenir la connexion PostgreSQL ainsi que les paramètres S3 (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ENDPOINT_URL_S3`, région, nom du bucket). Garder les secrets dans Neon.
2. Vérifier que le domaine est validé chez Resend, puis créer une clé API limitée à l'envoi. Garder cette clé dans Resend.
3. Préparer une sauvegarde cohérente de la base PostgreSQL locale et des images. Migrer cette sauvegarde vers Neon, puis vérifier les comptes, sujets, messages et images. **Ne pas basculer le domaine avant cette vérification.**
4. Mettre le code à jour dans le dépôt GitHub, puis créer un **Blueprint** Render depuis `render.yaml` en choisissant uniquement le plan **Free**. Les champs marqués `sync: false` sont demandés par Render. Dans `AWS_S3_ENDPOINT_URL`, utiliser la valeur Neon `AWS_ENDPOINT_URL_S3`. Laisser Render générer `SECRET_KEY`.
5. Vérifier l'adresse `onrender.com`, puis ajouter `nexus-arcana.fr` dans Render. Configurer les DNS chez OVHcloud selon les valeurs données par Render. Définir ensuite `FORUM_URL=https://nexus-arcana.fr` dans Render et redéployer.
6. Tester l'accueil, la connexion, les images, l'inscription et la récupération du mot de passe. Conserver une sauvegarde hors de Neon et tester sa restauration.

## Sources officielles

- [Render Free : limites, veille, fichiers temporaires et SMTP](https://render.com/docs/free)
- [Neon Free : base et stockage d'objets](https://neon.com/blog/neon-free-plan-1-gb-per-project)
- [Anymail avec l'API Resend](https://anymail.dev/en/stable/esps/resend/)
