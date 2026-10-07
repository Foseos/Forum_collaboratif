# Mise en ligne de Nexus Arcana

Le forum fonctionne aujourd'hui sur l'ordinateur local. La configuration publique est dans `compose.prod.yml` et ne remplace pas `docker-compose.yml` utilisé en local. Le domaine `nexus-arcana.fr` a été acheté ; le forum n'est pas encore publié à cette adresse.

## Ce qu'il faut obtenir

1. **Domaine acquis :** `nexus-arcana.fr`. Conserver l'accès au compte OVHcloud et surveiller son renouvellement.
2. **Hébergement à confirmer :** le compte Oracle Cloud est encore en cours de provisionnement. Attendre le courriel confirmant qu'il est entièrement prêt, puis vérifier qu'une instance compatible Always Free peut réellement être créée avant toute installation. Si ce n'est pas possible, choisir un autre hébergement adapté à Django et PostgreSQL.
3. **Envoi d'e-mails à configurer :** relier le domaine à un service d'envoi (par exemple Resend). Les inscriptions et la récupération des mots de passe dépendent de son bon fonctionnement.

Le compte chez l'hébergeur, le domaine et le service e-mail doivent appartenir à la fondatrice. Aucun mot de passe ou clé d'API ne doit être collé dans un message ou ajouté à GitHub.

## Préparer le serveur

1. Une fois l'hébergement disponible, installer Docker et le module Docker Compose sur le serveur. Mettre en place les mises à jour de sécurité et n'ouvrir que les ports nécessaires : SSH, 80 et 443.
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

## Sauvegardes automatiques après la mise en ligne

Les scripts `scripts/backup_forum.sh` et `scripts/verify_backup.sh` sont prêts. Leur programmation ne peut être activée qu'une fois le VPS et un espace de sauvegarde **distinct du VPS** disponibles. Le premier script exporte la base et les images, puis les envoie dans un dépôt chiffré restic. Les fichiers temporaires sont effacés à la fin. Le second récupère une copie dans un dossier temporaire et vérifie que les deux archives sont lisibles, sans toucher aux données du forum.

1. Prévoir un stockage externe compatible restic (par exemple un compte SFTP séparé). Installer `restic` et `flock` sur le VPS. Le stockage choisi peut être payant : vérifier son tarif avant de le créer.
2. Copier `.env.backup.example` vers `.env.backup` sur le VPS. Renseigner l'adresse du stockage externe et le chemin d'un fichier contenant un mot de passe de chiffrement long et unique. Garder ce mot de passe en lieu sûr **hors du VPS** : sans lui, aucune restauration n'est possible. Protéger `.env.backup` et le fichier du mot de passe avec `chmod 600`.
3. Charger les réglages avec `set -a; source .env.backup; set +a`, puis initialiser le dépôt une seule fois avec `restic init`. Lancer `bash scripts/backup_forum.sh` et `bash scripts/verify_backup.sh`. Contrôler le résultat avant toute programmation. Ne jamais mettre les sauvegardes ni les secrets dans GitHub.
4. Programmer l'exécution quotidienne sur le VPS, par exemple à 03 h avec la crontab du compte qui peut accéder à Docker : `0 3 * * * cd /chemin/vers/Forum_collaboratif && /usr/bin/bash scripts/backup_forum.sh >> /chemin/vers/backup.log 2>&1`. Remplacer les deux chemins et vérifier régulièrement ce journal et `restic snapshots` ; une tâche planifiée peut échouer silencieusement si personne ne surveille son résultat.
5. Tester périodiquement une **restauration complète sur un environnement séparé**. `verify_backup.sh` vérifie la lisibilité des archives, mais ne remplace pas cet essai de restauration de l'application et des images. Faire aussi une sauvegarde manuelle avant chaque mise à jour.

Le domaine et le VPS se renouvellent ; surveiller leurs dates de renouvellement et l'espace disque disponible pour les exports temporaires.
