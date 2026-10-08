"""Production routes for the combined Vue and Django Render service."""

from django.core.files.storage import default_storage
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import path, re_path
from django.views.generic import TemplateView
from xml.etree import ElementTree

from apps.forum.models import Category

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


def robots_txt(request):
    site_url = settings.FORUM_URL.rstrip('/')
    return HttpResponse(
        f"User-agent: *\nAllow: /\nDisallow: /admin/\n"
        f"Disallow: /profile\nDisallow: /parametres\n"
        f"Disallow: /notifications\nDisallow: /messageries\n"
        f"Sitemap: {site_url}/sitemap.xml\n",
        content_type="text/plain; charset=utf-8",
    )


def sitemap_xml(request):
    site_url = settings.FORUM_URL.rstrip('/')
    namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    root = ElementTree.Element('urlset', xmlns=namespace)
    paths = ['/', '/groupes', '/membres', '/bienvenue/parcours-arrivee']
    paths += [f'/categories/{slug}' for slug in Category.objects.exclude(slug='').values_list('slug', flat=True).distinct()]
    for page in paths:
        ElementTree.SubElement(ElementTree.SubElement(root, 'url'), 'loc').text = site_url + page
    return HttpResponse(ElementTree.tostring(root, encoding='utf-8', xml_declaration=True), content_type='application/xml')


urlpatterns = [
    path("health/", lambda request: HttpResponse("ok")),
    path("robots.txt", robots_txt),
    path("sitemap.xml", sitemap_xml),
    path("media/<path:name>", media_redirect),
    path("propositions/<path:name>", lambda request, name: public_asset_redirect(request, f"propositions/{name}")),
    path("Image_de_base_photo_de_profil.jpg", lambda request: public_asset_redirect(request, "Image_de_base_photo_de_profil.jpg")),
    path("demon-form-placeholder.svg", lambda request: public_asset_redirect(request, "demon-form-placeholder.svg")),
    *application_urls,
    re_path(r"^(?!api/|admin/|static/|media/).*$", TemplateView.as_view(template_name="frontend/index.html")),
]
