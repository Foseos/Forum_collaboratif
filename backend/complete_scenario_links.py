"""Add playable relationship cards to scenarios whose link area is empty."""

import json
import re
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.forum.models import Topic


# Each relationship is phrased as an open playing hook, not a fixed outcome.
LINKS = {
    "Briséis Argent": [
        ("Nyméa Argent", "Un nom en commun à explorer", "Nous portons le même nom, mais notre parenté éventuelle et notre histoire commune restent à définir ensemble. Un document ou un ancien pacte pourrait nous amener à chercher des réponses."),
        ("Kira Yukimura", "Magies à comparer", "Ton lien avec les esprits m'intrigue. Nous pourrions confronter nos expériences sans supposer que nos traditions fonctionnent de la même manière."),
        ("Vivienne Montana", "Une enquête possible", "Nous savons toutes deux que les histoires de famille laissent des traces. Une recherche dans les archives pourrait nous rapprocher, si nous choisissons de nous faire confiance."),
    ],
    "Nyméa Argent": [
        ("Briséis Argent", "Une histoire à définir", "Notre nom ouvre des questions, mais je ne veux pas nous inventer un passé commun. Cherchons ce qu'il signifie pour chacune avant de décider du lien que nous voulons construire."),
        ("Kira Yukimura", "Récits et esprits", "Ta manière d'aborder les esprits peut éclairer mes recherches. Je voudrais échanger avec toi sans prétendre que nos pouvoirs sont identiques."),
        ("Vivienne Montana", "Archives partagées", "Une trace de magie ancienne pourrait réunir nos recherches. Nous pouvons confronter nos sources et garder chacune le droit de choisir ce que nous révélons."),
    ],
    "Malia Tate": [
        ("Peter Hale", "Père, confiance à construire", "Notre lien de sang existe, mais il ne décide pas de ma loyauté. Je peux te parler sans te promettre d'approuver tes choix."),
        ("Scott McCall", "Meute choisie", "Ta meute m'a laissé une place quand j'en cherchais une. Je veux rester libre d'exprimer mes désaccords tout en répondant présente si nous décidons de nous entraider."),
        ("Stiles Stilinski", "Un passé qui compte", "Nous avons partagé des années difficiles et des moments précieux. Notre relation actuelle appartient à nos choix présents, pas à une histoire figée."),
    ],
    "Kira Yukimura": [
        ("Scott McCall", "Retrouvailles à leur rythme", "Notre histoire a compté pour moi. J'aimerais apprendre qui nous sommes devenus, sans présumer de ce que nous serons l'un pour l'autre."),
        ("Malia Tate", "Complicité possible", "Tu dis souvent tout haut ce que je n'ose pas formuler. Nous pouvons nous retrouver, parler de nos parcours et choisir de nouvelles aventures."),
        ("Lydia Martin", "Chercher des réponses", "Tes perceptions et mon lien aux esprits ne sont pas les mêmes. Nos questions pourraient pourtant se rejoindre lorsqu'une manifestation nous échappe."),
    ],
    "Liam Dunbar": [
        ("Scott McCall", "Alpha et ancien mentor", "Tu m'as sauvé la vie et appris à vivre avec la morsure. Je tiens à toi, mais j'ai aussi besoin de prendre mes propres décisions."),
        ("Malia Tate", "Franchise dans la meute", "Tu connais la difficulté de maîtriser une transformation sans perdre sa voix. Nous pouvons nous entraîner ou nous heurter, puis apprendre à mieux nous comprendre."),
        ("Derek Hale", "Expérience à écouter", "Ton passé de loup et d'Alpha pourrait m'aider. Je préfère poser des questions franches plutôt que te demander une réponse à tout."),
    ],
    "Isaac Lahey": [
        ("Derek Hale", "Une morsure et une histoire", "Tu m'as offert une issue lorsque je ne voyais plus de choix. Cela ne rend pas simples toutes les décisions prises ensuite ; nous pouvons en parler sans effacer le passé."),
        ("Scott McCall", "Amitié de meute", "Tu m'as traité comme un allié au moment où j'en avais besoin. Nous pouvons nous retrouver sans supposer que je reprendrai aussitôt mon ancienne place."),
        ("Allison Argent", "Souvenirs et liberté", "Ce que nous avons vécu reste important. Ton retour nous permet de parler, mais aucune relation présente ne doit être décidée avant nous."),
    ],
    "Jackson Whittemore": [
        ("Lydia Martin", "Une histoire transformée", "Tu as connu la personne que j'étais avant et pendant le Kanima. J'aimerais que nous puissions nous parler aujourd'hui sans être enfermés dans nos anciens rôles."),
        ("Scott McCall", "Une ancienne rivalité", "Nos débuts ont été difficiles. Si nous coopérons à San Francisco, ce sera sur ce que nous faisons maintenant, pas sur une confiance présumée."),
        ("Stiles Stilinski", "Des questions en suspens", "Tu as vu de près ce que ma transformation a coûté aux autres. Je peux entendre tes questions sans te demander d'oublier les faits."),
    ],
    "Chris Argent": [
        ("Allison Argent", "Père et fille retrouvés", "Ton retour me donne envie de te protéger encore davantage. Je dois aussi respecter tes décisions et découvrir la personne que tu es devenue."),
        ("Kate Argent", "Frère et sœur en désaccord", "Nous partageons une famille, pas la même manière de juger nos actes. Si nous reparlons, il faudra regarder notre histoire en face."),
        ("Scott McCall", "Confiance éprouvée", "J'ai appris à juger tes choix plutôt que ta nature. Nous pouvons agir ensemble sans être toujours d'accord sur la méthode."),
    ],
    "Kate Argent": [
        ("Chris Argent", "Famille fracturée", "Tu connais trop bien mes choix pour accepter une simple promesse. Nous pouvons nous confronter ou négocier, sans faire semblant que tout est réglé."),
        ("Allison Argent", "Tante et nièce", "Ton retour ne me donne aucun droit sur ta vie. Si tu souhaites me parler, je devrai accepter que tu poses tes propres limites."),
        ("Derek Hale", "Un passé sans pardon dû", "Ce que j'ai fait à ta famille ne disparaît pas. Toute rencontre devra respecter ton histoire et se jouer sans te demander de me pardonner."),
    ],
    "Jordan Parrish": [
        ("Lydia Martin", "Une confiance à redéfinir", "Tu m'as aidé à comprendre que mes perceptions avaient un sens. J'aimerais poursuivre nos échanges sans fixer à l'avance leur place dans nos vies."),
        ("Scott McCall", "Protection commune", "Tu connais les menaces que je perçois sans toujours pouvoir les expliquer. Nous pouvons enquêter ensemble, sans confondre intuition et certitude."),
        ("Chris Argent", "Alliés de terrain possibles", "Ton expérience de chasseur et mon instinct peuvent se compléter. Je veux d'abord comprendre notre objectif et les risques pour ceux que nous protégeons."),
    ],
}


with transaction.atomic():
    scenarios = {t.title: t for t in Topic.objects.select_for_update().filter(category__slug="scenarios-a-prendre")}
    if set(LINKS) - set(scenarios):
        raise ValueError("Fiches absentes : " + repr(set(LINKS) - set(scenarios)))
    preferred_images = {}
    for topic in scenarios.values():
        for card in topic.scenario_link_cards or []:
            for name in scenarios:
                if card.get("title", "").startswith(name + " — ") and card.get("gif"):
                    preferred_images.setdefault(name, card["gif"])
    for name in {target for relations in LINKS.values() for target, _, _ in relations}:
        if name not in scenarios:
            raise ValueError("Personnage lié absent : " + name)
        if name not in preferred_images:
            post = scenarios[name].posts.order_by("created_at", "pk").first()
            image = re.search(r'<img\b[^>]*src="([^"]+)"', post.content if post else "")
            if not image:
                raise ValueError("Portrait absent : " + name)
            preferred_images[name] = image.group(1)
    for name in LINKS:
        if scenarios[name].scenario_link_cards:
            raise ValueError("Liens déjà présents : " + name)
    backup_dir = Path(settings.BASE_DIR) / "data" / "scenario_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    (backup_dir / ("missing-links-" + timezone.now().strftime("%Y%m%dT%H%M%S%f") + ".json")).write_text(
        json.dumps([{"topic_id": scenarios[name].pk, "title": name, "cards": scenarios[name].scenario_link_cards, "links": scenarios[name].scenario_links} for name in LINKS], ensure_ascii=False), encoding="utf-8"
    )
    for name, relations in LINKS.items():
        topic = scenarios[name]
        topic.scenario_link_cards = [{"title": target + " — " + label, "text": text, "gif": preferred_images[target]} for target, label, text in relations]
        topic.save(update_fields=["scenario_link_cards"])
        print(name + " : " + str(len(relations)) + " liens")
