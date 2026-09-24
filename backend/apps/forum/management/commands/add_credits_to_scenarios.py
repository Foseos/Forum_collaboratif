from django.core.management.base import BaseCommand

from apps.forum.models import Topic


CREDITS_BLOCK = """
<p class="scenario-credit-line" style="margin:1.25rem 0 0;text-align:right;color:#8b7aa8;font-size:.7rem;font-style:italic;">
  <strong>Crédits :</strong> avatar, images, GIFs et ressources à renseigner.
</p>
""".strip()


class Command(BaseCommand):
    help = "Ajoute une ligne Crédits aux fiches de scénarios existantes."

    def handle(self, *args, **options):
        updated = 0
        topics = Topic.objects.filter(category__slug="scenarios-a-prendre")
        for topic in topics:
            post = topic.posts.order_by("created_at").first()
            if not post or "scenario-credit-line" in post.content:
                continue
            post.content = f"{post.content}\n{CREDITS_BLOCK}"
            post.save(update_fields=["content", "updated_at"])
            updated += 1
        self.stdout.write(self.style.SUCCESS(f"Ligne Crédits ajoutée à {updated} fiches de scénario."))
