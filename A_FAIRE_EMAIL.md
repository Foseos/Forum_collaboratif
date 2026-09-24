# À reprendre quand le forum sera terminé

L'envoi d'e-mails du forum n'est pas encore opérationnel : le test SMTP du 23 septembre 2026 a été refusé avec « Authentication credentials invalid ». Le forum affiche une erreur claire lors d'une inscription ou d'une demande de lien et ne crée pas de compte bloqué.

## Étapes à faire plus tard

1. Choisir un expéditeur : commencer éventuellement avec une adresse Gmail dédiée au forum, ou acheter un nom de domaine pour une adresse comme `contact@nom-du-forum.fr`.
2. Si Gmail est choisi : activer la validation en deux étapes, créer un mot de passe d'application et configurer l'envoi SMTP du forum. Ne jamais mettre le mot de passe Gmail habituel dans le projet.
3. Si un domaine est choisi : l'ajouter à Resend, recopier les réglages DNS fournis, attendre la vérification du domaine, créer une nouvelle clé Resend et remplacer les réglages d'expédition dans `.env`.
4. Redémarrer le forum et envoyer un message de test à la fondatrice, puis tester une inscription et un lien « Mot de passe oublié » de bout en bout.

Ne pas copier de clé API ou de mot de passe dans ce document ni dans une conversation. Les comptes déjà existants restent accessibles pendant cette attente.

## Mise en ligne et budget estimatif

- Le forum actuel a besoin d'un hébergement capable de faire tourner le site, le serveur et sa base de données. Un simple hébergement de pages statiques ne suffit pas.
- Point de départ envisagé : un petit VPS de 4 Go de RAM. Exemple consulté le 23 septembre 2026 : OVHcloud VPS-1 affiché à partir de 4,57 € TTC/mois, soit environ 55 € par an. Vérifier le prix et les conditions au moment de l'achat : https://www.ovhcloud.com/fr/vps/
- Domaine `.fr` : exemple OVHcloud consulté le 23 septembre 2026, 5,99 € TTC la première année puis 9,35 € TTC/an. Vérifier disponibilité et prix du nom souhaité : https://www.ovhcloud.com/fr/domains/tld/fr/
- Resend : offre gratuite affichée à 3 000 e-mails/mois, avec 100/jour, sous réserve des conditions en vigueur : https://resend.com/pricing
- Budget indicatif domaine + VPS : environ 60 à 65 € par an au départ, hors options, boîte mail éventuelle et variation tarifaire. Ce n'est pas un devis.
- Lors de la mise en ligne : relier le domaine au serveur, configurer HTTPS, vérifier sauvegardes et restauration, mettre à jour `FORUM_URL`, puis tester inscription, e-mails et récupération du mot de passe de bout en bout.
- Aucun achat ni réservation n'a été effectué.
