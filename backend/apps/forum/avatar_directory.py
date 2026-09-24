"""Extraction des célébrités indiquées dans les fiches de scénarios."""

import html
import re


AVATAR_PATTERN = re.compile(r"\bFt\s+([^<(—–|;]+)", re.IGNORECASE)
NAME_PREFIX = re.compile(r"^(?:recast\s*:|feat\.?\s+|ft\.?\s+)", re.IGNORECASE)


def clean_avatar_name(value):
    name = html.unescape(value or "").strip(" \t\n\r.,:–—")
    return NAME_PREFIX.sub("", name).strip(" \t\n\r.,:–—")


def scenario_avatar(content):
    match = AVATAR_PATTERN.search(content or "")
    if not match:
        return ""
    name = clean_avatar_name(match.group(1))
    return name if len(name) <= 100 else ""
