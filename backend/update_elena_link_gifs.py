import json
from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic
GIFS={
'Damon Salvatore':'https://media.tenor.com/W0xqbhSVKp0AAAAM/ian-somerhalder-damon-salvatore.gif',
'Stefan Salvatore':'https://media.tenor.com/wD9Tb8gIE1EAAAAM/stefan-salvatore.gif',
'Katherine Pierce':'https://media1.tenor.com/m/P_7oiEt8hx8AAAAC/katherine-pierce-gif.gif',
'Tatia Petrova':'https://media1.tenor.com/m/T4F8mWDK_o8AAAAC/tatia.gif',
'Bonnie Bennett':'https://media1.tenor.com/m/SgwzIqg9Z_QAAAAC/bonnie-bennett.gif',
'Jeremy Gilbert':'https://media1.tenor.com/m/4_q61C9YowAAAAAC/jeremy-gilbert-season-4-the-vampire-diaries.gif',
'Caroline Forbes':'https://media1.tenor.com/m/ID1okMHpppAAAAAC/caroline-forbes-candice-king.gif'}
NEW=[
('Bonnie Bennett — Meilleure amie, confiance profonde','Tu fais partie de ma vie depuis bien avant que le surnaturel ne bouleverse nos repères. Tu as tant donné pour ceux que tu aimes que je refuse de considérer ton aide comme un devoir. Je veux aussi être là pour toi, écouter tes projets et partager des moments où personne ne te demande de nous sauver. Le Nexus nous offre de nouveaux dangers, mais notre amitié mérite également des jours paisibles.'),
('Jeremy Gilbert — Petit frère, famille irremplaçable','Nous avons grandi ensemble et traversé des deuils qui ont changé notre famille. Mon premier réflexe reste de te protéger, parfois au point de trop décider pour toi. Pourtant, tu as ta propre vie et je dois respecter tes choix. Même lorsque nous ne sommes pas d’accord, je veux que tu saches que tu peux revenir vers moi. Notre lien ne se résume pas aux menaces que nous avons affrontées.'),
('Caroline Forbes — Meilleure amie, soutien et franchise','Notre amitié a grandi avec nous, entre confidences, désaccords et épreuves. Tu sais me secouer quand je m’enferme dans la culpabilité, et je connais la sensibilité derrière ton besoin de tout organiser. Notre nature vampirique nous permet de comprendre certaines difficultés sans vivre les choses de la même façon. Je veux préserver nos conversations, nos projets et ces moments simples qui nous rappellent pourquoi nous tenons l’une à l’autre.')]
def verify(item):
 name,url=item
 with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as response:
  assert response.read(6) in (b'GIF87a',b'GIF89a'),name
 return name
print('GIFs accessibles : '+', '.join(ThreadPoolExecutor(7).map(verify,GIFS.items())))
with transaction.atomic():
 t=Topic.objects.select_for_update().get(slug='elena-gilbert-salvatore',category__slug='scenarios-a-prendre')
 original=t.scenario_link_cards
 folder=Path(settings.BASE_DIR)/'data/scenario_backups';folder.mkdir(parents=True,exist_ok=True)
 (folder/('elena-links-'+timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')).write_text(json.dumps({'topic_id':t.pk,'scenario_link_cards':original},ensure_ascii=False),encoding='utf-8')
 cards=[dict(c) for c in original]
 for title,body in NEW:
  name=title.split(' — ')[0]
  if not any(c['title'].startswith(name) for c in cards):cards.append({'title':title,'text':body,'gif':''})
 for card in cards:
  for name,url in GIFS.items():
   if card['title'].startswith(name):card['gif']=url;break
 assert all(any(c['title'].startswith(name) and c['gif']==url for c in cards) for name,url in GIFS.items())
 for old in original:
  assert any(c['title']==old['title'] and c['text']==old['text'] for c in cards)
 t.scenario_link_cards=cards;t.save(update_fields=['scenario_link_cards'])
 t.refresh_from_db();assert t.scenario_link_cards==cards
 print('Elena : sept liens avec GIFs enregistrés ; textes existants conservés.')
