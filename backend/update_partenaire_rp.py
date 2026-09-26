from apps.users.models import User
from apps.forum.models import Topic

t = Topic.objects.filter(slug='demande-de-partenaire-de-rp').first()
p = t.posts.order_by('created_at').first()

# Change author to Ava Bartholomé
ava = User.objects.get(username='Ava Bartholom\u00e9')
t.author = ava
p.author = ava
t.save(update_fields=['author'])
p.save(update_fields=['author'])

F = "font-family: Georgia, 'Times New Roman', serif"

html = ''
html += '<div style="%s; background:#0d0a1a; color:#e2d9f3; padding:2rem; border-radius:10px; border:1px solid rgba(124,58,237,0.3); max-width:800px; margin:0 auto;">\n\n' % F

# En-tête
html += '<p style="margin:0 0 0.4rem; font-size:0.58rem; letter-spacing:0.38em; text-transform:uppercase; color:#6d28d9; text-align:center;">'
html += '\u2726 Nexus Arcana \u00b7 San Francisco \u2726</p>\n'
html += '<h1 style="margin:0 0 0.4rem; font-size:1.8rem; font-weight:normal; font-style:italic; color:#f5d76e; letter-spacing:0.04em; text-align:center;">'
html += 'Demandes de Partenaire de RP</h1>\n'
html += '<p style="margin:0 0 2rem; font-size:0.82rem; color:#a78bfa; font-style:italic; letter-spacing:0.06em; text-align:center;">'
html += 'Trouvez un partenaire d\u2019\u00e9criture \u2014 r\u00e9pondez \u00e0 ce sujet avec le mod\u00e8le ci-dessous</p>\n'

# Bloc intro
html += '<div style="margin-bottom:1.5rem; border:1px solid rgba(124,58,237,0.28); border-radius:7px; overflow:hidden;">\n'
html += '  <div style="background:linear-gradient(90deg,rgba(109,40,217,0.35),rgba(109,40,217,0.08)); padding:0.5rem 1rem; border-bottom:1px solid rgba(124,58,237,0.25);">\n'
html += '    <h2 style="margin:0; font-size:0.62rem; letter-spacing:0.3em; text-transform:uppercase; color:#a78bfa; font-weight:normal;">\u2727 Pr\u00e9sentation</h2>\n'
html += '  </div>\n'
html += '  <div style="padding:0.85rem 1rem; font-size:0.88rem; color:#c4b5d4; line-height:1.9;">\n'
html += '    <p style="margin:0 0 0.6rem;">Vous cherchez un partenaire pour d\u00e9velopper un arc narratif, explorer une relation entre personnages ou lancer une intrigue ? Vous \u00eates au bon endroit.</p>\n'
html += '    <p style="margin:0;">R\u00e9pondez \u00e0 ce sujet en copiant le <strong style="color:#e2d9f3;">mod\u00e8le de demande</strong> ci-dessous, en le compl\u00e9tant avec les informations de votre personnage et de vos attentes. Les autres membres pourront vous contacter via les messageries ou en r\u00e9pondant directement \u00e0 votre annonce.</p>\n'
html += '  </div>\n'
html += '</div>\n\n'

# Bloc règles
html += '<div style="margin-bottom:1.5rem; border:1px solid rgba(124,58,237,0.28); border-radius:7px; overflow:hidden;">\n'
html += '  <div style="background:linear-gradient(90deg,rgba(109,40,217,0.35),rgba(109,40,217,0.08)); padding:0.5rem 1rem; border-bottom:1px solid rgba(124,58,237,0.25);">\n'
html += '    <h2 style="margin:0; font-size:0.62rem; letter-spacing:0.3em; text-transform:uppercase; color:#a78bfa; font-weight:normal;">\u25c8 Consignes</h2>\n'
html += '  </div>\n'
html += '  <div style="padding:0.85rem 1rem;">\n'
html += '    <ul style="margin:0; padding-left:1.3rem; font-size:0.87rem; color:#c4b5d4; line-height:1.9;">\n'
html += '      <li>Une annonce par personnage \u2014 mettez-la \u00e0 jour plut\u00f4t que d\u2019en cr\u00e9er une nouvelle.</li>\n'
html += '      <li>Pr\u00e9cisez clairement le <strong style="color:#e2d9f3;">type de RP</strong> souhait\u00e9 (action, romance, drame, enqu\u00eate\u2026).</li>\n'
html += '      <li>Mentionnez votre <strong style="color:#e2d9f3;">disponibilit\u00e9</strong> et votre rythme d\u2019\u00e9criture habituel.</li>\n'
html += '      <li>Respectez les <a style="color:#a78bfa;" href="/topics/reglement-officiel-du-forum">r\u00e8gles du forum</a> dans vos annonces et \u00e9changes.</li>\n'
html += '    </ul>\n'
html += '  </div>\n'
html += '</div>\n\n'

# Bloc modèle de réponse (doré)
html += '<div style="margin-bottom:1.5rem; border:1px solid rgba(245,215,110,0.4); border-radius:7px; overflow:hidden; box-shadow:0 0 14px rgba(245,215,110,0.06);">\n'
html += '  <div style="background:linear-gradient(90deg,rgba(180,130,20,0.32),rgba(245,215,110,0.06)); padding:0.5rem 1rem; border-bottom:1px solid rgba(245,215,110,0.3);">\n'
html += '    <h2 style="margin:0; font-size:0.62rem; letter-spacing:0.3em; text-transform:uppercase; color:#f5d76e; font-weight:normal;">\u2728 Mod\u00e8le \u00e0 copier dans votre r\u00e9ponse</h2>\n'
html += '  </div>\n'
html += '  <div style="padding:0.85rem 1rem; background:rgba(13,10,26,0.5);">\n'

# Le template de réponse (compact)
tpl = ''
tpl += '<div style="%s; background:#0d0a1a; color:#e2d9f3; padding:1.25rem; border-radius:8px; border:1px solid rgba(124,58,237,0.3); max-width:680px; margin:0 auto;">\n' % F

# Header template
tpl += '<p style="margin:0 0 0.3rem; font-size:0.56rem; letter-spacing:0.35em; text-transform:uppercase; color:#6d28d9; text-align:center;">\u2726 Nexus Arcana \u00b7 Demande de Partenaire \u2726</p>\n'
tpl += '<h2 style="margin:0 0 1rem; font-size:1.4rem; font-weight:normal; font-style:italic; color:#f5d76e; letter-spacing:0.04em; text-align:center;">Pr\u00e9nom NOM</h2>\n'

def mini_section(title, body, gold=False):
    bc = 'rgba(245,215,110,0.25)' if gold else 'rgba(124,58,237,0.25)'
    bg = 'rgba(245,215,110,0.08),rgba(245,215,110,0.02)' if gold else 'rgba(109,40,217,0.28),rgba(109,40,217,0.06)'
    tc = '#f5d76e' if gold else '#a78bfa'
    s = '<div style="margin-bottom:0.75rem; border:1px solid %s; border-radius:6px; overflow:hidden;">\n' % bc
    s += '  <div style="background:linear-gradient(90deg,%s); padding:0.32rem 0.85rem; border-bottom:1px solid %s;">\n' % (bg, bc)
    s += '    <h3 style="margin:0; font-size:0.58rem; letter-spacing:0.28em; text-transform:uppercase; color:%s; font-weight:normal;">%s</h3>\n' % (tc, title)
    s += '  </div>\n'
    s += body
    s += '</div>\n'
    return s

def mini_row(label, value, sep='rgba(124,58,237,0.08)'):
    return (
        '<tr>'
        '<td style="padding:0.2rem 0.8rem 0.2rem 0; font-size:0.7rem; color:#6d5fa0; width:40%%; border-bottom:1px solid %s;">%s</td>'
        '<td style="padding:0.2rem 0; font-size:0.8rem; color:#e2d9f3; border-bottom:1px solid %s;">%s</td>'
        '</tr>\n'
    ) % (sep, label, sep, value)

# Section Personnage
body1 = '  <div style="padding:0.4rem 0.85rem;">\n'
body1 += '    <table style="width:100%; border-collapse:collapse;">\n'
body1 += mini_row('Personnage', '[Pr\u00e9nom NOM]')
body1 += mini_row('Race / Camp', '[Race \u00b7 Bien / Neutre / Mal]')
body1 += mini_row('Groupe / Faction', '[Nom de la faction ou aucune]')
body1 += mini_row('Pouvoirs principaux', '[Listez 1 \u00e0 3 pouvoirs]').replace('border-bottom:1px solid rgba(124,58,237,0.08);', '')
body1 += '    </table>\n  </div>\n'
tpl += mini_section('\u25c8 I. Mon Personnage', body1)

# Section Type de RP
body2 = '  <div style="padding:0.4rem 0.85rem;">\n'
body2 += '    <table style="width:100%; border-collapse:collapse;">\n'
body2 += mini_row('Type de sc\u00e8ne souhait\u00e9', '[Action / Romance / Drame / Enqu\u00eate / Autre]')
body2 += mini_row('Ambiance', '[Sombre / L\u00e9g\u00e8re / \u00c9quilibr\u00e9e]')
body2 += mini_row('Lieu envisag\u00e9', '[Quartier, lieu RP ou libre]')
body2 += mini_row('Personnages recherch\u00e9s', '[Toute race / Camp pr\u00e9cis / Faction sp\u00e9cifique]').replace('border-bottom:1px solid rgba(124,58,237,0.08);', '')
body2 += '    </table>\n  </div>\n'
tpl += mini_section('\u25c8 II. Type de RP Souhait\u00e9', body2)

# Section Disponibilités
body3 = '  <div style="padding:0.4rem 0.85rem;">\n'
body3 += '    <table style="width:100%; border-collapse:collapse;">\n'
body3 += mini_row('Disponibilit\u00e9s', '[Jours / horaires approximatifs]')
body3 += mini_row('Rythme d\u2019\u00e9criture', '[Rapide / Mod\u00e9r\u00e9 / Lent \u2014 longueur moyenne des posts]')
body3 += mini_row('Mode de contact', '[R\u00e9pondre ici / Messagerie priv\u00e9e]').replace('border-bottom:1px solid rgba(124,58,237,0.08);', '')
body3 += '    </table>\n  </div>\n'
tpl += mini_section('\u25c8 III. Disponibilit\u00e9s &amp; Rythme', body3)

# Section Idée de scénario
body4 = '  <div style="padding:0.5rem 0.85rem;">\n'
body4 += '    <p style="margin:0; line-height:1.85; color:#c4b5d4; font-size:0.85rem;">'
body4 += '[D\u00e9crivez bri\u00e8vement une id\u00e9e de sc\u00e9nario ou le type de relation que vous souhaitez explorer. Qu\u2019est-ce qui motive votre personnage \u00e0 croiser la route d\u2019un autre ? Quelles tensions, quelles alliances ou quels conflits vous int\u00e9ressent ?]'
body4 += '</p>\n  </div>\n'
tpl += mini_section('\u25c8 IV. Id\u00e9e de Sc\u00e9nario', body4)

# Section Hors personnage (dorée)
body5 = '  <div style="padding:0.4rem 0.85rem;">\n'
body5 += '    <table style="width:100%; border-collapse:collapse;">\n'
sg = 'rgba(245,215,110,0.07)'
body5 += mini_row('Pseudo forum', '[Votre pseudo]', sg)
body5 += mini_row('Exp\u00e9rience RP', '[D\u00e9butant / Interm\u00e9diaire / Confirm\u00e9]', sg)
body5 += mini_row('Contraintes', '[Sujets \u00e0 \u00e9viter si n\u00e9cessaire]', sg).replace('border-bottom:1px solid rgba(245,215,110,0.07);', '')
body5 += '    </table>\n  </div>\n'
tpl += mini_section('\u25c8 V. Hors Personnage', body5, gold=True)

tpl += '<p style="text-align:center; margin:0.75rem 0 0; font-size:0.56rem; color:#2d1f4a; font-style:italic; letter-spacing:0.16em;">'
tpl += '\u2726 Demande de partenaire \u2014 Nexus Arcana \u2726</p>\n'
tpl += '</div>'

html += tpl
html += '\n  </div>\n'
html += '</div>\n\n'

# Footer
html += '<p style="text-align:center; margin:1.25rem 0 0; font-size:0.58rem; color:#2d1f4a; font-style:italic; letter-spacing:0.18em;">'
html += '\u2726 Section officielle du Nexus Arcana \u2014 Ava Bartholom\u00e9 \u2726</p>\n'
html += '</div>'

p.content = html
p.save(update_fields=['content'])
print("Done - length:", len(html))
