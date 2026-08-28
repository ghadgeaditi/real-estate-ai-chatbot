"""Regenerate the bundled synthetic dataset.

No network requests are made by this module. The records are fictional and are
provided only to exercise normalization, retrieval, LLM grounding and UI flows.
"""
import json
from pathlib import Path

SOURCE = Path(__file__).with_name("properties.json")


def main() -> None:
    records = json.loads(SOURCE.read_text(encoding="utf-8"))
    print(f"Synthetic demo dataset contains {len(records)} records.")
    print("No live websites were scraped.")


if __name__ == "__main__":
    main()
