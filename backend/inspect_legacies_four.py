from apps.forum.models import Topic
import re
for t in Topic.objects.filter(slug__in=['landon-kirby','milton-greasley','caleb-hawkins','rafael-waithe']):
 print(t.slug,t.scenario_link_cards,t.posts.order_by('created_at','pk').first().content[-1150:])
source=open('find_elena_gifs.py').read()
source=re.sub(r'names=\[.*?\]',"names=['rafael-waithe','kaleb-hawkins','milton-greasley']",source,count=1)
exec(source)
