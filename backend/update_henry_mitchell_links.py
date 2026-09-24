from django.db import transaction
from apps.forum.models import Topic


links = [
    {
        'title': 'Paige Matthews Mitchell - Épouse',
        'gif': 'https://zupimages.net/up/26/38/m4he.gif',
        'text': "Paige a bouleversé ma vie et m’a ouvert les portes d’un monde dont j’ignorais tout. Découvrir sa nature de sorcière et d’être de lumière n’a pas toujours été simple, mais je n’ai jamais voulu fuir ce que nous construisions. Nous avons appris à être complémentaires. Je ne peux pas affronter chaque danger avec ses pouvoirs, mais je peux l’écouter, la soutenir et être présent lorsque le poids du monde magique devient trop lourd.",
    },
    {
        'title': 'Tamora Mitchell - Fille',
        'gif': 'https://zupimages.net/up/26/38/kqk5.gif',
        'text': "Avec Tamora, les discussions sont souvent orageuses. Elle supporte mal les limites que Paige et moi lui fixons, et mes conseils ressemblent trop souvent à des leçons de morale à ses yeux. Mon envie de la protéger peut devenir étouffante, j’en ai conscience. Même lorsque nous nous disputons, je veux qu’elle sache qu’elle peut compter sur moi, sans avoir besoin de renoncer à son caractère pour être aimée.",
    },
    {
        'title': 'Katlyn Mitchell - Fille',
        'gif': 'https://zupimages.net/up/26/30/opad.gif',
        'text': "Katlyn vient plus facilement se confier à moi. J’apprécie sa douceur et la confiance qu’elle m’accorde, mais je sais qu’elle essaie souvent d’arrondir les angles pour protéger Tamora. Je ne veux pas qu’elle s’efface ou porte seule les conséquences des décisions de sa sœur. Je tiens à l’écouter pour elle-même, à comprendre ses inquiétudes et à lui laisser la place dont elle a besoin.",
    },
    {
        'title': 'Henry Jr Mitchell - Fils adoptif',
        'gif': 'https://zupimages.net/up/26/38/s8up.gif',
        'text': "Nous avons accueilli Henry Jr alors qu’il venait de perdre sa mère, et il est devenu notre fils. Comme moi, il est humain dans une famille où la magie fait partie du quotidien. J’ai toujours voulu lui montrer que l’absence de pouvoirs ne diminuait ni sa valeur ni sa place parmi nous. Nous parlons librement de ses origines. Le voir grandir en se sentant pleinement légitime dans notre famille est l’une de mes plus grandes fiertés.",
    },
]

with transaction.atomic():
    topic = Topic.objects.select_for_update().get(slug='henry-mitchell')
    if topic.scenario_link_cards:
        raise RuntimeError('La fiche contient déjà des liens : aucune modification effectuée.')
    topic.scenario_link_cards = links
    topic.save(update_fields=['scenario_link_cards'])
    topic.refresh_from_db(fields=['scenario_link_cards'])
    assert topic.scenario_link_cards == links
    print(f'{topic.title}: {len(links)} liens enregistrés et vérifiés.')
