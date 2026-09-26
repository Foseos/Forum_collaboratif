import re
from apps.forum.models import Topic

t = Topic.objects.filter(slug='catalogue-boutique-magique').first()
if not t:
    print("Topic not found")
    exit()

p = t.posts.order_by('created_at').first()
if not p:
    print("Post not found")
    exit()

content = p.content

# Replace all prices: "NNN $" -> "NNN Arcana Flouz"
content = re.sub(r'(\d+) \$(<)', r'\1 Arcana Flouz\2', content)

# --- Section V: Artefacts de Luxe ---
sec5 = ''
sec5 += '\n<!-- == ARTEFACTS DE LUXE == -->\n'
sec5 += '<div style="margin-bottom: 1.5rem; border: 1px solid rgba(245,215,110,0.5); border-radius: 7px; overflow: hidden; box-shadow: 0 0 18px rgba(245,215,110,0.08);">\n'
sec5 += '  <div style="background: linear-gradient(90deg, rgba(180,130,20,0.38), rgba(245,215,110,0.08)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(245,215,110,0.35);">\n'
sec5 += '    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #f5d76e; font-weight: normal;">&#x2728; V. Artefacts de Luxe</h2>\n'
sec5 += '  </div>\n'
sec5 += '  <div style="padding: 0.4rem 1rem 0.6rem; font-size: 0.75rem; color: #a78bfa; font-style: italic; border-bottom: 1px solid rgba(245,215,110,0.15);">'
sec5 += 'Objets d\'une puissance exceptionnelle, uniques ou rarissimes. Chaque acquisition est soumise '
sec5 += 'à validation par la fondatrice et ne peut pas \xeatre revendue.</div>\n'
sec5 += '  <div style="padding: 0.5rem 0;">\n'
sec5 += '    <table style="width: 100%; border-collapse: collapse;">\n'
sec5 += '      <thead>\n'
sec5 += '        <tr style="background: rgba(180,130,20,0.12);">\n'
sec5 += '          <th style="padding: 0.4rem 1rem; text-align: left; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #c9a227; font-weight: normal;">Objet</th>\n'
sec5 += '          <th style="padding: 0.4rem 1rem; text-align: left; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #c9a227; font-weight: normal;">Fonctionnalit\xe9s</th>\n'
sec5 += '          <th style="padding: 0.4rem 1rem; text-align: right; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #c9a227; font-weight: normal;">Prix</th>\n'
sec5 += '        </tr>\n'
sec5 += '      </thead>\n'
sec5 += '      <tbody>\n'

items5 = [
    ("Orbe du Destin",
     "Permet d'entrevoir et d'alt\xe9rer l\xe9g\xe8rement un \xe9v\xe9nement futur proche (dans les 48 h). Usage unique par mois. Ne peut pas contrarier un destin fix\xe9.",
     "5 000"),
    ("Sceptre des Anc\xeatres",
     "Canalise la puissance cumul\xe9e de dix sorci\xe8res. D\xe9cuple l'intensit\xe9 d'un sort unique. Exige un groupe de cinq personnes minimum.",
     "3 500"),
    ("Amulette de R\xe9surrection",
     "Permet de rappeler \xe0 la vie un \xeatre d\xe9c\xe9d\xe9 depuis moins de 24 h. Usage absolument unique \u2014 l'amulette se d\xe9sint\xe8gre apr\xe8s.",
     "4 500"),
    ("Cristal d'Omniscience",
     "R\xe9v\xe8le la v\xe9rit\xe9 absolue sur n'importe quelle situation pass\xe9e ou pr\xe9sente. Contient \xe9galement les secrets de son d\xe9tenteur \u2014 \xe0 manier avec prudence.",
     "2 500"),
    ("Dague des Anciens",
     "Lame ench\xeeble forgée dans les abysses. Inflige une blessure insoignable aux \xeatres normalement immortels. Interdit d'usage hors de l\xe9gitime d\xe9fense.",
     "4 800"),
    ("Anneau des \xc9l\xe9ments",
     "Conf\xe8re une ma\xeetrise temporaire des quatre \xe9l\xe9ments (feu, eau, terre, air) pendant 30 minutes. Incompatible avec l'usage simultan\xe9 de pouvoirs innés.",
     "2 000"),
]

for i, (name, desc, price) in enumerate(items5):
    bg = ' background: rgba(255,255,255,0.015);' if i % 2 == 1 else ''
    sec5 += '        <tr style="border-top: 1px solid rgba(245,215,110,0.12);%s">\n' % bg
    sec5 += '          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #f5d76e; white-space: nowrap;">%s</td>\n' % name
    sec5 += '          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">%s</td>\n' % desc
    sec5 += '          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #f5d76e; text-align: right; white-space: nowrap;">%s Arcana Flouz</td>\n' % price
    sec5 += '        </tr>\n'

sec5 += '      </tbody>\n'
sec5 += '    </table>\n'
sec5 += '  </div>\n'
sec5 += '</div>\n'

# --- Section VI: Améliorations & Nouveaux Pouvoirs ---
sec6 = ''
sec6 += '\n<!-- == AMELIORATIONS POUVOIRS == -->\n'
sec6 += '<div style="margin-bottom: 1.5rem; border: 1px solid rgba(167,139,250,0.45); border-radius: 7px; overflow: hidden; box-shadow: 0 0 14px rgba(109,40,217,0.12);">\n'
sec6 += '  <div style="background: linear-gradient(90deg, rgba(109,40,217,0.45), rgba(109,40,217,0.08)); padding: 0.5rem 1rem; border-bottom: 1px solid rgba(167,139,250,0.3);">\n'
sec6 += '    <h2 style="margin: 0; font-size: 0.62rem; letter-spacing: 0.3em; text-transform: uppercase; color: #c4b5fd; font-weight: normal;">&#x26a1; VI. Am\xe9liorations &amp; Nouveaux Pouvoirs</h2>\n'
sec6 += '  </div>\n'
sec6 += '  <div style="padding: 0.4rem 1rem 0.6rem; font-size: 0.75rem; color: #a78bfa; font-style: italic; border-bottom: 1px solid rgba(167,139,250,0.15);">'
sec6 += 'D\xe9bloquez de nouveaux pouvoirs ou am\xe9liorez des pouvoirs existants. '
sec6 += 'Le co\xfbt augmente de <strong style="color: #e2d9f3;">300 Arcana Flouz</strong> \xe0 chaque acquisition. '
sec6 += 'Chaque achat est soumis \xe0 validation par la fondatrice.'
sec6 += '</div>\n'
sec6 += '  <div style="padding: 0.8rem 1rem;">\n'
sec6 += '    <table style="width: 100%; border-collapse: collapse;">\n'
sec6 += '      <thead>\n'
sec6 += '        <tr style="background: rgba(109,40,217,0.15);">\n'
sec6 += '          <th style="padding: 0.4rem 1rem; text-align: left; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Acquisition</th>\n'
sec6 += '          <th style="padding: 0.4rem 1rem; text-align: left; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Description</th>\n'
sec6 += '          <th style="padding: 0.4rem 1rem; text-align: right; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6d5fa0; font-weight: normal;">Co\xfbt</th>\n'
sec6 += '        </tr>\n'
sec6 += '      </thead>\n'
sec6 += '      <tbody>\n'

power_rows = [
    ("1re am\xe9lioration / nouveau pouvoir", "Premier ajout ou am\xe9lioration de pouvoir inn\xe9.", "300"),
    ("2e am\xe9lioration / nouveau pouvoir", "Deuxi\xe8me ajout. Le co\xfbt augmente \xe0 mesure que les pouvoirs s'accumulent.", "600"),
    ("3e am\xe9lioration / nouveau pouvoir", "Troisi\xe8me ajout. La ma\xeetrise requise est plus \xe9lev\xe9e.", "900"),
    ("4e am\xe9lioration / nouveau pouvoir", "Quatri\xe8me ajout. Approbation sp\xe9ciale de la fondatrice n\xe9cessaire.", "1 200"),
    ("5e am\xe9lioration / nouveau pouvoir", "Cinqui\xe8me ajout. R\xe9serv\xe9 aux personnages avec une longue anciennet\xe9.", "1 500"),
    ("6e et au-del\xe0 \u2014 \xe0 l'infini", "Chaque nouvel ajout co\xfbte 300 Arcana Flouz de plus que le pr\xe9c\xe9dent, sans limite.", "+ 300 Arcana Flouz/palier"),
]

for i, (acq, desc, cost) in enumerate(power_rows):
    bg = ' background: rgba(255,255,255,0.015);' if i % 2 == 1 else ''
    sec6 += '        <tr style="border-top: 1px solid rgba(124,58,237,0.1);%s">\n' % bg
    sec6 += '          <td style="padding: 0.55rem 1rem; font-size: 0.85rem; font-weight: 600; color: #e2d9f3; white-space: nowrap;">%s</td>\n' % acq
    sec6 += '          <td style="padding: 0.55rem 1rem; font-size: 0.78rem; color: #c4b5d4; line-height: 1.5;">%s</td>\n' % desc
    sec6 += '          <td style="padding: 0.55rem 1rem; font-size: 0.88rem; font-weight: 700; color: #a78bfa; text-align: right; white-space: nowrap;">%s</td>\n' % cost
    sec6 += '        </tr>\n'

sec6 += '      </tbody>\n'
sec6 += '    </table>\n'
sec6 += '    <p style="margin: 0.75rem 0 0; font-size: 0.72rem; color: #6d28d9; font-style: italic;">'
sec6 += '&#x26a0;&#xfe0f; Chaque am\xe9lioration doit \xeatre justifi\xe9e narrativement (arc RP, entra\xeenement, \xe9v\xe9nement sp\xe9cial). '
sec6 += 'La fondatrice se r\xe9serve le droit de refuser toute demande jugée d\xe9s\xe9quilibr\xe9e.'
sec6 += '</p>\n'
sec6 += '  </div>\n'
sec6 += '</div>\n\n'

# Insert both sections before the notice commande
marker = '<!-- Notice commande -->'
content = content.replace(marker, sec5 + sec6 + marker)

p.content = content
p.save()
print("Done - catalogue updated")
