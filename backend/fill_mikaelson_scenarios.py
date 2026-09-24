import ast,json,re
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic
module=ast.parse(Path('fill_dior_kaya.py').read_text(encoding='utf-8-sig'))
exec(compile(ast.Module(body=[n for n in module.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in ('p','section','CheckHTML')],type_ignores=[]),'layout','exec'))
DATA=json.loads(Path('mikaelson_data.json').read_text(encoding='utf-8-sig'))
GIFS={
'Klaus Mikaelson':'https://media.tenor.com/ZfPfiXgwQ1cAAAAM/niklaus-mikaelson-klaus.gif',
'Elijah Mikaelson':'https://media1.tenor.com/m/ukDD2pxS79kAAAAC/elijah-mikaelson-elijah.gif',
'Rebekah Mikaelson':'https://media1.tenor.com/m/VJYt5eapyBkAAAAC/rebekah-mikaelson-claire-holt.gif',
'Kol Mikaelson':'https://media1.tenor.com/m/TCAwaz1f1G0AAAAC/tvd-kol.gif',
'Finn Mikaelson':'https://media1.tenor.com/m/bJsWNU7W_MsAAAAC/finn-mikaelson-caspar-zafer.gif',
'Freya Mikaelson':'https://media1.tenor.com/m/ku_48xedFR8AAAAC/freya-mikaelson-riley-voelkel.gif',
'Esther Mikaelson':'https://media1.tenor.com/m/z7g_bQPyZEMAAAAC/esther-mikaelson-tvd.gif',
'Hope Mikaelson':'https://media1.tenor.com/m/flkkkhUPqKMAAAAC/hope-mikaelson4x16-tribrid-hope.gif',
'Tatia Petrova':'https://media1.tenor.com/m/T4F8mWDK_o8AAAAC/tatia.gif',
'Hayley Marshall':'https://media1.tenor.com/m/Yh-tjSCKpIkAAAAC/the-originals-hayley-marshall.gif',
'Marcel Gerard':'https://media1.tenor.com/m/qJH9L-7jazoAAAAC/marcel-gerard-legacies.gif',
'Davina Claire':'https://media1.tenor.com/m/UG48bExm7IQAAAAC/the-originals-danielle-campbell.gif',
'Keelin':'https://media.tenor.com/iQc2cvbBhEkAAAAM/the-originals-keelin-smile.gif'}
extras={
'klaus-mikaelson':[('Hayley Marshall','Mère de Hope','Nous partageons une responsabilité envers notre fille. Je dois respecter ta place et tes choix sans confondre protection et autorité sur toi.'),('Marcel Gerard','Fils de cœur, rival','Je t’ai aimé comme un fils et trop souvent traité comme un rival. Notre histoire commune ne me donne aucun droit de gouverner ta vie.')],
'elijah-mikaelson':[('Hayley Marshall','Attachement profond','Tu comptes pour moi au-delà des devoirs de notre famille. Notre relation présente doit se définir ensemble, sans faire de mes sentiments une obligation pour toi.')],
'rebekah-mikaelson':[('Marcel Gerard','Amour et liberté','Je veux que notre lien puisse exister hors des rivalités de ma famille. Nos projets et notre engagement actuel se construisent ensemble, sans nouvelle décision prise à notre place.')],
'kol-mikaelson':[('Davina Claire','Amour choisi','Tu as pris une place essentielle dans ma vie. Je veux être à tes côtés sans te demander de réparer mes fautes ni de choisir systématiquement contre ma famille.')],
'freya-mikaelson':[('Keelin','Épouse','Notre foyer et notre fils méritent ma présence. Je veux te montrer que notre vie est une priorité, même lorsque mes frères et sœurs appellent à l’aide.')],
'hope-mikaelson':[('Hayley Marshall','Mère','Tu m’as appris que je pouvais être forte sans renoncer à ma sensibilité. Ta place dans ma vie reste essentielle ; les détails de nos retrouvailles suivent ta propre histoire dans le Nexus.')]
}
for d in DATA:d['links'].extend(extras.get(d['slug'],[]))
def verify(name):
 with urlopen(Request(GIFS[name],headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:assert r.read(6) in (b'GIF87a',b'GIF89a'),name
 return name
print('GIFs vérifiés : '+', '.join(ThreadPoolExecutor(8).map(verify,GIFS)))
def abilities(d):
 parts=[]
 if d['kind'] in ('original','hybrid','tribrid'):
  parts+=[('Capacités vampiriques','Force, vitesse, réflexes, endurance, sens accrus, régénération et longévité surnaturelle. Le sang peut guérir un humain et permettre une transition selon les règles du jeu. Les émotions sont amplifiées ; l’influence sur les rêves et la contrainte nécessitent l’accord des joueurs concernés.'),('Contrainte et statut','Les Originels peuvent contraindre des humains et des vampires ordinaires, sans contrôle automatique des autres Originels ou des sorcières. Pour Hope, la portée de la contrainte suit celle des vampires ordinaires. La verveine protège des effets concernés.'),('Résistance et limites','Les capacités naturelles de l’espèce sont présentes, sans plafond de quatre pour cet héritage. Elles ne garantissent aucune victoire. La magie peut neutraliser ou affaiblir ; la faim demeure et toute blessure grave ou transformation d’un personnage se joue de manière concertée.')]
  if d['kind']=='original':parts.append(('Vulnérabilités des Originels','Le soleil reste douloureux et nécessite une protection pour circuler confortablement. Le chêne blanc peut tuer un Originel ; certaines dagues enchantées peuvent le neutraliser. La verveine et le venin lupin peuvent l’affaiblir. Les pouvoirs de sorcière perdus lors de la transformation ne sont pas conservés.'))
 if d['kind'] in ('hybrid','tribrid'):
  parts+=[('Héritage lupin','Transformation complète ou partielle, instincts de chasse, pistage et morsure venimeuse. La transformation n’est plus imposée par la pleine lune. L’hybridité permet de vivre au soleil et de résister au venin lupin ordinaire.'),('Sang et hybridité','Le sang de Klaus et de Hope peut guérir le venin lupin ordinaire et intervenir dans la création d’hybrides, selon les conditions propres à chacun. Cela ne permet pas de créer librement une armée : une transformation et ses conséquences nécessitent une intrigue validée.')]
  parts.append(('Faiblesse particulière','Le chêne blanc demeure une menace mortelle pour Klaus.' if d['kind']=='hybrid' else 'Le chêne rouge constitue une menace propre à Hope pleinement activée. Sa singularité ne la protège pas de toute magie et ne lui donne aucun savoir universel.'))
 if d['kind'] in ('witch','tribrid'):
  parts.append(('Quatre dons de sorcellerie au départ','Télékinésie : déplacer un objet visible avec effort. Bouclier : amortir brièvement une attaque, sans protection absolue. Perception des enchantements : ressentir une magie active sur un objet sans en connaître tous les secrets. Sceau d’alerte : percevoir le franchissement d’une ouverture marquée à proximité, sans identifier ni retenir la personne.'))
  parts.append(('Savoir rituel','Les connaissances historiques servent à rechercher, préparer et comprendre. Elles ne donnent pas tous les sorts gratuitement. Les grands rituels, retours à la vie, transferts de corps et changements de nature demandent une intrigue concertée. Aucun lien à Dahlia ou aux ancêtres ne fournit une réserve illimitée.'))
 return ''.join('<h3 style="color:#f5d76e;font-size:1rem;">'+escape(a)+'</h3>'+p(b) for a,b in parts)
with transaction.atomic():
 topics={t.slug:t for t in Topic.objects.select_for_update().filter(slug__in=[d['slug'] for d in DATA],category__slug='scenarios-a-prendre')}
 assert len(topics)==8
 posts={s:t.posts.select_for_update().order_by('created_at','pk').first() for s,t in topics.items()}
 for s,t in topics.items():assert 'Nom du pouvoir' in posts[s].content and not t.scenario_link_cards,'Fiche modifiée : '+s
 folder=Path(settings.BASE_DIR)/'data/scenario_backups';folder.mkdir(parents=True,exist_ok=True)
 (folder/('mikaelson-'+timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')).write_text(json.dumps([{'topic_id':t.pk,'post_id':posts[s].pk,'content':posts[s].content,'cards':t.scenario_link_cards} for s,t in topics.items()],ensure_ascii=False),encoding='utf-8')
 for d in DATA:
  t=topics[d['slug']];post=posts[d['slug']];old=post.content
  img=re.search(r'<img\b[^>]*src="([^"]+)"',old).group(1)
  caption=re.search(r'<p\b[^>]*>([^<]*\bFt [^<]*)</p>',old,re.I).group(1)
  credit=re.search(r'<p class="scenario-credit-line"[^>]*>.*?(?:</p>|$)',old,re.S).group(0).rstrip()
  if not credit.endswith('</p>'):credit+='</p>'
  content='<div data-mikaelson-scenario="1" style="font-family:Georgia,serif;background:#0d0a1a;color:#e2d9f3;padding:clamp(1rem,4vw,2rem);border-radius:10px;max-width:800px;margin:auto;">'+p('✦ Nexus Arcana · Livre des Ombres ✦')+'<div style="display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;"><div style="flex:1;min-width:180px;"><h1 style="color:#f5d76e;">'+escape(d['name'])+'</h1>'+p(d['race']+' · Neutre')+p('« '+d['quote']+' »')+'</div><figure style="margin:0;max-width:100%;"><img src="'+escape(img,quote=True)+'" alt="'+escape(d['name'])+'" style="width:200px;max-width:100%;height:320px;object-fit:cover;border-radius:8px;"><figcaption style="max-width:200px;font-size:.75rem;">'+caption+'</figcaption></figure></div>'
  fields=[('Âge',d['age']),('Origines',d['origin']),('Sexe',d['sex']),('Nature',d['race']),('Camp','Neutre'),('Famille',d['family']),('Activité',d['job']),('Orientation sexuelle','Au choix du joueur, en cohérence avec les relations conservées')]
  content+=section('I. Identité','<dl>'+''.join('<dt style="color:#a78bfa;margin-top:.6rem;">'+escape(a)+'</dt><dd style="margin:.2rem 0;">'+escape(b)+'</dd>' for a,b in fields)+'</dl>')
  content+=section('II. Nature et capacités',abilities(d))+section('III. Âme et caractère',''.join(p(x) for x in d['character']))
  content+=section('IV. Mémoire des âges · Histoire',''.join('<h3 style="color:#f5d76e;font-size:1rem;">'+escape(a)+'</h3>'+p(b) for a,b in d['history']))
  content+=section('V. Repères pour le jeu',p('Continuité Nexus Arcana : Klaus et Elijah sont vivants ; Finn et Esther sont revenus grâce à la Convergence. Ces retours ne constituent pas des pouvoirs reproductibles. Hope est pleinement tribride. Les proches conservent leur libre choix : le nom Mikaelson ne crée ni obéissance ni pardon automatique. Les métiers proposés et les détails des relations se personnalisent avec les joueurs concernés.'))+credit+'</div>'
  check=CheckHTML();check.feed(content);assert not check.stack
  assert 'Montana' not in content and 'Nom du pouvoir' not in content
  cards=[{'title':label if label.startswith(name+' — ') else name+' — '+label,'gif':GIFS[name],'text':body} for name,label,body in d['links']]
  post.content=content;post.save(update_fields=['content','is_edited','updated_at'])
  t.scenario_link_cards=cards;t.save(update_fields=['scenario_link_cards'])
  post.refresh_from_db();t.refresh_from_db();assert post.content==content and t.scenario_link_cards==cards
  print(d['name']+' : fiche complète, '+str(len(cards))+' liens avec GIFs, portrait/crédit conservés et balisage vérifié.')
