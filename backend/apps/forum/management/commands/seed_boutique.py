from django.core.management.base import BaseCommand

from apps.forum.models import Category, Topic, Post
from apps.users.models import User


BOUTIQUE_CONTENT = """<div style="font-family: Georgia, 'Times New Roman', serif; background: #0d0a1a; color: #e2d9f3; padding: 2rem; border-radius: 10px; border: 1px solid rgba(124,58,237,0.3); max-width: 800px; margin: 0 auto;">

<p style="margin: 0 0 0.4rem; font-size: 0.58rem; letter-spacing: 0.38em; text-transform: uppercase; color: #6d28d9; text-align: center;">✦ Nexus Arcana · San Francisco ✦</p>
<h1 style="margin: 0 0 0.4rem; font-size: 1.8rem; font-weight: normal; font-style: italic; color: #f5d76e; letter-spacing: 0.04em; text-align: center;">La Boutique Magique</h1>
<p style="margin: 0 0 2rem; font-size: 0.82rem; color: #a78bfa; font-style: italic; letter-spacing: 0.06em; text-align: center;">Objets enchantés, potions &amp; cristaux — Commandez en répondant à ce sujet</p>
<p style="margin: 0 0 1.5rem; font-size: 0.82rem; color: #c4b5d4; line-height: 1.6; text-align: center;">Les effets temporaires se comptent en <strong>tours de RP</strong> : un tour correspond à une intervention de chaque personnage directement concerné dans la scène. Le tour d'utilisation compte comme le premier.</p>

<!-- ══ POTIONS ══ -->
<div style="margin-bottom: 1.5rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.35), rgba(109,40,217,0.08)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">🧪 I. Potions &amp; Élixirs</h2>
  </div>
  <div style="padding: 0.5rem 0;">
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr style="background: rgba(109,40,217,0.1);">
          <th style="padding: 0.4rem 1rem; text-align: left; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Objet</th>
          <th style="padding: 0.4rem 1rem; text-align: left; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Vertus</th>
          <th style="padding: 0.4rem 1rem; text-align: right; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Prix</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Potion d'invisibilité</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Rend invisible pendant 3 tours de RP. Ne masque pas les bruits ni les odeurs.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">50 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1); background: rgba(255,255,255,0.015);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Potion de guérison</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Soigne les blessures mineures à modérées en 1 tour de RP. Inefficace sur les blessures mortelles.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">100 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Élixir de vérité</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Agit pendant 2 tours de RP, avec l'accord du joueur concerné. Résistance possible pour les êtres puissants.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">150 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1); background: rgba(255,255,255,0.015);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Potion de téléportation</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Permet une téléportation instantanée vers un lieu connu. Usage unique. Ne fonctionne pas dans les zones protégées.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">120 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Potion d'immunité magique</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Protège des sorts offensifs pendant 3 tours de RP. N'annule pas les sorts déjà actifs.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">200 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1); background: rgba(255,255,255,0.015);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Potion de sommeil profond</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Plonge la cible dans un sommeil de 2 tours de RP, avec l'accord de son joueur. Inodore et incolore une fois diluée.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">80 $</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- ══ CRISTAUX & PIERRES ══ -->
<div style="margin-bottom: 1.5rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.35), rgba(109,40,217,0.08)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">💎 II. Cristaux &amp; Pierres</h2>
  </div>
  <div style="padding: 0.5rem 0;">
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr style="background: rgba(109,40,217,0.1);">
          <th style="padding: 0.4rem 1rem; text-align: left; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Objet</th>
          <th style="padding: 0.4rem 1rem; text-align: left; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Vertus</th>
          <th style="padding: 0.4rem 1rem; text-align: right; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Prix</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Cristal de quartz pur</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Amplifie les pouvoirs magiques lors des rituels. Idéal pour les cercles de protection.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">30 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1); background: rgba(255,255,255,0.015);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Améthyste de protection</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Crée un bouclier contre les entités maléfiques de niveau faible à moyen lorsqu'elle est portée.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">80 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Obsidienne noire</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Absorbe l'énergie négative et les malédictions légères. À purifier après chaque usage.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">60 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1); background: rgba(255,255,255,0.015);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Pierre de lune sacrée</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Renforce les pouvoirs de divination et de visions. Particulièrement puissante lors des pleines lunes.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">90 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Rubis de feu</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Amplifie les pouvoirs de feu et de pyrokinésie. Dangereux sans maîtrise suffisante.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">150 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1); background: rgba(255,255,255,0.015);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Saphir des eaux profondes</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Accorde une résistance à l'hydrokinésie et aux sorts aquatiques. Favorise la clarté d'esprit.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">130 $</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- ══ OBJETS MAGIQUES ══ -->
<div style="margin-bottom: 1.5rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.35), rgba(109,40,217,0.08)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">🔮 III. Objets &amp; Artefacts</h2>
  </div>
  <div style="padding: 0.5rem 0;">
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr style="background: rgba(109,40,217,0.1);">
          <th style="padding: 0.4rem 1rem; text-align: left; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Objet</th>
          <th style="padding: 0.4rem 1rem; text-align: left; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Vertus</th>
          <th style="padding: 0.4rem 1rem; text-align: right; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Prix</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Miroir de vérité</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Révèle la vraie nature des êtres (démon, sorcière, mortel…) lorsqu'ils se regardent dedans.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">300 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1); background: rgba(255,255,255,0.015);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Amulette de protection</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Portée sur soi, repousse les entités de bas niveau et atténue les sorts de domination.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">70 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Talisman d'équilibre</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Stabilise les pouvoirs instables ou incontrôlés. Recommandé pour les jeunes sorcières.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">250 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1); background: rgba(255,255,255,0.015);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Grimoire vierge enchanté</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Résiste au feu et à l'eau. Les sorts qui y sont inscrits sont scellés contre la lecture non autorisée.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">40 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Baguette de saule pleureur</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Canalise les sorts de divination et de localisation. Amplifie la précision des pendules.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">200 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1); background: rgba(255,255,255,0.015);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Calice de cristal</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Amplifie les rituels de groupe jusqu'à ×3. Fragile — se brise si mal utilisé.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">120 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Pochette de sortilèges</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Contient et transporte jusqu'à 3 sorts actifs sans risque de déclenchement accidentel.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">90 $</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- ══ HERBES & INGRÉDIENTS ══ -->
<div style="margin-bottom: 1.5rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.35), rgba(109,40,217,0.08)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">🌿 IV. Herbes &amp; Ingrédients</h2>
  </div>
  <div style="padding: 0.5rem 0;">
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr style="background: rgba(109,40,217,0.1);">
          <th style="padding: 0.4rem 1rem; text-align: left; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Objet</th>
          <th style="padding: 0.4rem 1rem; text-align: left; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Vertus</th>
          <th style="padding: 0.4rem 1rem; text-align: right; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Prix</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Sauge blanche</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Purification des lieux et des objets. Chasse les esprits errants et les résidus magiques.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">20 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1); background: rgba(255,255,255,0.015);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Lavande enchantée</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Apaise les esprits agités et réduit l'emprise des entités de manipulation.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">15 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Belladone distillée</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Ingrédient clé des potions de sommeil et d'illusion. Usage réservé aux sorcières expérimentées.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">50 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1); background: rgba(255,255,255,0.015);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Herbes du solstice</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Décuple les pouvoirs lors des rituels aux solstices et équinoxes. Récoltées une fois par an.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">80 $</td>
        </tr>
        <tr style="border-top: 1px solid rgba(124,58,237,0.1);">
          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">Encens de purification</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">Chasse les esprits malveillants et neutralise les sorts résiduels dans un espace. Boîte de 12 bâtons.</td>
          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">25 $</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- Notice commande -->
<div style="border: 1px dashed rgba(245,215,110,0.3); border-radius: 7px; padding: 1rem 1.25rem; background: rgba(245,215,110,0.03);">
  <p style="margin: 0 0 0.4rem; font-size: 0.72rem; letter-spacing: 0.15em; text-transform: uppercase; color: #f5d76e;">📦 Comment commander ?</p>
  <p style="margin: 0; font-size: 0.82rem; color: #a78bfa; line-height: 1.7;">Répondez à ce sujet en précisant <strong style="color: #e2d9f3;">votre personnage</strong>, <strong style="color: #e2d9f3;">l'objet souhaité</strong> et la <strong style="color: #e2d9f3;">quantité</strong>. Un administrateur validera votre achat et déduira le montant de votre compte bancaire.</p>
</div>

<p style="text-align: center; margin: 1.5rem 0 0; font-size: 0.58rem; color: #2d1f4a; font-style: italic; letter-spacing: 0.18em;">✦ Boutique officielle du Nexus Arcana — San Francisco ✦</p>
</div>"""


class Command(BaseCommand):
    help = "Crée le topic et le post de la boutique magique."

    def handle(self, *args, **options):
        try:
            category = Category.objects.get(slug="boutique-magique")
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "Catégorie 'boutique-magique' introuvable. Lancez d'abord seed_categories."
            ))
            return

        admin = User.objects.filter(role="admin").first()
        if not admin:
            admin = User.objects.first()
        if not admin:
            self.stdout.write(self.style.ERROR("Aucun utilisateur trouvé."))
            return

        topic, created = Topic.objects.get_or_create(
            slug="catalogue-boutique-magique",
            defaults={
                "title": "📜 Catalogue de la Boutique Magique",
                "category": category,
                "author": admin,
                "is_pinned": True,
                "is_locked": False,
            },
        )

        if created:
            Post.objects.create(
                topic=topic,
                author=admin,
                content=BOUTIQUE_CONTENT,
            )
            self.stdout.write(self.style.SUCCESS("✓ Topic boutique créé avec succès."))
        else:
            self.stdout.write("— Topic boutique déjà existant.")
