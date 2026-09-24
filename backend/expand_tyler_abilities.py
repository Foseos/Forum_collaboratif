import ast,json,re
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic
module=ast.parse(Path('fill_dior_kaya.py').read_text(encoding='utf-8-sig'))
exec(compile(ast.Module(body=[n for n in module.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in ('p','section','CheckHTML')],type_ignores=[]),'layout','exec'))
groups=[('Capacités physiques communes',[
('Force, vitesse, agilité et réflexes surnaturels','Son hybridité renforce ses capacités physiques. Leur efficacité dépend de son état et de l’adversaire ; aucune victoire n’est automatique.'),
('Sens et pistage','Ouïe, odorat et vision accrus lui permettent de suivre des traces et de percevoir des détails qui échappent aux humains.'),
('Endurance et régénération','Résiste à des efforts importants et guérit rapidement de nombreuses blessures. Il peut cependant être affaibli, neutralisé ou tué.'),
('Longévité vampirique','Son corps ne vieillit plus normalement. Cette longévité ne constitue pas une invulnérabilité.')]),
('Héritage du loup-garou',[
('Transformation complète ou partielle','Peut prendre sa forme lupine ou manifester certains traits du loup, notamment les crocs et les yeux. Sa condition d’hybride lui permet de choisir ses transformations sans subir l’obligation de la pleine lune.'),
('Morsure venimeuse','Sa morsure peut empoisonner les vampires, y compris lorsqu’il conserve une apparence humaine. Les conséquences graves se jouent avec l’accord du joueur concerné.'),
('Instincts et colère','Ses instincts de chasse et de défense sont amplifiés. La colère peut renforcer ses réactions, mais compromettre son jugement.')]),
('Héritage du vampire',[
('Contrainte mentale','Peut influencer un humain non protégé et modifier ses souvenirs par contact visuel. La verveine protège de cet effet. Toute utilisation sur un personnage joué nécessite l’accord de son joueur.'),
('Influence sur les rêves','Peut agir sur les rêves dans le cadre des capacités vampiriques, avec proximité et accord du joueur concerné ; ce n’est pas une lecture libre de toutes les pensées.'),
('Sang guérisseur et transition','Son sang peut soigner des blessures humaines et permettre une transition vampirique si une personne meurt avec ce sang dans son organisme. Toute transformation se prépare avec le joueur et le staff.'),
('Émotions amplifiées et humanité','Ressent les émotions avec une intensité accrue et possède la faculté vampirique de couper son humanité. Une telle intrigue conserve les conséquences de ses actes.')]),
('Particularités de son hybridité',[
('Résistance au soleil et au venin lupin','Peut vivre au soleil sans bague de jour et résiste au venin ordinaire des loups-garous.'),
('Liberté retrouvée','Son ancien lien d’asservissement à Klaus est rompu. Il conserve les capacités de ses deux natures.')])]
body=p('Tyler possède l’ensemble des capacités naturelles d’un loup-garou et d’un vampire non originel. Cette fiche ne limite plus son héritage à quatre pouvoirs. Aucun achat d’évolution n’est nécessaire pour disposer de ces capacités de nature.')
for heading,abilities in groups:
 body+='<h3 style="color:#f5d76e;font-size:1.05rem;">'+escape(heading)+'</h3>'
 body+=''.join(p('<strong>'+escape(name)+'</strong> — '+escape(desc)) for name,desc in abilities)
body+=p('Limites : Tyler reste un hybride non originel. Il ne possède ni l’immortalité d’un Originel, ni le sang antidote de Klaus, ni sa capacité à créer des hybrides. La verveine, l’aconit, la magie et les blessures destructrices restent dangereux. La faim de sang et les règles d’invitation demeurent ; la décapitation ou l’arrachement du cœur peuvent le tuer.')
# p() accepts HTML in this established layout helper.
with transaction.atomic():
 t=Topic.objects.select_for_update().get(slug='tyler-lockwood',category__slug='scenarios-a-prendre')
 post=t.posts.select_for_update().order_by('created_at','pk').first()
 original=post.content
 matches=list(re.finditer(r'<section\b[^>]*>.*?</section>',original,re.S))
 target=[m for m in matches if 'II. Quatre pouvoirs de base</h2>' in m.group(0)]
 assert len(target)==1
 folder=Path(settings.BASE_DIR)/'data/scenario_backups';folder.mkdir(parents=True,exist_ok=True)
 (folder/('tyler-full-abilities-'+timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')).write_text(json.dumps({'post_id':post.pk,'content':original},ensure_ascii=False),encoding='utf-8')
 m=target[0]
 content=original[:m.start()]+section('II. Capacités de loup-garou et de vampire',body)+original[m.end():]
 check=CheckHTML();check.feed(content);assert not check.stack
 assert 'Quatre pouvoirs au total' not in content
 assert re.findall(r'<img\b[^>]*>',content)==re.findall(r'<img\b[^>]*>',original)
 post.content=content;post.save(update_fields=['content','is_edited','updated_at'])
 post.refresh_from_db();assert post.content==content
 print('Tyler : capacités complètes enregistrées ; portrait, crédits, histoire et liens conservés ; balisage vérifié.')
