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
    <h1 style="margin: 0 0 0.6rem; font-size: 2rem; font-weight: normal; font-style: italic; color: #f5d76e; letter-spacing: 0.04em; line-height: 1.2;">Cole<br>Turner</h1>
    <p style="margin: 0 0 1rem; font-size: 0.82rem; color: #a78bfa; font-style: italic; letter-spacing: 0.06em;">Mi-humain mi-démon · Balthazar · Le Bien</p>
    <p style="margin: 0; font-size: 0.75rem; color: #4b3a6b; font-style: italic; line-height: 1.7;">« J'ai été le pire des démons. Et j'ai choisi d'être le meilleur des hommes. Ce n'est pas la nature qui définit ce que l'on est — c'est chaque choix que l'on fait. »</p>
  </td>
  <td style="vertical-align: top; width: 210px; text-align: center;">
    <img src="https://zupimages.net/up/26/11/fpsi.jpg" alt="Cole Turner" style="width:200px;height:320px;object-fit:cover;border-radius:6px;border:2px solid rgba(124,58,237,0.35);display:block;margin:0 auto;">
    <p style="margin: 0.35rem 0 0; font-size: 0.6rem; color: #3d2d5e; font-style: italic;">Cole Turner — Ft Julian McMahon</p>
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
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; width: 42%; border-bottom: 1px solid rgba(124,58,237,0.08);">Âge</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">141 ans normalement / apparence d'un homme d'une quarantaine d'années (vieillissement ralenli par son héritage démoniaque)</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Date de naissance</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">14 novembre 1885, San Francisco</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Sexe</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Masculin</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Orientation sexuelle</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Hétérosexuel</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Situation familiale</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Divorcé · Ex-époux de Phoebe Halliwell · Père de Jensen Turner · Beau-père de Prudence Johanna, Parker et Peyton Halliwell</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Race</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Mi-humain mi-démon (alias démoniaque : Balthazar)</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Camp</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Le Bien</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Lieu de résidence</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">San Francisco — appartement au cœur du quartier SOMA</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0;">Métier</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3;">Avocat · Cabinet Turner &amp; Associates · Spécialité droit pénal et protection des victimes de crimes occultes</td></tr>
    </table>
  </div>
</div>

<!-- BOX II : POUVOIRS -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ II. Pouvoirs Magiques &amp; Aptitudes</h2>
  </div>
  <div style="padding: 0.85rem 1rem 0.75rem;">
    <p style="margin: 0 0 0.4rem; font-size: 0.78rem; font-weight: 600; color: #c4b5fd;">⚡ Pouvoirs actifs :</p>
    <ul style="margin: 0 0 0.9rem; padding-left: 1.3rem; line-height: 1.85; font-size: 0.87rem; color: #c4b5d4;">
      <li><strong style="color: #e2d9f3;">Boules d'énergie</strong> — Projette des sphères d'énergie démoniaque concentrée. Précises et dévastatrices, elles peuvent être chargées en intensité selon la menace. Signature de combat de Balthazar.</li>
      <li><strong style="color: #e2d9f3;">Shimmer</strong> — Téléportation démoniaque instantanée sous forme d'un scintillement bleuté. Silencieuse, rapide, utilisable en combat. Laisse une légère traînée d'énergie noire dans l'air.</li>
      <li><strong style="color: #e2d9f3;">Explosion moléculaire</strong> — Vestige de sa possession par la Source du Mal. Peut désintégrer des matières organiques et inorganiques d'un geste. Pouvoir violent qu'il n'utilise qu'en dernier recours, conscient de ce qu'il lui a coûté.</li>
      <li><strong style="color: #e2d9f3;">Force et résistance surhumaines</strong> — Son corps mi-démon encaisse des blessures qui seraient mortelles pour un humain. Cicatrise plus vite, résiste aux chutes, aux impacts, aux flammes ordinaires.</li>
      <li><strong style="color: #e2d9f3;">Immunité partielle</strong> — Certains sortilèges et pouvoirs magiques glissent sur lui ou voient leur effet atténué. Résistance innée héritée de son sang démoniaque — notamment aux sorts de révélation et de paralysie.</li>
    </ul>
    <p style="margin: 0 0 0.4rem; font-size: 0.78rem; font-weight: 600; color: #c4b5fd;">🔺 Faiblesses :</p>
    <ul style="margin: 0; padding-left: 1.3rem; line-height: 1.85; font-size: 0.87rem; color: #c4b5d4;">
      <li><strong style="color: #e2d9f3;">Dualité intérieure</strong> — Sa part démoniaque peut resurgir sous l'effet d'une magie noire puissante ou d'une rage extrême. Risque de régression vers Balthazar.</li>
      <li><strong style="color: #e2d9f3;">Eau bénite et charmes de purification</strong> — Agissent sur sa composante démoniaque, provoquant brûlures et désorientation.</li>
    </ul>
  </div>
</div>

<!-- BOX III : CARACTÈRE -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ III. Âme &amp; Caractère</h2>
  </div>
  <div style="padding: 1rem;">
    <p style="margin: 0; line-height: 1.9; color: #c4b5d4; text-align: justify; font-size: 0.9rem;">Cole Turner est un homme de contradictions profondes, et il en est pleinement conscient. Pendant plus d'un siècle, il a été Balthazar : froid, calculateur, impitoyable. Un prédateur au service du Mal qui ne connaissait ni hésitation ni remords. Cette part de lui n'a pas disparu — elle sommeille, contenue par une volonté de fer et un choix quotidien de ne pas la laisser gagner.<br><br>

En société, Cole présente un masque de sophistication élégante. Il est caustique, parfois sardonique, doté d'un humour noir qui peut déstabiliser ceux qui ne le connaissent pas. Il parle peu de ses émotions, préfère l'action à la confidence. Sous cette surface polie et distante se cache un homme qui a appris — à grand prix — ce que signifie réellement aimer quelqu'un.<br><br>

Sa transformation n'a pas été un éclair de grâce divine. Elle s'est faite à coups d'erreurs, de rechutes et d'un amour aussi douloureux qu'absolu pour Phoebe Halliwell. Il sait qu'il lui a causé une souffrance immense. Il porte cette dette sans chercher à l'effacer, seulement à la mériter autrement — en étant présent, en protégeant ceux qu'elle aime, en devenant le père que Jensen n'a pas eu.<br><br>

Face aux trois filles de Phoebe et Coop, Cole a adopté une posture particulière : jamais intrusif, jamais dans la surcompensation. Avec Prudence Johanna, il a dû gagner un respect difficile — elle est perceptive et n'accorde pas sa confiance facilement. Avec Parker, la plus rebelle, il a trouvé une complicité inattendue, reconnaissant en elle sa propre résistance à l'autorité. Avec Peyton, la plus réservée, il a été patient comme personne ne l'avait été pour lui — et elle le lui rend aujourd'hui avec une loyauté discrète mais sincère.<br><br>

Cole ne se définit plus comme un démon qui essaie d'être bien. Il se définit comme un homme qui porte un démon en lui et choisit, chaque matin, de ne pas le laisser conduire.</p>
  </div>
</div>

<!-- BOX IV : HISTOIRE -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ IV. Mémoire des Âges · Histoire</h2>
  </div>
  <div style="padding: 1rem;">
    <p style="margin: 0; line-height: 1.9; color: #c4b5d4; text-align: justify; font-size: 0.9rem;"><strong style="color: #e2d9f3;">Les premières années — 1885-1900</strong><br>
Cole Turner est né le 14 novembre 1885 dans un San Francisco en plein essor, fils d'Elizabeth Turner, une jeune femme humaine issue d'une famille discrète, et d'un démon connu sous le nom d'Abel — ou Balcoin, dans les cercles infernaux. Sa mère savait exactement ce qu'était son amant. Elle aimait trop pour s'en détourner. Cet amour interdit lui coûta la vie quand Cole eut sept ans, emportée par une fièvre que les médecins ne surent jamais expliquer.<br><br>

L'enfant grandît seul, tiraillé entre une humanité fragile et une puissance qu'il ne comprenait pas encore. Les miroirs lui montraient un garçon ordinaire. Les autres démons lui montraient un héritier. À quinze ans, les Triad le trouvèrent avant qu'il ne se trouve lui-même.<br><br>

<strong style="color: #e2d9f3;">Balthazar — un siècle au service du Mal — 1900-2000</strong><br>
Pendant plus d'un siècle, Cole Turner cessa d'exister. Il ne resta que Balthazar : l'un des démons les plus redoutés de sa génération, tueur de sorcières, agent des Triad. Il opérait avec une précision chirurgicale, sans états d'âme, sans attaches. Il apprit à ne jamais s'attarder sur les visages de ceux qu'il éliminait. Il apprit surtout à ne jamais se laisser approcher.<br><br>

Cette période ne fut pas que violence. Balthazar était aussi avocat — une façade parfaite pour infiltrer le monde des humains, accumuler ressources et informations. Il excella dans ce rôle, développant une intelligence légale redoutable qui lui servira bien plus tard, sous un autre nom.<br><br>

<strong style="color: #e2d9f3;">Phoebe Halliwell et la chute du démon — 2001</strong><br>
La mission reçue des Triad semblait identique aux précédentes : neutraliser les trois Sœurs Halliwell, les nouvelles Charmed Ones. Cole s'infiltra dans leur entourage sous son identité humaine. Il rencontra Phoebe. Et tout s'effondra.<br><br>

Phoebe Halliwell ne ressemblait à aucune des cibles qu'il avait connues. Elle était brillante, têtue, profondément vivante. Elle voyait en lui quelque chose qu'il ne voyait plus lui-même : la part humaine qu'il avait enterrée. Pour la première fois en cent ans, Balthazar hésita. Puis choisit. Il choisit Phoebe.<br><br>

Ce choix faillit le détruire plusieurs fois. Il dut naviguer entre trahisons forcées et protections secrètes. Il la sauva. Il lui mentit. Il la blessa. Elle lui pardonna. Et recommença. Leur relation fut la chose la plus difficile et la plus vraie qu'il ait jamais vécue.<br><br>

Jensen, leur fils, naquit dans cette période de chaos et de secret. Né d'une union entre une femme issue d'une longue lignée de sorcières et d'un demi-démon, l'enfant fut arraché à eux par des forces obscures qui virent en lui un potentiel à exploiter. Cole et Phoebe n'apprirent son existence que bien plus tard, quand il n'était plus en mesure de les retrouver seul.<br><br>

<strong style="color: #e2d9f3;">La Source, la chute et le divorce</strong><br>
Le mariage de Cole et Phoebe fut une victoire arrachée à l'impossible — et presque aussitôt menacée. Cole fut possédé par l'essence de la Source du Mal, transformé en un réceptacle pour la puissance la plus obscure de l'univers démoniaque. Pendant cette période, il agit sous une influence dont il n'avait pas pleinement conscience, causant des dommages qu'il ne pourra jamais entièrement réparer. Les Charmed Ones le libérèrent. Le divorce suivi.<br><br>

Phoebe avait tout donné. Elle ne pouvait plus. Cole le comprit. Il ne se battit pas contre sa décision — non par résignation, mais parce qu'il l'aimait assez pour respecter ce qu'elle choisissait pour elle-même.<br><br>

<strong style="color: #e2d9f3;">Les années de reconstruction — et Phoebe, Coop, les filles</strong><br>
Phoebe rencontra Coop Everhart. Elle eut trois filles avec lui : Prudence Johanna, Parker, et Peyton. Cole aurait pu disparaître. Il n'en fit rien.<br><br>

Non par amour possessif ou incapacité à tourner la page, mais parce que Jensen était quelque part dans le monde sous une emprise obscure, et parce que ces trois filles grandissaient dans un univers magique complexe. Cole resta — à distance d'abord, puis graduellement plus présent. Il ne chercha jamais à remplacer Coop. Il devint autre chose : un adulte de confiance, une présence stable, quelqu'un qui avait traversé le pire et était revenu.<br><br>

Avec Prudence Johanna, ce fut difficile. Elle est perspicace, méfiante, digne de sa mère. Elle mit des années à baisser sa garde. Aujourd'hui elle le respecte — pas comme un père de substitution, mais comme un allié.<br><br>

Avec Parker, la plus frondeuse, Cole reconnut immédiatement quelque chose de familier. Deux êtres qui refusent les règles qu'on ne leur a pas expliquées. Ils se chamaillent encore, mais avec une affection réelle.<br><br>

Avec Peyton, la plus discrète, Cole fut simplement patient. Il ne força rien. Il était là quand elle avait besoin, absent quand elle ne voulait pas. Cette constance silencieuse fit ce que les mots n'auraient pas pu faire.<br><br>

<strong style="color: #e2d9f3;">Jensen — le retour d'un fils — aujourd'hui</strong><br>
Jensen Turner a mis des années à s'affranchir de l'emprise qui l'avait tenu éloigné. Quand il revint vers sa famille, Cole fut l'un des premiers à lui tendre la main — sans condition, sans reproche. Il savait mieux que quiconque ce que signifiait choisir le bien alors que tout vous pousse vers le Mal.<br><br>

Aujourd'hui, Cole Turner exerce comme avocat spécialisé en protection des victimes de crimes occultes. Il travaille dans l'ombre des institutions, utilisant sa connaissance du monde démoniaque pour défendre ceux que la loi ordinaire ne sait pas protéger. Il n'est pas un héros. Il ne cherche pas à l'être. Il est juste, enfin, un homme qui fait le choix d'être bien — chaque jour, depuis cent quarante ans.</p>
  </div>
</div>

</div>"""

t = Topic.objects.filter(slug='cole-turner').first()
if not t:
    print("ERROR: topic 'cole-turner' not found")
    exit(1)

p = Post.objects.filter(topic=t).first()
if not p:
    print("ERROR: no post found for topic 'cole-turner'")
    exit(1)

p.content = CONTENT
p.save()
print(f"OK — fiche Cole Turner saved (post id={p.id}, {len(CONTENT)} chars)")
