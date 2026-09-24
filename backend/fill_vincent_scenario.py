from pathlib import Path
source=Path('fill_davina_scenario.py').read_text(encoding='utf-8-sig')
source=source.replace('davina_data.json','vincent_data.json').replace("'davina-'","'vincent-'").replace('data-davina-scenario','data-vincent-scenario')
source=source.replace("('Allumage magique','Allume une bougie ou une petite matière combustible proche. Ne contrôle pas un incendie, ne procure aucune immunité au feu et ne permet pas d’enflammer directement une personne.')", "('Sceau d’alerte','Marque une ouverture et perçoit son franchissement tant qu’il reste à proximité. Une ouverture à la fois ; aucun piège, identification ou contrôle du passant.')")
source=source.replace('La puissance de la Moisson, les dons des Ancêtres et ses anciens exploits ne sont pas disponibles automatiquement.','Les dons des Ancêtres, son ancienne fonction de régent et ses exploits passés ne sont pas des capacités supplémentaires disponibles automatiquement.').replace('Davina demeure vulnérable','Vincent demeure vulnérable')
source=source.replace('Continuité Nexus Arcana : Davina est une sorcière vivante et commence avec les quatre capacités décrites. Les dons manquants et les évolutions passent par la boutique en Arcana Flouz. Sa relation avec Kol, ses études et sa place dans les covens se construisent avec les joueurs concernés. Aucun titre passé n’impose l’obéissance d’autrui.','Continuité Nexus Arcana : Vincent est un sorcier vivant et libre de toute possession. Quatre capacités maximum à la création ; les dons manquants et les évolutions s’achètent ensuite en jeu avec des Arcana Flouz après validation. Sa place dans les covens et sa vie personnelle se construisent avec les joueurs concernés. Aucun ancien titre ne donne une autorité automatique.')
needle="start=source.index('def abilities(d):');end=source.index('with transaction.atomic():',start)"
addition='''source=source.replace('def verify(name):', "GIFS['Camille O’Connell']='https://media1.tenor.com/m/tVsc2Ss6QjsAAAAC/camille-o%27connell-leah-pipes.gif'\\ndef verify(name):")
'''
assert needle in source
source=source.replace(needle,addition+needle)
exec(compile(source,'vincent-renderer','exec'))
