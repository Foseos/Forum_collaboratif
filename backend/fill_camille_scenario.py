from pathlib import Path
source=Path('fill_marcel_scenario.py').read_text(encoding='utf-8-sig')
source=source.replace('marcel_data.json','camille_data.json').replace("'marcel-'","'camille-'").replace('data-marcel-scenario','data-camille-scenario')
source=source.replace('Continuité Nexus Arcana : Marcel est vampire et commence avec les quatre capacités indiquées. Son statut de vampire amélioré n’est pas acquis. Les dons manquants et les évolutions passent par la boutique en Arcana Flouz. Sa situation avec Rebekah, ses activités et sa place dans les communautés se construisent avec les joueurs concernés.','Continuité Nexus Arcana : Camille est vivante et vampire, avec quatre capacités maximum à la création. Les capacités manquantes et les évolutions s’achètent en jeu avec des Arcana Flouz après validation. Sa formation en psychologie ne lui donne aucun don de lecture mentale. Ses projets professionnels et sa situation sentimentale se construisent avec les joueurs concernés.')
# Add the two relevant GIFs to the renderer before verification, without executing another content script.
needle="start=source.index('def abilities(d):');end=source.index('with transaction.atomic():',start)"
addition='''source=source.replace('def verify(name):', "GIFS.update({'Vincent Griffith':'https://media1.tenor.com/m/scAqhVKhcYcAAAAC/vincent-griffith-yusuf-gatewood.gif','Aurora de Martel':'https://media1.tenor.com/m/y2Z6w3CEQKAAAAAC/rebecca-breeds-aurora-de-martel.gif'})\\ndef verify(name):")
'''
assert needle in source
source=source.replace(needle,addition+needle)
exec(compile(source,'camille-renderer','exec'))
