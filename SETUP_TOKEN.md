# Setup: `CATALOG_DISPATCH_TOKEN` org secret

This document covers the one-time setup required to make catalog auto-update
go live across both LOCI catalogs (`qupath-catalog-mikenelson` for general
extensions and `qupath-catalog-qpsc` for microscopy extensions).

It is split into two halves:

- **Part A** — what the maintainer (you) can do without org-admin powers.
- **Part B** — the request you hand to the org admin. Designed to be a
  single copy-paste so the admin only has to follow one document.

Once Part B is done, every future release on any of the eleven extension
repos will auto-bump the relevant catalog with no further human action.

---

# Part A — Things the maintainer can do alone

These steps don't need org-admin permission. They prepare the request and
verify the wiring is sound, so the admin's job is purely "create one
secret."

## Step 1 — Confirm the per-extension workflow files are in place

Browse to each repo's `.github/workflows/` folder on GitHub and confirm
`notify-catalog.yml` exists. Should be present on all 11.

**LOCI catalog targets (`uw-loci/qupath-catalog-mikenelson`):**
- https://github.com/uw-loci/qupath-extension-cell-analysis-tools/tree/main/.github/workflows
- https://github.com/uw-loci/qupath-extension-dialog-manager/tree/master/.github/workflows
- https://github.com/uw-loci/qupath-extension-dl-pixel-classifier/tree/master/.github/workflows
- https://github.com/uw-loci/qupath-extension-gated-object-classifier/tree/main/.github/workflows
- https://github.com/uw-loci/qupath-extension-image-export-toolkit/tree/main/.github/workflows
- https://github.com/uw-loci/qupath-extension-project-metadata-browser/tree/main/.github/workflows
- https://github.com/uw-loci/qupath-extension-wizard-wand/tree/main/.github/workflows

**QPSC catalog targets (`uw-loci/qupath-catalog-qpsc`):**
- https://github.com/uw-loci/qupath-extension-qpsc/tree/main/.github/workflows
- https://github.com/uw-loci/qupath-extension-ppm/tree/master/.github/workflows
- https://github.com/uw-loci/qupath-extension-ocr4labels/tree/main/.github/workflows
- https://github.com/uw-loci/qupath-extension-tiles-to-pyramid/tree/main/.github/workflows

## Step 2 — Confirm both catalogs have the receiver workflow

Open each catalog repo's Actions tab and verify "Update catalog on
extension release" is listed:
- https://github.com/uw-loci/qupath-catalog-mikenelson/actions
- https://github.com/uw-loci/qupath-catalog-qpsc/actions

You don't need to run anything here, just confirm the workflow is
registered.

## Step 3 — Pre-discuss the token-owner question with the admin

Have a quick chat (email/Slack, no GitHub access needed) with the admin
**before** sending the formal ticket: ask whether the org has a service
or bot account for automation tokens, or whether they'd prefer the token
come from a maintainer's personal account.

This shapes Step 1 of the admin ticket. Knowing the answer up front
saves a back-and-forth.

## Step 4 — Check whether you can do it yourself

The page is https://github.com/organizations/uw-loci/settings/secrets/actions.
If it loads for you, you have admin or "manage org secrets" permission
and can do the whole thing yourself: just follow Part B.

If it 404s or shows "you don't have permission," forward Part B to the
admin.

## Step 5 — Stage smoke-test extensions

Before the admin completes the ticket, decide which extension you'll
re-publish on each catalog for the verification round-trip.

- **LOCI side:** Wizard Wand (small, recently released, low blast
  radius).
- **QPSC side:** Tiles to Pyramid (small, similarly low blast radius).

Knowing this in advance lets you verify both catalogs in five minutes
once the token exists.

---

# Part B — Admin ticket (single combined request, copy/paste in full)

## Request: Create org secret `CATALOG_DISPATCH_TOKEN` on `uw-loci`

### What I'm asking for

Create one organization-level secret on the `uw-loci` GitHub
organization, scoped to eleven repositories. The secret holds a
fine-grained personal access token (PAT) that lets each QuPath-extension
repo notify its catalog repo when a new release is published, so the
catalog auto-updates instead of drifting behind.

There are **two** catalog repos (LOCI general + QPSC microscopy). The
same token writes to both, so this is a single secret with two catalog
repos in its scope.

**Secret name:** `CATALOG_DISPATCH_TOKEN`

**Secret value:** a fine-grained PAT (recipe in Step 1).

**Catalog repos the token can write to:**

- `uw-loci/qupath-catalog-mikenelson`
- `uw-loci/qupath-catalog-qpsc`

**Extension repos that need to read the secret (11 total):**

LOCI catalog targets:

- `uw-loci/qupath-extension-cell-analysis-tools`
- `uw-loci/qupath-extension-dialog-manager`
- `uw-loci/qupath-extension-dl-pixel-classifier`
- `uw-loci/qupath-extension-gated-object-classifier`
- `uw-loci/qupath-extension-image-export-toolkit`
- `uw-loci/qupath-extension-project-metadata-browser`
- `uw-loci/qupath-extension-wizard-wand`

QPSC catalog targets:

- `uw-loci/qupath-extension-qpsc`
- `uw-loci/qupath-extension-ppm`
- `uw-loci/qupath-extension-ocr4labels`
- `uw-loci/qupath-extension-tiles-to-pyramid`

The token does **not** need to be readable by the catalog repos
themselves.

### Background (skim or skip)

Each of the eleven extension repos has a workflow
`.github/workflows/notify-catalog.yml` that fires on `release: published`
and POSTs a `repository_dispatch` event to its corresponding catalog
repo. Each catalog repo has an `update-on-release` workflow that handles
the dispatch by editing `catalog.json` and committing the bump.

Without this token, the POST returns 403 and the catalog never updates.
With this token, both catalogs stay in sync automatically.

Full design and recovery procedures:

- LOCI: https://github.com/uw-loci/qupath-catalog-mikenelson/blob/master/MAINTAINERS.md
- QPSC: https://github.com/uw-loci/qupath-catalog-qpsc/blob/master/MAINTAINERS.md

### Step 1 — Generate the token

The token only needs permission to send `repository_dispatch` events to
two specific catalog repos. GitHub's "fine-grained PAT" lets us narrow
it to exactly that.

The cleanest practice is to create the token under a service / bot
account, not a personal one — that way it survives the original creator
leaving the project. If `uw-loci` already uses a bot account for similar
automation, prefer that. If not, a personal PAT from any maintainer
works as an interim and can be migrated later.

1. Sign in to the GitHub account that will own the token (bot or
   maintainer).
2. Go to: **Settings → Developer settings → Personal access tokens →
   Fine-grained tokens**
   (URL: https://github.com/settings/tokens?type=beta).
3. Click **Generate new token**.
4. Fill in:
   - **Token name:** `CATALOG_DISPATCH_TOKEN`
   - **Resource owner:** `uw-loci` (org dropdown). If `uw-loci` does
     not appear, the token-creating account isn't a member of the org
     and needs to be added first.
   - **Expiration:** 1 year (or org policy maximum). Set a calendar
     reminder for 11 months out to rotate.
   - **Description:** *Used by extension-repo `notify-catalog.yml`
     workflows to dispatch release events to qupath-catalog-mikenelson
     and qupath-catalog-qpsc.*
   - **Repository access:** **Only select repositories** → pick
     exactly **two**:
     - `uw-loci/qupath-catalog-mikenelson`
     - `uw-loci/qupath-catalog-qpsc`
   - **Repository permissions:** scroll to **Contents** and set it to
     **Read and write**. Leave every other permission at "No access".
     Specifically:
     - **Contents:** Read and write
     - everything else: No access
5. Click **Generate token**. Copy the token value immediately — GitHub
   only shows it once. It looks like `github_pat_11AAAAA0Y0...`
6. Paste it somewhere temporarily (e.g. a password manager) until
   Step 2 is done; then delete the temporary copy.

If your org policy requires SSO authorization for org-scoped tokens,
click **Configure SSO** on the token and authorize it for `uw-loci`
before continuing.

### Step 2 — Store the token as an org secret

This is the step that requires org-admin (or "Manage organization
secrets" permission) on `uw-loci`.

1. Go to: https://github.com/organizations/uw-loci/settings/secrets/actions
2. Click **New organization secret**.
3. Fill in:
   - **Name:** `CATALOG_DISPATCH_TOKEN` (exactly this — case-sensitive).
   - **Value:** the PAT generated in Step 1.
   - **Repository access:** **Selected repositories**. Click the
     gear/picker and add the eleven repos listed at the top of this
     document.
4. Click **Add secret**.

The secret value is now write-only — even org admins can't read it
back, only overwrite on rotation. That's expected.

### Step 3 — Verify

To confirm the wiring works without cutting a real release, re-publish
the most recent release on one repo per catalog. This fires a fresh
`release: published` event without changing anything user-visible.

**LOCI side:**

1. Go to https://github.com/uw-loci/qupath-extension-wizard-wand/releases
2. Click the latest release → pencil/edit icon → **Update release**
   (no edits needed).
3. Within ~30 seconds,
   https://github.com/uw-loci/qupath-extension-wizard-wand/actions
   should show a green run of "Notify catalog of release."
4. Within ~1 minute after that,
   https://github.com/uw-loci/qupath-catalog-mikenelson/commits/master
   should show an
   `Auto-bump uw-loci/qupath-extension-wizard-wand -> v0.4.2` commit
   (diff may be empty since the catalog is already at v0.4.2 — that's
   the no-op path and is correct).

**QPSC side:**

1. Go to https://github.com/uw-loci/qupath-extension-tiles-to-pyramid/releases
2. Same procedure: edit latest release → Update release.
3. Within ~30 seconds, that repo's Actions tab should show a green
   workflow run.
4. Within ~1 minute,
   https://github.com/uw-loci/qupath-catalog-qpsc/commits/master should
   show an `Auto-bump` commit.

If either workflow fails with **403** or **404** on the
`gh api .../dispatches` step, the most common causes are:

- The token wasn't authorized for SSO (Step 1, last paragraph).
- The token was scoped to the wrong repos (must be the two catalog
  repos, not the extension repos).
- The token's "Contents" permission is read-only (must be Read and
  write).
- The org secret's repository-access list doesn't include the extension
  repo trying to read it.

### Step 4 — Done

Once Step 3 passes for both catalogs, every future release on those
eleven repos auto-bumps the relevant catalog. Adding a new extension to
either catalog in the future requires:

- Adding the new repo to the org secret's repository-access list
  (Step 2.3).
- Verifying Step 3 round-trips for the new repo on its first release.

That's the only ongoing maintenance.

### Quick contact info

- **Requester:** Mike Nelson (`@MichaelSNelson`,
  imagescientistwebsite@gmail.com)
- **Why now:** all eleven extension repos already have the workflow
  files committed. They are inert until the token exists.
- **Risk if not done:** none — the existing manual catalog-edit
  process keeps working. We just don't get the automation.
- **Risk of doing it:** the token can write to `catalog.json` (and only
  that file) on two specific repos. It cannot touch source code,
  releases, settings, or any other repo. Worst case if leaked: someone
  could push junk commits to one or both catalog repos, which a
  maintainer would `git revert` in seconds.

### What's already in place (FYI for the admin)

These are already committed and pushed; the admin doesn't need to
verify or set them up:

- `.github/workflows/notify-catalog.yml` in all 11 extension repos
- `.github/workflows/update-on-release.yml` in both catalog repos
- `.ci/bump_catalog.py` in both catalog repos
- `MAINTAINERS.md` in both catalog repos

The only missing piece is the token + secret.
