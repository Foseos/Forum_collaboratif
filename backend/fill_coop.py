import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
sys.path.insert(0, '/app')
django.setup()

from apps.forum.models import Post, Topic

CONTENT = """<div style="font-family: Georgia, 'Times New Roman', serif; background: #0d0a1a; color: #e2d9f3; padding: 2rem; border-radius: 10px; border: 1px solid rgba(124,58,237,0.3); max-width: 720px; margin: 0 auto;">

<!-- EN-TÊTE -->
<table style="width: 100%; border-collapse: collapse; margin-bottom: 1.75rem; padding-bottom: 1.5rem; border-bottom: 1px solid rgba(124,58,237,0.2);">
<tr>
  <td style="vertical-align: top; padding-right: 1.5rem;">
    <p style="margin: 0 0 0.5rem; font-size: 0.58rem; letter-spacing: 0.38em; text-transform: uppercase; color: #6d28d9;">✦ Nexus Arcana · Livre des Ombres ✦</p>
    <h1 style="margin: 0 0 0.6rem; font-size: 2rem; font-weight: normal; font-style: italic; color: #f5d76e; letter-spacing: 0.04em; line-height: 1.2;">Coop<br>Everhart</h1>
    <p style="margin: 0 0 1rem; font-size: 0.82rem; color: #a78bfa; font-style: italic; letter-spacing: 0.06em;">Cupidon · Le Bien · Père de P.J., Parker et Peyton</p>
    <p style="margin: 0; font-size: 0.75rem; color: #4b3a6b; font-style: italic; line-height: 1.7;">« L'amour, c'est ma nature. Ma mission, mon sang, ma raison d'être. Alors même quand il fait mal — surtout quand il fait mal — je sais qu'il est réel. »</p>
  </td>
  <td style="vertical-align: top; width: 210px; text-align: center;">
    <img src="https://zupimages.net/up/26/11/ia6b.jpg" alt="Coop Everhart" style="width:200px;height:320px;object-fit:cover;border-radius:6px;border:2px solid rgba(124,58,237,0.35);display:block;margin:0 auto;">
    <p style="margin: 0.35rem 0 0; font-size: 0.6rem; color: #3d2d5e; font-style: italic;">Coop Everhart — Ft Victor Webster</p>
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
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; width: 42%; border-bottom: 1px solid rgba(124,58,237,0.08);">Âge</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Éternel · apparence d'un homme d'une quarantaine d'années</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Sexe</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Masculin</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Orientation sexuelle</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Hétérosexuel</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Situation familiale</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Divorcé de Phoebe Halliwell · Père de Prudence Johanna, Parker et Peyton Halliwell</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Race</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Cupidon</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Camp</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Le Bien</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0;">Métier</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3;">Cupidon actif · guide les âmes vers l'amour qui leur est destiné</td></tr>
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
    <ul style="margin: 0; padding-left: 1.3rem; line-height: 1.85; font-size: 0.87rem; color: #c4b5d4;">
      <li><strong style="color: #e2d9f3;">Anneau de Cupidon</strong> — Artefact magique propre à sa nature, l'anneau amplifie et canalise les émotions amoureuses. Il peut l'utiliser pour projeter de la chaleur, de la confiance ou de la paix dans l'âme d'un être en souffrance. Ne crée pas l'amour là où il n'existe pas — il révèle ce qui était déjà là.</li>
      <li><strong style="color: #e2d9f3;">Empathie émotionnelle</strong> — Coop perçoit avec une précision rare l'état émotionnel de ceux qui l'entourent, en particulier les sentiments liés à l'amour, au deuil ou à la peur de s'attacher. Ce don le rend difficile à tromper sur les intentions.</li>
      <li><strong style="color: #e2d9f3;">Localisation des âmes sœurs</strong> — Capacité à identifier les liens d'amour destinés entre deux personnes, même quand elles-mêmes ne les voient pas encore. Il ne les force pas à se rencontrer — il crée les conditions pour que cela arrive naturellement.</li>
      <li><strong style="color: #e2d9f3;">Téléportation (Flash)</strong> — Déplacement instantané propre aux Cupidons, discret et silencieux. Se manifeste par un éclat de lumière dorée.</li>
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

Chaleureux
Optimiste
Empathique
Patient
Bienveillant
Loyal envers ses filles
Idéaliste
Doux

Défauts

Trop idéaliste — donne parfois des leçons sans s'en rendre compte
Évite les confrontations difficiles
A du mal à accepter qu'il ne peut pas tout arranger par l'amour
Garde pour lui sa propre douleur
Peut paraître naïf face à la complexité du monde</p>
  </div>
</div>

<!-- BOX IV : HISTOIRE -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ IV. Mémoire des Âges · Histoire</h2>
  </div>
  <div style="padding: 1rem;">
    <p style="margin: 0; line-height: 1.9; color: #c4b5d4; text-align: justify; font-size: 0.9rem;"><strong style="color: #e2d9f3;">Un Cupidon parmi les hommes — des siècles de missions</strong><br>
Coop Everhart existe depuis plus longtemps qu'il ne sait l'expliquer. Les Cupidons ne naissent pas — ils émergent, façonnés par l'énergie de l'amour lui-même, porteurs d'une mission aussi ancienne que l'humanité : guider les âmes vers ce qui leur est destiné. Pendant des siècles, Coop accomplit cette mission avec la sérénité d'un être qui ne doute pas de sa nature. Il observait, guidait, disparaissait. Il ne s'attachait jamais. Ce n'était pas dans sa nature — ou du moins, c'est ce qu'il croyait.<br><br>

<strong style="color: #e2d9f3;">Phoebe Halliwell — l'assignation impossible</strong><br>
Les Anciens lui confièrent une mission particulière : Phoebe Halliwell, Charmed One, sorcière de la lignée Halliwell, avait vécu un amour dévastateur et n'arrivait plus à croire qu'un autre était possible. Sa mission — lui redonner confiance en l'amour, l'aider à s'ouvrir à quelqu'un de nouveau.<br><br>

Ce qu'il n'avait pas prévu, c'est que cet être radieux, entêté et profondément vivant allait le toucher comme aucune de ses assignées ne l'avait jamais fait. Coop tomba amoureux de Phoebe Halliwell. Pour un Cupidon, c'était une aberration — la règle fondamentale interdisait de ressentir soi-même ce qu'on était chargé d'offrir aux autres. Pourtant, les Anciens reconnurent quelque chose d'inévitable dans ce lien. Ils laissèrent faire.<br><br>

Coop et Phoebe se marièrent. Ce fut une période lumineuse — construite sur une tendresse réelle, une admiration mutuelle et la conviction partagée que l'amour pouvait se reconstruire sur les ruines de l'ancien.<br><br>

<strong style="color: #e2d9f3;">Prudence Johanna, Parker, Peyton</strong><br>
Prudence Johanna naquit en 2007. Petite fille sérieuse, déjà attentive aux émotions de ceux qui l'entouraient — héritière manifeste de la double nature de Phoebe et de Coop. Parker vint deux ans plus tard, explosive et frondeuse dès le premier jour. Peyton enfin, la plus jeune, silencieuse et profonde comme une eau tranquille.<br><br>

Trois filles, trois tempéraments radicalement différents, une même double nature mi-sorcière mi-cupidon. Coop s'attacha à chacune d'une façon particulière : avec P.J., une complicité intellectuelle et émotionnelle, une même vision idéaliste du monde. Avec Parker, une relation plus houleuse — elle refusait ses leçons, ses certitudes, son optimisme qu'elle trouvait trop facile. Avec Peyton, un lien presque silencieux : il avait le don de comprendre ce qu'elle ressentait sans qu'elle ait à parler, et elle le lui rendait en lui accordant une confiance que peu obtenaient.<br><br>

<strong style="color: #e2d9f3;">Le divorce — 2014</strong><br>
En 2014, Phoebe lui demanda le divorce. Coop ne fut pas surpris — il était Cupidon, il savait lire les âmes, et il avait senti depuis un moment que quelque chose en elle cherchait autre chose. Il aurait pu lutter. Il choisit de ne pas le faire. Parce qu'il aimait Phoebe assez pour ne pas la retenir contre sa propre vérité.<br><br>

Ce qu'il apprit ensuite — qu'elle retrouvait Cole Turner, l'homme qui l'avait précédée et marquée avant lui — fut douloureux d'une façon particulière. Pas par jalousie. Par la conscience aiguë d'avoir été, peut-être, une étape dans une histoire dont il n'était pas le chapitre final. Il porta cette douleur seul, comme il portait tout ce qui l'atteignait vraiment.<br><br>

<strong style="color: #e2d9f3;">Père avant tout — aujourd'hui</strong><br>
Le divorce ne changea pas ce qui comptait le plus : il reste le père de ses trois filles, et ce rôle, personne ne peut le lui reprendre. Il partage leur éducation avec Phoebe, avec une dignité que même Parker, pourtant prompte à tout critiquer, reconnaît en silence.<br><br>

Sa relation avec P.J. est douce et forte — elle partage sa vision de l'amour comme force constructive, et il la voit avancer dans la vie avec une fierté tranquille. Avec Parker, les accrochages continuent : elle le trouve trop idéaliste, il la trouve trop prompte à tout brûler. Mais sous les tensions, il y a un amour solide que ni l'un ni l'autre ne remettra jamais vraiment en question. Avec Peyton, il n'a pas besoin de beaucoup de mots — ils se comprennent dans le silence, et c'est suffisant.<br><br>

Cole Turner est désormais le beau-père de ses filles. Coop l'accepte, non sans effort, mais avec la lucidité d'un être dont la nature entière est tournée vers l'amour — et qui sait, mieux que quiconque, qu'on ne choisit pas qui on aime vraiment.<br><br>

Coop continue d'exercer son rôle de Cupidon. Il guide des âmes, organise des rencontres, révèle des liens. Et parfois, en observant deux êtres qui se trouvent enfin, il pense à Phoebe. Non avec amertume — avec la certitude tranquille que leur histoire, même incomplète, a produit les trois plus belles choses de son existence.</p>
  </div>
</div>

</div>"""

t = Topic.objects.filter(slug='coop-everhart').first()
if not t:
    print("ERROR: topic 'coop-everhart' not found")
    exit(1)

p = Post.objects.filter(topic=t).first()
if not p:
    print("ERROR: no post found")
    exit(1)

p.content = CONTENT
p.save()
print(f"OK — fiche Coop Everhart saved (post id={p.id}, {len(CONTENT)} chars)")
