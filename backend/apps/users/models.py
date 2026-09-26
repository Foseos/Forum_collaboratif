from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class RelaxedUsernameValidator(RegexValidator):
    """Accepte les lettres unicode, les espaces, les chiffres, tirets et apostrophes."""
    regex = r"^[\w\s\-'\.]+$"
    flags = 0  # unicode par défaut (pas re.ASCII)
    message = (
        "Le nom peut contenir des lettres (avec accents), espaces, "
        "chiffres, tirets et apostrophes."
    )


class User(AbstractUser):
    username_validator = RelaxedUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        verbose_name="Nom du personnage",
        error_messages={"unique": "Un personnage avec ce nom existe déjà."},
    )
    class Role(models.TextChoices):
        FONDATRICE = "fondatrice", "Fondatrice"
        ADMIN = "admin", "Administrateur"
        MODERATOR = "moderator", "Modérateur"
        USER = "user", "Utilisateur"

    class Sexe(models.TextChoices):
        FEMININ = "feminin", "Féminin"
        MASCULIN = "masculin", "Masculin"
        INDETERMINE = "indetermine", "Indéterminé"

    class FicheStatus(models.TextChoices):
        PENDING = "pending", "En attente"
        VALIDATED = "validated", "Validée"
        REJECTED = "rejected", "À corriger"

    class RpAvailability(models.TextChoices):
        OPEN = "open", "Ouvert aux RP"
        DISCUSS = "discuss", "À discuter"
        UNAVAILABLE = "unavailable", "Indisponible"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )
    show_in_staff_team = models.BooleanField(default=True, verbose_name="Afficher dans la team du staff")
    last_seen = models.DateTimeField(null=True, blank=True, verbose_name="Dernière activité")
    chat_last_seen = models.DateTimeField(null=True, blank=True, db_index=True)
    fiche_status = models.CharField(
        max_length=12,
        choices=FicheStatus.choices,
        default=FicheStatus.PENDING,
        verbose_name="Statut de fiche",
    )
    rp_availability = models.CharField(
        max_length=12, choices=RpAvailability.choices,
        default=RpAvailability.DISCUSS,
        verbose_name="Disponibilité RP",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )
    bio = models.TextField(blank=True)
    signature = models.TextField(
        blank=True,
        default="",
        verbose_name="Signature",
        help_text="Texte libre ou URL directe vers une image/GIF de signature.",
    )
    profile_gif_url = models.URLField(
        max_length=500,
        blank=True,
        default="",
        help_text="URL directe d'un petit GIF affiché sous le portrait du personnage.",
    )

    # --- Champs RPG (Carte d'identité) ---
    sexe = models.CharField(
        max_length=20,
        choices=Sexe.choices,
        blank=True,
        default="",
    )
    race = models.CharField(max_length=100, blank=True, default="")
    nature = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Nature",
        help_text="Sous-catégorie de la race (ex : Furie, Succube, Fantôme...)",
    )
    camp = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="Camp",
        help_text="Alignement moral du personnage (ex : Bien, Mal, Neutre)",
    )
    groupe = models.CharField(max_length=100, blank=True, default="")
    pseudo = models.CharField(max_length=100, blank=True, default="")
    situation = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name="Situation sociale et familiale",
    )
    metier = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Métier",
    )
    age_personnage = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="Âge du personnage",
    )
    pouvoirs = models.TextField(blank=True, default="")
    lieu_residence = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name="Lieu de résidence",
    )
    quartier_residentiel = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Quartier résidentiel",
    )
    credits = models.TextField(
        blank=True,
        default="",
        verbose_name="Crédits",
        help_text="Crédits pour les images, GIFs ou ressources du profil.",
    )
    compte_bancaire = models.IntegerField(
        default=0,
        verbose_name="Compte bancaire RP",
        help_text="Montant en monnaie fictive, modifiable uniquement par un administrateur.",
    )
    email_topic_replies = models.BooleanField(default=True, verbose_name="E-mails de réponse aux sujets")
    avatar_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Avatar (célébrité)",
    )
    double_compte = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Double compte",
    )
    pending_email = models.EmailField(blank=True, default="")
    last_confirmation_sent_at = models.DateTimeField(null=True, blank=True)
    last_password_reset_sent_at = models.DateTimeField(null=True, blank=True)
    main_account = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='linked_accounts',
        help_text='Compte principal lié après validation par le staff.',
    )

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role in (self.Role.ADMIN, self.Role.MODERATOR, self.Role.FONDATRICE)
