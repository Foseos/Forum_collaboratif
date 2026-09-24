"""
Modifie la description de la Dague des Anciens dans le catalogue boutique-magique.
Run: docker-compose exec backend python manage.py shell < update_dague.py
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

old_desc = "Lame ench\xeeble forg\xe9e dans les abysses. Inflige une blessure insoignable aux \xeatres normalement immortels. Interdit d\u2019usage hors de l\xe9gitime d\xe9fense."

new_desc = ("Lame ancestrale forg\xe9e dans les t\xe9n\xe8bres primordiales par les premiers d\xe9mons. "
            "Annule les pouvoirs inn\xe9s de sa cible pendant 48 heures au contact du sang. "
            "Immunise temporairement son porteur contre toute t\xe9l\xe9portation ennemie. "
            "Tout usage injustifi\xe9 retourne la mal\xe9diction sur celui qui la brandit.")

p.content = p.content.replace(old_desc, new_desc)
p.save()
print("Done — description de la Dague des Anciens mise à jour.")
