"""Export the published race directory's branches for the Groups page.

Run from the backend directory after editing expand_race_directory.py.
The source module is parsed rather than imported because importing it publishes a post.
"""

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "expand_race_directory.py"
TARGET = ROOT.parent / "frontend" / "src" / "data" / "raceSpecialties.json"

RACE_IDS = {
    "Elfe": "Elfes",
    "Cupidon": "Cupidons",
    "Phoenix": "Phénix",
    "Valkyrie": "Valkyries",
    "Nymphe/Satyre": "Nymphes et satyres",
    "Humain": "Humains",
    "sirene-triton-charmed": "Sirènes et tritons marins",
    "Vampire": "Vampires",
    "Loup-garou": "Loups-garous",
    "Fée": "Fées",
    "Muse": "Muses",
    "sorcier-tvd": "Sorciers TVD, The Originals et Legacies",
    "sirene-tvd": "Sirènes psychiques de The Vampire Diaries",
    "Banshee": "Banshees",
    "Kanima": "Kanimas",
    "Kitsune": "Kitsunes",
    "Chien de l'enfer": "Chiens de l’enfer (Hellhounds)",
    "Chimère": "Chimères",
    "Hérétique": "Hérétiques",
    "Sphinx": "Sphinx",
    "Hybride": "Hybrides",
}

tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
groups = next(
    ast.literal_eval(node.value)
    for node in tree.body
    if isinstance(node, ast.Assign)
    and any(isinstance(target, ast.Name) and target.id == "GROUPS" for target in node.targets)
)
entries = {name: variants for _, rows in groups for name, _, variants, _ in rows}
missing = set(RACE_IDS.values()) - set(entries)
if missing:
    raise ValueError(f"Races introuvables : {sorted(missing)}")
specialties = {
    race_id: [{"name": name, "description": description} for name, description in entries[source_name]]
    for race_id, source_name in RACE_IDS.items()
    if entries[source_name]
}
TARGET.write_text(json.dumps(specialties, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{len(specialties)} fiches de races synchronisées dans {TARGET}")
