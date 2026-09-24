import ast,json
from pathlib import Path
source=Path('fill_petrova_scenarios.py').read_text(encoding='utf-8-sig')
data=json.loads(Path('salvatore_scenario_data.json').read_text(encoding='utf-8-sig'))
for entry in data:
    entry['links']=[(name,name+' — '+label,body) for name,label,body in entry['links']]
module=ast.parse(source)
assignment=next(n for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DATA' for t in n.targets))
lines=source.splitlines(keepends=True)
lines[assignment.lineno-1:assignment.end_lineno]=['DATA = '+repr(data)+'\n']
source=''.join(lines)
source=source.replace("('Sexe','Féminin')","('Sexe',d['sex'])")
source=source.replace("'petrova-'","'salvatore-' ")
source=source.replace('data-petrova-scenario','data-salvatore-scenario')
source=source.replace('Adaptation Nexus Arcana : Elena et Katherine sont vampires ; Tatia est humaine, revenue grâce au Nexus. Les ressemblances ne permettent pas de contrôler une autre personne, de lire ses souvenirs ou de garantir une usurpation réussie. Les relations présentes et les révélations d’intrigue se construisent avec les joueurs concernés.','Adaptation Nexus Arcana : Damon, Stefan et Caroline restent vampires. Damon est marié à Elena ; Stefan est vivant et marié à Caroline. Leur histoire diverge donc du final de la série. Les dons sont limités aux quatre pouvoirs de base décrits. Les métiers proposés et les détails des relations se personnalisent avec les joueurs concernés.')
source=source.replace("images.get(slug,'')","GIFS[slug]")
source=source.replace('fiche et quatre liens enregistrés','fiche et cinq liens avec GIFs enregistrés')
source=source.replace('Force supérieure à celle d’une humaine','Force supérieure à celle d’un être humain')
# Read only the GIF dictionary, without executing the earlier mutation script.
gifmodule=ast.parse(Path('update_elena_link_gifs.py').read_text(encoding='utf-8-sig'))
gifs=next(ast.literal_eval(n.value) for n in gifmodule.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GIFS' for t in n.targets))
gifs.update({'Elena Gilbert Salvatore':'https://media1.tenor.com/m/TraCAjZMch8AAAAC/elena-gilbert.gif','Niklaus Mikaelson':'https://media.tenor.com/ZfPfiXgwQ1cAAAAM/niklaus-mikaelson-klaus.gif'})
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
def verify(name):
    with urlopen(Request(gifs[name],headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as response:
        assert response.read(6) in (b'GIF87a',b'GIF89a'),name
    return name
names={link[0] for d in data for link in d['links']}
print('GIFs vérifiés : '+', '.join(ThreadPoolExecutor(7).map(verify,names)))
# The shared renderer locks and backs up the three target topics, preserves their
# portrait and credit, validates the markup, then verifies the saved records.
exec(compile(source,'salvatore-renderer','exec'),{'GIFS':gifs})
