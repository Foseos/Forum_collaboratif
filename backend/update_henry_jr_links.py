from django.db import transaction
from apps.forum.models import Topic


links = [
    {
        'gif': 'https://zupimages.net/up/26/38/m4he.gif',
        'title': 'Paige Matthews Mitchell - Mère adoptive',
        'text': "Ma mère m’a adopté à ma naissance et m’a toujours aimé comme son propre fils. Elle ne m’a jamais caché mes origines et je sais que je peux en parler librement avec elle. Elle a elle-même été adoptée et comprend les questions que je peux me poser. Même si je suis humain, je me sens pleinement à ma place dans notre famille.",
    },
    {
        'gif': 'https://zupimages.net/up/26/38/txh3.jpeg',
        'title': 'Henry Mitchell - Père adoptif',
        'text': "Mon père m’a élevé avec Paige depuis ma naissance. Comme moi, il est humain au milieu d’une famille où la magie fait partie du quotidien. Nous partageons cette particularité, et sa présence me rappelle que nous n’avons pas besoin de pouvoirs pour appartenir à cette famille. Avec lui aussi, je peux parler ouvertement de mes origines.",
    },
    {
        'gif': 'https://zupimages.net/up/26/38/kqk5.gif',
        'title': 'Tamora Mitchell - Grande sœur adoptive',
        'text': "Tamora a un tempérament de feu, mais nous passons beaucoup de temps ensemble. Mon calme l’aide parfois à apaiser sa colère. Enfants, nous avons partagé de nombreuses escapades avec Katlyn : nous formions un véritable trio. Malgré nos différences de caractère, elle reste ma grande sœur et je tiens à notre complicité.",
    },
    {
        'gif': 'https://zupimages.net/up/26/30/opad.gif',
        'title': 'Katlyn Mitchell - Grande sœur adoptive',
        'text': "Avec Katlyn, notre relation est simple et apaisante. Je lui laisse la place de s’exprimer, sans qu’elle ait à rester dans l’ombre de Tamora. Nous avons grandi ensemble et partagé beaucoup d’aventures tous les trois. Elle compte autant pour moi que notre sœur, et je tiens à ce qu’elle le sache.",
    },
]

with transaction.atomic():
    topic = Topic.objects.select_for_update().get(slug='henry-jr-mitchell')
    existing = topic.scenario_link_cards or []
    if existing:
        raise RuntimeError('La fiche contient déjà des liens : aucune modification effectuée.')
    topic.scenario_link_cards = links
    topic.save(update_fields=['scenario_link_cards'])
    print(f'{topic.title}: {len(links)} liens ajoutés.')
