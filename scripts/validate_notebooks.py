from __future__ import annotations

from pathlib import Path

import nbformat


def iter_notebooks(root: Path) -> list[Path]:
    notebooks: list[Path] = []
    for path in root.rglob("*.ipynb"):
        if ".ipynb_checkpoints" in path.parts:
            continue
        notebooks.append(path)
    return sorted(notebooks)


def main() -> int:
    root = Path("notebooks")
    if not root.exists():
        print("No notebooks directory found; skipping validation.")
        return 0

    notebooks = iter_notebooks(root)
    if not notebooks:
        print("No notebooks found; skipping validation.")
        return 0

    errors: list[str] = []
    for path in notebooks:
        try:
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path}: {exc}")

    if errors:
        print("Notebook validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"Validated {len(notebooks)} notebook(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
