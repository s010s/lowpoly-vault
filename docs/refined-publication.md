# Explicit mixed publication of accepted refinements

This gate supports catalog replacements for **conifer-tree**, **fern-cluster**, and
**natural-arch** only. It neither reviews nor publishes a candidate automatically.
No real release descriptor or asset is supplied by this implementation.

The original ten GLB, Blender and preview files remain untouched. The existing
initial-publication exception and its QA are unchanged. A mixed release first
checks every original through `collectInitialRelease`, including originals whose
catalog entries will be replaced. It additionally pins the original
`assets/initial-publication.json` bytes to:

`4043e9a35d43773660c2dee061b0e2ca0897aa430427e430d0ca5f331f967275`

Changing that old approval, or changing and repinning it, cannot authorize a
revision. Initial metadata continues to use `metadata.json`. Revision metadata
must instead be named `release-metadata.json`, so it is not recursively discovered
as a second catalog entry for the same ID.

## Separate authority and immutable inputs

After independent candidate acceptance **and** explicit publication authorization,
prepare `assets/releases/<release-id>.json`. Its supported structure is below;
placeholders are intentionally non-executable. Each approved ID needs one revision
entry. There must be no missing, extra or duplicate entries.

```json
{
  "version": 1,
  "release_id": "three-structural-refinements-20261017",
  "release_status": "mixed",
  "authorization": "owner_requested_publication_of_accepted_revisions",
  "authorized_on": "<actual authorization timestamp with timezone>",
  "initial_publication": {
    "path": "assets/initial-publication.json",
    "sha256": "4043e9a35d43773660c2dee061b0e2ca0897aa430427e430d0ca5f331f967275"
  },
  "approved_asset_ids": ["conifer-tree", "fern-cluster", "natural-arch"],
  "revisions": [
    {
      "id": "conifer-tree",
      "revision": "<exact candidate revision>",
      "candidate_root": "experiments/structural-refinement-2026-10-17/conifer-tree",
      "candidate": {
        "path": "<candidate record path relative to candidate_root>",
        "sha256": "<exact independently accepted candidate JSON hash>"
      },
      "metadata": {
        "path": "assets/revisions/conifer-tree/<revision>/release-metadata.json",
        "sha256": "<exact release metadata hash>"
      },
      "sha256": {
        "glb": "<exact accepted GLB hash>",
        "blend": "<exact accepted source hash>",
        "preview": "<exact approved visual image hash>"
      },
      "provenance": {
        "author": "<revision creator attribution>",
        "source_url": "<public revision source URL, preferably a fixed commit>",
        "changes": "<specific structural, material or other modifications>"
      }
    }
  ]
}
```

The example abbreviates the revisions array: add the two other matching entries
before using all three approved IDs. A separately authorized subset of these three
is supported; omitted IDs retain their original WIP entries. Unknown descriptor
fields are rejected rather than treated as new gates or exceptions.

`candidate_root` is explicitly relative to the repository; `.` means the repository
itself. Both it and all candidate paths must remain inside their declared root,
with no symlinks or traversal. Asset-local roots preserve frozen brief and evidence
paths. Do not rewrite a frozen brief to rebase it into the publication directory.

Copy only exact accepted model/source/preview bytes into
`assets/revisions/<id>/<revision>/`. The release GLB and Blender files must match
the validated candidate artifacts; the preview (PNG, JPEG or WebP) must match an
image in the approved visual evidence. An attractive unreviewed poster cannot
substitute for that evidence.

Release metadata needs:

- Matching `id`, `revision`, `author`, `source_url`, and all three `sha256` values
- Bilingual `name` and `description` (`en` and `zh`)
- `license: "CC-BY-4.0"`, valid `category`, and `worlds` or `collection`
- Positive meter `dimensions` and the exact independently measured `triangles`
- `glb`, `blend`, `preview` paths directly in that same immutable revision directory
- Any accurate scientific context, uncertainty, licensing and provenance notes

Do not copy derived approval/publication state, `candidate_record`, `qa`, download
routes, website posters, turntables or `revision_provenance` into release metadata.
Those reserved fields are refused. Accepted state and credit provenance are derived
by the release gate. Private candidate/QA/evidence files are never added to the
asset delivery allowlist.

## Check, then explicitly generate

The checksum must identify the descriptor actually authorized for publication.
Computing a new checksum is not a substitute for reviewing changed release scope.

```sh
node site/refined-release.mjs assets/releases/<release-id>.json --sha256 <approved-descriptor-sha256> --check
node site/refined-release.mjs assets/releases/<release-id>.json --sha256 <approved-descriptor-sha256>
npm run publication:check
```

The first command reads and validates only. The second explicitly writes
`assets/manifest.json` after every check succeeds. Ordinary builds only check the
stored manifest; they never grant authority or generate a descriptor.

For each replacement the gate invokes the existing `validate_candidate.py` with
`--require-approved --json` and its explicit candidate root. Valid-but-pending,
failed, unknown, stale, self-reviewed and missing evidence cannot pass. A **production**
brief, exact asset ID/revision, GLB hash, editable source hash, approved preview
hash and measured triangle count must all match. Study acceptance does not suffice.
No alternate gate runner or bypass option is supported.

The stored manifest must exactly equal a fresh collection from the pinned
inputs. With all three accepted replacements it states:

- `release_status: "mixed"`, `quality_status: "mixed"`
- Three individual `quality_status: "accepted_for_brief"` entries
- Seven unchanged `quality_status: "work_in_progress"` entries
- Explicit approved and WIP ID lists in `publication`

Acceptance is for the frozen brief, not blanket scientific or artistic approval.
Download credits identify the revision creator/source/changes and preserve original
creator/source attribution and the original GLB hash. Original WIP downloads keep
their unchanged-original credit and ongoing-refinement notice.

## Website images remain separately sealed

Revised turntables are stored at
`assets/turntables/<id>/<revision>/v2-768-q90/`; revised posters use
`assets/card-previews/<id>-<revision>-v2-768-q90.webp`. Only individually accepted
IDs selected by the pinned mixed-publication manifest can use these routes.
Original paths and bytes remain unchanged. Old website image routes and hashes
**fail** against replacement models. Before a mixed production
build can pass, generate and pin website posters/frames for each revised GLB using
the current viewer preset, while retaining original hashes for unchanged entries.
For a preview that doubles as the website poster, its exact bytes must also be in
the candidate's approved visual evidence. This gate does not fabricate that review
or regenerate images. All 24 revision frames must contain encoded alpha, use the active renderer preset,
remain 768 × 768 at WebP quality 0.9, and use ordered deterministic paths.
Frame view/camera metadata must exactly match the shared preset and ordered azimuth.
Revision GLB filenames remain `<id>.glb` to preserve viewer snapshot identity. The
poster must exactly equal frame 0 and the independently approved publication preview.
The capture/recheck script uses the same revision path helper as delivery.
The existing output audit continues to allowlist only
manifest-authorized delivery files, downloads and separately checked website images.

## Regression checks

```sh
node site/refined-release-test.mjs
node site/initial-release-test.mjs
node site/manifest-test.mjs
node site/turntable-delivery-test.mjs
```

Mixed-release tests use temporary copies of the originals and explicitly synthetic
candidate evidence. They prove packaging boundaries, never approval of a real model.
They cover accepted/subset mixtures, unchanged originals, publication pins, candidate
root containment, production/acceptance gates, stale evidence, exact ID/revision/file
and preview bindings, measured counts, duplicate entries, prohibited delivery paths,
symlink substitutions/escapes, manifest equality and revision-aware ZIP credits.
