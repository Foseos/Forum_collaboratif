"""Single-service Render deployment with Neon Postgres and object storage."""

import os

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

from .prod import *  # noqa: F401, F403


database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise ImproperlyConfigured("DATABASE_URL doit être défini sur Render.")
DATABASES = {"default": dj_database_url.parse(database_url, conn_max_age=0)}
ROOT_URLCONF = "config.urls_render"
render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_hostname}")
FORUM_URL = os.environ.get("FORUM_URL") or f"https://{render_hostname}"

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_DIRS = [("frontend", BASE_DIR / "static" / "frontend")]
STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]

storage_keys = (
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_STORAGE_BUCKET_NAME",
    "AWS_S3_ENDPOINT_URL",
)
missing_storage_keys = [key for key in storage_keys if not os.environ.get(key)]
if missing_storage_keys:
    raise ImproperlyConfigured(
        "Stockage des images incomplet : " + ", ".join(missing_storage_keys)
    )

AWS_S3_REGION_NAME = os.environ.get("AWS_REGION", "us-east-2")
AWS_S3_ADDRESSING_STYLE = "path"
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None
STORAGES["default"] = {"BACKEND": "storages.backends.s3.S3Storage"}

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
if not RESEND_API_KEY:
    raise ImproperlyConfigured("RESEND_API_KEY doit être défini sur Render.")
EMAIL_BACKEND = "anymail.backends.resend.EmailBackend"
