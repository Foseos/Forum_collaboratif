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
    <h1 style="margin: 0 0 0.6rem; font-size: 2rem; font-weight: normal; font-style: italic; color: #f5d76e; letter-spacing: 0.04em; line-height: 1.2;">Henry<br>Mitchell</h1>
    <p style="margin: 0 0 1rem; font-size: 0.82rem; color: #a78bfa; font-style: italic; letter-spacing: 0.06em;">Humain · Le Bien · Époux de Paige Matthews</p>
    <p style="margin: 0; font-size: 0.75rem; color: #4b3a6b; font-style: italic; line-height: 1.7;">« Je ne peux pas orber, ni guérir, ni lancer de sortilège. Mais je peux être là — vraiment là — et ça, personne ne peut le faire à ma place. »</p>
  </td>
  <td style="vertical-align: top; width: 210px; text-align: center;">
    <img src="https://zupimages.net/up/26/11/5yif.jpg" alt="Henry Mitchell" style="width:200px;height:320px;object-fit:cover;border-radius:6px;border:2px solid rgba(124,58,237,0.35);display:block;margin:0 auto;">
    <p style="margin: 0.35rem 0 0; font-size: 0.6rem; color: #3d2d5e; font-style: italic;">Henry Mitchell — Ft Ivan Sergei</p>
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
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; width: 42%; border-bottom: 1px solid rgba(124,58,237,0.08);">Âge</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">53 ans</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Date de naissance</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">12 février 1973, San Francisco</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Sexe</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Masculin</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Orientation sexuelle</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Hétérosexuel</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Situation familiale</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Marié à Paige Matthews · Père de Tamora et Katlyn Mitchell · Père adoptif de Henry Jr Mitchell</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Race</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Humain</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0; border-bottom: 1px solid rgba(124,58,237,0.08);">Camp</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3; border-bottom: 1px solid rgba(124,58,237,0.08);">Le Bien</td></tr>
      <tr><td style="padding: 0.28rem 1rem 0.28rem 0; font-size: 0.74rem; color: #6d5fa0;">Métier</td><td style="padding: 0.28rem 0; font-size: 0.85rem; color: #e2d9f3;">Inspecteur de police · SFPD</td></tr>
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
      <li><strong style="color: #e2d9f3;">Aucun pouvoir magique</strong> — Henry Mitchell est pleinement humain. Sa force ne vient pas de la magie mais de ses années d'expérience, de son instinct de terrain et de sa capacité à garder la tête froide là où tout s'effondre.</li>
      <li><strong style="color: #e2d9f3;">Combat et tir</strong> — Inspecteur aguerri, formé aux techniques de combat rapproché et au maniement des armes. Dans un affrontement, il ne reste pas en retrait.</li>
      <li><strong style="color: #e2d9f3;">Connaissance du monde occulte</strong> — Des années aux côtés de Paige et de la famille Halliwell lui ont donné une connaissance pratique solide des démons, créatures et rituels magiques. Il ne peut pas lancer de sort, mais il sait reconnaître une menace.</li>
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

Courageux
Loyal
Ancré
Protecteur
Patient
Juste
Stable
Empathique

Défauts

Peut se sentir impuissant dans un monde magique qui le dépasse
Tendance à refouler ses inquiétudes pour ne pas alarmer les autres
Parfois trop protecteur, au point d'étouffer
Mal à l'aise avec ce qu'il ne peut pas contrôler</p>
  </div>
</div>

<!-- BOX IV : HISTOIRE -->
<div style="margin-bottom: 1.2rem; border: 1px solid rgba(124,58,237,0.28); border-radius: 7px; overflow: hidden;">
  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.3), rgba(109,40,217,0.08)); padding: 0.45rem 1rem; border-bottom: 1px solid rgba(124,58,237,0.25);">
    <h2 style="margin: 0; font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #a78bfa; font-weight: normal;">◈ IV. Mémoire des Âges · Histoire</h2>
  </div>
  <div style="padding: 1rem;">
    <p style="margin: 0; line-height: 1.9; color: #c4b5d4; text-align: justify; font-size: 0.9rem;"><strong style="color: #e2d9f3;">Origines — une vocation ordinaire</strong><br>
Henry Mitchell est né le 12 février 1973 à San Francisco, fils d'un ancien policier et d'une infirmière. Enfance modeste dans un quartier populaire, marquée par le sens du devoir et une foi tranquille dans la justice. À dix-huit ans, son choix était fait : il entrerait dans la police, comme son père avant lui. Sans éclat, sans grande déclaration. Parce que c'était ce qu'il savait faire et ce en quoi il croyait.<br><br>

Il gravit les échelons avec rigueur. Inspecteur au SFPD à vingt-six ans, il développa une réputation de calme sous pression et d'intuition sur le terrain. Des collègues fiables, des affaires résolues, une vie ordonnée. Il n'avait jamais entendu parler de démons.<br><br>

<strong style="color: #e2d9f3;">Paige Matthews — et tout ce qui vint avec elle</strong><br>
Paige entra dans sa vie comme elle entrait dans toutes les pièces : en prenant toute la place sans s'en rendre compte. Leur rencontre fut abrupte — une affaire sur laquelle leurs chemins professionnels se croisèrent. Henry fut frappé par son intelligence, son empathie et une énergie qu'il ne sut pas nommer tout de suite.<br><br>

La vérité sur sa nature lui fut révélée progressivement, et à sa façon caractéristique, Paige ne lui cacha rien longtemps. Sorcière. Mi-être de lumière. Charmed One. Henry encaissa tout cela avec le pragmatisme d'un homme habitué aux situations imprévisibles — même si quelques nuits sans sommeil furent nécessaires avant d'arriver à cette sérénité. Il ne recula pas. Il choisit Paige, et avec elle, tout l'univers qui l'accompagnait.<br><br>

Ils se marièrent. Henry apprit à reconnaître les signes d'une attaque démoniaque, à ne pas paniquer quand Paige orbait hors de sa portée, à garder son arme chargée et son sang-froid intact dans des situations que l'académie de police n'avait pas prévues.<br><br>

<strong style="color: #e2d9f3;">Tamora, Katlyn — et la surprise d'être père de sorcières</strong><br>
Le 22 juillet 2007, Tamora et Katlyn vinrent au monde. Jumelles — l'une brûlante et frondeuse, l'autre douce et silencieuse. Henry ne fut pas surpris que ses filles héritent de la magie de Paige. Il fut surtout frappé par la violence du monde qui s'intéresserait à elles dès leur premier souffle.<br><br>

Avec Tamora, la relation fut et reste orageuse. Elle n'accepte ni l'autorité ni les limites qu'on lui fixe — et elle a hérité de l'entêtement de sa mère en version amplifiée. Henry se bat souvent contre l'envie de la protéger d'elle-même. Il n'y réussit pas toujours. Mais il est là, systématiquement, à chaque fois qu'elle en a besoin sans le dire.<br><br>

Avec Katlyn, tout est plus silencieux. Elle se confie à ses parents là où sa sœur explose. Henry reconnaît en elle une sensibilité qu'il faut protéger sans étouffer. Elle arrondit les angles que Tamora crée — et il sait que ce rôle lui coûte plus qu'elle ne le montre.<br><br>

<strong style="color: #e2d9f3;">Henry Jr — le fils du cœur</strong><br>
Quelques semaines après la naissance des jumelles, Paige et Henry apprirent l'existence d'un nouveau-né dont la mère, une adolescente, venait d'être tuée par un démon. Sans hésitation, ils ouvrirent leur foyer. Henry Jr fut adopté en septembre 2007.<br><br>

Ce fils-là est humain, comme lui. Sans pouvoirs, dans une famille où tout le monde en a. Henry veilla à ce que cette différence ne soit jamais une blessure. Il grandit à ses côtés en lui montrant que la valeur d'un homme n'a rien à voir avec sa capacité à orber ou à lancer des sortilèges. Le fait que sa mère biologique ait elle-même été adoptée fut évoqué ouvertement, avec la transparence que Paige avait toujours défendue. Henry Jr grandit en se sentant légitime — et c'est la plus grande réussite de son père.<br><br>

<strong style="color: #e2d9f3;">Aujourd'hui — l'ancre</strong><br>
Henry Mitchell a cinquante-trois ans. Il est toujours inspecteur au SFPD, travaillant désormais sur des affaires qui croisent parfois le monde occulte — ce que ses supérieurs ne savent pas, et ce qu'il gère avec une discrétion rodée par des années de pratique.<br><br>

Dans une famille où ses enfants peuvent disparaître en orbes et où sa femme peut téléporter n'importe quel objet dans ses mains, Henry reste ce que peu savent être : l'ancre. L'homme qui fait le café le matin, qui vérifie les devoirs, qui conduit aux urgences quand la magie ne suffit pas, qui serre Paige dans ses bras quand le monde magique a été trop lourd ce soir-là. Ni sorcier, ni être de lumière. Juste Henry — et c'est exactement ce dont cette famille a besoin.</p>
  </div>
</div>

</div>"""

t = Topic.objects.filter(slug='henry-mitchell').first()
if not t:
    print("ERROR: topic 'henry-mitchell' not found")
    exit(1)

p = Post.objects.filter(topic=t).first()
if not p:
    print("ERROR: no post found")
    exit(1)

p.content = CONTENT
p.save()
print(f"OK — fiche Henry Mitchell saved (post id={p.id}, {len(CONTENT)} chars)")
