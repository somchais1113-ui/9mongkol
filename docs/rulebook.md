# Rulebook Governance

The project does **not** reverse-engineer or claim to reproduce Somjade's proprietary weights. `DEMO-2026.11.1` is a deterministic sandbox intended for technical validation. Some illustrative pair interpretations resemble ideas used in popular Thai number-belief content, but all written descriptions and numeric deltas in this project were newly authored for demonstration.

## Rule invariants

- Exactly two digits per `pair`.
- One unique entry per `pair` in this version.
- Deltas may reference only the six known attributes.
- `reason` must explain the classification in plain language, without pretending scientific validation.
- If rules/weights change, version bump + reindex + regression test.

## Traceability

The `/api/analyze` endpoint returns the core, ordered pairs, matched rule positions (1–7), deltas, attribute scores, career weights (via `/api/meta`), and a version. UI exposes both positive and negative adjustments. A matching score is simply an internal index, **not** a probability of suitability/success.

## Future

Add multiple rulebooks (licensed/open/public-domain as appropriate), source-specific attribution, analyst review workflow, effective dates, confidence/provenance tags, comparison between rulebooks, approved calculation versions, and retained before-after diff audits.
