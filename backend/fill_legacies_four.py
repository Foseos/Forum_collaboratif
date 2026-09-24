from pathlib import Path
source=Path('fill_mikaelson_scenarios.py').read_text(encoding='utf-8-sig')
source=source.replace('mikaelson_data.json','legacies_four_data.json').replace('assert len(topics)==8','assert len(topics)==4').replace("'mikaelson-'","'legacies-four-'").replace('data-mikaelson-scenario','data-legacies-four-scenario')
start=source.index('GIFS={');end=source.index('def verify(name):',start)
source=source[:start]+'''GIFS={
'Landon Kirby':'https://media.tenor.com/CJEvXyZPzIcAAAAM/landon-kirby-legacies.gif',
'Rafael Waithe':'https://media.tenor.com/Gw3FFTkuNT0AAAAM/rafael-waithe-legacies.gif',
'Kaleb Hawkins':'https://media1.tenor.com/m/6QDLl05zmSkAAAAC/legacies-legacies-season4.gif',
'Milton Greasley':'https://media1.tenor.com/m/md8CjX_XTy0AAAAC/legacies-legacies-season4.gif',
'Hope Mikaelson':'https://media1.tenor.com/m/flkkkhUPqKMAAAAC/hope-mikaelson4x16-tribrid-hope.gif',
'Alaric Saltzman':'https://media1.tenor.com/m/mrlGUC7RdMEAAAAC/alaric-saltzman-the-vampire-diaries.gif',
'Josie Saltzman':'https://media1.tenor.com/m/bO6PajzKtcQAAAAC/josie-saltzman-kaylee-bryant.gif',
'Lizzie Saltzman':'https://media1.tenor.com/m/iQSHhVwHW_QAAAAC/jenny-boyd-lizzie-saltzman.gif'}
'''+source[end:]
start=source.index('def abilities(d):');end=source.index('with transaction.atomic():',start)
source=source[:start]+'''def abilities(d):
 parts=d.get('powers') or [('Force surnaturelle','Force supérieure à celle d’un humain sur un effort ciblé. Aucun gain de vitesse, aucune invulnérabilité ni victoire automatique.'),('Vitesse surnaturelle','Accélération brève sur une courte distance dégagée. Ne permet ni téléportation ni perception surnaturelle supplémentaire.'),('Régénération','Guérison accélérée de blessures ordinaires selon leur gravité et son état. Ne soigne pas autrui, ne ressuscite pas et ne dissipe pas les malédictions.'),('Contrainte mentale','Influence limitée sur un humain non protégé, avec contact visuel et accord du joueur concerné. La verveine protège la cible. Aucun contrôle des vampires, lecture des pensées ou pouvoir sur les rêves.')]
 assert len(parts)==4
 limits=d.get('limits','La faim, la verveine, le soleil sans protection validée et les autres vulnérabilités vampiriques restent applicables. Aucun objet magique, venin, don draconique ou pouvoir supplémentaire gratuit. Les difficultés à maîtriser la soif ne constituent pas une cinquième capacité.')
 return p('Quatre capacités de départ au total, actives et passives comprises. Les capacités manquantes et les améliorations se débloquent ensuite en jeu avec des Arcana Flouz et la validation du staff. Les exploits racontés dans l’histoire ne donnent aucun don supplémentaire.')+''.join('<div data-base-power="1"><h3 style="color:#f5d76e;font-size:1rem;">'+escape(a)+'</h3>'+p(b)+'</div>' for a,b in parts)+p(limits)
'''+source[end:]
source=source.replace('II. Nature et capacités','II. Quatre capacités de départ')
start=source.index("p('Continuité Nexus Arcana : Klaus")
end=source.index('))+credit',start)
source=source[:start]+"p('Continuité Nexus Arcana : Landon est phénix, MG et Kaleb sont vampires, Rafael est loup-garou. Leurs adaptations sont précisées dans leurs histoires. Aucun statut, couple ou pouvoir supplémentaire ne découle automatiquement du passé de la série. Les relations présentes et les projets se construisent avec les joueurs concernés.'"+source[end:]
source=source.replace('old=post.content\n','old=post.content\n  notice_match=re.search(r\'<section[^>]*data-creation-cap="4"[^>]*>.*?</section>\',old,re.S)\n')
source=source.replace('credit=re.search',"caption=caption.replace('Caleb Hawlins','Kaleb Hawkins').replace('Caleb Hawkins','Kaleb Hawkins')\n  credit=re.search")
source=source.replace("if not credit.endswith('</p>'):","credit=credit.split('<section',1)[0].rstrip()\n  if not credit.endswith('</p>'):")
source=source.replace("'topic_id':t.pk,", "'topic_id':t.pk,'title':t.title,")
source=source.replace('check=CheckHTML();check.feed(content);assert not check.stack',"content+=(notice_match.group(0) if notice_match else '')\n  check=CheckHTML();check.feed(content);assert not check.stack\n  assert content.count('data-base-power=\"1\"')==4\n  assert img in content and credit in content")
source=source.replace("t.scenario_link_cards=cards;t.save(update_fields=['scenario_link_cards'])", "t.scenario_link_cards=cards\n  if t.slug=='caleb-hawkins':t.title='Kaleb Hawkins'\n  t.save(update_fields=['scenario_link_cards','title'])")
exec(compile(source,'legacies-four-renderer','exec'))
