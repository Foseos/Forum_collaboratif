import json
import re
from html import escape
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Post, Topic


PROFILES = {
    'macy-vaughn': {
        'name': 'Macy Vaughn', 'actor': 'Madeleine Mantock', 'age': '32 ans · ajustable avec le staff',
        'race': 'Sorcière à l’héritage démoniaque', 'orientation': 'Au choix du joueur',
        'job': 'Chercheuse en génétique · laboratoire à San Francisco',
        'family': 'Fille de Marisol Vera et Dexter Vaughn · sœur aînée de Maggie · demi-sœur aînée de Mélanie',
        'quote': 'Je peux chercher une explication à tout. Apprendre à laisser les autres m’aimer est une autre expérience.',
        'powers': [
            ('Télékinésie', 'Déplace des objets par la pensée. Elle privilégie la précision : saisir un outil, écarter un obstacle ou tenter une répulsion. La masse, la distance et le nombre de cibles augmentent l’effort. Une action visant un personnage se résout avec son joueur.'),
            ('Pyrokinésie liée à son héritage démoniaque', 'Manifestations de feu limitées, plus difficiles à maîtriser sous une émotion forte. Macy doit surveiller les risques pour ses proches et l’environnement. Ni immunité automatique aux flammes, ni puissance de la Source ; les manifestations majeures sont des évolutions à valider.'),
            ('Sorcellerie et travail rituel', 'Apprend et prépare des sorts et potions compatibles avec sa lignée. Les composants, la recherche et la coopération comptent. Le pouvoir collectif des trois sœurs exige leur participation ; il ne remplace pas celui des Halliwell et ne garantit aucune victoire.'),
        ],
        'qualities': 'Rigoureuse, perspicace, loyale, courageuse, attentive, persévérante.',
        'flaws': 'Réservée, perfectionniste, portée à tout analyser, sévère envers elle-même, réticente à demander de l’aide.',
        'character': [
            'Macy cherche d’abord à comprendre. Face à une anomalie magique, elle observe, compare et formule une hypothèse avant d’agir. Cette méthode rassure ses sœurs autant qu’elle peut les exaspérer lorsqu’une décision urgente s’impose. Elle n’est pas froide : elle a simplement appris à garder ses émotions dans un espace où personne ne pouvait les utiliser contre elle.',
            'Son attachement se manifeste dans les détails : un repas laissé pour une sœur rentrée tard, une recherche poursuivie pour trouver une solution, une présence silencieuse au bon moment. Elle redoute de devenir un danger à cause de son héritage démoniaque. Sa progression consiste autant à accepter le soutien des autres qu’à contrôler ses dons.',
        ],
        'history': [
            ('Grandir loin des Vera', 'Macy a grandi auprès de Dexter Vaughn, avec une famille incomplète et des questions auxquelles les adultes répondaient rarement jusqu’au bout. Elle ignorait que Marisol Vera était sa mère et que deux autres filles partageaient cet héritage. La curiosité est devenue sa manière de reprendre prise sur le monde. Les sciences, puis la génétique, lui ont offert une méthode pour approcher l’inconnu sans se laisser submerger.'),
            ('Une famille à découvrir', 'La disparition de Marisol et la découverte de traces de son passé ont conduit Macy jusqu’à Mélanie et Maggie. Elles ne se sont pas reconnues comme une famille en une seule conversation. Macy arrivait avec le besoin de comprendre ; Mélanie protégeait un foyer endeuillé ; Maggie cherchait une façon de faire une place à cette inconnue. Les premiers phénomènes magiques les ont obligées à coopérer avant même qu’elles sachent se faire confiance.'),
            ('La part qu’elle redoutait', 'Macy découvre que son héritage magique porte aussi une composante démoniaque. Cette révélation heurte tout ce qu’elle voudrait croire de sa propre maîtrise. Elle tente d’abord de traiter ce secret comme un problème à résoudre seule, puis comprend que le silence peut blesser ses sœurs davantage que la vérité. Elle choisit le Bien et apprend à distinguer sa nature de ses actes. Ses pouvoirs ne lui donnent ni autorité sur les démons ni accès automatique à leurs capacités.'),
            ('San Francisco, un nouveau point de départ', 'Dans cette adaptation à Nexus Arcana, Macy est vivante et les trois sœurs se retrouvent à San Francisco. Elle y reprend un travail de recherche tout en étudiant avec elles les perturbations surnaturelles qui touchent la ville. Leur lignée coexiste avec les autres familles magiques : elles n’arrivent ni pour remplacer les Halliwell ni pour diriger les communautés déjà présentes. Macy souhaite comprendre les phénomènes avant de leur attribuer une cause, et cette prudence peut devenir aussi utile que difficile à tenir lorsque ses proches sont menacés.'),
            ('Ce qu’il reste à jouer', 'Trouver sa place d’aînée sans prendre celle de Mélanie, développer une relation avec Maggie et accepter l’aide de Harry constituent ses premiers enjeux. Ses recherches, ses alliances et sa vie sentimentale restent à construire en RP. Aucun décès de la série ni événement final n’est imposé à cette version ; la suite dépend des joueurs et des intrigues du forum.'),
        ],
        'links': [
            ('melanie-vera', 'Mélanie Vera - Demi-sœur cadette', 'Mel a veillé sur Maggie bien avant mon arrivée. Je comprends qu’elle n’ait pas envie de céder sa place à une sœur qu’elle connaît encore mal. Sa façon de foncer se heurte souvent à mon besoin d’analyser. Pourtant, je reconnais dans sa colère une inquiétude que je partage : celle de perdre notre famille. Je veux construire notre confiance sans lui demander de devenir quelqu’un d’autre.'),
            ('maggie-vera', 'Maggie Vera - Petite sœur', 'Maggie m’a offert une place que je ne savais pas demander. Nous partageons les mêmes parents, mais pas les mêmes souvenirs d’enfance, et je ne veux pas prétendre rattraper toutes ces années en la protégeant de tout. Sa sensibilité me touche. J’apprends à me confier à elle et à reconnaître sa force, même lorsqu’elle s’exprime autrement que la mienne.'),
            ('harry-greenwood', 'Harry Greenwood - Être de lumière et allié', 'Harry connaît un monde dont je découvre encore les règles. Je lui pose beaucoup de questions et je ne peux pas me contenter d’un simple « c’est magique ». Sa patience et son soutien m’aident pourtant à avancer. Je veux pouvoir lui faire confiance sans renoncer à mon jugement. La profondeur de notre relation, et une éventuelle évolution sentimentale, sont à construire entre joueurs.'),
        ],
    },
    'melanie-vera': {
        'name': 'Mélanie « Mel » Vera', 'actor': 'Melonie Diaz', 'age': '29 ans · ajustable avec le staff',
        'race': 'Sorcière', 'orientation': 'Lesbienne',
        'job': 'Enseignante en études de genre · université de San Francisco',
        'family': 'Fille de Marisol et Ray Vera · demi-sœur cadette de Macy et demi-sœur aînée de Maggie',
        'quote': 'Protéger ceux que j’aime ne devrait pas vouloir dire choisir à leur place.',
        'powers': [
            ('Inhibition moléculaire', 'Dans cette adaptation, son pouvoir de ralentissement prend une forme moléculaire limitée : ralentir ou immobiliser brièvement une cible perceptible. Ce n’est pas un arrêt général du temps. Portée, durée et résistances sont encadrées par la fiche ; aucune immobilisation durable d’un personnage sans accord.'),
            ('Manipulation du froid', 'Branche de refroidissement et de gel localisé, à faible échelle. Nécessite concentration et maîtrise du support visé. Le gel n’est pas une solution automatique contre toute créature. Une tempête, un gel massif ou un effet temporel véritable nécessite une évolution explicitement validée.'),
            ('Sorcellerie et protections rituelles', 'Prépare des sorts, des potions et des cercles dans les limites de son apprentissage. Les rituels importants demandent du temps, des composants et des partenaires. Le pouvoir collectif des trois sœurs nécessite leur accord et leur participation, sans victoire automatique.'),
        ],
        'qualities': 'Déterminée, franche, solidaire, courageuse, protectrice, engagée.',
        'flaws': 'Impulsive, obstinée, méfiante envers l’autorité, parfois autoritaire, peu encline à reconnaître sa peur.',
        'character': [
            'Mel supporte difficilement l’injustice, surtout lorsque ceux qui la subissent n’ont pas les moyens de répondre. Elle prend position, parfois avant d’avoir toutes les informations. Sa franchise peut réconforter autant que heurter. Elle n’aime pas qu’une institution, magique ou humaine, lui demande de faire confiance sans explication.',
            'Au sein de sa famille, elle confond parfois protection et contrôle. Donner des directives lui paraît plus simple qu’avouer qu’elle a peur de perdre quelqu’un. Derrière ses prises de position se trouve une femme profondément loyale, capable de revenir vers ses proches même après une dispute. Apprendre à les écouter sans préparer immédiatement une réponse constitue un véritable défi.',
        ],
        'history': [
            ('L’aînée du foyer', 'Mel a grandi avec Marisol et Maggie, persuadée de connaître l’essentiel de sa famille. Elle s’est très tôt comportée comme celle qui tient bon et intervient lorsque quelque chose dérape. Sa proximité avec sa mère a nourri ses convictions et son intérêt pour les rapports de pouvoir. Ses études, puis l’enseignement, lui ont donné un espace pour défendre ces questions dans le monde humain.'),
            ('Le deuil et les secrets', 'La mort de Marisol a fait vaciller ses certitudes. À la peine s’est ajoutée la colère de découvrir une vie magique cachée et une sœur aînée dont personne ne lui avait parlé. L’arrivée de Macy n’a pas immédiatement réparé ce manque. Mel a d’abord voulu protéger Maggie et comprendre ce que cette inconnue attendait d’elles. Les dangers partagés l’ont peu à peu amenée à regarder Macy comme une personne, plutôt que comme un nouveau secret de leur mère.'),
            ('Apprendre à ne pas tout retenir', 'La découverte de ses pouvoirs semble répondre à son désir de suspendre le danger, mais elle ne peut pas arrêter toutes les pertes ni toutes les décisions qu’elle désapprouve. Dans Nexus Arcana, son ralentissement est adapté aux règles moléculaires du grimoire ; les manipulations temporelles majeures ne lui sont pas accordées librement. Elle travaille sa précision et ses protections au lieu de compter sur une puissance sans limites.'),
            ('S’installer à San Francisco', 'Réunie avec Macy et Maggie, Mel s’installe à San Francisco et reprend une activité d’enseignement. La coexistence de communautés surnaturelles différentes nourrit ses interrogations : qui fixe les règles, qui protège les plus vulnérables, et qui décide qu’une créature mérite d’être entendue ? Elle peut chercher des alliances, mais celles-ci restent à construire en jeu. Elle ne dispose d’aucune autorité particulière sur les familles ou les factions du forum.'),
            ('Une place à redéfinir', 'Macy occupe désormais la place d’aînée biologique, tandis que Maggie revendique le droit de faire ses propres choix. Mel doit apprendre qu’elle peut rester indispensable sans être responsable de tout. Sa vie sentimentale est libre à construire avec des partenaires consentantes ; aucune relation ni séparation de la série n’est imposée. Son avenir repose sur sa capacité à transformer son instinct de défense en une confiance partagée.'),
        ],
        'links': [
            ('macy-vaughn', 'Macy Vaughn - Demi-sœur aînée', 'L’arrivée de Macy a réveillé plus de questions que je ne voulais en affronter. Je n’ai pas besoin qu’une inconnue m’explique comment protéger Maggie, mais je sais aussi que Macy n’a pas choisi les secrets de notre mère. Ses raisonnements me ralentissent parfois au moment où je voudrais agir. J’apprends à reconnaître qu’ils peuvent nous éviter des erreurs, et qu’une sœur de plus ne m’enlève pas ma place.'),
            ('maggie-vera', 'Maggie Vera - Demi-sœur cadette', 'J’ai longtemps pensé que mon rôle consistait à empêcher Maggie de souffrir. À force de décider pour elle, je risque surtout de l’éloigner. Sa douceur ne la rend pas incapable de se défendre et ses choix méritent d’être écoutés. Nous nous disputons, mais elle reste ma petite sœur. Je dois apprendre à être présente sans surveiller chaque pas qu’elle fait.'),
            ('harry-greenwood', 'Harry Greenwood - Guide et allié discuté', 'Harry nous apporte des connaissances précieuses, mais je refuse d’obéir à une règle seulement parce qu’elle vient du monde magique. Je le questionne, je le contredis et je veux savoir à qui ses décisions profitent. La confiance se construit lorsqu’il nous traite comme des partenaires capables de choisir. Nos désaccords n’empêchent pas une réelle coopération.'),
        ],
    },
    'maggie-vera': {
        'name': 'Margarita « Maggie » Vera', 'actor': 'Sarah Jeffery', 'age': '25 ans · ajustable avec le staff',
        'race': 'Sorcière', 'orientation': 'Au choix du joueur',
        'job': 'Étudiante en psychologie · activité complémentaire au choix',
        'family': 'Fille de Marisol Vera et Dexter Vaughn · sœur cadette de Macy et demi-sœur cadette de Mélanie',
        'quote': 'Je ressens beaucoup de choses. Cela ne veut pas dire que je dois m’oublier pour les autres.',
        'powers': [
            ('Empathie', 'Perçoit les émotions de personnes proches et apprend à distinguer ses ressentis des leurs. Une émotion n’en révèle pas automatiquement la cause ni les pensées exactes. La foule et les émotions intenses peuvent la submerger. Toute influence sur un ressenti exige l’accord du joueur concerné.'),
            ('Prémonitions émotionnelles', 'Reçoit des fragments possibles d’avenir liés à une forte connexion ou une émotion. Les images sont brèves, incomplètes et interprétables. Elles n’offrent ni solution certaine ni accès libre aux secrets des autres. Les indices d’un événement sont fournis par le maître du jeu.'),
            ('Sorcellerie et coopération rituelle', 'Apprend les sorts et potions de sa lignée avec préparation et pratique. Le lien entre les trois sœurs soutient leur magie collective, mais ne lui accorde pas tous leurs dons. La copie empathique de pouvoirs et les influences mentales avancées restent des évolutions à faire valider.'),
        ],
        'qualities': 'Chaleureuse, empathique, sociable, adaptable, courageuse, attentive.',
        'flaws': 'En quête d’approbation, parfois indécise, prompte à cacher son mal-être, évite certains conflits, se laisse déborder par les émotions.',
        'character': [
            'Maggie aime créer du lien, détendre une conversation et trouver ce qui rapproche les gens. On peut confondre cette aisance avec de la légèreté. Elle observe pourtant beaucoup et perçoit les tensions avant qu’elles soient formulées. Sa difficulté consiste à ne pas considérer chaque malaise comme un problème qu’elle doit personnellement réparer.',
            'Elle souhaite une vie qui ne se résume pas aux urgences magiques : des études, des amitiés, des projets et le droit de se tromper. Elle peut sourire pour rassurer ses sœurs alors qu’elle ne va pas bien. Son courage apparaît lorsqu’elle accepte enfin de dire non, de demander de l’aide ou de défendre une décision qui lui appartient.',
        ],
        'history': [
            ('Une vie qu’elle croyait connaître', 'Maggie a grandi auprès de Marisol et de Mel en imaginant un avenir fait de rencontres, d’études et d’expériences ordinaires. Elle cherchait sa place à côté d’une sœur protectrice et très affirmée. La mort de leur mère a brisé cet équilibre au moment même où elle commençait à vouloir vivre davantage pour elle-même.'),
            ('Macy et les vérités de famille', 'Découvrir Macy a été aussi troublant que réconfortant. Maggie a essayé de lui ouvrir la porte sans effacer la douleur de Mel. Les révélations sur Dexter Vaughn, père biologique qu’elle partage avec Macy, ont ensuite modifié ce qu’elle croyait savoir de ses origines. Elles n’ont pas changé son amour pour Mel. Une filiation explique une partie d’une histoire ; elle ne remplace pas les années vécues ensemble.'),
            ('Ressentir sans se perdre', 'L’éveil de son empathie transforme les conversations les plus ordinaires en expériences parfois épuisantes. Maggie doit apprendre que les émotions des autres ne sont pas les siennes et qu’elle ne peut pas guérir chaque peine par sa seule présence. Les premières prémonitions ajoutent une incertitude : faut-il agir sur ce qu’elle a vu, ou risque-t-elle de mal l’interpréter ? Elle apprend à partager ses impressions avec ses sœurs plutôt qu’à porter seule la responsabilité d’un avenir possible.'),
            ('Construire sa place à San Francisco', 'Dans Nexus Arcana, Maggie rejoint Macy et Mel à San Francisco et poursuit un parcours en psychologie. Elle veut comprendre les relations humaines sans confondre son pouvoir avec une formation ou une vérité absolue sur autrui. Elle peut nouer des amitiés dans différentes communautés du forum, mais aucun lien extérieur n’est imposé aux personnages déjà joués. La magie reste une part de sa vie, pas l’ensemble de son identité.'),
            ('La cadette devient partenaire', 'Maggie refuse peu à peu d’être uniquement celle que l’on protège. Elle souhaite participer aux décisions et assumer les conséquences de ses choix. Ses amours, ses amitiés, son activité complémentaire et ses projets restent ouverts. Les trois sœurs sont vivantes et réunies dans cette continuité ; leurs épreuves futures seront celles écrites avec les joueurs de Nexus Arcana.'),
        ],
        'links': [
            ('macy-vaughn', 'Macy Vaughn - Sœur aînée', 'Macy n’a pas grandi avec nous, mais je ne veux pas qu’elle se sente invitée dans sa propre famille. J’aimerais qu’elle sache qu’elle peut parler sans avoir toutes les réponses. Découvrir que nous partageons le même père nous a rapprochées tout en soulevant beaucoup de questions. Je veux apprendre à la connaître au quotidien, pas seulement lorsque la magie nous met en danger.'),
            ('melanie-vera', 'Mélanie Vera - Demi-sœur aînée', 'Mel m’a protégée si longtemps qu’elle oublie parfois de me demander ce que je souhaite. Je sais que ses consignes viennent de la peur de me perdre, mais j’ai besoin de pouvoir choisir. Nous pouvons nous disputer très fort et nous chercher quelques minutes plus tard. Je veux qu’elle me voie comme une partenaire, sans que nous perdions la complicité de notre enfance.'),
            ('harry-greenwood', 'Harry Greenwood - Être de lumière et soutien', 'Harry m’aide à mettre des mots sur ce que la magie bouleverse dans ma vie. J’apprécie qu’il puisse expliquer les choses sans me réduire à la petite sœur qu’il faudrait mettre à l’abri. J’ai besoin de conseils, mais aussi d’encouragements pour essayer par moi-même. Notre confiance se construit dans les entraînements et les difficultés partagées.'),
        ],
    },
}


def paragraph(text):
    return '<p style="margin:0 0 .9rem;line-height:1.85;">' + escape(text) + '</p>'


def section(title, body):
    return '<section style="margin:1rem 0;border:1px solid rgba(124,58,237,.3);border-radius:8px;overflow:hidden;"><div style="padding:.65rem 1rem;background:rgba(124,58,237,.16);"><h2 style="margin:0;font-size:1rem;color:#c4b5fd;">' + escape(title) + '</h2></div><div style="padding:1rem;">' + body + '</div></section>'


def render(profile, image):
    rows = [
        ('Âge', profile['age']), ('Date de naissance', 'Jour et mois au choix · année à harmoniser avec l’âge et la chronologie du forum'),
        ('Sexe', 'Féminin'), ('Orientation sexuelle', profile['orientation']),
        ('Situation sentimentale', 'Au choix · relations à construire en RP'), ('Famille', profile['family']),
        ('Race', profile['race']), ('Camp', 'Bien'), ('Métier', profile['job']),
    ]
    identity = '<dl style="margin:0;">' + ''.join('<dt style="color:#a78bfa;font-size:.8rem;margin-top:.65rem;">' + escape(label) + '</dt><dd style="margin:.15rem 0 0;">' + escape(value) + '</dd>' for label, value in rows) + '</dl>'
    powers = ''.join(paragraph(name + ' — ' + text) for name, text in profile['powers'])
    character = paragraph('Qualités : ' + profile['qualities']) + paragraph('Défauts : ' + profile['flaws']) + ''.join(map(paragraph, profile['character']))
    history = ''.join('<h3 style="font-size:1rem;color:#f5d76e;margin:1.1rem 0 .5rem;">' + escape(title) + '</h3>' + paragraph(text) for title, text in profile['history'])
    return (
        '<div data-vera-scenario="1" style="font-family:Georgia,serif;background:#0d0a1a;color:#e2d9f3;padding:clamp(1rem,4vw,2rem);border-radius:10px;max-width:800px;margin:auto;">'
        '<p style="text-align:center;color:#a78bfa;font-size:.75rem;letter-spacing:.12em;">✦ Nexus Arcana · Livre des Ombres ✦</p>'
        '<div style="display:flex;flex-wrap:wrap;align-items:center;gap:1.5rem;">'
        '<div style="flex:1;min-width:180px;"><h1 style="color:#f5d76e;font-size:2rem;">' + escape(profile['name']) + '</h1>'
        + paragraph(profile['race'] + ' · Bien') + paragraph('« ' + profile['quote'] + ' »') + '</div>'
        '<figure style="margin:0;max-width:100%;"><img src="' + escape(image, quote=True) + '" alt="' + escape(profile['name'], quote=True) + '" style="width:200px;max-width:100%;height:320px;object-fit:cover;border-radius:8px;">'
        '<figcaption style="max-width:200px;font-size:.75rem;line-height:1.5;margin-top:.5rem;">' + escape(profile['name'] + ' — Ft ' + profile['actor']) + '</figcaption></figure></div>'
        + section('I. Identité', identity) + section('II. Pouvoirs magiques & aptitudes', powers)
        + section('III. Âme & caractère', character) + section('IV. Mémoire des âges · Histoire', history)
        + section('V. Repères pour l’interprétation', paragraph('Adaptation Nexus Arcana : Macy, Mélanie et Maggie sont vivantes et réunies à San Francisco. Leur histoire ne reproduit pas obligatoirement tous les événements de la série. Les différences de filiation ne changent pas leur lien de sœurs.') + paragraph('Les âges proposés respectent l’ordre de la fratrie. Leur ajustement, la date de naissance et les détails professionnels se discutent avec le staff. Les romances restent ouvertes. Les capacités majeures, les effets sur le temps et toute évolution doivent respecter le grimoire et la fiche validée.'))
        + '<p style="font-size:.75rem;color:#a99abb;line-height:1.6;margin-top:1.5rem;">Personnages inspirés de Charmed (2018), adaptés pour Nexus Arcana. Portrait conservé : crédit du créateur du visuel à renseigner.</p></div>'
    )


with transaction.atomic():
    topics = {t.slug: t for t in Topic.objects.select_for_update().filter(slug__in=PROFILES, category__slug='scenarios-a-prendre')}
    if set(topics) != set(PROFILES):
        raise RuntimeError('Scénario manquant : aucune modification.')
    posts = {slug: Post.objects.select_for_update().filter(topic=topic).order_by('created_at', 'pk').first() for slug, topic in topics.items()}
    images = {}
    for slug in [*PROFILES, 'harry-greenwood']:
        post = posts.get(slug) or Topic.objects.get(slug=slug).posts.order_by('created_at', 'pk').first()
        match = re.search(r'<img\b[^>]*\bsrc=[\"\x27]([^\"\x27]+)', post.content)
        if not match:
            raise RuntimeError('Portrait introuvable : ' + slug)
        images[slug] = match.group(1)
    if any('data-vera-scenario' in post.content or topics[slug].scenario_link_cards for slug, post in posts.items()):
        raise RuntimeError('Fiches déjà complétées ou liens présents : aucune modification.')
    backup = {slug: {'post_id': posts[slug].pk, 'content': posts[slug].content, 'scenario_link_cards': topic.scenario_link_cards} for slug, topic in topics.items()}
    folder = Path(settings.BASE_DIR) / 'data' / 'scenario_backups'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / ('vera-vaughn-' + timezone.now().strftime('%Y%m%dT%H%M%S%f') + '.json')).write_text(json.dumps(backup, ensure_ascii=False), encoding='utf-8')
    for slug, profile in PROFILES.items():
        post = posts[slug]
        post.content = render(profile, images[slug])
        assert not any(text in post.content for text in ['Montana', 'Nom du pouvoir', 'Prénom NOM'])
        post.save(update_fields=['content', 'is_edited', 'updated_at'])
        topic = topics[slug]
        topic.scenario_link_cards = [{'title': title, 'gif': images[target], 'text': text} for target, title, text in profile['links']]
        topic.save(update_fields=['scenario_link_cards'])
        post.refresh_from_db()
        topic.refresh_from_db()
        assert post.content == render(profile, images[slug])
        assert len(topic.scenario_link_cards) == 3
        print(f'{topic.title} : fiche complète et 3 liens enregistrés et vérifiés.')
