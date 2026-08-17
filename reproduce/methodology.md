# Methodology

## Request

Build a reproducible, read-only map of every account `@alejoacelas` follows; collect up to 20 recent original posts/reposts per account where X permits it; identify communities, bridges, weak ties, review candidates, and nearby generative people; borrow defensible methods from xiq; retain no unnecessary copyrighted tweet text; make no X mutations.

## Collection

Collected 2026-08-16 with Browser Control in Alejo's existing signed-in Chrome profile.

### Following

1. Opened `https://x.com/alejoacelas/following`.
2. Parsed each visible `data-testid="UserCell"` for handle, name, bio, verification, whether it follows Alejo, and bio mentions.
3. Scrolled 900 pixels, reparsed, and deduplicated by case-insensitive handle.
4. Stopped at 443 accounts after six consecutive passes added none. The last visible handles remained unchanged, showing the UI bottom rather than a silent sample.

Output: `data/raw/following.json`.

### Posts

For each followed account, opened its public Posts tab and collected up to 20 distinct `article[data-testid="tweet"]` records while scrolling. A record retained only the status URL and ID, timestamp, owner handle, repost/pinned flags, plus account-level term counts; full post text was discarded after feature extraction.

The first 28 profiles yielded 512 records. X then returned `Something went wrong. Try reloading.` on timeline regions while profile headers still loaded. A visible Retry failed. After a cooldown, a fresh profile returned the same error. This is consistent with a rate limit, but the UI did not identify a cause. I stopped rather than change accounts, inspect cookies, replay private APIs, or bypass X's UI.

Exact states: `data/raw/post-features.json` and `data/derived/coverage.json`.

### Nearby people

Recorded six unfollowed accounts shown on X's signed-in `Who to follow` surfaces, then opened each profile to collect its public bio and the displayed number of accounts Alejo follows that also follow it. No Follow buttons were pressed.

Output: `data/raw/candidates.json`.

## Analysis

`scripts/analyze.py` uses only Python's standard library.

- Text: tokenize bios and available aggregate post terms; normalize a small published synonym map; calculate TF–IDF vectors.
- Communities: deterministic, 12-start spherical k-means with `k = round(sqrt(n / 2))`, capped at 16. Cluster labels are the strongest centroid terms.
- Graph: connect each account to its six nearest semantic neighbors above cosine 0.075; overlay explicit mentions of another followed account in the bio.
- Bridges: combine sampled unweighted betweenness (55%) with the weighted share of cross-community edges (45%).
- Weak ties: rank cross-community semantic or bio-mention edges by edge weight times both endpoint bridge scores.
- Review list: flag only dated evidence: a latest collected post at least 365 days old, at most two visible posts on a successfully loaded profile, or an empty bio plus almost no graph evidence. Missing post coverage is never inactivity evidence.
- Nearby people: map each X recommendation's bio to the two nearest community centroids and retain X's mutual-follow context.

This is an ego network with inferred edges, not the directed follow graph among all 443 accounts. The report states that distinction wherever bridge results appear.

## Methods borrowed from xiq

- [A Birdseye view of your tweets](https://xiqo.substack.com/p/a-birdseye-view-of-your-tweets) embeds tweets, uses HDBSCAN, labels clusters, and distinguishes persistent topics from isolated events. This analysis borrows the embed → cluster → label shape. It uses TF–IDF because only bios and partial post features are available, and it does not claim hierarchical structure after xiq reports that automatic hierarchy was unreliable.
- [How to measure serendipity online](https://xiqo.substack.com/p/experiments-on-measuring-community) treats recent reciprocal exchanges as warmer ties, uses a second proxy when archive coverage is incomplete, removes top users as a sensitivity check, and inspects missingness before interpreting clusters. This analysis borrows multiple signals and explicit missingness; it cannot reproduce reciprocal-exchange metrics without interaction histories.
- [Discovering the postrat canon in the Community Archive](https://xiqo.substack.com/p/discovering-the-postrat-canon-in) combines quote-tweet structure with semantic search, defines cohesion/evolution/utility before scoring, and spot-checks automated summaries. This analysis borrows the separation of structural and semantic evidence and keeps the two edge sources visible.
- [Modelling the viability of opportunity networks](https://xiqo.substack.com/p/modelling-the-viability-of-opportunity) tests friends-of-friends, calibrates assumptions on observed data, reports wide uncertainty, and stresses user heterogeneity. This analysis borrows the second-order bridge question and calibrated caveats, but does not add simulated Barabási–Albert edges to observed accounts.

## Rebuild and checks

```sh
python3 scripts/analyze.py
python3 -m unittest discover -s tests -v
git diff --exit-code
```

Expected coverage on this snapshot: 443 following accounts, 512 post-feature records from 28 accounts, 56 profile-timeline attempts, 15 communities, and six nearby candidates.
