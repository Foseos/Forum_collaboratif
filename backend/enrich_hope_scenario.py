import json,re
from pathlib import Path
from html import escape
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic
from scenario_layout_helpers import CheckHTML, p, section
new=[
('Josie Saltzman — Amie, écoute réciproque','https://media1.tenor.com/m/bO6PajzKtcQAAAAC/josie-saltzman-kaylee-bryant.gif','Nous avons partagé un environnement où chacun essayait de comprendre sa place. Je veux entendre tes envies, pas seulement les solutions que tu trouves pour les autres. Notre amitié doit nous laisser à toutes les deux le droit d’avoir besoin d’aide.'),
('Lizzie Saltzman — De la friction à la confiance','https://media1.tenor.com/m/iQSHhVwHW_QAAAAC/jenny-boyd-lizzie-saltzman.gif','Nous savons nous provoquer et nous opposer. Cela ne nous empêche pas d’apprendre à compter l’une sur l’autre. Je souhaite construire notre lien présent sans prétendre que nos différences ou nos anciennes blessures ont disparu.'),
('Landon Kirby — Attachement et avenir ouvert','https://media.tenor.com/CJEvXyZPzIcAAAAM/landon-kirby-legacies.gif','Tu as compté dans ma façon d’imaginer une vie qui ne soit pas seulement une mission. Je veux que nos choix actuels nous appartiennent. Notre situation sentimentale et ton parcours dans le Nexus se définissent ensemble, sans retour amoureux imposé.'),
('Alaric Saltzman — Mentor, autonomie à respecter','https://media1.tenor.com/m/mrlGUC7RdMEAAAAC/alaric-saltzman-the-vampire-diaries.gif','Tu m’as aidée à apprendre et à préparer mes décisions. Je veux pouvoir bénéficier de ton expérience sans devenir un problème à contrôler ou la solution à chaque menace. La confiance doit aussi me laisser la possibilité de refuser.')]
def verify(row):
 with urlopen(Request(row[1],headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:assert r.read(6) in (b'GIF87a',b'GIF89a')
 return row[0]
print('GIFs vérifiés : '+', '.join(ThreadPoolExecutor(4).map(verify,new)))
with transaction.atomic():
 t=Topic.objects.select_for_update().get(slug='hope-mikaelson',category__slug='scenarios-a-prendre')
 post=t.posts.select_for_update().order_by('created_at','pk').first()
 old=post.content;original=t.scenario_link_cards
 assert 'data-hope-daily-life' not in old
 folder=Path(settings.BASE_DIR)/'data/scenario_backups';folder.mkdir(parents=True,exist_ok=True)
 (folder/('hope-enriched-'+timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')).write_text(json.dumps({'post_id':post.pk,'content':old,'topic_id':t.pk,'cards':original},ensure_ascii=False),encoding='utf-8')
 addition='<div data-hope-daily-life="1">'+section('VI. Une vie au-delà de l’héritage',p('Hope trouve dans le dessin et la peinture une manière de fixer ce qu’elle n’arrive pas toujours à raconter. Elle peut chercher un atelier, partager son travail ou garder certains carnets pour elle. Son art ne possède pas de fonction prophétique : il exprime son regard, ses souvenirs et ses envies.')+p('Au quotidien, elle alterne le besoin de solitude et l’envie de faire partie d’un groupe. La peur de perdre quelqu’un peut la pousser à cacher un danger ou à partir seule. Son évolution personnelle consiste à apprendre à prévenir, à écouter et à laisser les autres choisir leur place dans une épreuve.')+p('La présence de son père et de ses oncles dans cette continuité ne supprime pas les conflits familiaux. Hope peut aimer ses proches tout en refusant leurs méthodes. Son lien avec Hayley et les détails de leur histoire restent cohérents avec le scénario de sa mère ; aucun nouveau deuil n’est ajouté ici.')+p('Pistes de jeu : préparer une exposition avec un ami ; comparer un souvenir familial avec une archive ; demander conseil à Alaric sans lui confier toutes les décisions ; retrouver Josie et Lizzie dans un contexte ordinaire. Une intrigue peut commencer par un désir personnel, sans menace visant son sang.'))+'</div>'
 marker='<p class="scenario-credit-line"'
 assert marker in old
 content=old.replace(marker,addition+marker,1)
 cards=[dict(c) for c in original]
 for title,gif,body in new:
  name=title.split(' — ')[0]
  assert not any(c['title'].startswith(name) for c in cards)
  cards.append({'title':title,'gif':gif,'text':body})
 check=CheckHTML();check.feed(content);assert not check.stack
 assert cards[:len(original)]==original and content.replace(addition,'',1)==old
 post.content=content;post.save(update_fields=['content','is_edited','updated_at'])
 t.scenario_link_cards=cards;t.save(update_fields=['scenario_link_cards'])
 post.refresh_from_db();t.refresh_from_db();assert post.content==content and t.scenario_link_cards==cards
 print('Hope : quotidien et pistes de jeu approfondis ; dix liens avec GIFs ; fiche précédente conservée.')
