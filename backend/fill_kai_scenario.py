from pathlib import Path
source=Path('fill_mikaelson_scenarios.py').read_text(encoding='utf-8-sig')
source=source.replace('mikaelson_data.json','kai_data.json').replace('assert len(topics)==8','assert len(topics)==1').replace("'mikaelson-'","'kai-'").replace('data-mikaelson-scenario','data-kai-scenario')
start=source.index('GIFS={');end=source.index('extras={',start)
source=source[:start]+'''GIFS={
'Bonnie Bennett':'https://media1.tenor.com/m/SgwzIqg9Z_QAAAAC/bonnie-bennett.gif',
'Damon Salvatore':'https://media.tenor.com/W0xqbhSVKp0AAAAM/ian-somerhalder-damon-salvatore.gif',
'Alaric Saltzman':'https://media1.tenor.com/m/mrlGUC7RdMEAAAAC/alaric-saltzman-the-vampire-diaries.gif',
'Josie Saltzman':'https://media1.tenor.com/m/bO6PajzKtcQAAAAC/josie-saltzman-kaylee-bryant.gif',
'Lizzie Saltzman':'https://media1.tenor.com/m/iQSHhVwHW_QAAAAC/jenny-boyd-lizzie-saltzman.gif',
'Caroline Forbes':'https://media1.tenor.com/m/ID1okMHpppAAAAAC/caroline-forbes-candice-king.gif'}
'''+source[end:]
start=source.index('def abilities(d):');end=source.index('with transaction.atomic():',start)
source=source[:start]+'''def abilities(d):
 parts=[('Siphonnage magique','Au contact direct d’une source enchantée ou surnaturelle, absorbe une quantité limitée de magie qu’il conserve temporairement pour alimenter ses trois autres dons. Ne copie ni les capacités ni les souvenirs de la source. Un prélèvement sur un personnage se joue avec son accord ; aucune neutralisation complète ou levée de malédiction automatique.'),('Télékinésie','Avec de la magie préalablement absorbée, déplace un petit objet visible à courte distance. Le poids et la précision coûtent davantage d’énergie. Ne contrôle pas le corps ou les organes d’autrui.'),('Bouclier magique','Dépense sa réserve absorbée pour amortir brièvement un impact limité. Le bouclier peut céder et ne renvoie pas les attaques.'),('Allumage magique','Dépense un peu de magie absorbée pour allumer une bougie ou une petite matière combustible proche. Aucun contrôle d’incendie, aucune immunité au feu et aucune combustion directe d’une personne.')]
 return p('Quatre capacités maximum à la création, actives et passives comprises. Le siphonnage compte comme une capacité à part entière. Les capacités manquantes et les améliorations s’achètent ensuite en jeu avec des Arcana Flouz et la validation du staff.')+''.join('<div data-base-power="1"><h3 style="color:#f5d76e;font-size:1rem;">'+escape(a)+'</h3>'+p(b)+'</div>' for a,b in parts)+p('Kai ne produit pas de magie personnelle : sans source et sans réserve restante, ses sorts sont inutilisables. Son corps est humain, vulnérable aux blessures et à l’épuisement. Aucun don vampirique, réserve illimitée, détection magique, création de monde-prison ou rituel de Fusion n’est accordé par ses connaissances. La brèche du Nexus est un événement d’histoire, pas un cinquième pouvoir.')
'''+source[end:]
source=source.replace('II. Nature et capacités','II. Quatre capacités de départ')
start=source.index("p('Continuité Nexus Arcana : Klaus")
end=source.index("))+credit",start)
source=source[:start]+"p('Continuité Nexus Arcana : Kai reste un sorcier siphonneur vivant, sans Fusion ni transformation en Hérétique. Son arrivée résulte d’une bifurcation liée au Nexus. Les liens familiaux et les souvenirs issus de chronologies différentes s’accordent entre joueurs. Ses connaissances ne donnent aucun sort supplémentaire gratuit.'"+source[end:]
source=source.replace("old=post.content\\n", "old=post.content\\n") if False else source
source=source.replace('old=post.content\n','old=post.content\n  notice_match=re.search(r\'<section[^>]*data-creation-cap="4"[^>]*>.*?</section>\',old,re.S)\n')
source=source.replace("if not credit.endswith('</p>'):","credit=credit.split('<section',1)[0].rstrip()\n  if not credit.endswith('</p>'):")
source=source.replace('check=CheckHTML();check.feed(content);assert not check.stack',"content+=(notice_match.group(0) if notice_match else '')\n  check=CheckHTML();check.feed(content);assert not check.stack\n  assert content.count('data-base-power=\"1\"')==4")
exec(compile(source,'kai-renderer','exec'))
