# Data

- `raw/following.json`: the complete UI-visible Following list with public profile fields.
- `raw/post-features.json`: post metadata and aggregate terms; no full tweet text.
- `raw/candidates.json`: public profiles X recommended during collection.
- `derived/`: deterministic outputs from `scripts/analyze.py`.

Every file is a 2026-08-16 snapshot. See [`../reproduce/methodology.md`](../reproduce/methodology.md) before interpreting graph edges or missing posts.
