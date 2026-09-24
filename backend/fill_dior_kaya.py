import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic

DATA = [
dict(slug='dior-montana', name='Dior Montana', actor='Viola Davis', race='Sorcière', age='Cinquantaine · âge précis à harmoniser avec la chronologie familiale', family='Mère de Vivienne · compagne de Richard · tante d’Isabella · belle-sœur de Steve et Kaya', job='Libraire spécialisée dans les ouvrages anciens · métier proposé', quote='La magie n’est pas une excuse. Ce qui compte, c’est ce que nous choisissons d’en faire.',
powers=[
('Télékinésie', 'Déplace un petit objet visible à courte distance. La précision exige du calme et la fatigue augmente avec le poids. Aucun contrôle des organes ou du corps d’un autre personnage.'),
('Bouclier magique', 'Forme brièvement un écran devant elle pour amortir un impact limité. Il peut céder ; il ne renvoie pas les attaques et ne protège pas une maison entière.'),
('Perception des enchantements', 'Par contact avec un objet, ressent la présence d’une magie active. Elle n’en connaît pas automatiquement l’origine, la formule ou les intentions du créateur.'),
('Sceau d’alerte', 'Pose un signe temporaire sur une ouverture et perçoit son franchissement tant qu’elle reste à proximité. Une seule ouverture à la fois ; le sceau ne blesse, ne retient et n’identifie personne.')],
character=[
'Qualités : franche, chaleureuse, disciplinée, perspicace, courageuse et fidèle à ses engagements.',
'Défauts : exigeante, obstinée, parfois autoritaire, peu patiente avec les faux-semblants et réticente à montrer son épuisement.',
'Dior occupe une pièce sans avoir besoin de hausser la voix. Elle écoute, pose une question précise et attend une réponse qui ne contourne pas le problème. Cette franchise peut déstabiliser, mais elle ne cherche pas à humilier. Elle préfère un désaccord honnête à une paix obtenue en laissant quelqu’un se mettre en danger.',
'Son affection se traduit par des gestes concrets : préparer un espace calme, relire une note, rester présente pendant un apprentissage difficile. Elle croit à la discipline lorsqu’elle donne de la liberté, pas lorsqu’elle devient un moyen de faire taire. Son principal piège est de se sentir responsable de l’équilibre de tous les autres et d’oublier de demander ce dont elle a besoin.'
],
history=[
('Apprendre sans avoir peur', 'Dior a grandi dans une famille de sorciers où les manifestations magiques pouvaient être évoquées sans honte. Les adultes ne prétendaient pas que tout était facile, mais ils expliquaient les limites et prenaient le temps de recommencer un exercice. Elle en a conservé une conviction durable : un don se comprend mieux dans un cadre patient que dans le secret. Son nom de naissance et les membres de cette première famille restent libres, pour permettre au joueur de développer cet héritage personnel.'),
('Rencontrer Richard', 'Lorsqu’elle rencontre Richard Montana, il traverse une période où son rapport à la magie le fragilise. Dior ne voit ni un homme à sauver à tout prix ni une lignée dont elle devrait avoir peur. Elle lui offre une présence franche et des repères, tout en refusant de décider à sa place. Elle l’aide à reprendre une pratique mesurée ; cette aide ne repose sur aucun pouvoir capable de supprimer une dépendance ou de garantir qu’il ne connaîtra plus de difficultés.'),
('Entrer chez les Montana', 'Porter le nom Montana lui fait découvrir une histoire plus lourde que la sienne, marquée par les affrontements avec les Callaway et les drames transmis d’une génération à l’autre. Elle prend ces blessures au sérieux, mais refuse qu’elles deviennent une justification permanente. Sa place dans la famille se construit au fil des conversations difficiles et des choix quotidiens. Elle n’a pas vécu tous les événements anciens et ne possède pas toutes les réponses.'),
('Élever Vivienne', 'Avec Richard, Dior élève Vivienne dans l’idée que la magie engage une responsabilité. Elle lui transmet des méthodes, mais aussi le droit de questionner ce qu’on lui enseigne. Sa fille apprécie sa franchise et son caractère imposant ; Dior doit toutefois veiller à ne pas transformer cette confiance en attente de perfection. Aujourd’hui adulte, Vivienne reste sa fille sans être une enfant dont elle peut régler la vie.'),
('Une autre voix pour Isabella', 'Isabella trouve auprès d’elle une approche plus ouverte que celle de Steve. Dior participe à son apprentissage et comprend son envie d’explorer, tout en lui rappelant qu’une expérience engage parfois d’autres personnes. Elle ne souhaite ni se substituer à ses parents ni encourager une compétition entre les deux cousines. Avec Kaya, elle peut chercher une manière d’accompagner les jeunes femmes qui laisse de la place à leurs différences.'),
('Ce qu’elle veut encore construire', 'À San Francisco, Dior souhaite aussi disposer d’une vie qui ne se résume pas à contenir les inquiétudes familiales. Une librairie d’ouvrages anciens constitue une activité proposée, propice aux rencontres et aux recherches. Un carnet égaré, une demande d’aide ou un désaccord sur la transmission d’un savoir peuvent lancer ses premiers sujets. Sa force narrative tient à son expérience et à ses choix ; elle commence, comme les autres personnages, avec les quatre pouvoirs de base décrits ici.')],
links=[('Richard Montana', 'Compagnon', 'Je t’ai rencontré dans une période difficile et j’ai choisi de rester, sans promettre de porter ta vie à ta place. Je crois à ta capacité de choisir une magie mesurée. Notre confiance suppose que nous puissions parler de tes difficultés autant que de mes limites.'), ('Vivienne Montana', 'Fille', 'Je suis fière de ta rigueur et de ton désir de protéger les nôtres. Je veux aussi que tu puisses te tromper, poser tes limites et choisir ta propre vie. Tu n’as pas à réparer seule l’histoire de cette famille.'), ('Isabella Montana', 'Nièce', 'Ta curiosité me rappelle que la magie peut être une joie. Je t’ai aidée à apprivoiser tes dons et je continuerai à te demander de réfléchir à leurs conséquences. Je peux entendre ton désaccord sans approuver toutes tes décisions.'), ('Kaya Montana', 'Belle-sœur', 'Tu entends ce que beaucoup d’entre nous ne savent même pas écouter. Nous n’avons pas les mêmes dons, mais nous partageons le souci de laisser nos filles grandir. Je peux m’appuyer sur toi sans te confier toutes les blessures de la famille.'), ('Steve Montana', 'Beau-frère', 'Je respecte ce que ton histoire t’a coûté. Je ne crois pourtant pas qu’Isabella sera protégée en restant dans l’ignorance. Nous devons pouvoir discuter de son apprentissage sans la placer au milieu de nos désaccords.')]),
dict(slug='kaya-montana', name='Kaya Montana', actor='Lucy Liu', race='Humaine médium', age='Cinquantaine · âge précis à harmoniser avec la chronologie familiale', family='Mère d’Isabella · compagne de Steve · tante de Vivienne · belle-sœur de Richard et Dior', job='Archiviste · métier proposé', quote='Écouter les morts ne doit jamais nous faire oublier les vivants.',
powers=[
('Perception des esprits', 'Ressent une présence désincarnée à proximité, parfois sous la forme d’une silhouette fugitive. Elle ne détecte pas tous les êtres surnaturels et ne connaît pas automatiquement l’identité de l’esprit.'),
('Clairaudience médiumnique', 'Peut entendre un message bref d’un esprit présent qui parvient à communiquer. Les paroles peuvent être confuses ou mensongères ; elle ne convoque pas un défunt à volonté et ne lit pas les pensées des vivants.'),
('Psychométrie', 'Au contact d’un objet marqué par une émotion forte, reçoit une impression ou une image fragmentaire de son passé. Aucun récit complet ni preuve infaillible ; les informations liées à une intrigue sont fixées avec son maître du jeu.'),
('Rêves de présage', 'Reçoit occasionnellement un rêve symbolique annonçant un danger possible. Le don n’est pas déclenché à volonté et ne donne ni date certaine ni avenir immuable. Toute révélation concernant un autre personnage se convient avec son joueur.')],
character=[
'Qualités : douce, attentive, lucide, patiente, loyale et discrètement courageuse.',
'Défauts : évite parfois les affrontements, absorbe trop les soucis des autres, hésite à demander de l’aide et peut devenir inflexible lorsqu’une limite a été franchie.',
'La douceur de Kaya n’est pas une absence de caractère. Elle laisse les autres terminer leur phrase, remarque les silences et choisit ses mots avec soin. Lorsqu’elle dit non, elle le fait rarement sur un coup de tête. Cette fermeté tranquille surprend ceux qui avaient pris son écoute pour un accord.',
'Elle possède un humour discret et tient aux habitudes ordinaires qui la ramènent au présent. Ses perceptions la rendent attentive à ce qui demeure après un drame, mais elle refuse de réduire une personne à sa douleur. À force de servir d’intermédiaire, elle risque cependant de retarder les conversations que les autres devraient avoir directement.'
],
history=[
('Une sensibilité sans mode d’emploi', 'Kaya n’est pas une sorcière. Avant de rejoindre les Montana, elle connaissait déjà des perceptions qu’elle ne savait pas toujours nommer : une présence ressentie dans une pièce vide, quelques mots sans interlocuteur visible, une impression troublante au contact d’un objet. Elle a appris à distinguer une sensation d’une certitude et à ne pas promettre des réponses qu’elle ne pouvait pas donner. Son enfance et son nom de naissance restent à personnaliser.'),
('Trouver des repères', 'Plutôt que chercher à multiplier les expériences, elle construit des habitudes qui l’aident à garder pied dans le quotidien. Elle note ses impressions, accepte qu’une vision puisse rester obscure et sait interrompre une recherche lorsqu’elle est épuisée. Son activité d’archiviste est proposée comme prolongement de ce tempérament patient : retrouver une date ou une lettre exige un travail réel, même lorsqu’un objet lui laisse une sensation particulière.'),
('Partager la vie de Steve', 'Sa relation avec Steve l’amène au cœur d’une famille dont la magie a laissé de profondes blessures. Kaya comprend son envie de protéger les siens et les raisons de sa méfiance. Elle ne partage pourtant pas l’idée que tout héritage surnaturel doive être tenu à distance. Ses propres dons lui ont appris qu’ignorer une expérience ne suffit pas à la faire disparaître. Leur vie commune repose aussi sur cette différence qu’ils doivent apprendre à discuter.'),
('Accompagner Isabella', 'Isabella trouve en sa mère une présence plus tendre et un espace où parler sans commencer par se défendre. Kaya soutient la nécessité de règles, mais souhaite qu’elles soient expliquées. Elle ne donne pas systématiquement raison à sa fille contre Steve : elle l’aide à formuler ses envies et à reconnaître les risques. Elle voudrait qu’Isabella puisse explorer sa nature sans devoir prouver à chaque instant qu’elle a raison d’être sorcière.'),
('Une place entière dans la famille', 'Vivienne se tourne également vers Kaya pour chercher du soutien ou un éclairage différent. Dior reconnaît la valeur de son écoute, et Richard sait que ses dons de médium ne font pas d’elle une étrangère au surnaturel. Kaya n’a pas à rivaliser avec leurs pouvoirs pour compter. Elle refuse néanmoins de devenir un passage obligé vers les morts de la famille : ses perceptions sont limitées, et certains silences ne peuvent pas être levés par une séance.'),
('Choisir ce qu’elle transmet', 'À San Francisco, Kaya souhaite préserver des liens vivants tout en laissant chacun répondre de ses décisions. Un objet familial confié aux archives, un rêve ambigu ou une confidence d’Isabella peuvent amorcer son jeu. Aucun de ces signes ne résout à lui seul une enquête. Elle reste une humaine, vulnérable aux blessures et à la fatigue, avec quatre dons médiumniques de base ; elle ne dispose ni de la magie des sorcières ni d’un accès permanent à l’au-delà.')],
links=[('Steve Montana', 'Compagnon', 'Je comprends ta peur de voir notre famille souffrir encore. Je veux que nous protégions Isabella en lui donnant des repères qu’elle puisse comprendre. Nous pouvons être solidaires sans partager exactement la même vision de la magie.'), ('Isabella Montana', 'Fille', 'Tu peux venir me parler sans préparer ta défense. Je ne te promets pas de toujours approuver, mais je t’écouterai. Je veux t’aider à trouver ta mesure, pas choisir ta vie à ta place.'), ('Vivienne Montana', 'Nièce', 'Tu portes beaucoup de responsabilités sur tes épaules. Je suis là pour t’écouter et t’offrir un regard différent, sans te donner des certitudes que mes dons ne possèdent pas. Tu as le droit de demander du soutien.'), ('Dior Montana', 'Belle-sœur', 'Ta franchise me pousse parfois à dire ce que je remettais à plus tard. Nous cherchons toutes les deux à accompagner nos filles sans les enfermer. Je peux compter sur ton expérience, et tu peux aussi déposer tes inquiétudes auprès de moi.'), ('Richard Montana', 'Beau-frère', 'Ton parcours me rappelle qu’une personne ne se résume pas à ses moments les plus difficiles. Je respecte tes efforts. Mes perceptions ne me donnent pas le droit de fouiller ton passé ni de parler à ta place ; nous pouvons construire notre confiance autrement.')]),
]

def p(text):
    return '<p style="margin:0 0 .9rem;line-height:1.85;">' + escape(text) + '</p>'

def section(title, body):
    return '<section style="margin:1rem 0;border:1px solid rgba(124,58,237,.3);border-radius:8px;overflow:hidden;"><div style="padding:.65rem 1rem;background:rgba(124,58,237,.16);"><h2 style="margin:0;font-size:1rem;color:#c4b5fd;">' + escape(title) + '</h2></div><div style="padding:1rem;">' + body + '</div></section>'

class CheckHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
    def handle_starttag(self, tag, attrs):
        if tag not in ('img', 'br', 'hr', 'input', 'meta', 'link'):
            self.stack.append(tag)
    def handle_endtag(self, tag):
        assert self.stack and self.stack.pop() == tag, 'Invalid nesting: ' + tag

with transaction.atomic():
    topics = {t.slug: t for t in Topic.objects.select_for_update().filter(slug__in=['dior-montana','kaya-montana','vivienne-montana','isabella-montana'], category__slug='scenarios-a-prendre')}
    assert len(topics) == 4
    posts = {slug: t.posts.select_for_update().order_by('created_at','pk').first() for slug,t in topics.items()}
    images = {topics[slug].title: re.search(r'<img\b[^>]*src=[\"\x27]([^\"\x27]+)', post.content).group(1) for slug,post in posts.items()}
    for t in topics.values():
        for card in t.scenario_link_cards:
            name = card.get('title','').split(' - ')[0]
            if card.get('gif'):
                images[name] = card['gif']
    backup = []
    for d in DATA:
        t, post = topics[d['slug']], posts[d['slug']]
        assert post and 'Nom du pouvoir' in post.content and not t.scenario_link_cards, 'Fiche déjà modifiée : vérifier avant remplacement.'
        backup.append(dict(topic_id=t.pk, post_id=post.pk, content=post.content, scenario_link_cards=t.scenario_link_cards))
    folder = Path(settings.BASE_DIR) / 'data/scenario_backups'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / ('dior-kaya-' + timezone.now().strftime('%Y%m%dT%H%M%S%f') + '.json')).write_text(json.dumps(backup,ensure_ascii=False),encoding='utf-8')
    for d in DATA:
        t, post = topics[d['slug']], posts[d['slug']]
        portrait = re.search(r'<img\b[^>]*src=[\"\x27]([^\"\x27]+)',post.content).group(1)
        credit = re.search(r'<p class="scenario-credit-line"[^>]*>.*?</p>',post.content,re.S)
        assert credit, 'Crédit absent'
        content = '<div data-montana-parent-scenario="1" style="font-family:Georgia,serif;background:#0d0a1a;color:#e2d9f3;padding:clamp(1rem,4vw,2rem);border-radius:10px;max-width:800px;margin:auto;">'
        content += '<p style="text-align:center;color:#a78bfa;font-size:.75rem;letter-spacing:.12em;">✦ Nexus Arcana · Livre des Ombres ✦</p><div style="display:flex;flex-wrap:wrap;align-items:center;gap:1.5rem;"><div style="flex:1;min-width:180px;"><h1 style="color:#f5d76e;font-size:2rem;">' + escape(d['name']) + '</h1>' + p(d['race'] + ' · Bien') + p('« ' + d['quote'] + ' »') + '</div><figure style="margin:0;max-width:100%;"><img src="' + escape(portrait,quote=True) + '" alt="' + escape(d['name']) + '" style="width:200px;max-width:100%;height:320px;object-fit:cover;border-radius:8px;"><figcaption style="max-width:200px;font-size:.75rem;margin-top:.5rem;line-height:1.6;">' + escape(d['name'] + ' — Ft ' + d['actor'] + ' (négociable après échange avec le staff)') + '</figcaption></figure></div>'
        identity = [('Âge',d['age']),('Date de naissance','Jour, mois et année à fixer selon la chronologie du forum'),('Sexe','Féminin'),('Orientation sexuelle','Au choix du joueur'),('Famille',d['family']),('Situation sentimentale','Relation familiale établie ; statut marital précis à convenir avec les joueurs concernés'),('Race',d['race']),('Camp','Bien'),('Résidence','San Francisco'),('Métier',d['job'])]
        content += section('I. Identité','<dl style="margin:0;">' + ''.join('<dt style="color:#a78bfa;font-size:.8rem;margin-top:.65rem;">' + escape(k) + '</dt><dd style="margin:.15rem 0 0;">' + escape(v) + '</dd>' for k,v in identity) + '</dl>')
        content += section('II. Pouvoirs de base', ''.join('<div data-base-power="1"><h3 style="color:#f5d76e;font-size:1rem;">' + escape(name) + '</h3>' + p(desc) + '</div>' for name,desc in d['powers']))
        content += section('III. Âme et caractère',''.join(map(p,d['character'])))
        content += section('IV. Mémoire des âges · Histoire',''.join('<h3 style="color:#f5d76e;font-size:1rem;">' + escape(name) + '</h3>' + p(desc) for name,desc in d['history']))
        content += section('V. Repères pour l’interprétation',p('Les liens familiaux reprennent ceux des fiches de Vivienne et d’Isabella. L’âge précis, le métier proposé et les détails du passé personnel peuvent être adaptés avec le staff. Les quatre dons décrits restent des pouvoirs de départ aux effets limités ; l’expérience du personnage ne lui accorde pas de capacités supplémentaires.') + p('Les décisions, sentiments et réactions des autres personnages appartiennent à leurs joueurs. Les secrets familiaux et les révélations importantes se construisent ensemble en RP.'))
        content += credit.group(0) + '</div>'
        check = CheckHTML()
        check.feed(content)
        assert not check.stack and content.count('data-base-power="1"') == 4
        assert 'Nom du pouvoir' not in content and 'Vivienne Montana est née' not in content
        cards = [dict(title=name+' — '+relation, gif=images.get(name,''),text=text) for name,relation,text in d['links']]
        post.content = content
        post.save(update_fields=['content','is_edited','updated_at'])
        t.scenario_link_cards = cards
        t.save(update_fields=['scenario_link_cards'])
        post.refresh_from_db()
        t.refresh_from_db()
        assert post.content == content and t.scenario_link_cards == cards
        print(d['name'] + ' : fiche, 4 pouvoirs de base et 5 liens enregistrés ; balisage vérifié.')
