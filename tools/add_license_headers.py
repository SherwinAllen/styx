#!/usr/bin/env python3
"""
StyX - License Header Stamping Script
Adds Apache 2.0 license headers to all .js and .py source files in the repo.

Usage:
    python tools/add_license_headers.py          # dry run (preview only)
    python tools/add_license_headers.py --write  # actually stamp files

Run from the repo root.
"""

import os
import sys

# ── Configuration ─────────────────────────────────────────────────────────────

COPYRIGHT = "2025 Sherwin Allen, Shambo Sarkar, Sathvik S, Meeran Ahmed"

JS_HEADER = f"""\
/*
 * Copyright {COPYRIGHT}
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
"""

PY_HEADER = f"""\
# Copyright {COPYRIGHT}
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

HEADERS = {
    ".js": JS_HEADER,
    ".py": PY_HEADER,
}

# Directories to skip entirely
SKIP_DIRS = {
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "dist",
    "build",
    ".next",
    "tools",       # skip this script's own directory
}

# ── Logic ─────────────────────────────────────────────────────────────────────

def already_has_header(content: str, ext: str) -> bool:
    """Check if the file already contains the license header."""
    marker = "Apache License, Version 2.0"
    return marker in content[:1000]  # only check the top of the file


def stamp_file(filepath: str, header: str, dry_run: bool) -> str:
    """
    Stamp a single file with the license header.
    Returns a status string: 'stamped', 'skipped', or 'already has header'.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if already_has_header(content, os.path.splitext(filepath)[1]):
        return "already has header"

    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(header + content)

    return "stamped" if not dry_run else "would stamp"


def walk_repo(root: str, dry_run: bool):
    stamped, skipped, already = [], [], []

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skip dirs in-place so os.walk doesn't descend into them
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            if ext not in HEADERS:
                continue

            filepath = os.path.join(dirpath, filename)
            rel = os.path.relpath(filepath, root)
            status = stamp_file(filepath, HEADERS[ext], dry_run)

            if status in ("stamped", "would stamp"):
                stamped.append(rel)
            elif status == "already has header":
                already.append(rel)
            else:
                skipped.append(rel)

    return stamped, skipped, already


def main():
    dry_run = "--write" not in sys.argv
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if dry_run:
        print("DRY RUN — no files will be modified. Pass --write to apply.\n")
    else:
        print("WRITE MODE — stamping files...\n")

    stamped, skipped, already = walk_repo(repo_root, dry_run)

    label = "Would stamp" if dry_run else "Stamped"
    for f in stamped:
        print(f"  [{label}] {f}")
    for f in already:
        print(f"  [Already OK] {f}")

    print(f"\n{'─' * 50}")
    print(f"  {label}: {len(stamped)} file(s)")
    print(f"  Already had header: {len(already)} file(s)")
    if dry_run and stamped:
        print("\nRun with --write to apply changes.")


if __name__ == "__main__":
    main()