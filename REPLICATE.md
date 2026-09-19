# REPLICATE

## Finish the workspace migration

The human wanted the remaining folder reorganization finished and authorized interrupting conflicting sessions.

- Preserved this repository and its instruction wording, declared the tools group, and made CLAUDE.md import AGENTS.md. Its current path is /Users/alejo/best/tools/active/twitter/x-follow-graph.

Agent session 01a072fe-84d6-73f3-b37e-3bb912088c38 · Commits x-follow-graph: de45c30

## Agent instructions cleanup — 2026-09-19

Alejo asked to refresh project instructions and remove redundant Claude instruction files where native AGENTS.md loading is available.

- Updated the applicable instructions and removed redundant local Claude copies; distinct content and preserved snapshots remain.
- Checked instruction references and shared-context freshness; native Claude loading requires 2.1.277+ with the built-in feature enabled.

Agent session 01a0b915-3eb2-78b2-9add-6ba48ad9a3b1 · Commits 3bdd1fe60c703b8bd9e59ed2b41c016a83d29c62

## Explicit startup instructions

Alejo wanted shared instructions selected deliberately at startup, without copied text or automatic parent inheritance.

- Removed agent-context YAML and generated shared text; retained project-specific instructions locally.
- Shared groups: tools. Selection now lives in the machine's context registry; startup does not rewrite this file.

Agent session 01a0b915-3eb2-78b2-9add-6ba48ad9a3b1 · Commits 44c705e

<a id="construction-records"></a>

## Construction records

Preserved records from the former construction-notes folder.

<a id="record-methodology"></a>

### Methodology

#### Request

Build a reproducible, read-only map of every account `@alejoacelas` follows; collect up to 20 recent original posts/reposts per account where X permits it; identify communities, bridges, weak ties, review candidates, and nearby generative people; borrow defensible methods from xiq; retain no unnecessary copyrighted tweet text; make no X mutations.

#### Collection

Collected 2026-08-16 with Browser Control in Alejo's existing signed-in Chrome profile.

##### Following

1. Opened `https://x.com/alejoacelas/following`.
2. Parsed each visible `data-testid="UserCell"` for handle, name, bio, verification, whether it follows Alejo, and bio mentions.
3. Scrolled 900 pixels, reparsed, and deduplicated by case-insensitive handle.
4. Stopped at 443 accounts after six consecutive passes added none. The last visible handles remained unchanged, showing the UI bottom rather than a silent sample.

Output: `data/raw/following.json`.

##### Posts

For each followed account, opened its public Posts tab and collected up to 20 distinct `article[data-testid="tweet"]` records while scrolling. A record retained only the status URL and ID, timestamp, owner handle, repost/pinned flags, plus account-level term counts; full post text was discarded after feature extraction.

The first 28 profiles yielded 512 records. X then returned `Something went wrong. Try reloading.` on timeline regions while profile headers still loaded. A visible Retry failed. After a cooldown, a fresh profile returned the same error. This is consistent with a rate limit, but the UI did not identify a cause. I stopped rather than change accounts, inspect cookies, replay private APIs, or bypass X's UI.

Exact states: `data/raw/post-features.json` and `data/derived/coverage.json`.

##### Nearby people

Recorded six unfollowed accounts shown on X's signed-in `Who to follow` surfaces, then opened each profile to collect its public bio and the displayed number of accounts Alejo follows that also follow it. No Follow buttons were pressed.

Output: `data/raw/candidates.json`.

#### Analysis

`scripts/analyze.py` uses only Python's standard library.

- Text: tokenize bios and available aggregate post terms; normalize a small published synonym map; calculate TF–IDF vectors.
- Communities: deterministic, 12-start spherical k-means with `k = round(sqrt(n / 2))`, capped at 16. Cluster labels are the strongest centroid terms.
- Graph: connect each account to its six nearest semantic neighbors above cosine 0.075; overlay explicit mentions of another followed account in the bio.
- Bridges: combine sampled unweighted betweenness (55%) with the weighted share of cross-community edges (45%).
- Weak ties: rank cross-community semantic or bio-mention edges by edge weight times both endpoint bridge scores.
- Review list: flag only dated evidence: a latest collected post at least 365 days old, at most two visible posts on a successfully loaded profile, or an empty bio plus almost no graph evidence. Missing post coverage is never inactivity evidence.
- Nearby people: map each X recommendation's bio to the two nearest community centroids and retain X's mutual-follow context.

This is an ego network with inferred edges, not the directed follow graph among all 443 accounts. The report states that distinction wherever bridge results appear.

#### Methods borrowed from xiq

- [A Birdseye view of your tweets](https://xiqo.substack.com/p/a-birdseye-view-of-your-tweets) embeds tweets, uses HDBSCAN, labels clusters, and distinguishes persistent topics from isolated events. This analysis borrows the embed → cluster → label shape. It uses TF–IDF because only bios and partial post features are available, and it does not claim hierarchical structure after xiq reports that automatic hierarchy was unreliable.
- [How to measure serendipity online](https://xiqo.substack.com/p/experiments-on-measuring-community) treats recent reciprocal exchanges as warmer ties, uses a second proxy when archive coverage is incomplete, removes top users as a sensitivity check, and inspects missingness before interpreting clusters. This analysis borrows multiple signals and explicit missingness; it cannot reproduce reciprocal-exchange metrics without interaction histories.
- [Discovering the postrat canon in the Community Archive](https://xiqo.substack.com/p/discovering-the-postrat-canon-in) combines quote-tweet structure with semantic search, defines cohesion/evolution/utility before scoring, and spot-checks automated summaries. This analysis borrows the separation of structural and semantic evidence and keeps the two edge sources visible.
- [Modelling the viability of opportunity networks](https://xiqo.substack.com/p/modelling-the-viability-of-opportunity) tests friends-of-friends, calibrates assumptions on observed data, reports wide uncertainty, and stresses user heterogeneity. This analysis borrows the second-order bridge question and calibrated caveats, but does not add simulated Barabási–Albert edges to observed accounts.

#### Rebuild and checks

```sh
python3 scripts/analyze.py
python3 -m unittest discover -s tests -v
git diff --exit-code
```

Expected coverage on this snapshot: 443 following accounts, 512 post-feature records from 28 accounts, 56 profile-timeline attempts, 15 communities, and six nearby candidates.

## Retire construction folders

Alejo wanted all `reproduce` folders under `~/best` transitioned to `REPLICATE.md`.

- Consolidated the existing records and updated references for `reproduce`. Preserved scripts, data and maintained procedures in their own folders.
- Original tracked files remain in Git at `0c02fe85a7510c4b96c27256792aab134ba320c3`; a full local backup, including ignored files, is at `/Users/alejo/.local/state/reproduce-migration/2026-09-19-_qyg4u7a/before/tools/active/twitter/x-follow-graph`.

Agent session 01a0bb8d-6d31-76d3-ac4e-aca4c5dfce64 · Commits 3c98db8671f5d90be74e56e5596e0f96b92f3991
