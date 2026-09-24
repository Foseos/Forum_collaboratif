"""Complete the three existing Caine scenarios without recreating their posts."""
import json
import re
from html import escape
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Post, Topic


DATA = [
    dict(slug='abigael-jameson-caine', name='Abigael Jameson Caine', actor='Poppy Drayton', race='Sorcière et démone', age='Trentaine · date exacte au choix', job='Consultante en antiquités et objets occultes · couverture proposée', quote='Mon héritage explique mes cicatrices. Il ne décidera pas de mon avenir.',
         character=[
             'Qualités : lucide, ingénieuse, déterminée, courageuse et protectrice envers les rares personnes auxquelles elle se fie. Défauts : orgueilleuse, provocatrice, méfiante, secrète et tentée de manipuler une situation pour en garder la maîtrise.',
             'Abigael transforme volontiers une blessure en trait d’esprit. Son assurance, son élégance et son ironie lui permettent de détourner une conversation avant qu’elle ne devienne trop intime. Elle préfère paraître dangereuse plutôt que laisser deviner combien le rejet la touche.',
             'Son choix du Bien ne gomme pas ses contradictions. Elle sait négocier avec des interlocuteurs peu recommandables et peut défendre une bonne cause avec des méthodes discutables. Son défi consiste à demander la confiance sans chercher à contrôler ceux qui la lui accordent.'
         ],
         history=[
             ('Entre deux héritages', 'Fille de la sorcière Francesca Jameson et du démon Alastair Caine, Abigael grandit avec le sentiment que son existence dérange les frontières que les autres voudraient préserver. Dans cette adaptation, le rejet familial nourrit son besoin de devenir indispensable. Elle apprend à observer les rapports de force, à dissimuler ses fragilités et à ne jamais attendre une place que personne ne semble prêt à lui offrir.'),
             ('Le prix de la maîtrise', 'La magie devient un refuge autant qu’une arme. Abigael accumule des connaissances, s’intéresse aux objets occultes et comprend très tôt que posséder une information peut éviter un combat. Ses contacts avec le monde démoniaque lui donnent des ressources, mais aussi une réputation dont elle peine à se défaire. Aucune couronne ni autorité sur les démons du forum ne lui est acquise : ce qu’elle obtient doit encore se gagner en jeu.'),
             ('Une famille fragmentée', 'Parker est son demi-frère par leur père, tandis que Waverly est sa demi-sœur par leur mère. Ces deux liens touchent des blessures différentes. Parker lui renvoie la question du choix face à un héritage dangereux ; Waverly réveille le besoin ancien d’être reconnue comme une sœur. Abigael ne peut réparer ces relations par une promesse spectaculaire. Elle doit apprendre à respecter des limites et à répondre de ses actes.'),
             ('Choisir San Francisco', 'Abigael rejoint San Francisco pour prendre ses distances avec les ambitions attachées au nom Caine et trouver sa place parmi des traditions magiques qui se croisent. Ses activités autour des antiquités constituent une couverture proposée et un point de départ pour rencontrer d’autres personnages. Elle choisit le Bien, sans devenir soudainement docile ni irréprochable. Ses alliances demandent du temps et ne lui donnent aucun accès automatique aux secrets des autres.'),
             ('Une autre manière de rester', 'La présence de Waverly et de Parker lui offre la possibilité de construire une famille moins soumise à la peur. Les sœurs Vera-Vaughn peuvent également devenir des interlocutrices, en particulier Mélanie, dont la franchise bouscule ses habitudes. Une attirance éventuelle reste une piste libre. Pour commencer le jeu, un objet suspect, une dette ancienne ou une tentative de rapprochement familial peuvent l’obliger à choisir entre sa sécurité et la confiance qu’elle souhaite mériter.')
         ],
         powers=[
             ('Télékinésie', 'Déplacer un petit objet visible à courte distance, avec concentration ; pas d’écrasement interne ni de contrôle du corps d’autrui.', 'Déplacer un objet plus lourd.', 'Manipuler deux petits objets simultanément.'),
             ('Pyrokinésie', 'Produire une petite flamme contrôlée à proximité. La peur et la fatigue rendent sa maîtrise moins fiable ; aucune immunité générale au feu.', 'Maintenir la flamme plus longtemps.', 'Projeter une flamme à courte portée, avec possibilité d’esquive.'),
             ('Télépathie de contact', 'Avec l’accord du joueur concerné, transmettre une pensée brève par contact. Aucun accès libre aux souvenirs ni aucune vérité forcée.', 'Prolonger un échange de pensées consenti.', 'Établir un bref échange à quelques mètres avec une personne consentante connue.'),
             ('Voile d’ombre', 'Adaptation au forum : atténuer brièvement sa silhouette dans une zone sombre, sans devenir invisible ni traverser les obstacles.', 'Maintenir le voile un peu plus longtemps.', 'Dissimuler aussi un objet porté, sans masquer les sons ni les traces.')
         ],
         links=[('waverly-jameson', 'Waverly — Demi-sœur maternelle', 'Waverly connaît une part de mon passé que je ne peux pas embellir. Je voudrais me rapprocher d’elle, mais elle a le droit de garder ses distances. Notre lien se reconstruira par des gestes fiables et des limites respectées, pas par une dette familiale.'), ('parker-caine', 'Parker — Demi-frère paternel', 'Nous partageons un père et le poids de son nom, sans avoir vécu la même enfance. Je reconnais chez Parker le désir de choisir sa propre voie. Une solidarité est possible, à condition que je cesse de prendre ses décisions pour lui.'), ('melanie-vera', 'Mélanie — Franchise et alliance à construire', 'Mel pourrait devenir une alliée aussi exigeante que précieuse. Sa franchise mettrait à l’épreuve mes détours habituels. La confiance, une éventuelle amitié ou une attirance se construiront avec sa joueuse, sans relation déjà imposée.')]),
    dict(slug='parker-caine', name='Parker Caine', actor='Nick Hargrove', race='Mi-sorcier, mi-démon · adaptation propre à Nexus Arcana', age='Vingt-cinq à trente ans · date exacte au choix', job='Étudiant en reprise de cursus · emploi et discipline au choix', quote='Je porte un nom. Je ne suis pas obligé d’en suivre le destin.',
         character=[
             'Qualités : sensible, loyal, courageux, attentif et persévérant. Défauts : secret, culpabilisant, hésitant à demander de l’aide et parfois impulsif lorsqu’un proche est menacé.',
             'Parker cherche une vie dans laquelle il pourrait être apprécié avant que son nom ne soit connu. Il peut se montrer chaleureux et plein d’humour, puis se refermer dès qu’une question touche sa famille. Ce mouvement n’est pas toujours compris par ceux qui voudraient lui faire confiance.',
             'Il refuse de considérer sa part démoniaque comme une excuse. Pourtant, la peur de blesser les autres peut l’amener à cacher précisément les difficultés dont il devrait parler. Son évolution passe par la franchise, la responsabilité et le droit de recevoir de l’aide sans abandonner son autonomie.'
         ],
         history=[
             ('Le poids du nom Caine', 'Fils d’Alastair Caine, Parker grandit sous le poids d’attentes qui ne lui appartiennent pas. Dans cette version du forum, sa nature mi-sorcière, mi-démoniaque reprend le choix déjà inscrit dans son scénario. Elle constitue une adaptation de la série, où son ascendance est différente. Il ne possède au départ que les quatre dons décrits dans cette fiche.'),
             ('Une vie à soi', 'Parker souhaite étudier, nouer des amitiés et faire des projets ordinaires. Les exigences de son héritage compliquent cette recherche de normalité. Il découvre que le silence protège rarement longtemps : une difficulté cachée devient facilement un malentendu, puis une rupture de confiance. Ses études et ses habitudes quotidiennes restent à personnaliser pour donner au personnage une existence au-delà des conflits magiques.'),
             ('Maggie et la confiance', 'Maggie représente une possibilité de relation fondée sur autre chose que la peur de son nom. Leur histoire exacte et sa tonalité actuelle sont à convenir avec sa joueuse. Une ancienne proximité peut servir de base, mais ni couple, ni séparation précise, ni engagement ne sont imposés. Parker devra apprendre à parler de ses choix plutôt qu’attendre que quelqu’un devine ce qu’il tait.'),
             ('Refuser une place toute tracée', 'Parker choisit le Bien et refuse de devenir l’instrument d’une ambition familiale. Cette décision ne lui offre ni pardon automatique ni maîtrise parfaite. Abigael, sa demi-sœur paternelle, comprend une partie de ce conflit, même si ses méthodes peuvent les opposer. Leur relation offre autant de possibilités d’entraide que de discussions difficiles sur les moyens employés pour protéger les leurs.'),
             ('Un nouveau départ à San Francisco', 'Il arrive à San Francisco avec ses pouvoirs limités et la volonté de reconstruire une stabilité. La perte définitive de ses dons et le dénouement de la série ne sont pas repris ici. Une rencontre avec Waverly, liée à lui par Abigael mais sans parenté de sang, peut ouvrir un cercle familial choisi. Un service rendu, une menace ancienne ou une enquête avec Maggie sont des amorces possibles, à décider avec les autres joueurs.')
         ],
         powers=[
             ('Déplacement d’ombre', 'Rejoindre seul un point visible à quelques mètres. Les protections bloquent le passage ; pas de déplacement entre dimensions.', 'Atteindre un point visible un peu plus éloigné.', 'Emmener une personne consentante sur une courte distance avec fatigue accrue.'),
             ('Intangibilité brève', 'Rendre une main intangible quelques secondes pour franchir une matière ordinaire fine ; aucune attaque possible pendant cet état.', 'Étendre brièvement l’effet à un bras.', 'Traverser seul une paroi ordinaire mince, sans franchir une protection magique.'),
             ('Impulsion télékinétique', 'Repousser un petit objet proche par une impulsion simple ; aucune manipulation fine ni blessure interne.', 'Repousser un objet plus lourd.', 'Produire une poussée défensive contre une cible, dont la réaction reste à son joueur.'),
             ('Perception démoniaque', 'Adaptation au forum : ressentir une perturbation démoniaque proche, sans identifier son auteur ni ses intentions.', 'Mieux distinguer une trace récente d’une présence.', 'Suivre brièvement une trace récente dans une zone limitée, si elle n’est pas masquée.')
         ],
         links=[('abigael-jameson-caine', 'Abigael — Demi-sœur paternelle', 'Abigael sait ce que le nom de notre père peut représenter. Je peux accepter son aide sans lui laisser choisir ma vie. Notre solidarité reste à construire, avec de la franchise et la possibilité de nous opposer sans devenir des ennemis.'), ('maggie-vera', 'Maggie — Une confiance à définir ensemble', 'J’aimerais que Maggie puisse me connaître au-delà de mon héritage. Notre passé précis, notre proximité et une éventuelle romance restent à convenir avec sa joueuse. La confiance demande des paroles claires, pas une promesse de devenir parfait.'), ('waverly-jameson', 'Waverly — Un lien familial indirect', 'Nous ne sommes pas frère et sœur de sang : Abigael est le lien entre nos branches familiales. Une rencontre pourrait faire naître une entraide prudente. Je n’attends ni affection automatique ni accès à sa vie privée ; il faudra apprendre à nous connaître.')]),
    dict(slug='waverly-jameson', name='Waverly Jameson Caine', actor='Jessica Sipos', race='Sorcière', age='Adulte · plus jeune qu’Abigael, âge exact au choix', job='Restauratrice de livres et manuscrits · activité proposée', quote='Protéger les miens ne signifie plus vivre cachée.',
         character=[
             'Qualités : protectrice, observatrice, tenace, pragmatique et patiente. Défauts : méfiante, rigide lorsqu’elle a peur, rancunière et portée à tout assumer seule.',
             'Waverly choisit soigneusement ce qu’elle révèle et à qui. Elle observe les actes avant de croire aux discours. Sa douceur existe, mais elle se déploie dans les espaces où elle se sent en sécurité : une attention discrète, un ouvrage réparé, une présence fidèle valent pour elle davantage qu’une déclaration grandiose.',
             'Lorsqu’il s’agit de sa famille, elle peut confondre prudence et fermeture. Elle ne doit pas apprendre à faire confiance à tout le monde, mais à reconnaître les personnes capables de respecter ses limites. Sa magie reflète ce besoin de protéger sans chercher à dominer.'
         ],
         history=[
             ('La branche Jameson', 'Waverly est la demi-sœur maternelle d’Abigael : elles partagent Francesca Jameson comme mère. Le nom composé Jameson Caine est retenu pour cette version du forum à la demande de sa créatrice ; il ne fait pas d’Alastair son père. Parker est donc lié à elle par Abigael, sans être son frère de sang. Cette distinction permet de conserver des liens familiaux clairs.'),
             ('Des silences qui séparent', 'L’histoire familiale a appris à Waverly que l’affection pouvait se mêler à la peur et au contrôle. Elle et Abigael n’en ont pas gardé les mêmes réflexes. Là où l’une provoque pour reprendre l’initiative, l’autre se retire pour préserver un espace sûr. Leur éloignement ne se résout pas simplement parce qu’elles se retrouvent dans la même ville.'),
             ('Protéger Hope', 'La maternité donne un centre très concret à ses décisions. Hope, sa fille, compte davantage que les querelles d’héritage. Pour Nexus Arcana, son âge précis et les événements surnaturels qui la concernent sont à fixer avec le staff ; elle reste un personnage secondaire et ses éventuels dons ne constituent pas des pouvoirs supplémentaires utilisables par Waverly. Sa protection peut nourrir le jeu sans imposer un danger permanent ni une intrigue déjà résolue.'),
             ('Reprendre racine', 'Waverly choisit San Francisco pour bâtir une vie plus stable. La restauration de livres est une activité proposée qui relie son goût du travail patient aux bibliothèques, aux collectionneurs et aux archives de la ville. Elle peut y trouver des contacts sans appartenir d’emblée à une organisation secrète. Les détails de son logement et de ses soutiens restent libres pour faciliter son intégration.'),
             ('Ouvrir une porte', 'La proximité d’Abigael rend possible un rapprochement, mais Waverly garde le droit de dire non. Parker peut devenir un allié extérieur aux blessures de leur enfance, et Mélanie une interlocutrice sur la protection des proches. Un manuscrit à identifier, une protection qui faiblit ou une invitation familiale peuvent lancer ses premiers sujets. Son objectif n’est pas seulement de fuir une menace : elle veut enfin choisir ce qu’elle construit et avec qui.')
         ],
         powers=[
             ('Télékinésie', 'Déplacer lentement un petit objet visible. La précision demande du calme ; aucun contrôle du corps ou des organes d’autrui.', 'Déplacer un objet plus lourd.', 'Manipuler deux petits objets avec précision.'),
             ('Barrière protectrice', 'Adaptation au forum : former brièvement devant elle un écran qui amortit un faible impact ; il peut céder et ne renvoie pas les attaques.', 'Résister à un impact un peu plus fort.', 'Élargir l’écran pour abriter aussi une personne proche pendant un bref instant.'),
             ('Détection d’enchantement', 'Adaptation au forum : par contact avec un objet, ressentir qu’il porte une magie, sans en connaître automatiquement la fonction ni la formule.', 'Distinguer une magie active d’une trace résiduelle.', 'Percevoir une tendance protectrice ou hostile, avec résultat fixé par le maître du jeu.'),
             ('Sceau d’alerte', 'Adaptation au forum : poser sur une ouverture un sceau temporaire qui la prévient s’il est franchi lorsqu’elle reste proche ; ni piège ni identification du passant.', 'Prolonger la tenue du sceau.', 'Surveiller deux ouvertures proches simultanément.')
         ],
         links=[('abigael-jameson-caine', 'Abigael — Demi-sœur maternelle', 'Abigael est ma sœur, mais ce mot ne suffit pas à effacer notre histoire. Je peux envisager de lui ouvrir une place sans renoncer aux limites qui protègent mon foyer. Une réconciliation doit se jouer progressivement et ne lui est pas due.'), ('parker-caine', 'Parker — Une rencontre au-delà du nom Caine', 'Parker et moi n’avons pas de parent de sang en commun. Abigael relie nos histoires. Je pourrais découvrir en lui quelqu’un qui cherche aussi à sortir des attentes familiales, mais notre entente reste une possibilité à construire.'), ('melanie-vera', 'Mélanie — Solidarité possible entre sorcières', 'Mel pourrait comprendre mon besoin de protéger les miens tout en me rappelant que je n’ai pas à tout porter seule. Une rencontre autour d’un manuscrit ou d’une recherche magique peut amorcer notre lien ; aucune amitié préalable n’est imposée.')]),
]


def p(text):
    return '<p style="line-height:1.85;margin:0 0 .9rem;">' + escape(text) + '</p>'


def section(title, body):
    return '<section style="margin:1rem 0;padding:1rem;border:1px solid #574477;border-radius:8px;"><h2 style="font-size:1.1rem;color:#c4b5fd;">' + escape(title) + '</h2>' + body + '</section>'


def portrait(post):
    match = re.search(r'<img\b[^>]*\bsrc=[\"\x27]([^\"\x27]+)', post.content)
    if not match:
        raise RuntimeError('Portrait absent : ' + str(post.pk))
    return match.group(1)


with transaction.atomic():
    slugs = {d['slug'] for d in DATA} | {link[0] for d in DATA for link in d['links']}
    topics = {t.slug: t for t in Topic.objects.select_for_update().filter(slug__in=slugs, category__slug='scenarios-a-prendre')}
    posts = {slug: Post.objects.select_for_update().filter(topic=t).order_by('created_at', 'pk').first() for slug, t in topics.items()}
    if set(topics) != slugs or any(post is None for post in posts.values()):
        raise RuntimeError('Scénario ou premier message absent.')
    images = {slug: portrait(post) for slug, post in posts.items()}
    for d in DATA:
        if 'data-caine-scenario' in posts[d['slug']].content or topics[d['slug']].scenario_link_cards:
            raise RuntimeError('Scénario déjà complété : ' + d['slug'])
    folder = Path(settings.BASE_DIR) / 'data' / 'scenario_backups'
    folder.mkdir(parents=True, exist_ok=True)
    backup = [dict(topic_id=topics[d['slug']].pk, title=topics[d['slug']].title, post_id=posts[d['slug']].pk, content=posts[d['slug']].content, scenario_link_cards=topics[d['slug']].scenario_link_cards) for d in DATA]
    (folder / ('caine-family-' + timezone.now().strftime('%Y%m%dT%H%M%S%f') + '.json')).write_text(json.dumps(backup, ensure_ascii=False), encoding='utf-8')
    for d in DATA:
        topic, post = topics[d['slug']], posts[d['slug']]
        content = '<div data-caine-scenario="1" style="font-family:Georgia,serif;background:#0d0a1a;color:#e2d9f3;padding:clamp(1rem,4vw,2rem);border-radius:10px;max-width:800px;margin:auto;">'
        content += p('✦ Nexus Arcana · Livre des Ombres ✦')
        content += '<header style="display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;"><div style="flex:1;min-width:180px;"><h1 style="color:#f5d76e;">' + escape(d['name']) + '</h1>' + p(d['race'] + ' · Bien') + p('« ' + d['quote'] + ' »') + '</div><figure style="margin:0;"><img src="' + escape(images[d['slug']], quote=True) + '" alt="' + escape(d['name']) + '" style="width:200px;max-width:100%;height:320px;object-fit:cover;border-radius:8px;"><figcaption>' + escape('Ft ' + d['actor']) + '</figcaption></figure></header>'
        identity = [('Âge', d['age']), ('Origines et résidence', 'Héritage familial Jameson / Caine selon la branche · installé(e) à San Francisco'), ('Race', d['race']), ('Camp', 'Bien'), ('Activité', d['job']), ('Vie sentimentale', 'Au choix du joueur, en accord avec les partenaires concernés')]
        content += section('I. Identité', ''.join(p(label + ' : ' + value) for label, value in identity))
        power_html = p('Quatre pouvoirs de base à la création. Chacun peut être amélioré deux fois : base → évolution 1 achetée → évolution 2 achetée. Chaque achat suit la boutique et la validation du staff. Les pistes ci-dessous ne sont pas débloquées au départ et restent à valider ; aucune cinquième capacité de base n’est accordée.')
        for name, base, first, second in d['powers']:
            power_html += '<div data-base-power="1"><h3 style="color:#f5d76e;font-size:1rem;">' + escape(name) + '</h3>' + p('Base — ' + base) + p('Évolution 1, après achat — ' + first) + p('Évolution 2, après second achat — ' + second) + '</div>'
        power_html += p('Les connaissances occultes et compétences professionnelles sont des savoir-faire, pas des dons supplémentaires. Les rituels éventuels suivent les règles du grimoire et ne permettent pas de contourner les limites des quatre pouvoirs. Aucun effet sur un autre personnage n’est imposé à son joueur.')
        content += section('II. Quatre pouvoirs et leurs évolutions', power_html)
        content += section('III. Âme et caractère', ''.join(map(p, d['character'])))
        content += section('IV. Histoire', ''.join('<h3 style="color:#f5d76e;font-size:1rem;">' + escape(title) + '</h3>' + p(body) for title, body in d['history']))
        content += section('V. Repères pour le jeu', p('Version adaptée à Nexus Arcana : les trois sœurs Vera-Vaughn sont vivantes et réunies à San Francisco. Les pouvoirs proposés sont équilibrés pour le forum et ne constituent pas une liste exhaustive des capacités de la série. Les événements futurs, alliances et romances se décident en jeu. Les activités proposées et les dates précises restent personnalisables avec le staff.'))
        content += '<footer style="font-size:.75rem;color:#a99abb;">Personnage inspiré de Charmed (2018), adapté pour Nexus Arcana. Portrait conservé : crédit du créateur du visuel à renseigner.</footer></div>'
        cards = [dict(title=title, gif=images[slug], text=body) for slug, title, body in d['links']]
        assert len(d['powers']) == 4 and content.count('data-base-power="1"') == 4
        assert not any(term in content for term in ('Montana', 'Callaway', 'Nom du pouvoir', 'Prénom NOM'))
        post.content = content
        post.save(update_fields=['content', 'is_edited', 'updated_at'])
        topic.title = d['name']
        topic.scenario_link_cards = cards
        topic.save(update_fields=['title', 'scenario_link_cards'])
        post.refresh_from_db()
        topic.refresh_from_db()
        assert post.content == content and topic.scenario_link_cards == cards and topic.title == d['name']
        print(d['name'] + ' : fiche enregistrée, 4 pouvoirs et 3 liens vérifiés.')
