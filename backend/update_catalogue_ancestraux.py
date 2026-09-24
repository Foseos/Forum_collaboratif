"""
Renomme "Artefacts de Luxe" → "Artefacts ancestraux" dans le catalogue boutique-magique.
Run: docker-compose exec backend python manage.py shell < update_catalogue_ancestraux.py
"""
from apps.forum.models import Topic

t = Topic.objects.filter(slug='catalogue-boutique-magique').first()
if not t:
    print("Topic not found")
    exit()

p = t.posts.order_by('created_at').first()
if not p:
    print("Post not found")
    exit()

content = p.content

content = content.replace(
    '&#x2728; V. Artefacts de Luxe',
    '&#x2728; V. Artefacts ancestraux'
)
content = content.replace(
    '<!-- == ARTEFACTS DE LUXE == -->',
    '<!-- == ARTEFACTS ANCESTRAUX == -->'
)

p.content = content
p.save()
print("Done — section renommée 'Artefacts ancestraux'.")
