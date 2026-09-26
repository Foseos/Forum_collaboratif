import json
from pathlib import Path
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic
slugs=['scott-mccall','allison-argent','stiles-stilinski','lydia-martin']
with transaction.atomic():
 topics=list(Topic.objects.select_for_update().filter(slug__in=slugs))
 assert len(topics)==4
 posts=[t.posts.select_for_update().order_by('created_at','pk').first() for t in topics]
 folder=Path('data/scenario_backups');folder.mkdir(parents=True,exist_ok=True)
 (folder/('teenwolf-2033-'+timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')).write_text(json.dumps([{'topic_id':t.pk,'post_id':p.pk,'content':p.content} for t,p in zip(topics,posts)],ensure_ascii=False),encoding='utf-8')
 for t,p in zip(topics,posts):
  content=p.content
  assert 'data-teenwolf-four-scenario' in content
  content=content.replace('Adulte · âge précis à accorder à la chronologie du forum','Adulte en 2033 · âge précis à fixer selon la chronologie personnelle retenue dans cette adaptation')
  content=content.replace('Adulte · âge apparent et temps écoulé à accorder à son retour','Adulte en 2033 · âge apparent distinct des années écoulées depuis sa mort ; à préciser selon la date de son retour')
  content=content.replace('Continuité Nexus Arcana : Scott est','Année actuelle du forum : 2033. Les événements de Beacon Hills appartiennent au passé ; les retrouvailles et les projets à San Francisco se jouent en 2033. La Convergence ne rajeunit pas automatiquement les personnages. Continuité Nexus Arcana : Scott est')
  assert content!=p.content
  p.content=content;p.save(update_fields=['content','is_edited','updated_at'])
  p.refresh_from_db();assert p.content==content
  print(t.title+' : repère 2033 enregistré, liens et portrait conservés.')
