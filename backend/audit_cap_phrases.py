import re
from apps.forum.models import Topic
for t in Topic.objects.filter(category__slug='scenarios-a-prendre'):
 p=t.posts.order_by('created_at','pk').first()
 if not p:continue
 s=re.sub('<[^>]+>',' ',p.content)
 matches=[m.group(0) for m in re.finditer(r'.{0,55}(?:cinquième|aucun pouvoir supplémentaire|gratuitement|tous les pouvoirs|capacités naturelles|pas des pouvoirs supplémentaires).{0,110}',s,re.I)]
 if matches:print(t.slug, ' | '.join(matches))
