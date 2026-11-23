#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path


NOTEBOOK = Path("Fabric_Lakehouse_Optimization_and_Maintenance_Customer.ipynb")
UUID = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-"
    r"[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"
)
JWT = re.compile(r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\b")


def main() -> int:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    errors: list[str] = []
    concrete_uuids: set[str] = set()

    for index, cell in enumerate(notebook.get("cells", [])):
        source = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code":
            if cell.get("outputs"):
                errors.append(f"cell {index}: notebook output is not empty")
            if cell.get("execution_count") is not None:
                errors.append(f"cell {index}: execution_count must be null")

        if JWT.search(source):
            errors.append(f"cell {index}: possible JWT/token")
        concrete_uuids.update(UUID.findall(source))

    if concrete_uuids:
        errors.append(
            "notebook contains concrete UUIDs: "
            + ", ".join(sorted(concrete_uuids))
        )

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1

    print("Public notebook validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
