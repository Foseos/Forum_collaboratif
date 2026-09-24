import json
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Topic, Post, SitePage

RULE = '''<section data-power-progression="4-2" style="margin:1rem 0;padding:1rem;border:1px solid rgba(245,215,110,.35);border-radius:8px;line-height:1.8;">
<h2 style="margin:0 0 .6rem;color:#f5d76e;font-size:1rem;">Pouvoirs de départ et évolutions</h2>
<p>Chaque personnage commence avec <strong>4 pouvoirs de base</strong>, cohérents avec sa race et son histoire et validés dans sa fiche.</p>
<p>Chacun de ces quatre pouvoirs peut être amélioré <strong>deux fois au maximum</strong>. Chaque amélioration nécessite un <strong>achat d’évolution à la boutique magique</strong> et sa validation par le staff avant utilisation en RP.</p>
<p><strong>Pour chaque pouvoir : base → évolution 1 achetée → évolution 2 achetée.</strong> Un achat améliore un seul pouvoir d’un seul palier. La seconde évolution d’un pouvoir nécessite d’avoir acquis sa première évolution.</p>
<p>Un personnage dispose ainsi de <strong>4 pouvoirs de base et de 8 améliorations possibles au total</strong>. Une évolution développe un pouvoir existant ; elle n’ajoute pas un cinquième pouvoir de base. Les évolutions doivent être justifiées en jeu et respecter les limites du grimoire.</p>
</section>'''

def append_rule(content):
    if 'data-power-progression="4-2"' in content:
        return content
    before, closing, after = content.rpartition('</div>')
    return before + RULE + closing + after if closing else content + RULE

with transaction.atomic():
    slugs = ['reglement-officiel-du-forum', 'liste-des-pouvoirs-magiques', 'catalogue-boutique-magique']
    posts = {}
    for slug in slugs:
        topic = Topic.objects.get(slug=slug)
        posts[slug] = Post.objects.select_for_update().filter(topic=topic).order_by('created_at', 'pk').first()
        if posts[slug] is None:
            raise RuntimeError('Contenu manquant : ' + slug)
    page = SitePage.objects.select_for_update().get(slug='reglement-du-forum')
    backup = {slug: {'post_id': post.pk, 'content': post.content} for slug, post in posts.items()}
    backup['reglement_page'] = page.content
    folder = Path(settings.BASE_DIR) / 'data' / 'rules_backups'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / (timezone.now().strftime('%Y%m%dT%H%M%S%f') + '.json')).write_text(json.dumps(backup, ensure_ascii=False), encoding='utf-8')
    for slug, post in posts.items():
        text = post.content
        if slug == 'liste-des-pouvoirs-magiques':
            text = text.replace('trois pouvoirs de base maximum à la création', 'quatre pouvoirs de base à la création, avec deux évolutions achetées au maximum pour chacun')
            text = text.replace("un nouveau pouvoir se gagne par une évolution jouée, un événement ou une validation du staff ; il ne se débloque pas seulement par ancienneté.", 'chaque personnage commence avec quatre pouvoirs de base. Chacun peut recevoir deux évolutions, achetées à la boutique et validées par le staff ; aucune évolution automatique par ancienneté.')
        if slug == 'catalogue-boutique-magique':
            text = text.replace('Améliorations &amp; Nouveaux Pouvoirs', 'Évolutions des quatre pouvoirs de base')
            text = text.replace('Débloquez de nouveaux pouvoirs ou améliorez des pouvoirs existants.', 'Améliorez vos quatre pouvoirs de base, deux fois chacun au maximum.')
            text = text.replace('amélioration / nouveau pouvoir', 'achat d’évolution')
            text = text.replace('Premier ajout ou amélioration de pouvoir inné.', 'Première évolution achetée pour l’un des quatre pouvoirs de base.')
            text = text.replace("6e et au-delà — à l'infini", '6e à 8e achats d’évolution — maximum')
            text = text.replace('Chaque nouvel ajout coûte 300 Arcana Flouz de plus que le précédent, sans limite.', 'Chaque achat coûte 300 Arcana Flouz de plus que le précédent : 1 800, 2 100 puis 2 400 Arcana Flouz. Maximum : huit achats par personnage et deux évolutions par pouvoir.')
        post.content = append_rule(text)
        post.save(update_fields=['content', 'is_edited', 'updated_at'])
        post.refresh_from_db()
        assert 'data-power-progression="4-2"' in post.content
        print(slug + ' : règle enregistrée et vérifiée.')
    if page.content.strip():
        page.content = append_rule(page.content)
        page.save(update_fields=['content', 'updated_at'])
        print('Page personnalisée du règlement mise à jour.')
