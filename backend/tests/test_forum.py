from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.forum.models import Category, Post, Topic

User = get_user_model()


class CategoryTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="admin", password="AdminPass123!", role="admin"
        )
        self.user = User.objects.create_user(
            username="user", password="UserPass123!"
        )

    def test_list_categories(self):
        Category.objects.create(name="Tech", description="Technology")
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(row["name"] == "Tech" for row in response.data["results"]))

    def test_create_category_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Science", "description": "Science stuff"}
        response = self.client.post("/api/categories/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_as_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "Science", "description": "Science stuff"}
        response = self.client.post("/api/categories/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_detail(self):
        Category.objects.create(name="Tech", slug="tech")
        response = self.client.get("/api/categories/tech/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Tech")


class TopicTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="user", password="UserPass123!", fiche_status="validated"
        )
        self.category = Category.objects.create(name="Tech", slug="tech")

    def test_create_topic(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "First Topic",
            "category": self.category.pk,
            "first_post_content": "Hello, this is the first post!",
        }
        response = self.client.post("/api/categories/tech/topics/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Topic.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 1)

    def test_create_topic_unauthenticated(self):
        data = {
            "title": "First Topic",
            "category": self.category.pk,
            "first_post_content": "Hello!",
        }
        response = self.client.post("/api/categories/tech/topics/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_topics_in_category(self):
        topic = Topic.objects.create(
            title="Test Topic", category=self.category, author=self.user
        )
        Post.objects.create(topic=topic, author=self.user, content="Content")
        response = self.client.get("/api/categories/tech/topics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)


class ScenarioRepliesTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username="scenario-admin", password="AdminPass123!", role="admin")
        self.moderator = User.objects.create_user(username="scenario-moderator", password="ModPass123!", role="moderator")
        self.member = User.objects.create_user(username="scenario-member", password="MemberPass123!")
        self.category = Category.objects.create(name="Scénarios à prendre", slug="scenarios-a-prendre")
        self.topic = Topic.objects.create(title="Scénario test", slug="scenario-test", category=self.category, author=self.admin)
        self.sheet = Post.objects.create(topic=self.topic, author=self.admin, content="Fiche originale")

    def test_member_can_reply_but_cannot_edit_scenario_sheet(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.post("/api/topics/scenario-test/posts/", {"content": "Je suis intéressée."})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.patch(f"/api/posts/{self.sheet.pk}/", {"content": "Fiche modifiée"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.sheet.refresh_from_db()
        self.assertEqual(self.sheet.content, "Fiche originale")

    def test_moderator_cannot_edit_scenario_sheet_or_title(self):
        self.client.force_authenticate(user=self.moderator)
        self.assertEqual(self.client.patch(f"/api/posts/{self.sheet.pk}/", {"content": "Fiche modifiée"}).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.patch("/api/topics/scenario-test/", {"title": "Titre modifié"}).status_code, status.HTTP_403_FORBIDDEN)

    def test_member_can_edit_own_scenario_reply(self):
        reply = Post.objects.create(topic=self.topic, author=self.member, content="Premier message")
        self.client.force_authenticate(user=self.member)
        response = self.client.patch(f"/api/posts/{reply.pk}/", {"content": "Message corrigé"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reply.refresh_from_db()
        self.assertEqual(reply.content, "Message corrigé")


class PostTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="user", password="UserPass123!", fiche_status="validated"
        )
        self.other_user = User.objects.create_user(
            username="other", password="OtherPass123!"
        )
        self.category = Category.objects.create(name="Tech", slug="tech")
        self.topic = Topic.objects.create(
            title="Test Topic", slug="test-topic",
            category=self.category, author=self.user,
        )

    def test_create_post(self):
        self.client.force_authenticate(user=self.user)
        data = {"content": "This is a reply"}
        response = self.client.post("/api/topics/test-topic/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_own_post(self):
        post = Post.objects.create(
            topic=self.topic, author=self.user, content="Original"
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/posts/{post.pk}/", {"content": "Edited"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_edit_others_post(self):
        post = Post.objects.create(
            topic=self.topic, author=self.user, content="Original"
        )
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(f"/api/posts/{post.pk}/", {"content": "Hacked"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_delete_post(self):
        moderator = User.objects.create_user(
            username="mod", password="ModPass123!", role="moderator"
        )
        post = Post.objects.create(
            topic=self.topic, author=self.user, content="Delete me"
        )
        self.client.force_authenticate(user=moderator)
        response = self.client.delete(f"/api/posts/{post.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReactionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="user", password="UserPass123!"
        )
        self.category = Category.objects.create(name="Tech", slug="tech")
        self.topic = Topic.objects.create(
            title="Test", slug="test",
            category=self.category, author=self.user,
        )
        self.post = Post.objects.create(
            topic=self.topic, author=self.user, content="Content"
        )

    def test_add_reaction(self):
        self.client.force_authenticate(user=self.user)
        data = {"reaction_type": "like"}
        response = self.client.post(f"/api/posts/{self.post.pk}/reactions/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_toggle_reaction(self):
        self.client.force_authenticate(user=self.user)
        data = {"reaction_type": "like"}
        # Add
        self.client.post(f"/api/posts/{self.post.pk}/reactions/", data)
        # Remove (toggle)
        response = self.client.post(f"/api/posts/{self.post.pk}/reactions/", data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reaction_unauthenticated(self):
        data = {"reaction_type": "like"}
        response = self.client.post(f"/api/posts/{self.post.pk}/reactions/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
