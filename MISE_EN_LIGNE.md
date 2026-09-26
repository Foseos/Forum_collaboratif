# Mise en ligne de Nexus Arcana

Le forum fonctionne aujourd'hui sur l'ordinateur local. La configuration publique est dans `compose.prod.yml` et ne remplace pas `docker-compose.yml` utilisé en local.

## Ce qu'il faut obtenir

1. Un nom de domaine, par exemple `nexus-arcana.fr` **si ce nom est disponible**. Vérifier sa disponibilité et son prix de renouvellement avant l'achat.
2. Un VPS Linux avec au moins 4 Go de RAM pour faire tourner le site, Django et PostgreSQL. Prévoir l'accès administrateur au VPS.
3. Un service d'envoi d'e-mails lié au domaine (par exemple Resend). Les inscriptions et la récupération des mots de passe dépendent de son bon fonctionnement.

Le compte chez l'hébergeur, le domaine et le service e-mail doivent appartenir à la fondatrice. Aucun mot de passe ou clé d'API ne doit être collé dans un message ou ajouté à GitHub.

## Préparer le serveur

1. Installer Docker et le module Docker Compose sur le VPS. Mettre en place les mises à jour de sécurité et n'ouvrir que les ports nécessaires : SSH, 80 et 443.
2. Pointer l'enregistrement DNS `A` du domaine vers l'adresse IPv4 du VPS. Si un enregistrement `AAAA` existe, il doit viser l'IPv6 du même VPS ; sinon, le retirer.
3. Récupérer le dépôt privé ou public sur le VPS et copier `.env.production.example` dans `.env.production`.
4. Remplacer toutes les valeurs d'exemple dans `.env.production`. Générer `SECRET_KEY` et `DB_PASSWORD` aléatoirement. Configurer `FORUM_DOMAIN`, `FORUM_URL`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` et l'adresse d'expédition avec le domaine réellement acheté.
5. Vérifier le domaine chez le fournisseur d'e-mails et renseigner les entrées DNS qu'il demande. Placer les identifiants SMTP dans `.env.production` sur le VPS uniquement.

Le fichier `.env.production` est ignoré par Git. Le garder lisible seulement par le compte qui administre le serveur.

## Préserver les données déjà créées

La base PostgreSQL locale contient les comptes, scénarios, sujets et messages ; le volume `media_data` contient les images envoyées. **Ne pas démarrer un forum public vide en pensant que GitHub transporte ces données.**

Les anciens scripts ponctuels qui ont servi à rédiger ou corriger les scénarios ont été retirés du code actif. Ils restent consultables dans l'archive Git `archive-scenario-scripts-2026-09-26`. Cette archive ne remplace pas la sauvegarde de la base : les contenus publiés se trouvent dans PostgreSQL.

Avant la migration, arrêter temporairement les nouvelles écritures sur le forum local, créer une sauvegarde cohérente de la base et une archive du volume `media_data`, puis transférer les deux au VPS par un canal chiffré. Restaurer la base et les images sur le serveur avant l'ouverture publique. Contrôler les nombres de comptes, sujets et messages ainsi que plusieurs avatars et images. Conserver une copie de secours hors du VPS et tester une restauration.

Les sauvegardes contiennent des données personnelles : elles ne vont ni sur GitHub ni dans une conversation.

## Démarrer et vérifier

Sur le VPS, après restauration des données :

```bash
docker compose --env-file .env.production -f compose.prod.yml config --quiet
docker compose --env-file .env.production -f compose.prod.yml up -d --build
docker compose --env-file .env.production -f compose.prod.yml ps
```

Caddy obtient automatiquement le certificat HTTPS lorsque le domaine pointe vers le VPS et que les ports 80 et 443 sont accessibles. Le service PostgreSQL n'est pas exposé à Internet. Les images et les fichiers statiques sont conservés dans des volumes distincts.

Avant d'annoncer l'ouverture, vérifier depuis un navigateur extérieur : page d'accueil, scénario, image, connexion, inscription avec confirmation e-mail, réinitialisation du mot de passe, notification de réponse et message privé. Tester aussi la restauration d'une sauvegarde et vérifier que l'administration n'est accessible qu'aux comptes autorisés.

## Entretien

Sauvegarder régulièrement la base **et** les images vers un stockage indépendant du VPS. Tester périodiquement la restauration. Avant chaque mise à jour du forum, faire une nouvelle sauvegarde. Le domaine et le VPS se renouvellent ; surveiller les dates de renouvellement et l'espace disque.
