"""Publie les pouvoirs de fonction dans les données de la page Groupes."""

import json
from pathlib import Path

from faction_role_powers import FACTION_ROLES


target = Path(__file__).resolve().parent.parent / "frontend" / "src" / "data" / "factionRoles.json"
target.write_text(json.dumps(FACTION_ROLES, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{sum(map(len, FACTION_ROLES.values()))} rôles synchronisés dans {target}")
