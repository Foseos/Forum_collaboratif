from django.contrib import admin

from .models import Category, Post, Reaction, Topic


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order", "topic_count", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order"]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author", "is_pinned", "is_locked", "created_at"]
    list_filter = ["category", "is_pinned", "is_locked"]
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
