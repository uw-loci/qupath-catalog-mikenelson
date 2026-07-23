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
    - PREPENDS a new release (tag + asset URL) to that entry's `releases`
      list, leaving older release entries in place. The new release inherits
      the `version_range` of the current newest release (or a default for a
      brand-new entry).
    - Writes back with 2-space indent + trailing newline (idempotent if
      the bump is a no-op).
    - Exits 0 if catalog.json was modified, 78 (EX_NOOP) if no change was
      needed, non-zero on any error.

Why prepend instead of replace:
    QuPath's Extension Manager re-matches an INSTALLED extension to this
    catalog by exact release-name string equality (Catalog.createExtensionsFromCatalog
    in qupath/extension-manager). If the release the user currently has
    installed is no longer listed, QuPath resolves the extension as "not
    installed" and never offers an update -- it skips straight past "update
    available". Keeping older release entries preserves that match, so a user
    on v1.0.0 still sees the catalog list v1.0.0 (installed) AND the newer
    v1.0.1 (the strictly-greater compatible release that triggers the update
    notification). QuPath selects the max-by-version compatible release, so
    list order is for human readability only.

Pre-release handling:
    The catalog already lists pre-releases (e.g. v0.2.2-rc1 was published
    earlier), so this script does NOT skip them. If you decide later that
    the catalog should track only stable releases, add a `--skip-prerelease`
    flag here and gate it from the workflow side via the dispatch payload.
"""
import argparse
import copy
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

    # If this exact tag is already listed, update its asset URL in place
    # rather than adding a duplicate entry (no-op if the URL also matches).
    existing = next((r for r in releases if r.get("name") == args.tag), None)
    if existing is not None:
        if existing.get("main_url") == args.asset_url:
            print(f"No change: {target['name']} already lists {args.tag}")
            return 78  # EX_NOOP
        existing["main_url"] = args.asset_url
        print(f"Updated asset URL for {target['name']} {args.tag}")
    else:
        # New release: PREPEND so older entries stay matchable for users still
        # on a previous version (see module docstring). Inherit the current
        # newest release's version_range so a human-tightened range carries
        # forward; fall back to a default for a brand-new entry.
        if releases:
            version_range = copy.deepcopy(
                releases[0].get("version_range", {"min": "v0.7.0"})
            )
        else:
            version_range = {"min": "v0.7.0"}
        releases.insert(0, {
            "name": args.tag,
            "main_url": args.asset_url,
            "version_range": version_range,
        })
        print(f"Added {target['name']} {args.tag}")

    # Pretty-print with the same conventions catalog.json already uses
    text = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    catalog_path.write_text(text, encoding="utf-8")
    print(f"Updated {target['name']} -> {args.tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
