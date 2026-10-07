# À reprendre quand le forum sera terminé

La préparation de la mise en ligne est maintenant décrite dans [MISE_EN_LIGNE.md](MISE_EN_LIGNE.md). Ce document conserve le diagnostic de l'envoi d'e-mails local et les étapes de configuration à terminer avant l'ouverture publique.

L'envoi d'e-mails du forum n'est pas encore opérationnel : le test SMTP du 23 septembre 2026 a été refusé avec « Authentication credentials invalid ». Le forum affiche une erreur claire lors d'une inscription ou d'une demande de lien et ne crée pas de compte bloqué.

## Étapes à faire plus tard

1. Le domaine `nexus-arcana.fr` est acheté. Créer un compte auprès du service d'envoi retenu, par exemple Resend, puis y ajouter ce domaine.
2. Recopier chez OVHcloud les réglages DNS fournis par le service d'envoi et attendre la vérification du domaine.
3. Créer la clé d'envoi et configurer l'expéditeur du forum, par exemple `contact@nexus-arcana.fr`, dans les réglages privés du serveur.
4. Après la mise en ligne, envoyer un message de test à la fondatrice, puis tester une inscription et un lien « Mot de passe oublié » de bout en bout.

Ne pas copier de clé API ou de mot de passe dans ce document ni dans une conversation. Les comptes déjà existants restent accessibles pendant cette attente.

## Mise en ligne et budget estimatif

- Le forum actuel a besoin d'un hébergement capable de faire tourner le site, le serveur et sa base de données. Un simple hébergement de pages statiques ne suffit pas.
- Point de départ envisagé : un petit VPS de 4 Go de RAM. Exemple consulté le 23 septembre 2026 : OVHcloud VPS-1 affiché à partir de 4,57 € TTC/mois, soit environ 55 € par an. Vérifier le prix et les conditions au moment de l'achat : https://www.ovhcloud.com/fr/vps/
- Domaine `.fr` : exemple OVHcloud consulté le 23 septembre 2026, 5,99 € TTC la première année puis 9,35 € TTC/an. Vérifier disponibilité et prix du nom souhaité : https://www.ovhcloud.com/fr/domains/tld/fr/
- Resend : offre gratuite affichée à 3 000 e-mails/mois, avec 100/jour, sous réserve des conditions en vigueur : https://resend.com/pricing
- Budget indicatif domaine + VPS : environ 60 à 65 € par an au départ, hors options, boîte mail éventuelle et variation tarifaire. Ce n'est pas un devis.
- Lors de la mise en ligne : relier le domaine au serveur, configurer HTTPS, vérifier sauvegardes et restauration, mettre à jour `FORUM_URL`, puis tester inscription, e-mails et récupération du mot de passe de bout en bout.
- Le domaine `nexus-arcana.fr` a été acheté ; l'hébergement public et le service d'envoi restent à finaliser.
