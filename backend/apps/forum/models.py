from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='subcategories'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def topic_count(self):
        return self.topics.count()

    @property
    def post_count(self):
        return Post.objects.filter(topic__category=self).count()


class AvatarDirectoryEntry(models.Model):
    avatar = models.CharField(max_length=100)
    character = models.CharField(max_length=150)
    status = models.CharField(max_length=10, choices=[
        ("taken", "Pris"), ("pending", "En attente"), ("scenario", "Scénario"),
    ], default="taken")
    url = models.CharField(max_length=250, blank=True)
    negotiable = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.character} — {self.avatar}"


class DemonicFormEntry(models.Model):
    name = models.CharField(max_length=120, unique=True)
    image_url = models.URLField(max_length=500, blank=True)
    character = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} — {self.character}"


class Topic(models.Model):
    class ScenarioStatus(models.TextChoices):
        FREE = "free", "Libre"
        RESERVED = "reserved", "Réservé"
        PLAYED = "played", "Joué"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="topics"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="topics"
    )
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    scenario_status = models.CharField(
        max_length=10,
        choices=ScenarioStatus.choices,
        default=ScenarioStatus.FREE,
        help_text="Statut réservé aux scénarios à prendre.",
    )
    scenario_avatar_name = models.CharField(max_length=100, blank=True, default="")
    scenario_links = models.TextField(
        blank=True,
        default="",
        help_text="Liens, relations et pistes de jeu du scénario.",
    )
    scenario_link_cards = models.JSONField(
        default=list,
        blank=True,
        help_text="Cartes GIF et textes de survol pour les liens du scénario.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_pinned", "-created_at"]
        unique_together = ["category", "slug"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness within category
            original_slug = self.slug
            counter = 1
            while Topic.objects.filter(
                category=self.category, slug=self.slug
            ).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def last_post(self):
        return self.posts.order_by("-created_at").first()


class Post(models.Model):
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="posts"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField()
    dice_result = models.PositiveSmallIntegerField(null=True, blank=True, editable=False)
    is_trusted_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Post by {self.author} in {self.topic}"

    def save(self, *args, **kwargs):
        if self.pk:
            self.is_edited = True
        super().save(*args, **kwargs)


class LotteryDraw(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lottery_draws')
    qualifying_post = models.OneToOneField(Post, on_delete=models.PROTECT, related_name='lottery_draw')
    prize = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class ArcanaTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='arcana_transactions')
    amount = models.IntegerField()
    balance_after = models.IntegerField()
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-id']


class Reaction(models.Model):
    class ReactionType(models.TextChoices):
        LIKE = "like", "J'aime"
        DISLIKE = "dislike", "Je n'aime pas"
        LOVE = "love", "J'adore"
        LAUGH = "laugh", "Haha"
        THINK = "think", "Intéressant"

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="reactions"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reactions"
    )
    reaction_type = models.CharField(
        max_length=20,
        choices=ReactionType.choices,
        default=ReactionType.LIKE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["post", "user", "reaction_type"]

    def __str__(self):
        return f"{self.user} - {self.reaction_type} on {self.post}"


class ChatMessage(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages'
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author} : {self.content[:50]}"


class PrivateMessage(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_pms'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_pms'
    )
    subject = models.CharField(max_length=200, blank=True, default='(Sans objet)')
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    is_deleted_by_sender = models.BooleanField(default=False)
    is_deleted_by_recipient = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"PM: {self.sender} → {self.recipient} | {self.subject[:30]}"


class ContactRequest(models.Model):
    class Kind(models.TextChoices):
        PRIVACY = 'privacy', 'Données personnelles'
        REPORT = 'report', 'Signalement'
        GENERAL = 'general', 'Autre demande'

    kind = models.CharField(max_length=10, choices=Kind.choices)
    email = models.EmailField()
    message = models.TextField(max_length=3000)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class SitePage(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField(blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='site_pages_edited'
    )

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return f"SitePage: {self.slug}"
