"""
Test Edge Cases for Handbook Variations:
1. Handbook with completely missing contact table
2. Handbook with foreign / international phone formats (+65, +1, hyphens, brackets)
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from condo_classifier.semantic_rag import SemanticRAGEngine


def test_missing_contact_table(tmp_path: Path):
    print("\n=== TEST EDGE CASE 1: Completely Missing Contact Table ===")
    kb_text = """# Sunset Villas Resident Handbook

## 1. General Rules
Residents must maintain cleanliness in common areas. No dumping of bulky waste.

## 2. Swimming Pool
Pool hours are 07:00 to 21:00 daily.
"""
    kb_file = tmp_path / "sunset_villas.md"
    kb_file.write_text(kb_text, encoding="utf-8")

    engine = SemanticRAGEngine(kb_path=kb_file)
    engine.initialize()

    print(f"Detected Estate Name: {repr(engine.estate_name)}")
    print(f"Primary Contact: {repr(engine.primary_estate_contact)}")

    res = engine.query("What time does the swimming pool close?")
    print(f"Answer:\n{res.answer}")
    return engine, res


def test_foreign_phone_formats(tmp_path: Path):
    print("\n=== TEST EDGE CASE 2: International / Non-standard Phone Formats ===")
    kb_text = """# Royal Palms Residences Handbook

## Important Estate Directory
| Management Office | Tel: | +65 6789-0123 |
| Concierge / Guardhouse | Hotline: | +65 (0) 6888 7766 |
| Emergency Lift Hotline | Phone: | +1-800-555-0199 |

## 1. Gym Guidelines
The gym is open 24/7 for residents.
"""
    kb_file = tmp_path / "royal_palms.md"
    kb_file.write_text(kb_text, encoding="utf-8")

    engine = SemanticRAGEngine(kb_path=kb_file)
    engine.initialize()

    print(f"Detected Estate Name: {repr(engine.estate_name)}")
    print(f"Primary Contact: {repr(engine.primary_estate_contact)}")

    res = engine.query("What are the gym hours?")
    print(f"Answer:\n{res.answer}")
    return engine, res


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        test_missing_contact_table(p)
        test_foreign_phone_formats(p)
