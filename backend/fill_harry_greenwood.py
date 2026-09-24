import json
import re
from html import escape
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Post, Topic


def paragraph(text):
    return '<p style="margin:0 0 .9rem;line-height:1.85;">' + escape(text) + '</p>'


def section(title, body):
    return '<section style="margin:1rem 0;border:1px solid rgba(124,58,237,.3);border-radius:8px;overflow:hidden;"><div style="padding:.65rem 1rem;background:rgba(124,58,237,.16);"><h2 style="margin:0;font-size:1rem;color:#c4b5fd;">' + escape(title) + '</h2></div><div style="padding:1rem;">' + body + '</div></section>'


identity = [
    ('Âge', 'Apparence d’un homme d’une quarantaine d’années · plusieurs décennies d’existence surnaturelle'),
    ('Date de naissance', 'Date précise à fixer avec le staff selon la chronologie retenue pour sa vie humaine'),
    ('Origines', 'Britanniques · établi à San Francisco'),
    ('Sexe', 'Masculin'), ('Orientation sexuelle', 'Au choix du joueur'),
    ('Situation sentimentale', 'Au choix · aucune relation imposée avec Macy'),
    ('Race', 'Être de lumière'), ('Camp', 'Bien'),
    ('Métier', 'Enseignant dans le supérieur à San Francisco · discipline à préciser avec le joueur'),
    ('Rôle surnaturel', 'Guide et protecteur des sœurs Vera-Vaughn'),
]

powers = [
    ('Orbing', 'Déplacement surnaturel par dissolution et réapparition. Harry peut rejoindre une destination accessible et connue dans les limites de sa connexion magique. Le transport d’une personne consentante reste limité et fatigant. Les barrières adaptées, les protections de lieux et les règles des dimensions peuvent empêcher le passage ; aucun voyage temporel libre.'),
    ('Guérison', 'Soigne par contact des blessures compatibles avec sa nature et sa mission. La gravité des blessures, sa concentration et ses réserves influencent le résultat. Il ne peut pas ressusciter, effacer toutes les malédictions ou remettre immédiatement un groupe entier sur pied. Les conséquences importantes d’une blessure se décident avec les joueurs et le maître du jeu.'),
    ('Connexion aux protégées', 'Perçoit un appel ou une détresse de ses protégées lorsque leur lien peut s’exprimer. Il ne lit pas leurs pensées et ne connaît pas en permanence leurs gestes ou leur position exacte. Une protection ou une perturbation peut brouiller la connexion. Les informations concernant un événement sont déterminées avec son maître du jeu.'),
    ('Savoirs magiques et accompagnement', 'Reconnaît des signes surnaturels, transmet des méthodes de protection et aide à préparer les recherches et les rituels. Ses connaissances ne sont pas universelles, particulièrement face aux lignées du crossover. Il ne possède pas automatiquement les pouvoirs des sorcières qu’il accompagne et ne remplace pas leur participation au pouvoir collectif.'),
]

character = [
    'Qualités : patient, cultivé, attentif, loyal, courageux, méthodique, doté d’un humour discret.',
    'Défauts : secret, parfois paternaliste, trop attaché aux procédures, enclin à la culpabilité, réticent à parler de ses propres besoins.',
    'Harry garde une politesse presque cérémonieuse, y compris lorsque la situation devient absurde. Une remarque sèche, un silence appuyé ou une tasse de thé lui permettent parfois de reprendre contenance. Cette réserve n’est pas de l’indifférence : il s’attache profondément et redoute de laisser ses sentiments compromettre ceux qu’il veut protéger.',
    'Son réflexe est d’expliquer, d’organiser et de prévoir une issue. Il peut cependant oublier qu’un conseil n’est pas un ordre et qu’une protégée n’est pas une enfant. Les trois sœurs le forcent à remettre ses certitudes en question. Il devient plus fiable lorsqu’il accepte de dire « je ne sais pas » plutôt que dissimuler un doute derrière son rôle de guide.',
    'Il supporte mal l’idée de ne pas arriver à temps. Cette peur peut le pousser à s’épuiser ou à cacher une difficulté. Apprendre à recevoir de l’aide et à exister autrement que par sa mission représente une part essentielle de son évolution.',
]

history = [
    ('Une vie derrière un nom', 'Harry Greenwood n’a pas toujours été un être de lumière. Sa vie humaine appartient à une histoire britannique dont il ne possède plus un récit parfaitement continu. Des souvenirs, des habitudes et des impressions subsistent sans toujours lui permettre de comprendre ce qu’ils signifient. Dans cette adaptation, les détails de cette existence et leur découverte restent des pistes à construire avec le staff, plutôt qu’une liste de révélations imposées au joueur.'),
    ('Protéger comme raison d’être', 'Devenu guide de sorcières, Harry a appris à observer les menaces, à transmettre des connaissances et à intervenir lorsque ses protégées ont besoin de lui. Il s’est longtemps appuyé sur les règles du monde magique pour donner un sens à une existence dont une partie lui échappait. Cette discipline lui apporte de la stabilité, mais elle ne répond pas à toutes les situations : une instruction peut être incomplète, une autorité se tromper, et une personne protégée refuser le chemin que l’on avait imaginé pour elle.'),
    ('Les Vera-Vaughn', 'La mort de Marisol et la réunion de Macy, Mélanie et Maggie placent Harry auprès de trois femmes qui n’ont ni les mêmes souvenirs ni la même façon d’affronter le danger. Il les accompagne dans la découverte de leur héritage et de leur coopération magique. Très vite, il comprend qu’une leçon ne suffira pas à faire d’elles un groupe uni. Il doit écouter leur deuil, leurs désaccords et leur besoin de décider elles-mêmes de ce qu’elles souhaitent devenir.'),
    ('Trois façons de lui faire confiance', 'Macy exige des explications et refuse de renoncer à son esprit scientifique. Mélanie questionne les règles et lui rappelle que protéger ne signifie pas diriger. Maggie cherche des repères, mais veut être reconnue comme une partenaire capable d’apprendre et de choisir. Harry ne peut pas leur offrir le même accompagnement. Il apprend à adapter sa présence, à avouer les limites de ses connaissances et à construire une confiance qui ne repose pas uniquement sur son statut.'),
    ('San Francisco', 'Dans la continuité de Nexus Arcana, Harry reste un être de lumière et accompagne les trois sœurs vivantes à San Francisco. Il y reprend une activité d’enseignement qui lui donne une place dans la vie quotidienne de la ville. Les rencontres entre lignées et traditions surnaturelles lui montrent que son expérience n’est qu’une partie d’un monde plus vaste. Il peut chercher des échanges avec d’autres protecteurs, mais aucune amitié, alliance ou autorité sur les personnages existants n’est présumée acquise.'),
    ('Ce qu’il reste à découvrir', 'Les perturbations magiques de la ville peuvent éprouver sa connexion aux sœurs et remettre en question ses habitudes. Son passé humain, ses propres désirs et la frontière entre devoir et attachement offrent autant de pistes de jeu. Une proximité particulière avec Macy peut se développer si les deux joueurs le souhaitent ; elle n’est ni obligatoire ni déjà établie. Les changements de nature et les événements de fin de série ne sont pas imposés à cette version du personnage.'),
]

links = [
    ('macy-vaughn', 'Macy', 'Macy Vaughn - Protégée et confiance à construire', 'Macy ne se contente jamais d’une réponse vague, et je respecte cette exigence même lorsqu’elle me met en difficulté. Sa rigueur nous aide à regarder autrement les problèmes magiques. Je souhaite qu’elle sache que son héritage démoniaque ne la condamne pas et qu’elle peut demander de l’aide sans perdre son indépendance. Une éventuelle évolution sentimentale reste à construire ensemble, sans engagement imposé.'),
    ('melanie-vera', 'Mélanie', 'Mélanie Vera - Protégée et partenaire exigeante', 'Mel conteste mes règles, parfois avant que j’aie fini de les expliquer. Elle me rappelle pourtant une chose essentielle : mon rôle est de l’accompagner, pas de choisir à sa place. Sa loyauté envers ses sœurs mérite mieux que des consignes sans explication. Je veux construire notre confiance sur la franchise, même lorsque nous ne sommes pas d’accord sur la manière d’agir.'),
    ('maggie-vera', 'Maggie', 'Maggie Vera - Protégée et apprentissage partagé', 'Maggie ressent beaucoup et tente souvent de rassurer les autres avant de parler de ses propres difficultés. Je veux lui donner des repères pour apprivoiser ses dons sans lui faire croire qu’elle est responsable de toutes les émotions qui l’entourent. Elle n’est pas seulement la cadette à protéger. Je tiens à lui laisser essayer, poser ses limites et prendre sa place dans nos décisions.'),
]

with transaction.atomic():
    topic = Topic.objects.select_for_update().get(slug='harry-greenwood', category__slug='scenarios-a-prendre')
    post = Post.objects.select_for_update().filter(topic=topic).order_by('created_at', 'pk').first()
    if not post or 'data-harry-scenario' in post.content or topic.scenario_link_cards:
        raise RuntimeError('Fiche absente ou déjà complétée : aucune modification.')
    image_match = re.search(r'<img\b[^>]*\bsrc=[\"\x27]([^\"\x27]+)', post.content)
    if not image_match:
        raise RuntimeError('Portrait introuvable.')
    sisters = list(Topic.objects.filter(slug__in=[item[0] for item in links]))
    cards = []
    for slug, keyword, title, text in links:
        target = next(t for t in sisters if t.slug == slug)
        # Reuse the most recently saved relationship image where available.
        image = next((c['gif'] for sister in sisters for c in sister.scenario_link_cards if keyword in c.get('title', '') and c.get('gif')), None)
        if not image:
            image = re.search(r'<img\b[^>]*\bsrc=[\"\x27]([^\"\x27]+)', target.posts.order_by('created_at').first().content).group(1)
        cards.append({'title': title, 'gif': image, 'text': text})
    original = {'topic_id': topic.pk, 'post_id': post.pk, 'content': post.content, 'scenario_link_cards': topic.scenario_link_cards}
    folder = Path(settings.BASE_DIR) / 'data' / 'scenario_backups'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / ('harry-greenwood-' + timezone.now().strftime('%Y%m%dT%H%M%S%f') + '.json')).write_text(json.dumps(original, ensure_ascii=False), encoding='utf-8')
    identity_html = '<dl style="margin:0;">' + ''.join('<dt style="color:#a78bfa;font-size:.8rem;margin-top:.65rem;">' + escape(label) + '</dt><dd style="margin:.15rem 0 0;">' + escape(value) + '</dd>' for label, value in identity) + '</dl>'
    history_html = ''.join('<h3 style="color:#f5d76e;font-size:1rem;margin:1.1rem 0 .5rem;">' + escape(title) + '</h3>' + paragraph(text) for title, text in history)
    content = '<div data-harry-scenario="1" style="font-family:Georgia,serif;background:#0d0a1a;color:#e2d9f3;padding:clamp(1rem,4vw,2rem);border-radius:10px;max-width:800px;margin:auto;">'
    content += '<p style="text-align:center;color:#a78bfa;font-size:.75rem;letter-spacing:.12em;">✦ Nexus Arcana · Livre des Ombres ✦</p><div style="display:flex;flex-wrap:wrap;align-items:center;gap:1.5rem;"><div style="flex:1;min-width:180px;"><h1 style="color:#f5d76e;font-size:2rem;">Harry Greenwood</h1>'
    content += paragraph('Être de lumière · Bien') + paragraph('« Être un guide ne signifie pas connaître toutes les réponses. Cela signifie ne pas abandonner ceux qui les cherchent. »')
    content += '</div><figure style="margin:0;max-width:100%;"><img src="' + escape(image_match.group(1), quote=True) + '" alt="Harry Greenwood" style="width:200px;max-width:100%;height:320px;object-fit:cover;border-radius:8px;"><figcaption style="max-width:200px;font-size:.75rem;margin-top:.5rem;">Harry Greenwood — Ft Rupert Evans</figcaption></figure></div>'
    content += section('I. Identité', identity_html)
    content += section('II. Pouvoirs magiques & aptitudes', ''.join(paragraph(name + ' — ' + text) for name, text in powers))
    content += section('III. Âme & caractère', ''.join(map(paragraph, character)))
    content += section('IV. Mémoire des âges · Histoire', history_html)
    content += section('V. Repères pour l’interprétation', paragraph('Adaptation Nexus Arcana, cohérente avec les fiches de Macy, Mélanie et Maggie. Harry reste leur être de lumière ; il ne dispose d’aucune autorité automatique sur les autres protecteurs ou communautés de San Francisco.') + paragraph('Le passé humain, les détails de sa couverture professionnelle et la vie sentimentale sont à développer avec les joueurs et le staff. Les évolutions de pouvoirs suivent le grimoire. Aucun effacement de mémoire, aucune résurrection ni transformation de nature ne découle librement de son rôle de guide.'))
    content += '<p style="font-size:.75rem;color:#a99abb;line-height:1.6;">Personnage inspiré de Charmed (2018), adapté pour Nexus Arcana. Auteur du portrait non indiqué dans la fiche d’origine.</p></div>'
    assert not any(term in content for term in ['Montana', 'Nom du pouvoir', 'Prénom NOM'])
    post.content = content
    post.save(update_fields=['content', 'is_edited', 'updated_at'])
    topic.scenario_link_cards = cards
    topic.save(update_fields=['scenario_link_cards'])
    post.refresh_from_db()
    topic.refresh_from_db()
    assert post.content == content and topic.scenario_link_cards == cards
    print('Harry Greenwood : fiche complète et 3 liens enregistrés et vérifiés.')
