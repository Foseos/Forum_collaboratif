from apps.users.models import User
from apps.forum.models import Topic, Post

t = Topic.objects.filter(slug='demande-de-partenaire-de-rp').first()
p = t.posts.order_by('created_at').first()

F = "font-family: Georgia, 'Times New Roman', serif"

html = ''
html += '<div style="%s; background:#0d0a1a; color:#e2d9f3; padding:2rem; border-radius:10px; border:1px solid rgba(124,58,237,0.3); max-width:760px; margin:0 auto;">\n\n' % F

# En-tête épuré
html += '<p style="margin:0 0 0.3rem; font-size:0.55rem; letter-spacing:0.4em; text-transform:uppercase; color:#6d28d9; text-align:center;">\u2726 Nexus Arcana \u2726</p>\n'
html += '<h1 style="margin:0 0 0.5rem; font-size:1.6rem; font-weight:normal; font-style:italic; color:#f5d76e; text-align:center;">Recherche de Partenaire RP</h1>\n'
html += '<p style="margin:0 0 2rem; font-size:0.78rem; color:#4b3a6b; text-align:center; letter-spacing:0.04em;">R\u00e9pondez \u00e0 ce sujet en copiant le mod\u00e8le ci-dessous</p>\n'

# Séparateur
html += '<div style="border-top:1px solid rgba(124,58,237,0.2); margin-bottom:1.75rem;"></div>\n\n'

# Intro courte
html += '<p style="margin:0 0 1.75rem; font-size:0.85rem; color:#a78bfa; line-height:1.8; text-align:center; font-style:italic;">'
html += 'Vous cherchez un partenaire d\u2019\u00e9criture\u00a0? Partagez votre annonce en utilisant le mod\u00e8le suivant.'
html += '</p>\n\n'

# ── Modèle épuré ──────────────────────────────────────────────────
html += '<div style="border:1px solid rgba(245,215,110,0.3); border-radius:8px; padding:1.5rem; background:rgba(13,10,26,0.5);">\n'
html += '<p style="margin:0 0 1.2rem; font-size:0.58rem; letter-spacing:0.3em; text-transform:uppercase; color:#f5d76e;">\u2728 Mod\u00e8le \u00e0 copier</p>\n'

tpl = ''
tpl += '<div style="%s; background:#0d0a1a; color:#e2d9f3; padding:1.5rem; border-radius:8px; border:1px solid rgba(124,58,237,0.25); max-width:680px; margin:0 auto;">\n\n' % F

# Titre perso
tpl += '<h2 style="margin:0 0 0.2rem; font-size:1.5rem; font-weight:normal; font-style:italic; color:#f5d76e; text-align:center;">Pr\u00e9nom NOM</h2>\n'
tpl += '<p style="margin:0 0 1.2rem; font-size:0.75rem; color:#6d5fa0; text-align:center; letter-spacing:0.08em;">Race \u00b7 Camp \u00b7 Faction</p>\n'
tpl += '<div style="border-top:1px solid rgba(124,58,237,0.15); margin-bottom:1.2rem;"></div>\n\n'

# Bloc infos en liste simple
def line(label, placeholder):
    return (
        '<p style="margin:0 0 0.55rem; font-size:0.85rem; color:#e2d9f3;">'
        '<span style="color:#6d5fa0; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em;">%s</span><br>'
        '<span style="color:#c4b5d4;">%s</span>'
        '</p>\n'
    ) % (label, placeholder)

tpl += line('Pouvoirs', '[Listez vos 2\u20133 pouvoirs principaux]')
tpl += line('Type de RP souhait\u00e9', '[Action / Romance / Drame / Enqu\u00eate / Libre]')
tpl += line('Ambiance', '[Sombre / L\u00e9g\u00e8re / \u00c9quilibr\u00e9e]')
tpl += line('Personnages recherch\u00e9s', '[Toute race, camp pr\u00e9cis, ou d\u00e9tailler]')
tpl += line('Disponibilit\u00e9s & rythme', '[Jours / horaires \u2014 longueur moyenne des posts]')

# Idée scénario
tpl += '<div style="border-top:1px solid rgba(124,58,237,0.12); margin:1rem 0 0.85rem;"></div>\n'
tpl += '<p style="margin:0 0 0.3rem; font-size:0.72rem; color:#6d5fa0; text-transform:uppercase; letter-spacing:0.08em;">Id\u00e9e de sc\u00e9nario</p>\n'
tpl += '<p style="margin:0; font-size:0.85rem; color:#c4b5d4; line-height:1.8; font-style:italic;">'
tpl += '[D\u00e9crivez bri\u00e8vement votre id\u00e9e ou le type de relation que vous souhaitez explorer.]'
tpl += '</p>\n\n'

# Contact
tpl += '<div style="border-top:1px solid rgba(124,58,237,0.12); margin:1rem 0 0.7rem;"></div>\n'
tpl += '<p style="margin:0; font-size:0.78rem; color:#6d5fa0;">'
tpl += 'Contact\u00a0: <span style="color:#e2d9f3;">[R\u00e9pondre ici / Messagerie priv\u00e9e]</span>'
tpl += '</p>\n'

tpl += '</div>'

html += tpl
html += '\n</div>\n\n'

# Footer
html += '<div style="border-top:1px solid rgba(124,58,237,0.2); margin-top:1.75rem; padding-top:0.85rem;">\n'
html += '<p style="margin:0; font-size:0.58rem; color:#2d1f4a; font-style:italic; letter-spacing:0.16em; text-align:center;">'
html += '\u2726 Section officielle du Nexus Arcana \u2014 Ava Bartholom\u00e9 \u2726</p>\n'
html += '</div>\n\n'
html += '</div>'

p.content = html
p.save(update_fields=['content'])
print("Done - length:", len(html))
