"""Reviewed French corrections, applied only to public text, never HTML attributes."""
import json
import re
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.forum.models import Category, Post, SitePage, Topic

WORDS = {
    'Epinglé':'Épinglé', 'Héterosexuelle':'Hétérosexuelle',
    'soeur':'sœur', 'soeurs':'sœurs', 'Soeur':'Sœur', 'Soeurs':'Sœurs',
    'ainée':'aînée', 'ainées':'aînées', 'ainé':'aîné', 'ainés':'aînés',
    'connaitre':'connaître', 'maitriser':'maîtriser', 'entrainé':'entraîné',
    'extrèmement':'extrêmement', 'dèjà':'déjà', 'dangeureuse':'dangereuse',
    'dangeureux':'dangereux', 'accariatre':'acariâtre', 'strice':'stricte',
    'echec':'échec', 'surement':'sûrement', 'diners':'dîners',
    'Epoux':'Époux', 'Epouse':'Épouse', 'apriori':'a priori',
}
PHRASES = {
    'leurs choix passés.  Phoebe et Cole se remarient.':'leurs choix passés, Phoebe et Cole se remarient.',
    "Elle revient cependant à la vie, avec l’âge qu'elle aurait dû avoir si elle avait continué de vivre. donc, à 36 ans.":"Elle revint cependant à la vie avec l’âge qu’elle aurait dû avoir si elle avait continué de vivre, donc à 36 ans.",
    'telle une bourreau de travail':'tel un bourreau de travail',
    '\n\nà 43 ans, elle devient une fondatrice':'\n\nÀ 43 ans, elle devient une fondatrice.',
    'Ils se marièrent également\n':'Ils se marièrent également.\n',
    "elle revient cependant":"elle revint cependant",
    'le livre des ombres dans le grenier':'le Livre des Ombres dans le grenier',
    'Temple officiel':'Temple officiel',
    'Template officiel pour créer votre personnage.':'Modèle officiel pour créer votre personnage.',
    'Je me suis beaucoup mise entre elles':'Je me suis beaucoup mise entre elle',
    'le poil sur le dos':'le poil sur le dos',
    "je suis beaucoup plus posée et peut":"je suis beaucoup plus posée et peux",
    'nous devons apporter grande importance':'nous devons accorder une grande importance',
    "d'avantage":"davantage", "d’avantage":"davantage",
    'moi même':'moi-même', 'elle même':'elle-même', 'lui même':'lui-même',
    'beau père':'beau-père', 'Beau père':'Beau-père', 'ex mari':'ex-mari',
    'Demi petite soeur':'Demi-sœur cadette', 'Demi petite sœur':'Demi-sœur cadette',
    'Demi frère':'Demi-frère', 'Demi sœur':'Demi-sœur', 'non retour':'non-retour',
    "jusqu'a ":"jusqu’à ", "à la hate":"à la hâte", "l'age":"l’âge",
    'ans ans':'ans', '50 ans physiquement ans. 62 ans normalement':'50 ans physiquement, 62 ans normalement',
    'un nombre d efois':'un nombre de fois', 'de nombreux cheveux blanc':'de nombreux cheveux blancs',
    "J'ai du ":"J’ai dû ", 'Nous avons du ':'Nous avons dû ',
    "j'ai également du ":"j’ai également dû ", "j'ai toujours du ":"j’ai toujours dû ",
    'nous avons construits':'nous avons construit', 'nous avons vécus':'nous avons vécu',
    'a finit par':'a fini par', 'tout cela à renforcé':'tout cela a renforcé',
    'jumelles à pu':'jumelles a pu', 'en aucun points':'en aucun point',
    'quelques temps':'quelque temps', 'quelques peur':'quelques peurs',
    'les même erreurs':'les mêmes erreurs', 'de manière plus tempérer':'de manière plus tempérée',
    'il poursuit d’assumer':'il continue d’assumer', "il poursuit d'assumer":"il continue d’assumer",
    'Ile me comprend':'Il me comprend', 'elle me protège malgré tout tel une lionne':'elle me protège malgré tout telle une lionne',
    'Elle me protège malgré tout tel une lionne':'Elle me protège malgré tout telle une lionne',
    "moi qui en voulait un":"moi qui en voulais un", "même si j'aimerai qu'elle":"même si j’aimerais qu’elle",
    'Je ne remplierai pas':'Je ne remplirais pas', 'je me tenais pas à cela':'je m’en tenais pas à cela',
    "que j'ai tenu pendant":"que j’ai tenue pendant", 'entre elles et d’autres personnes':'entre elle et d’autres personnes',
    "entre elles et d'autres personnes":"entre elle et d’autres personnes",
    'je suis déjà comme intégrée':'je suis déjà comme intégré',
    'je temporise sa surprotectrice':'je tempère sa surprotection',
    "j'en suis sûre, mais j'ai toujours":"j’en suis sûr, mais j’ai toujours",
    'par moment un':'par moments un', "discussions ou j'entends":"discussions où j’entends",
    'à partir du moment ou':'à partir du moment où', 'de son Kourou':'de son courroux',
    'pour respecter les codes':'de respecter les codes',
    'nous avons appris à être complémentaire':'nous avons appris à être complémentaires',
    "elle m'a directement accepté comme son égal":"elle m’a directement acceptée comme son égale",
    'quelques instants avec Katlyn':'quelques instants avant Katlyn',
    "a durant toute son enfance était source":"a durant toute son enfance été source",
    "un démon. qui s'en était pris":"un démon qui s’en était pris",
    "comme mon propre fils":"comme mon propre fils",
    "Il n'a connu d'autres parents que nous":"Il n’a connu d’autres parents que nous",
    "m'avait élevé comme une mère":"m’avait élevée comme une mère", 'lorsque la notre':'lorsque la nôtre',
    'Je ne pu me résoudre':'Je ne pus me résoudre', "je l'ai même protégé pendant":"je l’ai même protégée pendant",
    "elle n'était pas la pour ça":"elle n’était pas là pour ça", 'avec elle elle est':'avec elle. Elle est',
    "je n'arriverai pas à être une bonne mère":"je n’arriverais pas à être une bonne mère",
    'beaucoup de mordants':'beaucoup de mordant', "que j'ai eu avec":"que j’ai eue avec",
    'P,J':'P.J.', "Je l'aime plus que tout et a su":"Je l’aime plus que tout et elle a su",
    'son père et avons divorcé':'son père et nous avons divorcé',
    'Je suis beaucoup plus posée et peut':'Je suis beaucoup plus posée et peux',
    "qui s'es perdu":"qui s’est perdu", 'pour redore le blason':'pour redorer le blason',
    "j'estime être la pour":"j’estime être là pour", 'apporter grande importance':'accorder une grande importance',
    'la première personne a m’avoir':'la première personne à m’avoir',
    'la première personne a m\'avoir expliqué"':'la première personne à m’avoir expliqué',
    'suite à tout le monde qui a pu se produire':'suite à tout le mal qui a pu se produire',
    'elle en a tout le même caractère':'elle en a tout à fait le même caractère',
    'beaucoup plus imposée et caractérielle':'beaucoup plus imposante et caractérielle',
    'une petite rose fragile a qui':'une petite rose fragile à qui',
    'Modèle fiche de présentation':'Modèle de fiche de présentation', 'Centre ville':'Centre-ville',
    'fiche personnage':'fiche de personnage', 'fiches personnages':'fiches de personnages',
    'Questions invités':'Questions des invités', 'Questions membres':'Questions des membres',
    "puisse la lire et vous accompagne":"puisse la lire et vous accompagner",
    'effectifs maximum':'effectifs maximaux', 'nombre de personnages max simultanés':'nombre maximal de personnages simultanés',
    'Mi sorcière':'Mi-sorcière', 'Mi Sorcière':'Mi-sorcière', 'mi sorcière':'mi-sorcière',
    'Mi sorcier':'Mi-sorcier', 'mi sorcier':'mi-sorcier', 'Mi démon':'Mi-démon',
    'Mi démone':'Mi-démone', 'mi démon':'mi-démon', 'mi démone':'mi-démone',
    'Mi être de lumière':'Mi-être de lumière', 'mi être de lumière':'mi-être de lumière',
    'Mi Cupidon':'Mi-Cupidon', 'Mi cupidon':'Mi-cupidon',
}

def prose(text):
    for old,new in PHRASES.items():
        text = text.replace(old,new)
    for old,new in WORDS.items():
        text = re.sub(r'(?<!\w)' + re.escape(old) + r'(?!\w)', lambda _:new,text)
    text = re.sub(r'\bca\b','ça',text)
    text = re.sub(r'\bCa\b','Ça',text)
    text = re.sub(r'[ \t]+([,.])',r'\1',text)
    text = re.sub(r'(?<=[A-Za-zÀ-ÿ])[ \t]*([!?;:])[ \t]*',r' \1 ',text)
    text = re.sub(r',(?=[A-Za-zÀ-ÿ])',', ',text)
    text = re.sub(r'(?<=[a-zà-ÿ])\.(?=[A-ZÀ-Ý])','. ',text)
    text = re.sub(r'(?<=[.!?])([ \t]+)(je|il|elle|ils|elles|nous|notre|parfois|une)\b',lambda m:m[1]+m[2].capitalize(),text)
    text = re.sub(r'(?m)^(\s*)(en 2006|ils restèrent|avec mon petit frère)',lambda m:m[1]+m[2][0].upper()+m[2][1:],text)
    return text

def correct(text):
    # Leave tags, URLs, entities and code blocks byte-for-byte intact.
    parts = re.split(r'(<(?:script|style|pre|code)\b[^>]*>.*?</(?:script|style|pre|code)>|<!--.*?-->|<[^>]*>|https?://[^\s<>]+|&(?:#\d+|#x[\da-fA-F]+|\w+);)',text,flags=re.S)
    return ''.join(part if i%2 else prose(part) for i,part in enumerate(parts))

with transaction.atomic():
    changes=[]
    for model, fields in [(Category,['name','description']),(Topic,['title','scenario_links']),(Post,['content']),(SitePage,['content'])]:
        for obj in model.objects.select_for_update().all():
            old={}
            for field in fields:
                value=getattr(obj,field)
                new=correct(value)
                if new != value:
                    old[field]=value
                    setattr(obj,field,new)
            if model is Topic:
                cards=[dict(card) for card in obj.scenario_link_cards]
                for card in cards:
                    for field in ['title','text']:
                        if field in card:
                            card[field]=correct(card[field])
                if cards != obj.scenario_link_cards:
                    old['scenario_link_cards']=obj.scenario_link_cards
                    obj.scenario_link_cards=cards
            if old:
                changes.append((obj,old))
    folder=Path(settings.BASE_DIR)/'data/spelling_backups'
    folder.mkdir(parents=True,exist_ok=True)
    (folder/(timezone.now().strftime('%Y%m%dT%H%M%S%f')+'.json')).write_text(json.dumps([dict(model=obj._meta.label,pk=obj.pk,fields=old) for obj,old in changes],ensure_ascii=False),encoding='utf-8')
    counts={}
    for obj,old in changes:
        # Direct field updates avoid publication rewards and unrelated save hooks.
        obj.__class__.objects.filter(pk=obj.pk).update(**{field:getattr(obj,field) for field in old})
        expected={field:getattr(obj,field) for field in old}
        obj.refresh_from_db()
        assert all(getattr(obj,field)==value for field,value in expected.items())
        counts[obj._meta.label]=counts.get(obj._meta.label,0)+1
    print('Corrections enregistrées et relues :',counts)
