"""Production routes for the combined Vue and Django Render service."""

from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import path, re_path
from django.views.generic import TemplateView

from .urls import urlpatterns as application_urls


def media_redirect(request, name):
    # Old post bodies contain /media/... links. Keep them valid after migration.
    if ".." in name.split("/"):
        return HttpResponseBadRequest()
    return HttpResponseRedirect(default_storage.url(name))


def public_asset_redirect(request, name):
    if ".." in name.split("/"):
        return HttpResponseBadRequest()
    return HttpResponseRedirect(f"/static/frontend/{name}")


urlpatterns = [
    path("health/", lambda request: HttpResponse("ok")),
    path("media/<path:name>", media_redirect),
    path("propositions/<path:name>", lambda request, name: public_asset_redirect(request, f"propositions/{name}")),
    path("Image_de_base_photo_de_profil.jpg", lambda request: public_asset_redirect(request, "Image_de_base_photo_de_profil.jpg")),
    path("demon-form-placeholder.svg", lambda request: public_asset_redirect(request, "demon-form-placeholder.svg")),
    *application_urls,
    re_path(r"^(?!api/|admin/|static/|media/).*$", TemplateView.as_view(template_name="frontend/index.html")),
]
