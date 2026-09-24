from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.forum.models import Post, Reaction

from .models import Notification


@receiver(post_save, sender=Post)
def notify_on_new_post(sender, instance, created, **kwargs):
    if not created:
        return

    topic = instance.topic
    if instance.is_trusted_html and 'data-nexus-validation="1"' in instance.content:
        Notification.objects.create(
            recipient=topic.author,
            sender=instance.author,
            notification_type=Notification.NotificationType.TOPIC_REPLY,
            message=f"Votre fiche « {topic.title} » a été validée par la fondatrice.",
            target_content_type=ContentType.objects.get_for_model(instance),
            target_object_id=instance.pk,
        )
        return
    # Notify topic author if someone else replied
    if topic.author != instance.author:
        Notification.objects.create(
            recipient=topic.author,
            sender=instance.author,
            notification_type=Notification.NotificationType.TOPIC_REPLY,
            message=f"{instance.author.username} a répondu à votre sujet « {topic.title} »",
            target_content_type=ContentType.objects.get_for_model(instance),
            target_object_id=instance.pk,
        )


@receiver(post_save, sender=Reaction)
def notify_on_reaction(sender, instance, created, **kwargs):
    if not created:
        return

    post = instance.post
    if post.author != instance.user:
        Notification.objects.create(
            recipient=post.author,
            sender=instance.user,
            notification_type=Notification.NotificationType.REACTION,
            message=f"{instance.user.username} a réagi à votre message",
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=post.pk,
        )
