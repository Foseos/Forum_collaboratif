import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
sys.path.insert(0, '/app')
django.setup()

from apps.forum.models import Category, Topic, Post
from apps.users.models import User

author = User.objects.filter(is_superuser=True).first()

# 1. Sous-catégorie
parent = Category.objects.get(slug='reglement-magique')
sub, created = Category.objects.get_or_create(
    slug='grimoire-des-pouvoirs',
    defaults={
        'name': 'Grimoire des Pouvoirs',
        'description': 'Répertoire officiel de tous les pouvoirs magiques du forum, avec leurs évolutions et conditions d\'acquisition.',
        'parent': parent,
        'order': 1,
    }
)
print(f"{'Created' if created else 'Exists'} sub-category id={sub.id}")

# 2. Topic
t, tcreated = Topic.objects.get_or_create(
    slug='liste-des-pouvoirs-magiques',
    defaults={
        'title': 'Liste des Pouvoirs Magiques & Évolutions',
        'category': sub,
        'author': author,
        'is_pinned': True,
        'is_locked': True,
    }
)
print(f"{'Created' if tcreated else 'Exists'} topic id={t.id}")

# 3. Post
CONTENT = """<div style="font-family: Georgia, 'Times New Roman', serif; background: #0d0a1a; color: #e2d9f3; padding: 2rem; border-radius: 10px; border: 1px solid rgba(124,58,237,0.3); max-width: 820px; margin: 0 auto;">

<!-- EN-TÊTE -->
<div style="text-align: center; margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
  <p style="margin: 0 0 0.5rem; font-size: 0.58rem; letter-spacing: 0.38em; text-transform: uppercase; color: #6d28d9;">✦ Nexus Arcana · Grimoire des Pouvoirs ✦</p>
  <h1 style="margin: 0 0 0.6rem; font-size: 2rem; font-weight: normal; font-style: italic; color: #f5d76e; letter-spacing: 0.06em;">Répertoire des Pouvoirs Magiques</h1>
  <p style="margin: 0; font-size: 0.82rem; color: #a78bfa; font-style: italic;">Évolutions, conditions et règles d'acquisition — usage réservé aux membres</p>
</div>

<!-- INTRO -->
<div style="margin-bottom: 1.5rem; padding: 0.85rem 1.1rem; background: rgba(109,40,217,0.08); border-left: 3px solid rgba(124,58,237,0.5); border-radius: 0 6px 6px 0;">
  <p style="margin: 0; font-size: 0.88rem; color: #c4b5d4; line-height: 1.8;">Ce grimoire ne recense ni tous les pouvoirs ni toutes leurs évolutions possibles. Vous pouvez proposer un pouvoir ou une évolution au staff et en discuter avec l'équipe avant de l'intégrer à votre fiche ou de l'utiliser en RP. Chaque personnage commence avec quatre capacités maximum, actives et passives comprises, choisies selon sa nature et validées dans sa fiche. Les capacités supplémentaires et les évolutions s'acquièrent ensuite en jeu selon les règles de la boutique. Le symbole <span style="color: #f5d76e;">★</span> signale une validation explicite de l'équipe avant utilisation.</p>
</div>

<!-- SECTION : POUVOIRS OFFENSIFS -->
<div style="margin-bottom: 1.4rem; border: 1px solid rgba(239,68,68,0.3); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(239,68,68,0.25), rgba(239,68,68,0.06)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(239,68,68,0.2);">
    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #f87171; font-weight: normal;">⚡ I. Pouvoirs Offensifs</h2>
  </div>
  <div style="padding: 0.75rem 1rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.86rem;">
      <thead>
        <tr style="border-bottom: 1px solid rgba(239,68,68,0.2);">
          <th style="text-align: left; padding: 0.35rem 0.75rem 0.35rem 0; color: #f87171; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 28%;">Pouvoir</th>
          <th style="text-align: left; padding: 0.35rem 0.75rem; color: #f87171; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 32%;">Description</th>
          <th style="text-align: left; padding: 0.35rem 0; color: #f87171; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;">Évolution(s) possible(s)</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Boules d'énergie</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Projection de sphères d'énergie pure vers une cible.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Éclairs d'énergie (portée accrue) · Boules d'énergie noire ★ · Salve multiple ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Télékinésie</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Déplacement d'objets et de personnes par la pensée.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Répulsion télékinétique · Vol télékinétique ★ · Démolition moléculaire ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Pyrokinésie</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Création et manipulation du feu à volonté.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Torrent de feu · Bouclier de feu · Feu magique (immunité aux sortilèges) ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Cryokinésie</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Génération et contrôle du froid et de la glace.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Glacier (immobilisation totale) · Tempête de glace ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Combustion moléculaire</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Accélération des molécules d'une cible jusqu'à l'explosion.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Explosion en chaîne · Combustion à distance ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Décélération moléculaire</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Ralentissement des molécules pour immobiliser ou figer.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Arrêt moléculaire total · Explosion moléculaire ★ · Zone de gel ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Foudre / Électrokinésie</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Génération et projection d'arcs électriques.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Cage électrique · Tempête électrique ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Vague de force</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Émission d'une onde de choc repoussant tout obstacle.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Onde de destruction ★ · Vague omnidirectionnelle ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Cyclogenèse</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Création de tourbillons et de tornades magiques.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Tornade dévastatrice ★ · Mur de vent ★</td>
        </tr>
        <tr>
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Combustion par le regard</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Embrasement d'une cible par simple concentration du regard.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Combustion instantanée · Regard de désintégration ★</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- SECTION : POUVOIRS DÉFENSIFS -->
<div style="margin-bottom: 1.4rem; border: 1px solid rgba(59,130,246,0.3); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(59,130,246,0.22), rgba(59,130,246,0.05)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(59,130,246,0.2);">
    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #93c5fd; font-weight: normal;">🛡️ II. Pouvoirs Défensifs & Protecteurs</h2>
  </div>
  <div style="padding: 0.75rem 1rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.86rem;">
      <thead>
        <tr style="border-bottom: 1px solid rgba(59,130,246,0.2);">
          <th style="text-align: left; padding: 0.35rem 0.75rem 0.35rem 0; color: #93c5fd; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 28%;">Pouvoir</th>
          <th style="text-align: left; padding: 0.35rem 0.75rem; color: #93c5fd; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 32%;">Description</th>
          <th style="text-align: left; padding: 0.35rem 0; color: #93c5fd; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;">Évolution(s) possible(s)</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Bouclier d'énergie</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Création d'un dôme protecteur absorbant les attaques.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Bouclier de groupe · Bouclier réfléchissant ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Invulnérabilité partielle</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Résistance accrue aux attaques physiques et magiques.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Invulnérabilité totale ★ (accord staff obligatoire)</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Absorption de magie</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Neutralisation d'un sort ou d'un pouvoir dirigé vers soi.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Renvoi de pouvoir · Absorption totale ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Camouflage magique</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Dissimulation de l'aura magique aux détecteurs et sorts.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Invisibilité complète ★ · Illusion d'identité ★</td>
        </tr>
        <tr>
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Immunité aux flammes</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Résistance totale au feu naturel et magique.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Immunité élémentaire étendue (froid, foudre) ★</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- SECTION : POUVOIRS DE SOIN & SOUTIEN -->
<div style="margin-bottom: 1.4rem; border: 1px solid rgba(34,197,94,0.3); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(34,197,94,0.2), rgba(34,197,94,0.05)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(34,197,94,0.2);">
    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #86efac; font-weight: normal;">✨ III. Pouvoirs de Soin & Soutien</h2>
  </div>
  <div style="padding: 0.75rem 1rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.86rem;">
      <thead>
        <tr style="border-bottom: 1px solid rgba(34,197,94,0.2);">
          <th style="text-align: left; padding: 0.35rem 0.75rem 0.35rem 0; color: #86efac; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 28%;">Pouvoir</th>
          <th style="text-align: left; padding: 0.35rem 0.75rem; color: #86efac; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 32%;">Description</th>
          <th style="text-align: left; padding: 0.35rem 0; color: #86efac; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;">Évolution(s) possible(s)</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Guérison</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Soin des blessures physiques par imposition des mains.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Guérison à distance · Résurrection ★ (conditions très strictes)</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Empathie</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Perception et absorption des émotions d'autrui.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Absorption de pouvoirs (temporaire) · Projection empathique ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Localisation</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Détection de la position d'une personne ou d'un objet.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Localisation à travers les dimensions ★ · Brouillage de piste ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Transmission de pouvoirs</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Don temporaire d'un pouvoir à un autre être.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Amplification de pouvoirs ★ · Don permanent ★</td>
        </tr>
        <tr>
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Lien vital</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Partage de force vitale pour maintenir quelqu'un en vie.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Lien de groupe ★</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- SECTION : POUVOIRS DE DÉPLACEMENT -->
<div style="margin-bottom: 1.4rem; border: 1px solid rgba(168,85,247,0.35); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.07)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">🌀 IV. Pouvoirs de Déplacement</h2>
  </div>
  <div style="padding: 0.75rem 1rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.86rem;">
      <thead>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.25);">
          <th style="text-align: left; padding: 0.35rem 0.75rem 0.35rem 0; color: #a78bfa; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 28%;">Pouvoir</th>
          <th style="text-align: left; padding: 0.35rem 0.75rem; color: #a78bfa; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 32%;">Description</th>
          <th style="text-align: left; padding: 0.35rem 0; color: #a78bfa; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;">Évolution(s) possible(s)</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Orbing</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Téléportation par dissolution en orbes lumineuses (êtres de lumière).</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Orbing de groupe · Orbing interdimensionnel ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Téléportation / Flash</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Disparition et réapparition instantanée (Cupidon, Anciens).</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Flash de groupe · Téléportation temporelle ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Shimmer</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Dissolution rapide dans les ombres, propre aux démons de rang élevé.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Shimmer silencieux (indétectable) ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Lévitation</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Élévation dans les airs par contrôle du poids corporel.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Vol · Lévitation de groupe ★</td>
        </tr>
        <tr>
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Portail temporel</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Ouverture d'un portail vers le passé ou le futur.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Portail dimensionnel ★ (accord staff obligatoire)</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- SECTION : POUVOIRS DE PERCEPTION -->
<div style="margin-bottom: 1.4rem; border: 1px solid rgba(245,215,110,0.3); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(245,215,110,0.15), rgba(245,215,110,0.03)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(245,215,110,0.2);">
    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #f5d76e; font-weight: normal;">👁️ V. Pouvoirs de Perception & Divination</h2>
  </div>
  <div style="padding: 0.75rem 1rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.86rem;">
      <thead>
        <tr style="border-bottom: 1px solid rgba(245,215,110,0.2);">
          <th style="text-align: left; padding: 0.35rem 0.75rem 0.35rem 0; color: #f5d76e; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 28%;">Pouvoir</th>
          <th style="text-align: left; padding: 0.35rem 0.75rem; color: #f5d76e; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 32%;">Description</th>
          <th style="text-align: left; padding: 0.35rem 0; color: #f5d76e; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;">Évolution(s) possible(s)</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Précognition</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Vision du futur par contact avec un objet ou une personne.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Rétrocognition · Précognition active (sans contact) ★ · Projection astrale ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Clairvoyance</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Perception d'événements distants en temps réel.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Vision dimensionnelle ★ · Clairvoyance de masse ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Télépathie</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Lecture et transmission de pensées à distance.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Contrôle mental ★ · Télépathie de masse ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Nécromancie</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Communication avec les esprits des défunts.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Invocation d'esprits · Commandement des morts ★</td>
        </tr>
        <tr>
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Détection de magie</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Perception des auras et signatures magiques environnantes.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Analyse de sort · Identification de race ★</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- SECTION : POUVOIRS DE MÉTAMORPHOSE -->
<div style="margin-bottom: 1.4rem; border: 1px solid rgba(20,184,166,0.3); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(20,184,166,0.2), rgba(20,184,166,0.04)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(20,184,166,0.2);">
    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #5eead4; font-weight: normal;">🪞 VI. Pouvoirs de Métamorphose & Illusion</h2>
  </div>
  <div style="padding: 0.75rem 1rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.86rem;">
      <thead>
        <tr style="border-bottom: 1px solid rgba(20,184,166,0.2);">
          <th style="text-align: left; padding: 0.35rem 0.75rem 0.35rem 0; color: #5eead4; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 28%;">Pouvoir</th>
          <th style="text-align: left; padding: 0.35rem 0.75rem; color: #5eead4; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 32%;">Description</th>
          <th style="text-align: left; padding: 0.35rem 0; color: #5eead4; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;">Évolution(s) possible(s)</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Métamorphose</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Modification de l'apparence physique à volonté.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Copie de pouvoirs ★ · Métamorphose de masse ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Illusion</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Création d'images et d'environnements illusoires.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Illusion tactile (perçue par tous les sens) ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Invisibilité</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Disparition du champ visuel sans se déplacer.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Invisibilité de groupe · Invisibilité magique (passe les sorts de détection) ★</td>
        </tr>
        <tr>
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Projection astrale</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Séparation de l'âme du corps pour observer ou agir à distance.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Possession ★ · Projection matérielle ★</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- SECTION : POUVOIRS LIÉS À LA NATURE -->
<div style="margin-bottom: 1.4rem; border: 1px solid rgba(132,204,22,0.3); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(132,204,22,0.18), rgba(132,204,22,0.04)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(132,204,22,0.2);">
    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #bef264; font-weight: normal;">🌿 VII. Pouvoirs Liés à la Nature</h2>
  </div>
  <div style="padding: 0.75rem 1rem;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.86rem;">
      <thead>
        <tr style="border-bottom: 1px solid rgba(132,204,22,0.2);">
          <th style="text-align: left; padding: 0.35rem 0.75rem 0.35rem 0; color: #bef264; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 28%;">Pouvoir</th>
          <th style="text-align: left; padding: 0.35rem 0.75rem; color: #bef264; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; width: 32%;">Description</th>
          <th style="text-align: left; padding: 0.35rem 0; color: #bef264; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;">Évolution(s) possible(s)</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Contrôle végétal</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Animation et direction des plantes environnantes.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Appel de la forêt · Forêt labyrinthique ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Contrôle de l'eau</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Manipulation des flux d'eau, création de vagues ou de barrières.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Maîtrise des marées · Noyade à distance ★</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(124,58,237,0.08);">
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Communication animale</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Compréhension et interaction avec les animaux.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Commandement animal · Transformation animale ★</td>
        </tr>
        <tr>
          <td style="padding: 0.45rem 0.75rem 0.45rem 0; color: #e2d9f3; font-weight: 600;">Géokinésie</td>
          <td style="padding: 0.45rem 0.75rem; color: #c4b5d4;">Déplacement et façonnage de la terre et des pierres.</td>
          <td style="padding: 0.45rem 0; color: #c4b5d4;">Séisme · Mur de pierre ★</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- NOTE DE BAS DE PAGE -->
<div style="margin-top: 1.5rem; padding: 0.85rem 1.1rem; background: rgba(245,215,110,0.05); border: 1px solid rgba(245,215,110,0.2); border-radius: 6px; text-align: center;">
  <p style="margin: 0 0 0.3rem; font-size: 0.72rem; color: #f5d76e; letter-spacing: 0.15em; text-transform: uppercase;">★ Légende</p>
  <p style="margin: 0; font-size: 0.82rem; color: #c4b5d4; line-height: 1.7;">Les pouvoirs sans marquage restent soumis au plafond de quatre capacités à la création et à la validation de la fiche.<br>Le symbole <strong style="color: #f5d76e;">★</strong> indique un effet ou une évolution qui demande l'accord explicite de l'équipe avant utilisation en RP.<br>Une évolution ou une nouvelle capacité s'acquiert en jeu selon les règles de la boutique ; aucun pouvoir n'est accordé automatiquement par ce catalogue. En cas de doute, échangez avec le staff pour trouver ensemble une manière de jouer votre idée.</p>
</div>

</div>"""

if Post.objects.filter(topic=t).exists():
    p = Post.objects.filter(topic=t).first()
    p.content = CONTENT
    p.save()
    print(f"Updated post id={p.id}")
else:
    p = Post.objects.create(topic=t, author=author, content=CONTENT)
    print(f"Created post id={p.id}")

print("Done.")
