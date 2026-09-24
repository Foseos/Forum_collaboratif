import ast,json
from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
payload=json.loads(Path('bonnie_scenario_data.json').read_text(encoding='utf-8-sig'))
source=Path('fill_petrova_scenarios.py').read_text(encoding='utf-8-sig')
module=ast.parse(source)
lines=source.splitlines(keepends=True)
replacements=[]
for node in module.body:
 if isinstance(node,ast.Assign):
  names=[t.id for t in node.targets if isinstance(t,ast.Name)]
  for name,value in [('DATA',payload['data']),('VAMPIRE_POWERS',payload['powers'])]:
   if name in names:replacements.append((node.lineno,node.end_lineno,name+' = '+repr(value)+'\n'))
for start,end,replacement in sorted(replacements,reverse=True):lines[start-1:end]=[replacement]
source=''.join(lines)
source=source.replace("'petrova-'","'bonnie-'").replace('data-petrova-scenario','data-bonnie-scenario')
source=source.replace("images.get(slug,'')","GIFS[slug]")
source=source.replace('fiche et quatre liens enregistrés','fiche et cinq liens avec GIFs enregistrés')
old='La faim de sang et les vulnérabilités vampiriques restent présentes. Le soleil exige une protection enchantée validée et l’entrée dans une habitation protégée nécessite une invitation. Aucun objet protecteur n’est accordé automatiquement. Les sens exceptionnels ou autres capacités non décrites ne s’ajoutent pas librement à ces quatre dons.'
new='Ces quatre pouvoirs de base constituent ses capacités actives au départ. Ses connaissances des grimoires ne lui donnent pas accès à tous les sorts. Les rituels exceptionnels exigent un cadre et une validation du staff ; ils ne sont pas garantis. Bonnie reste vulnérable aux blessures et à l’épuisement. L’ancienneté de sa lignée ne lui accorde aucun pouvoir supplémentaire.'
assert old in source
source=source.replace(old,new)
old='Adaptation Nexus Arcana : Elena et Katherine sont vampires ; Tatia est humaine, revenue grâce au Nexus. Les ressemblances ne permettent pas de contrôler une autre personne, de lire ses souvenirs ou de garantir une usurpation réussie. Les relations présentes et les révélations d’intrigue se construisent avec les joueurs concernés.'
source=source.replace(old,'Adaptation Nexus Arcana : Bonnie est une sorcière vivante, avec quatre pouvoirs de base. Ses exploits exceptionnels dans la série ne sont pas des capacités librement reproductibles. Sa situation amoureuse, son activité proposée et les détails de sa chronologie se construisent avec les joueurs concernés. Une archive Bennett, un échange entre sorcières ou un voyage avec une amie peuvent amorcer son jeu.')
gifmodule=ast.parse(Path('update_elena_link_gifs.py').read_text(encoding='utf-8-sig'))
gifs=next(ast.literal_eval(n.value) for n in gifmodule.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GIFS' for t in n.targets))
gifs['Elena Gilbert Salvatore']='https://media1.tenor.com/m/TraCAjZMch8AAAAC/elena-gilbert.gif'
def verify(name):
 with urlopen(Request(gifs[name],headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as response:assert response.read(6) in (b'GIF87a',b'GIF89a'),name
 return name
print('GIFs accessibles : '+', '.join(ThreadPoolExecutor(5).map(verify,[link[0] for link in payload['data'][0]['links']])))
exec(compile(source,'bonnie-renderer','exec'),{'GIFS':gifs})
