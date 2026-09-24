from apps.forum.models import Topic
import re
print(list(Topic.objects.filter(category__slug='scenarios-a-prendre').values_list('slug','title')))
source=open('find_elena_gifs.py').read()
source=re.sub(r'names=\[.*?\]',"names=['scott-mccall','allison-argent','stiles-stilinski','lydia-martin','derek-hale','chris-argent']",source,count=1)
exec(source)
