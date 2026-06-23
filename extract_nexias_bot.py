#!/usr/bin/env python3
"""
extract_nexias_bot.py

Usage: run this from the repository root to extract the files contained in the
`nexias-bot` zip-like file (the repository currently contains a single file named
`nexias-bot` which is a ZIP archive). The script will extract all entries into
the target directory (default: current directory) and preserve internal
subdirectories. Existing files will be overwritten only if --overwrite is used.

Example:
  python3 extract_nexias_bot.py --target . --overwrite

"""
import argparse
import zipfile
import sys
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description="Extract the 'nexias-bot' archive into the repo root")
    p.add_argument("archive", nargs="?", default="nexias-bot", help="path to the archive file (default: 'nexias-bot')")
    p.add_argument("--target", "-t", default=".", help="target directory to extract into (default: current directory)")
    p.add_argument("--overwrite", "-o", action="store_true", help="overwrite existing files")
    args = p.parse_args()

    archive = Path(args.archive)
    target_dir = Path(args.target)

    if not archive.exists():
        print(f"Error: archive '{archive}' not found. Run this from the repository root where the file 'nexias-bot' is located.")
        sys.exit(2)

    if not zipfile.is_zipfile(archive):
        print(f"Error: file '{archive}' does not appear to be a zip archive.")
        sys.exit(2)

    target_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(archive, 'r') as z:
        members = z.infolist()
        if not members:
            print("Archive is empty.")
            return
        for info in members:
            # Skip directories (ZipFile.extract handles them)
            dest_path = target_dir / info.filename
            if dest_path.exists() and not args.overwrite:
                print(f"Skipping existing file: {dest_path} (use --overwrite to replace)")
                continue
            # Ensure parent directory exists
            if dest_path.parent and not dest_path.parent.exists():
                dest_path.parent.mkdir(parents=True, exist_ok=True)
            z.extract(info, path=target_dir)
            print(f"Extracted: {info.filename}")

    print("Extraction complete.")


if __name__ == '__main__':
    main()
