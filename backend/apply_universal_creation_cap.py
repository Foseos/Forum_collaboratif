import json,re
from pathlib import Path
from html import escape
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic,Post,SitePage
from scenario_layout_helpers import CheckHTML, p, section
RULE='''<section data-power-progression="creation-max-4" style="margin:1rem 0;padding:1rem;border:1px solid rgba(245,215,110,.35);border-radius:8px;line-height:1.8;"><h2 style="color:#f5d76e;font-size:1rem;">Création et progression des capacités</h2><p><strong>Tous les personnages commencent avec 4 capacités maximum au total.</strong> Cette limite s’applique à toutes les races, y compris les hybrides, tribrides et Originels. Les capacités sont réparties entre les héritages : aucun quota supplémentaire par nature.</p><p>Chaque effet surnaturel distinct, actif ou passif, compte dans cette limite. La force, la vitesse, la régénération, les sens accrus, une immunité ou la transformation sont des capacités distinctes. Un intitulé général ne permet pas de cumuler plusieurs dons. La nature, l’âge ou les exploits de la série ne débloquent rien automatiquement. Les humains ne reçoivent pas de pouvoirs magiques : leurs aptitudes restent humaines.</p><p><strong>Après la création, les capacités manquantes et les évolutions se débloquent en jeu avec des ARCANA FLOUZ.</strong> Un achat peut débloquer une nouvelle capacité cohérente avec le personnage ou améliorer une capacité acquise. Chaque capacité peut recevoir deux améliorations, dans l’ordre : base → évolution 1 → évolution 2. Une nouvelle capacité n’est pas une amélioration gratuite.</p><p>Le plafond de quatre concerne la création, pas le nombre total de capacités après des achats validés. L’ancien plafond global de huit achats ne s’applique plus. Aucun déblocage n’est automatique par ancienneté, changement de forme, rituel ou héritage.</p><p>Présentez à la boutique l’effet demandé, ses limites. Le staff valide, débite les Arcana Flouz et met à jour la fiche avant utilisation. Le barème existant est conservé : 300 Arcana Flouz pour le premier achat, puis 300 de plus par acquisition, déblocages et améliorations comptés ensemble. Les achats déjà validés restent acquis ; aucune capacité achetée n’est retirée par cette règle de création.</p></section>'''
NOTICE='''<section data-creation-cap="4" style="margin:1rem 0;padding:.8rem;border:1px solid #574477;border-radius:8px;"><h2 style="font-size:1rem;color:#c4b5fd;">Capacités à la création</h2><p>4 capacités maximum au total, actives et passives comprises, même pour les hybrides, tribrides et Originels. Les dons décrits dans l’histoire ou liés à l’espèce ne sont pas automatiquement disponibles. Seules les capacités retenues dans la fiche validée sont utilisables au départ. Les capacités manquantes et les améliorations s’achètent ensuite en jeu avec des Arcana Flouz, selon le règlement et la boutique. Un humain conserve des aptitudes humaines.</p></section>'''
base={
'force':('Force surnaturelle','Force accrue sur une action ciblée ; aucun avantage automatique de vitesse, de résistance ou de régénération.'),
'vitesse':('Vitesse surnaturelle','Accélération sur une courte distance dégagée ; ce don ne confère ni téléportation ni sens accrus.'),
'regeneration':('Régénération','Récupération accélérée de blessures ordinaires selon leur gravité et l’état du personnage ; ni résurrection ni guérison d’autrui.'),
'contrainte':('Contrainte mentale','Influence limitée selon la nature du personnage et les protections de la cible. Accord du joueur requis ; pas de lecture des pensées ni d’action sur les rêves incluse.'),
'transformation':('Transformation lupine','Transformation en loup avec effort et fatigue. Cette capacité ne débloque pas gratuitement force accrue, vitesse surnaturelle, venin, sens surnaturels ou immunités.'),
'kinesis':('Télékinésie','Déplace un petit objet visible à courte distance avec concentration ; aucun contrôle interne du corps d’autrui.'),
'bouclier':('Bouclier magique','Écran bref qui amortit un impact limité ; peut céder et ne protège pas toute une zone.'),
'perception':('Perception des enchantements','Au contact d’un objet, ressent une magie active sans identifier automatiquement son auteur ou sa formule.'),
'sceau':('Sceau d’alerte','Marque une ouverture et perçoit son franchissement à proximité, sans identifier, retenir ou blesser le passant.')}
sets={s:['force','vitesse','regeneration','contrainte'] for s in ['finn-mikaelson','kol-mikaelson','elijah-mikaelson','rebekah-mikaelson']}
sets.update({s:['transformation','force','vitesse','regeneration'] for s in ['tyler-lockwood','hayley-marshall']})
sets.update({'klaus-mikaelson':['transformation','force','regeneration','contrainte'],'hope-mikaelson':['transformation','regeneration','kinesis','bouclier'],'freya-mikaelson':['kinesis','bouclier','perception','sceau'],'esther-mikaelson':['kinesis','bouclier','perception','sceau']})
slugs=['reglement-officiel-du-forum','liste-des-pouvoirs-magiques','catalogue-boutique-magique','encyclopedie-des-creatures-et-races']
def rules(text):
 text=re.sub(r'<section\b[^>]*data-power-progression="[^"]+"[^>]*>.*?</section>',RULE,text,flags=re.S)
 if 'data-power-progression="creation-max-4"' not in text:text+=RULE
 text=text.replace('chaque personnage commence avec quatre pouvoirs de base. Chacun peut recevoir deux évolutions, achetées à la boutique et validées par le staff ; aucune évolution automatique par ancienneté.','quatre capacités maximum à la création, tous héritages confondus. Les capacités manquantes et les améliorations s’achètent en Arcana Flouz, avec validation du staff.')
 text=text.replace('accès aux dons de leurs héritages mais aussi à toutes leurs contraintes. Leur création et chaque évolution majeure nécessitent le staff.','quatre capacités maximum à la création, réparties entre leurs héritages, capacités actives et passives comprises. Les dons manquants s’achètent en Arcana Flouz et se valident avant utilisation.')
 text=text.replace('Chaque personnage commence avec quatre pouvoirs de base validés','Chaque personnage commence avec quatre capacités maximum validées')
 text=text.replace('Quatre pouvoirs au total','Quatre capacités maximum à la création').replace('quatre pouvoirs au total','quatre capacités maximum à la création')
 text=text.replace('Les quatre pouvoirs sont répartis entre les héritages','Les quatre capacités maximum de départ sont réparties entre les héritages')
 text=text.replace('ne permet pas de contourner les quatre dons validés','ne permet pas de contourner les capacités effectivement acquises et validées')
 return text
with transaction.atomic():
 targets=list(Topic.objects.select_for_update().filter(category__slug='scenarios-a-prendre'))+list(Topic.objects.select_for_update().filter(slug__in=slugs))
 assert set(slugs).issubset({t.slug for t in targets})
 backups=[];updates=[]
 for t in targets:
  post=t.posts.select_for_update().order_by('created_at','pk').first()
  if not post:continue
  old=post.content;content=old
  if t.slug in slugs:
   content=rules(content)
   if t.slug=='catalogue-boutique-magique':
    content=content.replace('Évolutions des quatre pouvoirs de base','Capacités supplémentaires et évolutions')
    content=content.replace('Améliorez vos quatre pouvoirs de base, deux fois chacun au maximum.','Débloquez une capacité manquante ou améliorez une capacité acquise, deux fois maximum par capacité.')
    content=content.replace('1re achat d’évolution','1er achat de capacité ou d’évolution').replace('achat d’évolution','achat de capacité ou d’évolution')
    content=content.replace('Première évolution achetée pour l’un des quatre pouvoirs de base.','Premier déblocage d’une capacité manquante ou première amélioration d’une capacité acquise.')
    content=content.replace('6e à 8e achats d’évolution — maximum','À partir du 6e achat de capacité ou d’évolution')
    content=content.replace('Chaque achat coûte 300 Arcana Flouz de plus que le précédent : 1 800, 2 100 puis 2 400 Arcana Flouz. Maximum : huit achats par personnage et deux évolutions par pouvoir.','Chaque acquisition coûte 300 Arcana Flouz de plus que la précédente : 1 800, 2 100, 2 400, puis 2 700, etc. Deux améliorations maximum par capacité ; les déblocages supplémentaires restent soumis à validation.')
  else:
   if t.slug in sets:
    sections=list(re.finditer(r'<section\b[^>]*>.*?</section>',content,re.S))
    selected=[m for m in sections if re.search(r'>II\. ',m.group(0))]
    assert len(selected)==1,t.slug
    body=p('Sélection de départ : quatre capacités distinctes au total, tous héritages confondus. Les autres capacités de l’espèce sont verrouillées jusqu’à leur acquisition en jeu avec des Arcana Flouz et validation du staff.')
    for key in sets[t.slug]:
     name,desc=base[key];body+='<div data-base-power="1"><h3 style="color:#f5d76e;font-size:1rem;">'+escape(name)+'</h3>'+p(desc)+'</div>'
    body+=p('La race, l’ancienneté et les faits de l’histoire ne procurent pas d’effet supplémentaire utilisable. Les vulnérabilités restent celles de la nature du personnage. Les compétences ordinaires ne permettent pas de reproduire un don surnaturel manquant.')
    m=selected[0];content=content[:m.start()]+section('II. Quatre capacités de départ',body)+content[m.end():]
    content=content.replace('Les capacités naturelles sont décrites sans évolutions à acheter dans cette fiche.','Les capacités non retenues à la création se débloquent en jeu avec des Arcana Flouz, après validation du staff.')
    check=CheckHTML();check.feed(content);assert not check.stack,t.slug
    assert content.count('data-base-power="1"')==4,t.slug
   if 'data-creation-cap="4"' not in content:content+=NOTICE
  if content!=old:
   backups.append({'model':'Post','pk':post.pk,'topic':t.slug,'content':old})
   assert re.findall(r'<img\b[^>]*>',old)==re.findall(r'<img\b[^>]*>',content),t.slug
   updates.append((post,content))
 page=SitePage.objects.select_for_update().get(slug='reglement-du-forum')
 if page.content.strip():backups.append({'model':'SitePage','pk':page.pk,'content':page.content});updates.append((page,rules(page.content)))
 folder=Path(settings.BASE_DIR)/'data/rules_backups';folder.mkdir(parents=True,exist_ok=True)
 (folder/('universal-cap-'+timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')).write_text(json.dumps(backups,ensure_ascii=False),encoding='utf-8')
 for obj,content in updates:
  obj.content=content
  obj.save(update_fields=['content','is_edited','updated_at'] if isinstance(obj,Post) else ['content','updated_at'])
  obj.refresh_from_db();assert obj.content==content
 print(str(len(updates))+' contenus harmonisés ; dix listes de capacités ramenées à quatre ; portraits et liens conservés.')
 for slug in slugs:
  content=Topic.objects.get(slug=slug).posts.order_by('created_at','pk').first().content
  assert 'data-power-progression="creation-max-4"' in content
  assert 'huit achats par personnage' not in content
  assert 'n’ajoute pas un cinquième' not in content
 for slug in sets:
  content=Topic.objects.get(slug=slug).posts.order_by('created_at','pk').first().content
  assert 'sans plafond de quatre' not in content and 'ne limite plus' not in content
 print('Règlement, boutique, grimoire et bottin vérifiés ; anciennes exceptions supprimées.')
