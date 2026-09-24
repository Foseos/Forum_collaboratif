from django.db import transaction
from apps.forum.models import Topic


def card(title, image, text):
    return {'title': title, 'gif': image, 'text': text}


PHOEBE = 'https://zupimages.net/up/26/38/zka2.gif'
COLE = 'https://zupimages.net/up/26/38/w78v.gif'
COOP = 'https://zupimages.net/up/26/38/fpca.gif'
PJ = 'https://zupimages.net/up/26/38/sjm5.gif'
PARKER = 'https://zupimages.net/up/26/38/y6h2.gif'
PEYTON = 'https://zupimages.net/up/26/38/un3l.gif'

updates = {
    'andy-trudeau': [
        card('Prue Halliwell Trudeau - Amour de jeunesse et épouse', 'https://zupimages.net/up/26/38/jveb.gif',
             "Prue est mon amour de jeunesse. Nous avons été séparés par la mort, mais nos retrouvailles nous ont offert la seconde chance que je n’osais plus espérer. J’aime sa force de caractère et je ne cherche pas à la changer. Je suis là pour l’écouter, l’apaiser et la soutenir, dans notre vie de famille comme face aux dangers du monde magique."),
        card('Elyse Halliwell Trudeau - Fille unique', 'https://zupimages.net/up/26/38/yjr2.gif',
             "Elyse est la fille que Prue et moi pensions ne jamais pouvoir avoir. J’ai toujours voulu être un père présent et une oreille attentive. Elle se confie facilement à moi, et je lui accorde parfois davantage de liberté que sa mère. Je sais que mon indulgence ne lui rend pas toujours service, mais je tiens à ce qu’elle puisse venir me parler sans crainte."),
    ],
    'cole-turner': [
        card('Phoebe Halliwell Turner - Épouse, second mariage', PHOEBE,
             "Phoebe a vu en moi une humanité que j’avais presque oubliée. Notre histoire a traversé les mensonges, la Source et un premier divorce. Nous nous sommes retrouvés après sa séparation avec Coop, puis remariés. Je connais le prix des blessures que je lui ai infligées. Aujourd’hui, je veux lui montrer par mes choix quotidiens qu’elle peut construire sa vie avec moi."),
        card('Jensen Turner - Fils aîné retrouvé', 'https://zupimages.net/up/26/38/dyjf.gif',
             "Nous avons cru Jensen mort alors qu’il grandissait loin de nous, entre les mains de forces maléfiques. Le retrouver a réveillé autant de colère contre ceux qui nous l’ont arraché que d’espoir. Je connais le combat qu’il mène pour choisir le Bien malgré son passé. Je ne lui demande pas de justifier chaque erreur : je veux lui laisser le temps de trouver sa place auprès de nous."),
        card('Primerose Halliwell Turner - Fille cadette', 'https://zupimages.net/up/26/36/0tp3.gif',
             "Primerose est née de notre seconde chance, à Phoebe et moi. Son héritage démoniaque fait partie d’elle, comme il fait partie de moi. Je veux l’aider à comprendre cette part d’elle-même et à la maîtriser, sans lui laisser croire que sa nature décide de son avenir. Je connais trop bien les dangers du monde infernal pour les prendre à la légère lorsqu’il s’agit de ma fille."),
        card('Prudence Johanna Halliwell Swann - Belle-fille', PJ,
             "P.J. était assez grande pour comprendre mon arrivée et pour s’en méfier. Il m’a fallu du temps pour gagner sa confiance. Je n’ai jamais voulu remplacer Coop ; je voulais lui prouver que je pouvais être une présence fiable. Aujourd’hui, elle me laisse une place dans sa vie, et je tiens à être digne de cette confiance."),
        card('Parker Halliwell Swann - Belle-fille', PARKER,
             "Parker et moi avons deux caractères qui ne se laissent pas facilement dicter leur conduite. Nos échanges peuvent être vifs, mais je comprends son besoin de ne pas être réduite à ses écarts. Elle a fini par m’accepter et me respecter. Je veux rester quelqu’un vers qui elle peut se tourner, même lorsque nous ne sommes pas d’accord."),
        card('Peyton Halliwell Swann - Belle-fille', PEYTON,
             "Peyton était encore très petite lorsque je suis revenu dans la vie de Phoebe. Mon passé l’a inquiétée, et j’ai dû lui montrer qu’elle pouvait me faire confiance. Je préfère lui offrir une présence patiente plutôt que forcer ses confidences. Savoir qu’elle peut désormais venir vers moi compte beaucoup à mes yeux."),
        card('Coop Swann - Père de mes belles-filles', COOP,
             "Coop est le père de P.J., Parker et Peyton, et mon mariage avec Phoebe ne change rien à cette place. Notre famille recomposée porte une histoire difficile, particulièrement pour lui. Je ne cherche pas à lui prendre son rôle. Nous avons en commun de vouloir le bonheur et la sécurité des filles, et c’est sur cela que je souhaite m’appuyer."),
    ],
    'leo-wyatt': [
        card('Piper Halliwell - Épouse', 'https://zupimages.net/up/26/38/3fgr.gif',
             "Aimer Piper m’a conduit à remettre en question les règles des Anciens et à choisir la vie que je voulais réellement mener. Nous avons traversé tant d’obstacles pour construire notre famille. J’ai renoncé à mes pouvoirs pour être présent auprès d’elle et de nos enfants. Même après leur retour, je n’ai jamais oublié cette priorité : être son mari, son soutien et son compagnon au quotidien."),
        card('Wyatt Matthew Halliwell - Fils aîné', 'https://zupimages.net/up/26/38/jd2l.gif',
             "Wyatt porte depuis sa naissance une puissance et des attentes qui auraient pu écraser n’importe qui. Avec Piper, nous avons dû le protéger de nombreuses convoitises. Je veux aussi être le père qui l’apaise lorsqu’il doute, et lui rappeler qu’il est mon fils avant d’être un être promis à une destinée exceptionnelle. Je lui transmets ce que je peux de mon expérience d’être de lumière."),
        card('Christopher Halliwell - Fils', 'https://zupimages.net/up/23/13/iqsi.gif',
             "Chris cache souvent sa sensibilité derrière une volonté de tout affronter seul. Je reconnais cette solitude et je voudrais qu’il sache qu’il peut demander de l’aide. Son courage et ce qu’il a accompli pour protéger Wyatt me rendent fier. Entre mes deux fils, j’essaie de maintenir le dialogue sans comparer leur valeur ni minimiser ce que chacun traverse."),
        card('Mélinda Halliwell - Fille cadette', 'https://zupimages.net/up/26/38/se6z.gif',
             "Mélinda est venue compléter notre famille alors que nous pensions que ma vie humaine avait changé notre avenir magique. Elle sait qu’elle peut me confier ses peines et ses émotions. J’aime être cette présence calme auprès d’elle. Je veux veiller sur ma fille tout en lui laissant la place de grandir, même lorsque mon instinct de protection me pousse à m’inquiéter."),
    ],
    'coop-swann': [
        card('Phoebe Halliwell Turner - Ex-épouse et mère de mes filles', PHOEBE,
             "Je suis entré dans la vie de Phoebe pour l’aider à croire de nouveau en l’amour, et je suis tombé amoureux d’elle. Notre mariage nous a donné trois filles. Le divorce et son retour auprès de Cole m’ont blessé, mais je n’ai pas voulu la retenir contre ses sentiments. Nous restons leurs parents, et je tiens à ce que notre séparation ne les prive ni de mon amour ni de ma présence."),
        card('Prudence Johanna Halliwell Swann - Fille aînée', PJ,
             "P.J. partage avec moi une sensibilité à l’amour et aux émotions qui nous rapproche profondément. Je lui ai transmis ce que je sais de notre nature de Cupidon. Malgré le divorce, nous avons gardé beaucoup de temps et de complicité ensemble. Je suis fier de la jeune femme qu’elle devient, et je veux qu’elle sache qu’elle n’a pas à porter seule le bien-être de toute la famille."),
        card('Parker Halliwell Swann - Fille', PARKER,
             "Parker trouve souvent mon optimisme trop facile et mes conseils trop moralisateurs. Son tempérament nous conduit à nous heurter, surtout quand j’essaie d’apaiser une colère qu’elle estime légitime. Je l’aime sans lui demander de ressembler à ses sœurs. J’apprends à l’écouter sans vouloir immédiatement lui expliquer comment régler chaque difficulté."),
        card('Peyton Halliwell Swann - Fille cadette', PEYTON,
             "Avec Peyton, les mots ne sont pas toujours nécessaires. Elle est discrète, sensible, et je cherche avant tout à lui offrir un endroit où elle se sent comprise. Je la rassure sans lui demander de devenir plus bruyante ou plus affirmée pour être entendue. La confiance qu’elle m’accorde est précieuse, et je tiens à rester disponible pour elle."),
        card('Cole Turner - Époux de Phoebe et beau-père de mes filles', COLE,
             "Accepter le retour de Cole auprès de Phoebe n’a pas été facile. Il fait désormais partie du quotidien de mes filles, et je dois composer avec cette réalité. Je reste leur père, tandis qu’il occupe une autre place dans leur vie. Je souhaite que nous puissions respecter ces places pour qu’elles n’aient pas à choisir entre les adultes qu’elles aiment."),
    ],
}

with transaction.atomic():
    topics = list(Topic.objects.select_for_update().filter(slug__in=updates))
    if len(topics) != len(updates):
        raise RuntimeError('Un scénario est introuvable : aucune modification effectuée.')
    if any(topic.scenario_link_cards for topic in topics):
        raise RuntimeError('Un scénario contient déjà des liens : aucune modification effectuée.')
    for topic in topics:
        topic.scenario_link_cards = updates[topic.slug]
        topic.save(update_fields=['scenario_link_cards'])
        print(f'{topic.title}: {len(topic.scenario_link_cards)} liens ajoutés.')
