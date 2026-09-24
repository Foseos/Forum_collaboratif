from pathlib import Path
source=Path('fill_legacies_four.py').read_text(encoding='utf-8-sig')
source=source.replace('legacies_four_data.json','teenwolf_four_data.json').replace('legacies-four','teenwolf-four')
start=source.index("source=source[:start]+'''GIFS={")
end=source.index("'''+source[end:]",start)+len("'''+source[end:]")
source=source[:start]+'''source=source[:start]+\'''GIFS={
'Scott McCall':'https://media.tenor.com/r6NfGr_30lEAAAAM/tyler-posey-scott-mccall.gif',
'Allison Argent':'https://media1.tenor.com/m/vEeKvXhteMoAAAAC/allison-in-teen-wolf.gif',
'Stiles Stilinski':'https://media1.tenor.com/m/fNE6FgpcG0gAAAAC/stiles-stillinski.gif',
'Lydia Martin':'https://media1.tenor.com/m/8XKX6IsFAZUAAAAC/lydia.gif',
'Derek Hale':'https://media1.tenor.com/m/kJ5gh4nvuI0AAAAC/tyler-hoechlin-derek-hale.gif',
'Chris Argent':'https://media1.tenor.com/m/_3SeTln0vQYAAAAC/chris-arget-teen-wolf.gif'}
\'''+source[end:]'''+source[end:]
source=source.replace('Continuité Nexus Arcana : Landon est phénix, MG et Kaleb sont vampires, Rafael est loup-garou. Leurs adaptations sont précisées dans leurs histoires. Aucun statut, couple ou pouvoir supplémentaire ne découle automatiquement du passé de la série. Les relations présentes et les projets se construisent avec les joueurs concernés.','Continuité Nexus Arcana : Scott est un loup-garou Vrai Alpha, Allison une humaine chasseuse revenue grâce à la Convergence, Stiles un humain libéré du Nogitsune et Lydia une banshee. Les couples actuels se définissent ensemble. Quatre capacités au maximum sont disponibles à la création ; pour les humains, il s’agit d’aptitudes ordinaires. Les capacités surnaturelles manquantes et leurs améliorations passent par les Arcana Flouz et les règles du forum.')
exec(compile(source,'teenwolf-four-wrapper','exec'))
