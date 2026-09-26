from django.contrib import admin

from .models import AvatarDirectoryEntry, Category, ContactRequest, DemonicFormEntry, Post, Reaction, Topic


@admin.register(AvatarDirectoryEntry)
class AvatarDirectoryEntryAdmin(admin.ModelAdmin):
    list_display = ["character", "avatar", "status"]
    search_fields = ["character", "avatar"]


@admin.register(DemonicFormEntry)
class DemonicFormEntryAdmin(admin.ModelAdmin):
    list_display = ["name", "character"]
    search_fields = ["name", "character"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order", "topic_count", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order"]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author", "scenario_status", "is_pinned", "is_locked", "created_at"]
    list_filter = ["category", "scenario_status", "is_pinned", "is_locked"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["__str__", "author", "topic", "created_at", "is_edited"]
    list_filter = ["is_edited", "created_at"]
    search_fields = ["content"]


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "reaction_type", "created_at"]
    list_filter = ["reaction_type"]


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['kind', 'email', 'post', 'is_resolved', 'created_at']
    list_filter = ['kind', 'is_resolved', 'created_at']
    search_fields = ['email', 'message']
    readonly_fields = ['kind', 'email', 'message', 'post', 'author', 'created_at']
