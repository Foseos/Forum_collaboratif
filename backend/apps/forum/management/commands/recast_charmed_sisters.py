"""Apply the approved Paige, Piper and Phoebe recasts consistently."""

import json
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from PIL import Image

from apps.forum.models import Topic
from apps.users.models import User


RECASTS = (
    {
        "username": "Paige Matthews Mitchell", "slug": "paige-matthews-charmed-one",
        "old_actor": "Deborah Ann Woll", "actor": "Anne Hathaway",
        "old_image": "https://zupimages.net/up/26/38/l0vf.jpg",
        "old_link_gif": "https://zupimages.net/up/26/38/m4he.gif",
        "filename": "recast-paige-anne-hathaway.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Anne_Hathaway_at_The_Apprentice_in_NYC_03_(cropped).jpg",
        "download": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Anne_Hathaway_at_The_Apprentice_in_NYC_03_(cropped).jpg?width=600",
        "credit": "Portrait : Jay Dixit, Wikimedia Commons, CC BY-SA 4.0 (recadré).",
    },
    {
        "username": "Piper Halliwell", "slug": "piper-halliwell-charmed-one",
        "old_actor": "Jennifer Love Hewitt", "actor": "Sarah Michelle Gellar",
        "old_image": "https://zupimages.net/up/25/51/lk9a.jpg",
        "old_link_gif": "https://zupimages.net/up/26/38/3fgr.gif",
        "filename": "recast-piper-sarah-michelle-gellar.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Sarah_Michelle_Gellar_(54305143551).jpg",
        "download": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Sarah_Michelle_Gellar_(54305143551).jpg?width=600",
        "credit": "Portrait : Matt Boulton, Wikimedia Commons, CC BY-SA 2.0.",
    },
    {
        "username": "Phoebe Halliwell Turner", "slug": "phoebe-halliwell-charmed-one",
        "old_actor": "Gal Gadot", "actor": "Jennifer Love Hewitt",
        "old_image": "https://zupimages.net/up/26/38/cz0r.jpg",
        "old_link_gif": "https://zupimages.net/up/26/38/zka2.gif",
        "filename": "recast-phoebe-jennifer-love-hewitt.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Jennifer_Love_Hewitt_(40605995140).jpg",
        "download": "https://commons.wikimedia.org/wiki/Special:Redirect/file/Jennifer_Love_Hewitt_(40605995140).jpg?width=600",
        "credit": "Portrait : Greg2600, Wikimedia Commons, CC BY-SA 2.0.",
    },
)


def get_portrait(recast):
    path = f"avatars/{recast['filename']}"
    if default_storage.exists(path):
        return path
    request = Request(recast["download"], headers={"User-Agent": "NexusArcanaForum/1.0 (character portraits)"})
    with urlopen(request, timeout=30) as response:
        data = response.read(5 * 1024 * 1024)
        if not response.headers.get("Content-Type", "").startswith("image/jpeg"):
            raise ValueError(f"Le portrait reçu n'est pas un JPEG : {recast['actor']}")
    with Image.open(BytesIO(data)) as image:
        image.verify()
    return default_storage.save(path, ContentFile(data))


class Command(BaseCommand):
    help = "Met à jour les avatars de Paige, Piper et Phoebe et leurs références visuelles."

    def handle(self, *args, **options):
        portraits = {item["slug"]: get_portrait(item) for item in RECASTS}
        with transaction.atomic():
            backup = {"users": [], "topics": []}
            topics_to_backup = set()
            for item in RECASTS:
                user = User.objects.select_for_update().get(username=item["username"])
                topic = Topic.objects.select_for_update().get(slug=item["slug"])
                post = topic.posts.order_by("created_at", "pk").first()
                if post is None:
                    raise ValueError(f"Scénario sans contenu : {item['slug']}")
                old_avatar = user.avatar.name if user.avatar else ""
                old = {"id": user.pk, "avatar_name": user.avatar_name, "avatar": old_avatar,
                       "profile_gif_url": user.profile_gif_url, "credits": user.credits}
                backup["users"].append(old)
                backup["topics"].append({"id": topic.pk, "scenario_avatar_name": topic.scenario_avatar_name,
                                         "post_id": post.pk, "post_content": post.content})
                topics_to_backup.add(topic.pk)

                user.avatar_name = f"Recast: {item['actor']}"
                user.avatar.name = portraits[item["slug"]]
                user.profile_gif_url = ""
                credit = f"{item['credit']} {item['source']}"
                if credit not in user.credits:
                    user.credits = (user.credits.strip() + "\n" + credit).strip()
                user.save(update_fields=["avatar_name", "avatar", "profile_gif_url", "credits"])

                content = post.content
                if item["old_actor"] in content:
                    content = content.replace(item["old_actor"], item["actor"])
                if item["old_image"] in content:
                    content = content.replace(item["old_image"], default_storage.url(portraits[item["slug"]]))
                content = content.replace('alt="Prénom NOM"', f'alt="{item["username"]} — {item["actor"]}"', 1)
                if item["source"] not in content:
                    content += (
                        '<p style="font-size:.65rem;color:#8f83a5;text-align:center;margin:.5rem 0">'
                        f'{item["credit"]} <a href="{item["source"]}" style="color:#a78bfa">Source du portrait</a>'
                        '</p>'
                    )
                if item["actor"] not in content or default_storage.url(portraits[item["slug"]]) not in content:
                    raise ValueError(f"Recast incomplet : {item['slug']}")
                if content != post.content:
                    post.content = content
                    post.save(update_fields=["content"])
                topic.scenario_avatar_name = item["actor"]
                topic.save(update_fields=["scenario_avatar_name"])

            replacements = {item["old_link_gif"]: default_storage.url(portraits[item["slug"]]) for item in RECASTS}
            for topic in Topic.objects.select_for_update().all():
                cards = topic.scenario_link_cards
                if not cards or not any(card.get("gif") in replacements for card in cards):
                    continue
                if topic.pk not in topics_to_backup:
                    backup["topics"].append({"id": topic.pk, "scenario_link_cards": cards})
                else:
                    next(row for row in backup["topics"] if row["id"] == topic.pk)["scenario_link_cards"] = cards
                topic.scenario_link_cards = [dict(card, gif=replacements.get(card.get("gif"), card.get("gif"))) for card in cards]
                topic.save(update_fields=["scenario_link_cards"])

            folder = Path(settings.BASE_DIR) / "data" / "recast_backups"
            folder.mkdir(parents=True, exist_ok=True)
            filename = folder / f"charmed-{timezone.now():%Y%m%dT%H%M%S%f}.json"
            filename.write_text(json.dumps(backup, ensure_ascii=False), encoding="utf-8")
        self.stdout.write(self.style.SUCCESS("Recast de Paige, Piper et Phoebe appliqué."))
