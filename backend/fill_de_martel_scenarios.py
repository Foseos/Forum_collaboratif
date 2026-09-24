from pathlib import Path
source=Path('fill_marcel_scenario.py').read_text(encoding='utf-8-sig')
source=source.replace('marcel_data.json','de_martel_data.json').replace("'marcel-'","'de-martel-'").replace('data-marcel-scenario','data-de-martel-scenario').replace("'assert len(topics)==1'","'assert len(topics)==2'")
source=source.replace('Continuité Nexus Arcana : Marcel est vampire et commence avec les quatre capacités indiquées. Son statut de vampire amélioré n’est pas acquis. Les dons manquants et les évolutions passent par la boutique en Arcana Flouz. Sa situation avec Rebekah, ses activités et sa place dans les communautés se construisent avec les joueurs concernés.','Continuité Nexus Arcana : Aurora et Tristan sont présents, libres et vampires non originels. Chacun commence avec quatre capacités maximum, actives et passives comprises. Les capacités manquantes et les évolutions passent par la boutique en Arcana Flouz. Les relations, fonctions et alliances se construisent avec les joueurs concernés.')
needle="start=source.index('def abilities(d):');end=source.index('with transaction.atomic():',start)"
addition='''source=source.replace('def verify(name):', "GIFS.update({'Aurora de Martel':'https://media1.tenor.com/m/y2Z6w3CEQKAAAAAC/rebecca-breeds-aurora-de-martel.gif','Tristan de Martel':'https://media1.tenor.com/m/WoUKf81NCUgAAAAC/the-originals.gif','Lucien Castle':'https://media.tenor.com/j4Z0nTuDGD4AAAAM/lucien-castle-lucien.gif','Camille O’Connell':'https://media1.tenor.com/m/tVsc2Ss6QjsAAAAC/camille-o%27connell-leah-pipes.gif'})\\ndef verify(name):")
source=source.replace("credit=re.search", "if d['slug']=='tristan-de-martel':caption=caption.replace('Aurora De Martel','Tristan de Martel').replace('Olivier Ackland','Oliver Ackland')\\n  credit=re.search")
'''
assert needle in source
source=source.replace(needle,addition+needle)
source=source.replace(needle,"source=source.replace(\"if not credit.endswith('</p>'):\", \"credit=credit.split('<section',1)[0].rstrip()\\n  if not credit.endswith('</p>'):\")\n"+needle)
exec(compile(source,'de-martel-renderer','exec'))
