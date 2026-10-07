"""Identify the forum categories used as roleplay locations."""

from .models import Category


RP_ROOTS = {
    'san-francisco', 'mystic-falls', 'la-nouvelle-orleans', 'beacon-hills',
    'les-enfers', 'les-cieux', 'dimensions-alternatives', 'continents',
    'repaires-des-alliances',
}


def rp_category_ids():
    categories = list(Category.objects.values('id', 'slug', 'parent_id'))
    # San Francisco's location categories were created without parent links;
    # their reserved order range identifies those RP locations.
    selected = {row['id'] for row in categories if row['slug'] in RP_ROOTS}
    selected.update(Category.objects.filter(order__gte=100, order__lt=300).values_list('id', flat=True))
    while True:
        expanded = selected | {row['id'] for row in categories if row['parent_id'] in selected}
        if expanded == selected:
            return selected
        selected = expanded
