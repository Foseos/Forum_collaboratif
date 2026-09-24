import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
sys.path.insert(0, '/app')
django.setup()

from apps.forum.models import Post, Topic

CONTENT = """<div style="font-family: Georgia, 'Times New Roman', serif; background: #0d0a1a; color: #e2d9f3; padding: 2rem; border-radius: 10px; border: 1px solid rgba(124,58,237,0.3); max-width: 720px; margin: 0 auto;">

<!-- EN-TÊTE : nom à gauche, image à droite -->
<table style="width: 100%; border-collapse: collapse; margin-bottom: 1.75rem; padding-bottom: 1.5rem; border-bottom: 1px solid rgba(124,58,237,0.2);">
<tr>
  <td style="vertical-align: top; padding-right: 1.5rem;">
    <p style="margin: 0 0 0.5rem; font-size: 0.58rem; letter-spacing: 0.38em; text-transform: uppercase; color: #6d28d9;">✦ Nexus Arcana · Livre des Ombres ✦</p>
    <h1 style="margin: 0 0 0.6rem; font-size: 2rem; font-weight: normal; font-style: italic; color: #f5d76e; letter-spacing: 0.04em; line-height: 1.2;">Leo<br>Wyatt</h1>
    <p style="margin: 0 0 1rem; font-size: 0.82rem; color: #a78bfa; font-style: italic; letter-spacing: 0.06em;">Ancien être de lumière · Humain par choix · Le Bien</p>
    <p style="margin: 0; font-size: 0.75rem; color: #4b3a6b; font-style: italic; line-height: 1.7;">« J'ai renoncé à l'éternité. Pas par faiblesse — parce qu'une vie ordinaire avec eux valait infiniment plus que l'immortalité sans eux. »</p>
  </td>
  <td style="vertical-align: top; width: 210px; text-align: center;">
    <img src="https://zupimages.net/up/26/11/fpsi.jpg" alt="Leo Wyatt" style="width:200px;height:320px;object-fit:cover;border-radius:6px;border:2px solid rgba(124,58,237,0.35);display:block;margin:0 auto;">
    <p style="margin: 0.35rem 0 0; font-size: 0.6rem; color: #3d2d5e; font-style: italic;">Leo Wyatt — Ft Brian Krause</p>
  </td>
</tr>
</table>

<!-- BOX I : IDENTITÉ -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ I. Identité</h2>
  </div>
  <div style="padding: 0.6rem 1rem;">
    <table style="width: 100%; border-collapse: collapse;">
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; width: 42%; border-bottom: 1px solid rgba(124,58,237,0.08);">Âge</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">102 ans sur le papier / apparence d'un homme d'une quarantaine d'années (figé en tant qu'être de lumière, vieillissement lent depuis son retour à l'humanité)</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Date de naissance</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">7 mai 1924, San Francisco</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Sexe</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Masculin</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Orientation sexuelle</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Hétérosexuel</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Situation familiale</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Marié à Piper Halliwell · Père de Wyatt Matthew, Christopher et Mélinda Halliwell</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Race</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Ancien être de lumière (Blanchisseur, puis Ancien) · Humain depuis 2005</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Camp</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Le Bien</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0;">Métier</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3;">Professeur d'histoire · Université de San Francisco</td></tr>
    </table>
  </div>
</div>

<!-- BOX II : POUVOIRS -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ II. Pouvoirs Magiques &amp; Aptitudes</h2>
  </div>
  <div style="padding: 0.85rem 1rem 0.75rem;">
    <p style="margin: 0 0 0.4rem; font-size: 0.78rem; font-weight: 600; color: #c4b5fd;">✦ Pouvoirs anciens (renoncés) :</p>
    <ul style="margin: 0 0 0.9rem; padding-left: 1.3rem; line-height: 1.85; font-size: 0.87rem; color: #c4b5d4;">
      <li><strong style="color: #e2d9f3;">Orbing</strong> — Téléportation par dissolution en orbes de lumière blanche. Signature des êtres de lumière. Leo y a renoncé en même temps qu'à son statut.</li>
      <li><strong style="color: #e2d9f3;">Guérison</strong> — Capacité à soigner les blessures physiques par imposition des mains, réservée aux êtres du Bien. Ce pouvoir fut l'un des derniers à disparaître après sa renonciation — il lui arriva encore, dans les premières années, de sentir la chaleur monter dans ses paumes.</li>
      <li><strong style="color: #e2d9f3;">Localisation</strong> — Sens aigu permettant de percevoir la détresse et la présence de ceux placés sous sa protection. Disparu officiellement, mais Leo affirme qu'il sait encore, parfois, quand ses enfants sont en danger.</li>
      <li><strong style="color: #e2d9f3;">Bouclier de lumière</strong> — Écran protecteur contre les attaques démoniaques. Abandonné avec le reste.</li>
    </ul>
    <p style="margin: 0 0 0.4rem; font-size: 0.78rem; font-weight: 600; color: #c4b5fd;">⚡ Aujourd'hui :</p>
    <ul style="margin: 0; padding-left: 1.3rem; line-height: 1.85; font-size: 0.87rem; color: #c4b5d4;">
      <li><strong style="color: #e2d9f3;">Humain</strong> — Leo n'a plus de pouvoirs actifs. Sa force réside désormais dans son expérience, sa connaissance approfondie du monde magique et la profondeur de ses liens familiaux.</li>
    </ul>
  </div>
</div>

<!-- BOX III : CARACTÈRE -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ III. Âme &amp; Caractère</h2>
  </div>
  <div style="padding: 1rem;">
    <p style="margin: 0; line-height: 1.9; color: #c4b5d4; text-align: justify; font-size: 0.9rem;">Qualités

Sage
Patient
Dévoué
Protecteur
Ancré
Empathique
Courageux sans éclat
Loyal

Défauts

Tendance à se sentir inutile sans ses pouvoirs
Parfois trop effacé face à la force de caractère de Piper
Peut sous-estimer ses propres limites humaines
Porte encore la culpabilité des absences passées</p>
  </div>
</div>

<!-- BOX IV : HISTOIRE -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ IV. Mémoire des Âges · Histoire</h2>
  </div>
  <div style="padding: 1rem;">
    <p style="margin: 0; line-height: 1.9; color: #c4b5d4; text-align: justify; font-size: 0.9rem;"><strong style="color: #e2d9f3;">Une vie ordinaire, une mort ordinaire — 1924-1944</strong><br>
Leo Wyatt est né le 7 mai 1924 à San Francisco, fils d'un menuisier et d'une institutrice. Enfance simple, foi tranquille, sens du devoir chevillé au corps. À vingt ans, il s'engagea comme médecin de campagne lors de la Seconde Guerre mondiale. Il mourut en 1944 sur le sol européen, soignant un blessé sous les tirs. Pas en héros. En homme qui faisait ce qu'il fallait faire.<br><br>

<strong style="color: #e2d9f3;">Blanchisseur — des décennies au service du Bien</strong><br>
Sa mort ne fut pas une fin. Les Anciens le virent tel qu'il était — un être de lumière avant même d'en porter le nom — et lui offrirent une place parmi les Blanchisseurs. Leo accepta sans hésitation. Pendant des décennies, il protégea des sorcières à travers les générations, discret, constant, toujours là où il fallait être.<br><br>

Il devint ensuite Ancien — une élévation qui lui conférait plus de pouvoir, mais l'éloignait davantage du monde des mortels. Cette période fut la plus solitaire de son existence. Haut placé, mais coupé de ce qui lui avait toujours donné un sens : le contact humain, les liens réels, la chaleur d'un foyer.<br><br>

<strong style="color: #e2d9f3;">Piper Halliwell — l'interdit et l'évidence</strong><br>
Lorsqu'il fut assigné aux Sœurs Halliwell, Leo s'attendait à une mission comme les autres. Il rencontra Piper. Ce fut tout sauf une mission comme les autres.<br><br>

Piper Halliwell était exactement ce que les règles des Anciens lui interdisaient d'aimer : une protégée, une mortelle, une sorcière. Il lutta contre ses sentiments avec la discipline d'un homme qui avait passé des décennies à obéir. Il échoua. Elle l'aimait aussi. Ils se marièrent malgré les interdits, malgré les crises, malgré les tentatives des Anciens de les séparer. Leo choisit Piper à chaque fois qu'il eut à choisir — et à chaque fois, ce choix eut un prix.<br><br>

<strong style="color: #e2d9f3;">Wyatt, Chris — et le poids d'une destinée</strong><br>
Le 27 novembre 2002, Wyatt Matthew Halliwell vint au monde. Le premier enfant deux fois béni — né de l'union d'une sorcière et d'un être de lumière, porteur d'une puissance hors norme qui attira immédiatement l'attention des forces du Mal comme du Bien. Leo vit dans les yeux de son fils aîné une lumière magnifique et une cible. Les deux à la fois.<br><br>

Christopher naquit le 16 juillet 2004. Moins éclatant que son frère aux yeux du monde magique, mais tout aussi profond. Leo perçut très tôt en Chris une complexité que les autres mettaient du temps à voir : une intelligence acérée, une sensibilité dissimulée sous une carapace dure, une volonté de prouver sa valeur sans jamais l'exprimer. La relation entre ses deux fils serait compliquée — il le sut dès le début. Il fit ce qu'il put pour être le pont entre eux, sans toujours y parvenir.<br><br>

<strong style="color: #e2d9f3;">La renonciation — 2005</strong><br>
En 2005, Leo prit la décision la plus difficile et la plus claire de son existence : renoncer à son statut d'être de lumière. Renoncer aux pouvoirs, à l'immortalité, à la mission. Renoncer à tout ce qu'il avait été pendant plus de soixante ans.<br><br>

Pas par lassitude. Par amour. Piper et ses fils avaient besoin d'un père présent — pas d'un guide qui disparaissait en orbes blanches au milieu des repas. Il voulait vieillir avec elle. Il voulait être là, physiquement, irrémédiablement là, quand ses enfants auraient besoin de lui.<br><br>

La renonciation fut prononcée. Ses pouvoirs s'éteignirent progressivement. La guérison fut la dernière à partir — comme si son corps refusait d'abandonner l'instinct de protéger.<br><br>

<strong style="color: #e2d9f3;">Mélinda — la surprise</strong><br>
Mélinda naquit le 9 mars 2007. Conçue alors que Leo était déjà pleinement humain, sa famille pensait qu'elle serait uniquement sorcière. Les êtres de lumière ne transmettent leurs dons qu'à travers leur nature active — or Leo n'en avait plus.<br><br>

Mélinda démentit toutes les prévisions. Sa nature mi-sorcière, mi-être de lumière se manifesta avec l'évidence d'une vérité ancienne. Leo n'eut pas d'explication. Il eut seulement de la gratitude — et la certitude tranquille que certaines choses ne s'expliquent pas, elles s'acceptent.<br><br>

<strong style="color: #e2d9f3;">Professeur, père, mari — aujourd'hui</strong><br>
Leo enseigne l'histoire à l'université de San Francisco depuis 2008. Ses étudiants le trouvent passionné, précis, avec un rapport au passé qui dépasse la simple érudition — ils ne savent pas à quel point c'est juste. Il a vécu des pans entiers de ce qu'il leur enseigne.<br><br>

Il regarde ses enfants grandir avec une fierté mêlée d'inquiétude constante. Wyatt porte un poids immense et Leo connaît ce que ce genre de poids peut faire à un homme. Chris avance seul là où il pourrait demander de l'aide, et Leo reconnaît aussi cette solitude — il a été cet homme-là trop longtemps. Mélinda, sa cadette, brûle d'un feu qu'il espère ne jamais voir s'éteindre.<br><br>

Il est humain. Il n'a plus de pouvoirs. Dans un univers où ses enfants peuvent orber, guérir et exploser des démons d'un geste, Leo Wyatt arrive avec ses deux mains, son histoire et sa présence. Ce n'est pas rien. C'est même, parfois, ce dont ils ont le plus besoin.</p>
  </div>
</div>

</div>"""

t = Topic.objects.filter(slug='leo-wyatt').first()
if not t:
    print("ERROR: topic 'leo-wyatt' not found")
    exit(1)

p = Post.objects.filter(topic=t).first()
if not p:
    print("ERROR: no post found")
    exit(1)

p.content = CONTENT
p.save()
print(f"OK — fiche Leo Wyatt saved (post id={p.id}, {len(CONTENT)} chars)")
