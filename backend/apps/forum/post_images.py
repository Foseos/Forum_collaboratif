"""Image and GIF uploads for forum replies."""

from uuid import uuid4

from django.core.files.storage import default_storage
from PIL import Image, UnidentifiedImageError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


IMAGE_FORMATS = {"JPEG": "jpg", "PNG": "png", "GIF": "gif", "WEBP": "webp"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024
MAX_IMAGE_PIXELS = 16_000_000


class PostImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        upload = request.FILES.get("image")
        if upload is None:
            return Response({"detail": "Choisissez une image ou un GIF."}, status=400)
        if upload.size > MAX_IMAGE_BYTES:
            return Response({"detail": "L’image doit peser moins de 5 Mo."}, status=400)
        try:
            with Image.open(upload) as image:
                image_format = image.format
                if image_format not in IMAGE_FORMATS or image.width * image.height > MAX_IMAGE_PIXELS:
                    return Response({"detail": "Format ou dimensions d’image non acceptés."}, status=400)
                image.verify()
        except (UnidentifiedImageError, OSError, ValueError):
            return Response({"detail": "Ce fichier n’est pas une image valide."}, status=400)
        upload.seek(0)
        path = default_storage.save(f"post_images/{uuid4().hex}.{IMAGE_FORMATS[image_format]}", upload)
        return Response({"url": default_storage.url(path)}, status=201)
