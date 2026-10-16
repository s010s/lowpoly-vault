# Asset browser redesign: implementation checklist

Status: **work in progress, review only**. Branch checkpoints preserve code and original model sources; they do not approve asset QA, merge to main, or deploy GitHub Pages.

## Scope

- [ ] Preserve original candidate IDs, source geometry, authored scale and file paths.
- [ ] Separate worlds, multi-membership curated packs, cross-world categories and reliable technical specifications.
- [ ] Make global assets a searchable grid; reserve the map for an explicitly selected small real pack.
- [ ] Generate genuine English and Simplified Chinese static detail/listing HTML with useful no-JS content, metadata, canonical/hreflang, sitemap and ordinary links under GitHub Pages base paths.
- [ ] Enhance list clicks with the existing modal and FLIP; retain filter/query/sort/page/scroll through Back/Forward; direct links remain useful.
- [ ] Reduce visual noise, remove permanent format badges and replay entrance, show measured file sizes, previous/next model links, same-pack related models and honest download initiation feedback.
- [ ] Package source/model with CREDITS.txt; copy release files through an approved-manifest allowlist only.
- [ ] Preserve the singleton renderer, bounded cache/cancellation, on-demand drawing, disposal and reduced-motion behavior; add a truthful optional metric reference.
- [ ] Experiment on dinosaur-nest, lepidodendron and natural-arch: matched rendering rules, 12–16 frame scrub, encoded/decode size and alpha/shadow comparison. Integrate only if evidence supports it.
- [ ] Test 10 real assets and a 10,000-item uneven many-category fixture, static routes, URL state, accessibility, keyboard and actual download paths.
- [ ] Capture actual UI screenshots; distinguish cloud fallback tests from GPU/mobile/continuous-animation acceptance.
- [ ] Keep English-first Skills and bilingual README current; maintain this checklist and checkpoint work periodically.

## Preservation and acceptance boundaries

The original working directory and port-5188 review build remain intact. Implementation runs in an independent worktree populated from the complete current candidate snapshot. Existing previews and experiments remain available for comparison. No candidate becomes release-approved through this UI work. The cloud browser currently has no WebGL; actual GPU checks remain a separate required test. Bounded Node/DOM checks do not prove network, GPU or frame-rate performance. No external reference artwork is included in release output.

## Checkpoints

- Initial checkpoint: candidate snapshot plus this scope, before implementation.
