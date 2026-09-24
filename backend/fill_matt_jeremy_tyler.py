import ast,json
from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
items=json.loads(Path('matt_jeremy_tyler_data.json').read_text(encoding='utf-8-sig'))
for d in items:
 d.update(camp='Bien',age='Adulte · âge précis à harmoniser avec la chronologie du forum',origin='Mystic Falls, Virginie')
 d['links']=[(name,name+' — '+label,body) for name,label,body in d['links']]
source=Path('fill_petrova_scenarios.py').read_text(encoding='utf-8-sig')
module=ast.parse(source)
n=next(n for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DATA' for t in n.targets))
lines=source.splitlines(keepends=True);lines[n.lineno-1:n.end_lineno]=['DATA = '+repr(items)+'\n'];source=''.join(lines)
source=source.replace("('Sexe','Féminin')","('Sexe','Masculin')").replace("'petrova-'","'matt-jeremy-tyler-'")
source=source.replace('data-petrova-scenario','data-mystic-scenario').replace("images.get(slug,'')","GIFS[slug]")
source=source.replace('fiche et quatre liens enregistrés','fiche et cinq liens avec GIFs enregistrés')
start=source.index("        if d['slug']=='tatia-petrova':")
end=source.index("        content+=section('III. Âme",start)
source=source[:start]+'''        human=d['slug']!='tyler-lockwood'
        intro='Ces quatre aptitudes sont humaines : elles ne constituent pas des pouvoirs magiques. Aucun objet de résurrection ni immunité surnaturelle ne sont accordés.' if human else 'Quatre pouvoirs au total pour ses deux natures. La faim de sang, la fatigue et les vulnérabilités restent à prendre en compte selon le règlement. Aucun pouvoir supplémentaire de contrainte, venin ou guérison d’autrui n’est accordé par cette fiche.'
        content+=section('II. Aptitudes humaines' if human else 'II. Quatre pouvoirs de base',p(intro)+''.join('<div><h3 style="color:#f5d76e;font-size:1rem;">'+escape(name)+'</h3>'+p(body)+'</div>' for name,body in d['powers']))
'''+source[end:]
source=source.replace('Adaptation Nexus Arcana : Elena et Katherine sont vampires ; Tatia est humaine, revenue grâce au Nexus. Les ressemblances ne permettent pas de contrôler une autre personne, de lire ses souvenirs ou de garantir une usurpation réussie. Les relations présentes et les révélations d’intrigue se construisent avec les joueurs concernés.','Adaptation Nexus Arcana : Matt est humain, Jeremy humain chasseur et Tyler hybride vivant, libre de son ancien lien d’asservissement. Les métiers proposés, la situation amoureuse et les détails des relations se construisent avec les joueurs concernés. Les aptitudes et pouvoirs restent limités à ce qui est décrit dans cette fiche.')
gm=ast.parse(Path('update_elena_link_gifs.py').read_text(encoding='utf-8-sig'))
gifs=next(ast.literal_eval(n.value) for n in gm.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GIFS' for t in n.targets))
gifs.update({'Elena Gilbert Salvatore':'https://media1.tenor.com/m/TraCAjZMch8AAAAC/elena-gilbert.gif','Niklaus Mikaelson':'https://media.tenor.com/ZfPfiXgwQ1cAAAAM/niklaus-mikaelson-klaus.gif','Matt Donovan':'https://media1.tenor.com/m/Juwqktnk7SoAAAAC/matt-donovan-matt-donovan-smolder.gif','Tyler Lockwood':'https://media1.tenor.com/m/zVCfiQi04eAAAAAC/tyler-lockwood-the-vampire-diaries-season-3.gif'})
def verify(name):
 with urlopen(Request(gifs[name],headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:assert r.read(6) in (b'GIF87a',b'GIF89a'),name
 return name
print('GIFs accessibles : '+', '.join(ThreadPoolExecutor(8).map(verify,{l[0] for d in items for l in d['links']})))
exec(compile(source,'mystic-renderer','exec'),{'GIFS':gifs})
