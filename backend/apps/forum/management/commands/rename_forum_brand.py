import re

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models, transaction


OLD_BRAND = re.compile(r"charmed(?:\s|&nbsp;|&#160;|&#xA0;)+arcana", re.IGNORECASE)


def replace_brand(value):
    if isinstance(value, str):
        return OLD_BRAND.sub("Nexus Arcana", value)
    if isinstance(value, list):
        return [replace_brand(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_brand(item) for key, item in value.items()}
    return value


class Command(BaseCommand):
    help = "Update the forum name in existing text and JSON content."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        total = 0
        for model in apps.get_models():
            if model._meta.app_label not in {"forum", "users", "notifications"}:
                continue
            fields = [
                field.name for field in model._meta.concrete_fields
                if isinstance(field, (models.CharField, models.TextField, models.JSONField))
                and not field.primary_key
            ]
            if not fields:
                continue
            count = 0
            for row in model.objects.values("pk", *fields).iterator():
                changes = {}
                for name in fields:
                    updated = replace_brand(row[name])
                    if updated != row[name]:
                        changes[name] = updated
                if changes:
                    count += 1
                    if options["apply"]:
                        model.objects.filter(pk=row["pk"]).update(**changes)
            if count:
                self.stdout.write(f"{model._meta.label}: {count}")
            total += count
        self.stdout.write(f"{'Updated' if options['apply'] else 'Matching'} records: {total}")
