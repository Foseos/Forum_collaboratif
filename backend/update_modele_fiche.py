from apps.forum.models import Topic

t = Topic.objects.filter(slug='modele-de-fiche-de-presentation').first()
p = t.posts.order_by('created_at').first()

F = "font-family: Georgia, 'Times New Roman', serif"

html = ''

# ── Wrapper principal ──────────────────────────────────────────────
html += '<div style="%s; background:#0d0a1a; color:#e2d9f3; padding:2rem; border-radius:10px; border:1px solid rgba(124,58,237,0.3); max-width:800px; margin:0 auto;">\n\n' % F

# ── En-tête intro ──────────────────────────────────────────────────
html += '<p style="margin:0 0 0.4rem; font-size:0.58rem; letter-spacing:0.38em; text-transform:uppercase; color:#6d28d9; text-align:center;">'
html += '\u2726 Nexus Arcana \u00b7 Livre des Ombres \u2726</p>\n'
html += '<h1 style="margin:0 0 0.4rem; font-size:1.8rem; font-weight:normal; font-style:italic; color:#f5d76e; letter-spacing:0.04em; text-align:center;">'
html += 'Mod\u00e8le de Fiche de Pr\u00e9sentation</h1>\n'
html += '<p style="margin:0 0 2rem; font-size:0.82rem; color:#a78bfa; font-style:italic; letter-spacing:0.06em; text-align:center;">'
html += 'Copiez le code ci-dessous dans l\u2019\u00e9diteur pour cr\u00e9er votre fiche</p>\n'

# ── Bloc intro instructions ────────────────────────────────────────
html += '<div style="margin-bottom:1.5rem; border:1px solid rgba(124,58,237,0.28); border-radius:7px; overflow:hidden;">\n'
html += '  <div style="background:linear-gradient(90deg,rgba(109,40,217,0.35),rgba(109,40,217,0.08)); padding:0.45rem 1rem; border-bottom:1px solid rgba(124,58,237,0.25);">\n'
html += '    <h2 style="margin:0; font-size:0.6rem; letter-spacing:0.3em; text-transform:uppercase; color:#a78bfa; font-weight:normal;">\u25c8 Mode d\u2019emploi</h2>\n'
html += '  </div>\n'
html += '  <div style="padding:0.85rem 1rem; font-size:0.87rem; color:#c4b5d4; line-height:1.9;">\n'
html += '    <ol style="margin:0; padding-left:1.4rem;">\n'
html += '      <li>Cliquez sur <strong style="color:#e2d9f3;">Cr\u00e9er ma fiche</strong> dans la cat\u00e9gorie <em>Bienvenue \u00e0 San Francisco</em>.</li>\n'
html += '      <li>Copiez l\u2019int\u00e9gralit\u00e9 du code HTML ci-dessous et collez-le dans l\u2019\u00e9diteur.</li>\n'
html += '      <li>Remplissez chaque champ en rempla\u00e7ant les textes entre crochets <strong style="color:#e2d9f3;">[&nbsp;]</strong> par vos informations.</li>\n'
html += '      <li>Pour l\u2019image, remplacez l\u2019attribut <code style="color:#f5d76e; font-size:0.78rem;">src</code> par l\u2019URL de votre photo de personnage.</li>\n'
html += '      <li>Utilisez l\u2019onglet <strong style="color:#e2d9f3;">Aper\u00e7u</strong> pour v\u00e9rifier le rendu avant d\u2019envoyer.</li>\n'
html += '    </ol>\n'
html += '    <p style="margin:0.75rem 0 0; font-size:0.78rem; color:#6d28d9;">'
html += '\u26a0\ufe0f La fiche doit comporter un <strong>minimum de 30 lignes d\u2019histoire</strong> et <strong>15 lignes de caract\u00e8re</strong> pour \u00eatre valid\u00e9e.'
html += '</p>\n'
html += '  </div>\n'
html += '</div>\n\n'

# ── Code à copier (format compact) ────────────────────────────────
html += '<div style="margin-bottom:1.5rem; border:1px solid rgba(245,215,110,0.35); border-radius:7px; overflow:hidden;">\n'
html += '  <div style="background:linear-gradient(90deg,rgba(180,130,20,0.3),rgba(245,215,110,0.06)); padding:0.45rem 1rem; border-bottom:1px solid rgba(245,215,110,0.25);">\n'
html += '    <h2 style="margin:0; font-size:0.6rem; letter-spacing:0.3em; text-transform:uppercase; color:#f5d76e; font-weight:normal;">\u2728 Code \u00e0 copier dans l\u2019\u00e9diteur</h2>\n'
html += '  </div>\n'
html += '  <div style="padding:0.75rem 1rem; background:rgba(13,10,26,0.6);">\n'

# Le template fiche en format compact (margins/paddings réduits)
tpl = ''
tpl += '<div style="%s; background:#0d0a1a; color:#e2d9f3; padding:1rem; border-radius:8px; border:1px solid rgba(124,58,237,0.3); max-width:720px; margin:0 auto;">\n' % F

tpl += '<table style="width:100%; border-collapse:collapse; margin-bottom:1rem; padding-bottom:0.85rem; border-bottom:1px solid rgba(124,58,237,0.2);">\n'
tpl += '<tr>\n'
tpl += '  <td style="vertical-align:top; padding-right:1rem;">\n'
tpl += '    <p style="margin:0 0 0.3rem; font-size:0.56rem; letter-spacing:0.35em; text-transform:uppercase; color:#6d28d9;">\u2726 Nexus Arcana \u00b7 Livre des Ombres \u2726</p>\n'
tpl += '    <h1 style="margin:0 0 0.4rem; font-size:1.7rem; font-weight:normal; font-style:italic; color:#f5d76e; letter-spacing:0.04em; line-height:1.2;">Pr\u00e9nom(s)<br>Nom</h1>\n'
tpl += '    <p style="margin:0 0 0.6rem; font-size:0.8rem; color:#a78bfa; font-style:italic; letter-spacing:0.06em;">Race \u00b7 Camp</p>\n'
tpl += '    <p style="margin:0; font-size:0.74rem; color:#4b3a6b; font-style:italic; line-height:1.6;">"Une citation ou accroche qui d\u00e9finit votre personnage en quelques mots."</p>\n'
tpl += '  </td>\n'
tpl += '  <td style="vertical-align:top; width:200px; text-align:center;">\n'
tpl += '    <img src="/Image_de_base_photo_de_profil.jpg" alt="Pr\u00e9nom NOM" style="width:190px;height:290px;object-fit:cover;border-radius:6px;border:2px solid rgba(124,58,237,0.35);display:block;margin:0 auto;">\n'
tpl += '    <p style="margin:0.25rem 0 0; font-size:0.58rem; color:#3d2d5e; font-style:italic;">Pr\u00e9nom NOM \u2014 c\u00e9l\u00e9brit\u00e9 jou\u00e9e</p>\n'
tpl += '  </td>\n'
tpl += '</tr>\n</table>\n\n'

def section(num, title, body, gold=False):
    bc = 'rgba(245,215,110,0.22)' if gold else 'rgba(124,58,237,0.28)'
    bg_h = 'rgba(245,215,110,0.1), rgba(245,215,110,0.03)' if gold else 'rgba(109,40,217,0.3), rgba(109,40,217,0.08)'
    bc_h = 'rgba(245,215,110,0.2)' if gold else 'rgba(124,58,237,0.25)'
    tc = '#f5d76e' if gold else '#a78bfa'
    s = '<div style="margin-bottom:0.8rem; border:1px solid %s; border-radius:7px; overflow:hidden;">\n' % bc
    s += '  <div style="background:linear-gradient(90deg,%s); padding:0.35rem 0.85rem; border-bottom:1px solid %s;">\n' % (bg_h, bc_h)
    s += '    <h2 style="margin:0; font-size:0.58rem; letter-spacing:0.28em; text-transform:uppercase; color:%s; font-weight:normal;">\u25c8 %s. %s</h2>\n' % (tc, num, title)
    s += '  </div>\n'
    s += body
    s += '</div>\n\n'
    return s

def row(label, value, sep='rgba(124,58,237,0.08)'):
    return (
        '<tr>'
        '<td style="padding:0.22rem 0.85rem 0.22rem 0; font-size:0.72rem; color:#6d5fa0; width:42%%; border-bottom:1px solid %s;">%s</td>'
        '<td style="padding:0.22rem 0; font-size:0.82rem; color:#e2d9f3; border-bottom:1px solid %s;">%s</td>'
        '</tr>\n'
    ) % (sep, label, sep, value)

# Section I Identité
body1 = '  <div style="padding:0.45rem 0.85rem;">\n'
body1 += '    <table style="width:100%; border-collapse:collapse;">\n'
body1 += row('\u00c2ge', 'XX ans')
body1 += row('Date de naissance', 'JJ Mois AAAA')
body1 += row('Sexe', 'F\u00e9minin / Masculin / Autre')
body1 += row('Orientation sexuelle', '...')
body1 += row('Situation familiale', 'C\u00e9libataire / Mari\u00e9(e) / ...')
body1 += row('Race', 'Sorci\u00e8re / D\u00e9mon / ...')
body1 += row('Camp', 'Bien / Neutre / Mal')
body1 += row('M\u00e9tier', '...').replace('border-bottom:1px solid rgba(124,58,237,0.08);', '')
body1 += '    </table>\n  </div>\n'
tpl += section('I', 'Identit\u00e9', body1)

# Section II Pouvoirs
body2 = '  <div style="padding:0.65rem 0.85rem 0.6rem;">\n'
body2 += '    <p style="margin:0 0 0.3rem; font-size:0.76rem; font-weight:600; color:#c4b5fd;">\u26a1 Pouvoirs actifs :</p>\n'
body2 += '    <ul style="margin:0; padding-left:1.2rem; line-height:1.75; font-size:0.85rem; color:#c4b5d4;">\n'
for _ in range(5):
    body2 += '      <li><strong style="color:#e2d9f3;">Nom du pouvoir</strong> \u2014 Description et limites du pouvoir</li>\n'
body2 += '    </ul>\n  </div>\n'
tpl += section('II', 'Pouvoirs Magiques &amp; Aptitudes', body2)

# Section III Caractère
body3 = '  <div style="padding:0.75rem 0.85rem;">\n'
body3 += '    <p style="margin:0; line-height:1.85; color:#c4b5d4; text-align:justify; font-size:0.88rem;">'
body3 += '[D\u00e9crivez la personnalit\u00e9 de votre personnage\u00a0: ses traits dominants, ses habitudes, ses valeurs, ses peurs, ses forces et faiblesses. Comment se comporte-t-il face aux autres\u00a0? Quel est son rapport \u00e0 la magie, au destin, \u00e0 la trahison\u00a0? Comment r\u00e9agit-il sous pression\u00a0? Minimum 15 lignes.]'
body3 += '</p>\n  </div>\n'
tpl += section('III', '\u00c2me &amp; Caract\u00e8re', body3)

# Section IV Histoire
body4 = '  <div style="padding:0.75rem 0.85rem;">\n'
body4 += '    <p style="margin:0; line-height:1.85; color:#c4b5d4; text-align:justify; font-size:0.88rem;">'
body4 += '[Racontez l\u2019histoire compl\u00e8te de votre personnage\u00a0: ses origines, les \u00e9v\u00e9nements qui l\u2019ont fa\u00e7onn\u00e9, les \u00e9preuves travers\u00e9es, et ce qui l\u2019a conduit \u00e0 San Francisco. Comment a-t-il d\u00e9couvert le monde magique\u00a0? Quels secrets porte-t-il\u00a0? Minimum 30 lignes.]'
body4 += '</p>\n  </div>\n'
tpl += section('IV', 'M\u00e9moire des \u00c2ges \u00b7 Histoire', body4)

# Section V Hors personnage (dorée)
body5 = '  <div style="padding:0.45rem 0.85rem;">\n'
body5 += '    <table style="width:100%; border-collapse:collapse;">\n'
sep_g = 'rgba(245,215,110,0.07)'
body5 += row('Pseudonyme sur le forum', '...', sep_g)
body5 += row('\u00c2ge', '...', sep_g)
body5 += row('Comment avez-vous connu le forum\u00a0?', '...', sep_g)
body5 += row('Souhaitez-vous un parrain / une marraine\u00a0?', 'Oui / Non', sep_g).replace('border-bottom:1px solid rgba(245,215,110,0.07);', '')
body5 += '    </table>\n  </div>\n'
tpl += section('V', 'Hors Personnage', body5, gold=True)

tpl += '<p style="text-align:center; margin:0.85rem 0 0; font-size:0.56rem; color:#2d1f4a; font-style:italic; letter-spacing:0.18em;">'
tpl += '\u2726 Fiche soumise \u00e0 la validation du Nexus Arcana \u2726</p>\n'
tpl += '</div>'

# Afficher le template dans un bloc HTML visible + copyable
html += tpl
html += '\n  </div>\n'
html += '</div>\n\n'

# ── Footer ─────────────────────────────────────────────────────────
html += '<p style="text-align:center; margin:1.25rem 0 0; font-size:0.58rem; color:#2d1f4a; font-style:italic; letter-spacing:0.18em;">'
html += '\u2726 Mod\u00e8le officiel du Nexus Arcana \u2014 Ava Bartholom\u00e9 \u2726</p>\n'
html += '</div>'

p.content = html
p.save()
print("Done - modele fiche updated, length:", len(html))
