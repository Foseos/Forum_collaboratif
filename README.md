# Forum Public

Forum de discussion moderne, open-source, construit avec Django REST Framework et Vue 3.

## Stack Technique

- **Backend** : Django 5 + Django REST Framework
- **Frontend** : Vue 3 + Pinia + Vite (Phase 3)
- **Base de données** : SQLite (dev) / PostgreSQL (prod)
- **Déploiement** : Docker + GitHub Actions

## Fonctionnalités

- Authentification JWT (inscription, connexion, profil)
- Catégories de discussion
- Sujets (topics) et messages (posts)
- Système de réactions (like, dislike, emojis)
- Notifications avec polling
- Rôles : admin, modérateur, utilisateur
- API RESTful documentée (Swagger)

## Lancement rapide

### Prérequis

- Python 3.12+
- pip

### Installation

```bash
# Cloner le dépôt
git clone <repo-url>
cd Forum

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou : venv\Scripts\activate  # Windows

# Installer les dépendances
make install

# Appliquer les migrations
make migrate

# Créer un superutilisateur
make createsuperuser

# Lancer le serveur
make run
```

Le serveur sera accessible sur http://localhost:8000

### Documentation API

- Swagger UI : http://localhost:8000/api/docs/
- Schema OpenAPI : http://localhost:8000/api/schema/

### Docker

```bash
# Lancer tous les services
make docker-up

# Arrêter les services
make docker-down
```

## Structure du Projet

```
Forum/
├── backend/
│   ├── apps/
│   │   ├── users/          # Gestion des utilisateurs
│   │   ├── forum/          # Catégories, topics, posts, réactions
│   │   └── notifications/  # Notifications
│   ├── config/             # Configuration Django
│   └── requirements/       # Dépendances Python
├── frontend/               # Vue 3 (Phase 3)
├── docker-compose.yml
└── Makefile
```

## Commandes utiles

| Commande | Description |
|---|---|
| `make install` | Installer les dépendances |
| `make migrate` | Appliquer les migrations |
| `make run` | Lancer le serveur dev |
| `make test` | Lancer les tests |
| `make lint` | Lancer les linters |
| `make createsuperuser` | Créer un superutilisateur |

## Contribution

1. Forker le dépôt
2. Créer une branche (`git checkout -b feature/ma-fonctionnalite`)
3. Commiter les changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Pousser la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrir une Pull Request

## Licence

MIT
