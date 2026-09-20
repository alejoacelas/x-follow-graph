# X follow graph decisions

## Core decisions

### Collection boundaries

- [Keep collection read-only and stop at inaccessible UI](#decision-1).
- [Retain post features without unnecessary full tweet text](#decision-2).

### Interpretation

- [Describe edges as semantic similarity and explicit bio mentions](#decision-3).
- [Never treat missing post coverage as inactivity](#decision-4).

### Reproducibility

- [Keep analysis deterministic and methods appropriate to the available data](#decision-5).

## Details

<a id="decision-1"></a>

### Keep collection read-only and stop at inaccessible UI

Use the signed-in following/profile surfaces without changing follows or Lists. The recorded timeline failure was a generic error after 28 profiles, including a failed retry and a later fresh-profile attempt; its cause was not established. Do not relabel it as a proven rate limit or bypass the boundary. See [data/derived/coverage.json](data/derived/coverage.json).

<a id="decision-2"></a>

### Retain post features without unnecessary full tweet text

Keep identifiers, links, timestamps and aggregate terms needed for the analysis; full post text was discarded after extraction. Preserve dated snapshots so later observations cannot silently alter the meaning of this report. See [data/README.md](data/README.md).

<a id="decision-3"></a>

### Describe edges as semantic similarity and explicit bio mentions

This is an ego-list analysis, not the directed follow network among all accounts. Keep the two edge sources visible; bridge and weak-tie scores cannot establish reciprocal interaction or actual friendships. See [scripts/analyze.py](scripts/analyze.py).

<a id="decision-4"></a>

### Never treat missing post coverage as inactivity

Only successfully collected evidence may support review flags. Coverage is sparse and uneven; retain the uncertainty beside clusters and candidate suggestions rather than score unobserved accounts as inactive. See [report.md](report.md).

<a id="decision-5"></a>

### Keep analysis deterministic and methods appropriate to the available data

The standard-library TF–IDF and clustering pipeline uses bios and partial features. Borrow the cited structural ideas without claiming hierarchical communities, reciprocal-exchange measures or simulated edges absent from the observations. See [tests/test_analyze.py](tests/test_analyze.py). History inspected: [244f566](https://github.com/alejoacelas/x-follow-graph/commit/244f566), [6c2bac7](https://github.com/alejoacelas/x-follow-graph/commit/6c2bac7).
