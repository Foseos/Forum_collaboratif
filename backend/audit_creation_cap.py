import re,json
from apps.forum.models import Topic,SitePage
for t in Topic.objects.filter(slug__in=['reglement-officiel-du-forum','liste-des-pouvoirs-magiques','catalogue-boutique-magique','encyclopedie-des-creatures-et-races']):
 p=t.posts.order_by('created_at','pk').first();s=re.sub('<[^>]+>',' ',p.content)
 print(t.slug)
 print('\n'.join(m.group(0) for m in re.finditer(r'.{0,130}(?:quatre|cinquième|huit|8 |300|600|maximum|hybride|Trybride).{0,220}',s,re.I)))
for t in Topic.objects.filter(category__slug='scenarios-a-prendre'):
 p=t.posts.order_by('created_at','pk').first();s=re.sub('<[^>]+>',' ',p.content)
 if any(x in s for x in ['sans plafond','ne limite plus','ensemble des capacités','Quatre dons de sorcellerie']):print('EXCEPTION',t.slug)
