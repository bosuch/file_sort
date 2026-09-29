#!/usr/bin/env python3
"""
Sort files in a directory into subfolders named after the first letter or number of each file name.

    report.docx   -> R\report.docx
    2024_notes.txt -> 2\2024_notes.txt
    _scratch.txt  -> _Other\_scratch.txt   (first char isn't a letter/number)

Only files directly inside the target directory are moved (no recursion), and existing subfolders are left alone.

Usage:
    python sort_files_by_first_char.py "C:\\Users\\Bill\\Downloads"
    python sort_files_by_first_char.py "C:\\Users\\Bill\\Downloads" --dry-run
"""

import argparse
import shutil
import sys
from pathlib import Path

OTHER_FOLDER = "_Other"


def folder_for(filename: str) -> str:
    """Return the subfolder name for a file based on its first character."""
    first = filename[0]
    if first.isalnum():
        return first.upper()  # Windows is case-insensitive, so merge a/A
    return OTHER_FOLDER


def unique_destination(dest: Path) -> Path:
    """If dest already exists, return 'name (1).ext', 'name (2).ext', etc."""
    if not dest.exists():
        return dest
    counter = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({counter}){dest.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def sort_directory(directory: Path, dry_run: bool = False) -> None:
    script_path = Path(__file__).resolve()
    moved = skipped = errors = 0

    for item in sorted(directory.iterdir()):
        if not item.is_file():
            continue
        if item.resolve() == script_path:
            skipped += 1
            continue

        target_dir = directory / folder_for(item.name)
        destination = unique_destination(target_dir / item.name)

        if dry_run:
            print(f"[dry run] {item.name} -> {destination.relative_to(directory)}")
            moved += 1
            continue

        try:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
            print(f"{item.name} -> {destination.relative_to(directory)}")
            moved += 1
        except (OSError, shutil.Error) as exc:
            print(f"ERROR moving {item.name}: {exc}", file=sys.stderr)
            errors += 1

    verb = "Would move" if dry_run else "Moved"
    print(f"\n{verb} {moved} file(s). Skipped {skipped}. Errors: {errors}.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Move files into subfolders named for the first character of the file name."
    )
    parser.add_argument("directory", type=Path, help="Directory to organize")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would happen without moving anything"
    )
    args = parser.parse_args()

    directory = args.directory.expanduser().resolve()
    if not directory.is_dir():
        sys.exit(f"Error: '{directory}' is not a directory.")

    sort_directory(directory, args.dry_run)


if __name__ == "__main__":
    main()
