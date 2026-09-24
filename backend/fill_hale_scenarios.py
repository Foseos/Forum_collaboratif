from pathlib import Path
import json
# Reuse the checked four-sheet renderer, with the Hale content and current casting.
source=Path('fill_legacies_four.py').read_text(encoding='utf-8-sig')
source=source.replace('legacies_four_data.json','hale_data.json').replace('legacies-four','hale-four')
start=source.index("source=source[:start]+'''GIFS={")
end=source.index("'''+source[end:]",start)+len("'''+source[end:]")
gifs={
 'Derek Hale':'https://media1.tenor.com/m/kJ5gh4nvuI0AAAAC/tyler-hoechlin-derek-hale.gif',
 'Laura Hale':'https://media1.tenor.com/m/4CYyW3agdvcAAAAC/dakota-johnson.gif',
 'Cora Hale':'https://media1.tenor.com/m/xgMjatDQdo4AAAAC/stranger-things-millie-bobby-brown.gif',
 'Peter Hale':'https://media1.tenor.com/m/2D8tcS-pjx4AAAAC/teen-wolf-peter-hale.gif',
 'Malia Tate':'https://media1.tenor.com/m/n7a7CPCFbr8AAAAC/malia-tate.gif',
 'Scott McCall':'https://media.tenor.com/r6NfGr_30lEAAAAM/tyler-posey-scott-mccall.gif',
 'Stiles Stilinski':'https://media1.tenor.com/m/fNE6FgpcG0gAAAAC/stiles-stillinski.gif'}
powers=[['Transformation partielle','Manifestation des traits lupins, des crocs et des griffes. Le contrôle se fragilise sous une émotion intense ou à la pleine lune. Ne donne pas de forme animale complète ni de capacités distinctes supplémentaires.'],['Force surnaturelle','Force supérieure à celle d’un humain sur un effort ciblé. Aucun gain de vitesse, aucune invulnérabilité ni domination automatique.'],['Régénération','Récupération accélérée de blessures ordinaires selon leur gravité et son état. Ne ressuscite pas, ne soigne pas autrui et ne neutralise pas les poisons ou malédictions.'],['Odorat accru','Suit une odeur proche, récente et suffisamment marquée. Le vent, la pluie et les odeurs mêlées peuvent brouiller une piste. Aucun détecteur de mensonge, aucune ouïe ou vision surnaturelle incluse.']]
setup='GIFS='+repr(gifs)+'\nfor d in DATA:\n d["powers"]='+repr(powers)+'\n d["limits"]='+repr('Quatre capacités seulement sont utilisables à la création. La vitesse accrue, les autres sens, l’absorption de douleur, les formes animales complètes ou monstrueuses et les dons non retenus passent par la progression en Arcana Flouz. Les anciens rangs ne donnent aucun pouvoir gratuit. L’aconit, les barrières adaptées et la perte de contrôle demeurent des risques. Une morsure transformante ou un changement de rang demande une intrigue validée.')+'\n'
source=source[:start]+'source=source[:start]+'+repr(setup)+'+source[end:]'+source[end:]
source=source.replace('Continuité Nexus Arcana : Landon est phénix, MG et Kaleb sont vampires, Rafael est loup-garou. Leurs adaptations sont précisées dans leurs histoires. Aucun statut, couple ou pouvoir supplémentaire ne découle automatiquement du passé de la série. Les relations présentes et les projets se construisent avec les joueurs concernés.','Année actuelle : 2033. Derek, Cora et Peter sont vivants ; Laura revient exceptionnellement grâce à la Convergence. Le Nexus ne rajeunit pas automatiquement les personnages. Le passé d’Alpha de Laura, Derek et Peter ne leur restitue ni rang ni capacités supplémentaires. Aucun retour à la vie n’est un don reproductible. Les relations présentes se construisent entre joueurs, sans pardon ni obéissance imposés. Les capacités manquantes et les améliorations s’achètent en Arcana Flouz selon les règles du forum.')
exec(compile(source,'hale-renderer','exec'))
