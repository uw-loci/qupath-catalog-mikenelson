# Catalog Maintainer Guide

This document explains how the LOCI QuPath extension catalog auto-update
machinery works, how to debug it when something breaks, and how to add a
new extension to the catalog. Anyone taking over maintenance of these
repos should be able to onboard from this file alone.

If you only need to know "what changed when I cut a release," skim the
**Quick Reference** section and stop. If something is broken, jump to
**Recovery Procedures**.

---

## Quick Reference

When an extension repo publishes a release, the catalog should bump
itself within ~1 minute, with no human action required. The flow:

1. Maintainer runs `gh release create vX.Y.Z ... <jar>` (or uses the web
   UI) on an extension repo.
2. The extension repo's `notify-catalog.yml` workflow fires on
   `release: published` and POSTs a `repository_dispatch` to this
   catalog repo with payload `{repo, tag, asset_url}`.
3. This repo's `update-on-release.yml` workflow handles the dispatch,
   runs `.ci/bump_catalog.py`, commits the change as
   `Auto-bump <repo> -> <tag>`, and pushes.
4. Anyone running `Manage extension catalogs > Refresh` in QuPath now
   sees the new version.

The flow has **one** secret: `CATALOG_DISPATCH_TOKEN`, an org-level
secret on `uw-loci`. Every extension repo inherits it; this repo's
workflow doesn't need it (it just runs on its own).

---

## Why it exists

The QuPath extension catalog is consumed by the QuPath Extension Manager
UI. Each entry pins users to a specific tag + jar URL via
`releases[0].name` and `releases[0].main_url` in `catalog.json`. If the
catalog drifts behind the actual extension releases:

- Fresh installs from the catalog still receive the *old* jar.
- The Extension Manager has no way to discover newer releases.
- Users hit bugs that were fixed weeks ago and have no clear path to
  the fix.

We have already shipped a user-visible regression because of this drift
(the QP-CAT v0.2.2-rc1 -> v0.2.3 harmonypy fix on Windows; before
auto-update was wired up, a fix that landed in the extension repo took
hours to reach catalog users via a manual catalog edit).

The auto-update workflow exists to make catalog drift impossible by
construction: the only way for the catalog to be out of date is for
the dispatch round-trip to fail, which is a clear monitorable signal.

---

## Architecture

```
+------------------------+              +------------------------------+
|  extension repo        |              |  qupath-catalog-mikenelson   |
|  (e.g. wizard-wand)    |              |  (this repo)                 |
+------------------------+              +------------------------------+
| .github/workflows/     |              | .github/workflows/           |
|   notify-catalog.yml   |              |   update-on-release.yml      |
|     |                  |              |     |                        |
|     | release event    |              |     | repository_dispatch    |
|     | "extension-      |              |     | "extension-release"    |
|     |  release"        |              |     v                        |
|     v                  |              | .ci/bump_catalog.py          |
|  POST /dispatches      |--CATALOG_--->|     |                        |
|  on this repo          |  DISPATCH_   |     | rewrite catalog.json   |
|                        |  TOKEN       |     v                        |
|                        |              | git commit + push            |
+------------------------+              +------------------------------+
```

### Files in this repo (the catalog)

| Path | Role |
|------|------|
| `catalog.json` | Source of truth. The QuPath Extension Manager fetches the raw GitHub URL of this file. Hand-editable, but should normally be auto-edited. |
| `README.md` | User-facing description of the catalog and one section per extension. Currently maintained by hand; auto-update only touches `catalog.json`. |
| `.ci/bump_catalog.py` | Single-purpose script: locate an extension by repo name, replace its `releases[0].name` and `releases[0].main_url`, write back. |
| `.github/workflows/update-on-release.yml` | Listens for `repository_dispatch: extension-release` from each extension repo. Also exposes `workflow_dispatch` for manual recovery. |
| `MAINTAINERS.md` | This document. |

### Files in each extension repo

| Path | Role |
|------|------|
| `.github/workflows/notify-catalog.yml` | Fires on `release: published`. Picks the `*-all.jar` asset and POSTs a `repository_dispatch` to this catalog repo. |

The workflow expects exactly one asset whose name ends in `-all.jar`.
If your extension uses a different naming convention, you must edit the
`jq` selector in `notify-catalog.yml`. The `qupath-conventions` Gradle
plugin produces `*-all.jar` by default, so this matches all current
LOCI QuPath extensions.

### The catalog-side workflow logic

`.github/workflows/update-on-release.yml` resolves its inputs from
*either* a real `repository_dispatch` payload *or* manual
`workflow_dispatch` inputs, so a human can always run the bump by hand
if a dispatch is missed or a `notify-catalog.yml` is misconfigured.

The bump script returns:

| Exit code | Meaning | Workflow action |
|-----------|---------|-----------------|
| 0 | Real change written to `catalog.json` | Commit + push |
| 78 | No-op (already at this version) | Log and stop |
| Other (2, 3, ...) | Error (file not found, repo not in catalog, etc.) | Fail the workflow with `::error::` |

The `78` exit code is `EX_NOOP` from `sysexits.h`; choosing it
deliberately means a re-fired dispatch (e.g., from a workflow rerun)
does not produce an empty commit.

---

## How `bump_catalog.py` matches an extension

The script suffix-matches the dispatch's `repo` field
(e.g. `uw-loci/qupath-extension-wizard-wand`) against each entry's
`homepage` URL (e.g. `https://github.com/uw-loci/qupath-extension-wizard-wand`).
Trailing slashes and case differences are tolerated. If no extension
matches, the script exits non-zero and prints all known homepages so
the failure mode is obvious in the workflow log.

This means **the homepage field in `catalog.json` must contain the
canonical GitHub URL of the extension repo** for auto-update to work.
If a repo is renamed or moved, update the homepage in `catalog.json`
manually before the next release, otherwise the dispatch will fail to
match.

---

## Adding a new extension to the catalog

1. **Add the entry to `catalog.json`.** Place the new object in the
   `extensions` array, alphabetically by display name. Required fields:
   `name`, `description`, `author`, `homepage`, `releases` (array
   containing at least one entry with `name`, `main_url`, and
   `version_range`).
   - `homepage` MUST be the canonical GitHub URL of the extension repo
     (e.g. `https://github.com/uw-loci/qupath-extension-foo`); the
     auto-update script keys on it.
   - `releases[0].main_url` should follow the standard pattern:
     `https://github.com/<owner>/<repo>/releases/download/<tag>/<repo>-<version>-all.jar`.
2. **Mirror the entry into `README.md`.** Add a section under
   "Available Extensions" with the same description text. README is
   not auto-maintained; do it manually.
3. **Add `.github/workflows/notify-catalog.yml` to the extension
   repo.** Copy from any sibling repo (the file is identical across
   every extension - the catalog repo URL inside it is the only
   variable, and all current entries point at this repo).
4. **Verify the org secret is in scope.** `CATALOG_DISPATCH_TOKEN` is
   defined at the `uw-loci` org level. Confirm the new repo inherits
   it: settings -> secrets -> actions -> "Organization secrets" should
   list `CATALOG_DISPATCH_TOKEN` as available. If not, the org admin
   needs to grant it.
5. **Cut a real release on the new repo.** The first `release: published`
   event will exercise the dispatch round-trip. Within ~1 minute, this
   repo should receive an `Auto-bump <repo> -> <tag>` commit. If it
   doesn't, see Recovery Procedures.

---

## Recovery Procedures

### "I cut a release but the catalog didn't update"

**Step 1 - Did `notify-catalog.yml` run?**

Check the extension repo's Actions tab. The "Notify catalog of release"
workflow should appear, triggered by the release. Common failures:

- **No run at all**: the workflow file isn't present, or YAML is
  malformed. Verify `.github/workflows/notify-catalog.yml` exists on
  the default branch.
- **Run failed at the `gh api ...dispatches` step with 404**: the
  catalog repo URL in the workflow is wrong, or the repo was renamed.
  Update the workflow to point at the correct catalog repo name.
- **Run failed at the `gh api ...dispatches` step with 403**: the
  `CATALOG_DISPATCH_TOKEN` secret is missing, expired, or scoped to
  the wrong repo. Regenerate at the org level with `contents: write`
  on the catalog repo.
- **Run failed at `No '*-all.jar' asset found`**: the release was
  published without the shadow jar attached. Edit the release on
  GitHub, attach the jar, and re-trigger by manually firing
  `notify-catalog.yml` via the Actions tab (or run the catalog-side
  manual bump in Step 3).

**Step 2 - Did `update-on-release.yml` run?**

Check this repo's Actions tab. The "Update catalog on extension release"
workflow should appear, triggered by `repository_dispatch`. Common
failures:

- **Not found in catalog (exit 3)**: the dispatch payload's `repo`
  doesn't suffix-match any `homepage` in `catalog.json`. Either the
  extension wasn't added to the catalog yet, or the homepage URL is
  stale. Add the entry or fix the URL, then re-fire (Step 3).
- **Permission denied on git push**: the workflow's
  `permissions: contents: write` was removed, or branch protection on
  `main`/`master` blocks the GitHub Actions bot. Adjust branch protection
  to allow the workflow user, or push the bump manually.

**Step 3 - Manual recovery via `workflow_dispatch`**

The catalog-side workflow exposes a manual run button. Open this repo
in the browser, go to **Actions > Update catalog on extension release**,
click **Run workflow**, and fill in the three inputs:

- `repo`: e.g. `uw-loci/qupath-extension-wizard-wand`
- `tag`: e.g. `v0.4.3`
- `asset_url`: e.g. `https://github.com/uw-loci/qupath-extension-wizard-wand/releases/download/v0.4.3/qupath-extension-wizard-wand-0.4.3-all.jar`

This skips the per-extension dispatch entirely and goes straight to the
bump script. Use it any time the dispatch round-trip is broken.

**Step 4 - Direct edit (last resort)**

If even `workflow_dispatch` is broken, edit `catalog.json` by hand,
commit, push. The QuPath Extension Manager only cares about the file
contents at the latest commit; how it got there doesn't matter.

### "The dispatch fired twice and I got two bumps to the same tag"

The bump script is idempotent: re-firing for the same tag/url returns
exit 78 (no-op) and the workflow logs "already up to date". You should
see one real commit and one no-op log. If you see two commits, the
script's idempotency check is broken; file a bug.

### "I need to roll back the catalog to a previous version of an extension"

Use `workflow_dispatch` with the older tag and asset URL. There's no
special revert path - the bump script is "set to whatever was passed in,"
not "advance forward only."

---

## Testing the round-trip

To verify the system end-to-end without cutting a real release:

1. On any extension repo, draft a release with a fake tag like
   `v0.0.0-dispatch-test`. **Do not publish yet.**
2. Attach a placeholder file named like `*-all.jar` (any content; the
   catalog never downloads it itself, only the QuPath Extension Manager
   does, and it won't try unless a user installs that version).
3. Click Publish. The `notify-catalog.yml` workflow should fire.
4. Within ~1 minute, this repo should have an
   `Auto-bump <repo> -> v0.0.0-dispatch-test` commit.
5. Inspect `catalog.json` to confirm.
6. Clean up: delete the test release, delete the tag, and revert the
   catalog commit (or fire `workflow_dispatch` with the previous real
   tag to roll forward instead).

---

## Future considerations

- **Skip prereleases.** Right now a `release.prerelease == true` event
  still triggers a bump. If you want the catalog to track only stable
  releases, add a guard in `notify-catalog.yml`
  (`if: ${{ !github.event.release.prerelease }}`) or pass
  `prerelease: ${{ github.event.release.prerelease }}` in the dispatch
  payload and gate at the bump-script level via a new flag.
- **Multiple releases per extension.** `bump_catalog.py` currently
  rewrites `releases[0]` only. If the catalog ever needs to keep a
  history of multiple supported versions per extension (e.g. one for
  QuPath 0.5.x compat and another for 0.6.x), update the script to
  insert/replace by `version_range.min` instead of always head-of-list.
- **Auto-PR mode.** For high-stakes catalog edits, switch the
  catalog-side workflow from "commit + push to default branch" to
  "open a PR for human review before merging." Trivial change; just
  swap the final `git push` step for an `actions/create-pull-request`
  step. Keeps the same idempotent bump-script logic.

---

## Contact

- Maintainer: Mike Nelson (`@MichaelSNelson`)
- Bugs in the auto-update workflow: open an issue on this catalog repo.
- Questions about the QuPath catalog format: see
  [qupath/extension-catalog-model](https://github.com/qupath/extension-catalog-model).
