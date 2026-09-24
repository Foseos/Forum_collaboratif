from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image
from rest_framework.test import APIClient

from apps.forum.html_safety import sanitize_member_html


class PostImageUploadTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username="image-user", password="Secret123!")

    def test_authenticated_player_can_upload_an_image(self):
        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            self.client.force_authenticate(user=self.user)
            buffer = BytesIO()
            Image.new("RGB", (10, 10), "red").save(buffer, format="PNG")
            image = SimpleUploadedFile("test.png", buffer.getvalue(), content_type="image/png")
            response = self.client.post("/api/posts/images/", {"image": image}, format="multipart")
            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.data["url"].startswith("/media/post_images/"))

    def test_non_image_is_rejected(self):
        self.client.force_authenticate(user=self.user)
        image = SimpleUploadedFile("test.png", b"not an image", content_type="image/png")
        response = self.client.post("/api/posts/images/", {"image": image}, format="multipart")
        self.assertEqual(response.status_code, 400)

    def test_reply_formatting_survives_publication_sanitizer(self):
        html = '<strike>Rayé</strike><span style="color:#a78bfa">Coloré</span><div style="text-align:center">Centré</div><img src="/media/post_images/demo.gif" alt="GIF">'
        cleaned = sanitize_member_html(html)
        self.assertIn('<strike>Rayé</strike>', cleaned)
        self.assertIn('color:', cleaned)
        self.assertIn('text-align:center', cleaned)
        self.assertIn('/media/post_images/demo.gif', cleaned)

    def test_internal_link_survives_and_unsafe_link_is_removed(self):
        cleaned = sanitize_member_html('<a href="/topics/mon-sujet">Mon sujet</a><a href="javascript:alert(1)">Mauvais</a>')
        self.assertIn('href="/topics/mon-sujet"', cleaned)
        self.assertNotIn('javascript:', cleaned)
