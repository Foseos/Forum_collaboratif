import ast,json
from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
source=Path('fill_petrova_scenarios.py').read_text(encoding='utf-8-sig')
items=json.loads(Path('enzo_nadia_data.json').read_text(encoding='utf-8-sig'))
module=ast.parse(source);n=next(n for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DATA' for t in n.targets))
lines=source.splitlines(keepends=True);lines[n.lineno-1:n.end_lineno]=['DATA = '+repr(items)+'\n'];source=''.join(lines)
source=source.replace("('Sexe','Féminin')","('Sexe',d['sex'])").replace("'petrova-'","'enzo-nadia-'").replace('data-petrova-scenario','data-enzo-nadia-scenario').replace("images.get(slug,'')","GIFS[slug]").replace('fiche et quatre liens enregistrés','fiche et cinq liens avec GIFs enregistrés')
source=source.replace('Adaptation Nexus Arcana : Elena et Katherine sont vampires ; Tatia est humaine, revenue grâce au Nexus. Les ressemblances ne permettent pas de contrôler une autre personne, de lire ses souvenirs ou de garantir une usurpation réussie. Les relations présentes et les révélations d’intrigue se construisent avec les joueurs concernés.','Adaptation Nexus Arcana : Enzo et Nadia sont présents en tant que vampires. Les fins tragiques décrites dans la série ne sont pas imposées à cette continuité. Les métiers proposés, la situation amoureuse et les détails des relations se construisent avec les joueurs concernés.')
gm=ast.parse(Path('update_elena_link_gifs.py').read_text(encoding='utf-8-sig'));gifs=next(ast.literal_eval(n.value) for n in gm.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GIFS' for t in n.targets))
gifs.update({'Elena Gilbert Salvatore':'https://media1.tenor.com/m/TraCAjZMch8AAAAC/elena-gilbert.gif','Matt Donovan':'https://media1.tenor.com/m/Juwqktnk7SoAAAAC/matt-donovan-matt-donovan-smolder.gif'})
def verify(name):
 with urlopen(Request(gifs[name],headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:assert r.read(6) in (b'GIF87a',b'GIF89a'),name
 return name
print('GIFs vérifiés : '+', '.join(ThreadPoolExecutor(8).map(verify,{l[0] for d in items for l in d['links']})))
exec(compile(source,'enzo-nadia-renderer','exec'),{'GIFS':gifs})
