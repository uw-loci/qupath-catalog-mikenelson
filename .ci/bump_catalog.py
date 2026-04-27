#!/usr/bin/env python3
"""
Update one extension entry in catalog.json with a newly-published release.

Invoked by the `update-on-release` GitHub workflow when a downstream
extension fires a `repository_dispatch` event.

Inputs (CLI flags):
    --repo       owner/name of the extension repo (e.g. uw-loci/qupath-extension-foo)
    --tag        the release tag (e.g. v0.1.2)
    --asset-url  download URL of the .jar asset to publish

Behaviour:
    - Loads catalog.json
    - Finds the extension entry whose `homepage` ends with the given repo
      (matching is suffix-based so http/https and trailing-slash variants
      are tolerated).
    - Replaces the *first* element of that entry's `releases` list with
      the new tag + asset URL, preserving `version_range`. (The catalog
      currently keeps a single release per extension; if that ever changes,
      revisit this.)
    - Writes back with 2-space indent + trailing newline (idempotent if
      the bump is a no-op).
    - Exits 0 if catalog.json was modified, 78 (EX_NOOP) if no change was
      needed, non-zero on any error.

Pre-release handling:
    The catalog already lists pre-releases (e.g. v0.2.2-rc1 was published
    earlier), so this script does NOT skip them. If you decide later that
    the catalog should track only stable releases, add a `--skip-prerelease`
    flag here and gate it from the workflow side via the dispatch payload.
"""
import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", required=True,
                   help="owner/name of the extension repo")
    p.add_argument("--tag", required=True,
                   help="release tag, e.g. v0.1.2")
    p.add_argument("--asset-url", required=True,
                   help="download URL of the jar asset")
    p.add_argument("--catalog", default="catalog.json",
                   help="path to catalog.json (default: ./catalog.json)")
    args = p.parse_args()

    catalog_path = Path(args.catalog)
    if not catalog_path.is_file():
        print(f"ERROR: {catalog_path} not found", file=sys.stderr)
        return 2

    with catalog_path.open("r", encoding="utf-8") as f:
        catalog = json.load(f)

    extensions = catalog.get("extensions", [])
    target = None
    repo_suffix = args.repo.lower().rstrip("/")

    for ext in extensions:
        homepage = (ext.get("homepage") or "").lower().rstrip("/")
        if homepage.endswith(repo_suffix):
            target = ext
            break

    if target is None:
        print(f"ERROR: no extension in {catalog_path} has homepage matching "
              f"{args.repo}", file=sys.stderr)
        print("Known homepages:", file=sys.stderr)
        for ext in extensions:
            print(f"  - {ext.get('homepage')}", file=sys.stderr)
        return 3

    releases = target.setdefault("releases", [])
    if not releases:
        # First-ever release for this extension entry. Build a fresh release
        # object with a default version_range; the human can tighten it later.
        releases.append({
            "name": args.tag,
            "main_url": args.asset_url,
            "version_range": {"min": "v0.6.0"},
        })
    else:
        head = releases[0]
        old_name = head.get("name")
        old_url = head.get("main_url")
        if old_name == args.tag and old_url == args.asset_url:
            print(f"No change: {target['name']} already at {args.tag}")
            return 78  # EX_NOOP
        head["name"] = args.tag
        head["main_url"] = args.asset_url
        # version_range is preserved deliberately

    # Pretty-print with the same conventions catalog.json already uses
    text = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    catalog_path.write_text(text, encoding="utf-8")
    print(f"Updated {target['name']} -> {args.tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
