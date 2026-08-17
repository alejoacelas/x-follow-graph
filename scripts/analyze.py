#!/usr/bin/env python3
"""Build a deterministic, dependency-free analysis of Alejo's X follow graph."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path


STOP = set("""
a about above after again against all am an and any are as at be because been before being below between both but by can could did do does doing down during each few for from further had has have having he her here hers herself him himself his how i if in into is it its itself just me more most my myself no nor not now of off on once only or other our ours ourselves out over own same she should so some such than that the their theirs them themselves then there these they this those through to too under until up very was we were what when where which while who whom why will with would you your yours yourself yourselves
ai agi account also building build make making new one people person prev really research researcher tweets twitter x work working works via using use world
com org views opinions phd chief currently run web open independent senior fellow ceo co-founder nonprofit organization
""".split())

NORMALIZE = {
    "alignment": "ai-safety", "safety": "ai-safety", "misalignment": "ai-safety",
    "models": "models", "model": "models", "llm": "models", "llms": "models",
    "communities": "community", "social": "community", "collective": "community",
    "institutions": "institutions", "institutional": "institutions", "governance": "institutions",
    "philosophical": "philosophy", "philosopher": "philosophy",
    "economic": "economics", "economist": "economics",
    "scientist": "science", "scientific": "science",
    "founder": "founders", "startups": "founders", "startup": "founders",
    "developers": "software", "developer": "software", "coding": "software", "code": "software",
}


def tokens(text: str) -> list[str]:
    text = re.sub(r"https?://\S+", " ", text.lower())
    out = []
    for token in re.findall(r"[a-z][a-z0-9_-]{2,}", text):
        token = NORMALIZE.get(token, token)
        if token not in STOP and not token.startswith("http"):
            out.append(token)
    return out


def load_json(path: Path, default):
    return json.loads(path.read_text()) if path.exists() else default


def vectorize(documents: dict[str, list[str]]):
    n = len(documents)
    dfs = Counter()
    tfs = {}
    for key, words in documents.items():
        tf = Counter(words)
        tfs[key] = tf
        dfs.update(tf.keys())
    vectors = {}
    for key, tf in tfs.items():
        vector = {}
        for word, count in tf.items():
            idf = math.log((1 + n) / (1 + dfs[word])) + 1
            vector[word] = (1 + math.log(count)) * idf
        norm = math.sqrt(sum(v * v for v in vector.values())) or 1
        vectors[key] = {w: v / norm for w, v in vector.items()}
    return vectors


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(value * b.get(word, 0.0) for word, value in a.items())


def mean_vector(items: list[dict[str, float]]) -> dict[str, float]:
    total = Counter()
    for item in items:
        total.update(item)
    if not items:
        return {}
    vector = {w: v / len(items) for w, v in total.items()}
    norm = math.sqrt(sum(v * v for v in vector.values())) or 1
    return {w: v / norm for w, v in vector.items()}


def _kmeans_once(vectors, k, first):
    keys = sorted(vectors)
    seeds = [first]
    while len(seeds) < k:
        candidate = min(
            (x for x in keys if x not in seeds),
            key=lambda x: (max(cosine(vectors[x], vectors[s]) for s in seeds), x),
        )
        seeds.append(candidate)
    centroids = [vectors[x] for x in seeds]
    labels = {}
    for _ in range(50):
        updated = {
            key: max(range(k), key=lambda i: (cosine(vector, centroids[i]), -i))
            for key, vector in vectors.items()
        }
        if updated == labels:
            break
        labels = updated
        groups = [[vectors[x] for x in keys if labels[x] == i] for i in range(k)]
        centroids = [mean_vector(group) if group else vectors[seeds[i]] for i, group in enumerate(groups)]
    objective = sum(cosine(vectors[key], centroids[labels[key]]) for key in keys)
    return labels, objective


def kmeans(vectors: dict[str, dict[str, float]], k: int) -> dict[str, int]:
    """Deterministic multi-start spherical k-means."""
    keys = sorted(vectors)
    starters = sorted(keys, key=lambda x: (-len(vectors[x]), x))[:min(12, len(keys))]
    labels, _ = max((_kmeans_once(vectors, k, first) for first in starters), key=lambda x: x[1])
    # Renumber by descending size so IDs are stable and readable.
    sizes = Counter(labels.values())
    remap = {old: new for new, old in enumerate(sorted(sizes, key=lambda x: (-sizes[x], x)), 1)}
    return {key: remap[value] for key, value in labels.items()}


def semantic_graph(vectors, mentions, neighbors=6, threshold=0.075):
    keys = sorted(vectors)
    sims = {key: [] for key in keys}
    for i, left in enumerate(keys):
        for right in keys[i + 1:]:
            sim = cosine(vectors[left], vectors[right])
            if sim >= threshold:
                sims[left].append((sim, right))
                sims[right].append((sim, left))
    edges = {}
    for left in keys:
        for sim, right in sorted(sims[left], reverse=True)[:neighbors]:
            edge = tuple(sorted((left, right)))
            edges[edge] = max(edges.get(edge, 0), sim)
    known = set(keys)
    for left, targets in mentions.items():
        for right in targets:
            right = right.lower()
            if right in known and right != left:
                edge = tuple(sorted((left, right)))
                edges[edge] = max(edges.get(edge, 0), 0.35) + 0.35
    adjacency = {key: {} for key in keys}
    for (left, right), weight in edges.items():
        adjacency[left][right] = weight
        adjacency[right][left] = weight
    return edges, adjacency


def sampled_betweenness(adjacency, max_sources=80):
    nodes = sorted(adjacency)
    if len(nodes) > max_sources:
        step = len(nodes) / max_sources
        sources = [nodes[int(i * step)] for i in range(max_sources)]
    else:
        sources = nodes
    score = Counter()
    for source in sources:
        stack, predecessors = [], {v: [] for v in nodes}
        sigma, distance = Counter({source: 1.0}), {source: 0}
        queue = deque([source])
        while queue:
            v = queue.popleft(); stack.append(v)
            for w in adjacency[v]:
                if w not in distance:
                    queue.append(w); distance[w] = distance[v] + 1
                if distance[w] == distance[v] + 1:
                    sigma[w] += sigma[v]; predecessors[w].append(v)
        delta = Counter()
        while stack:
            w = stack.pop()
            for v in predecessors[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != source:
                score[w] += delta[w]
    scale = (len(nodes) / max(1, len(sources))) / 2
    return {node: score[node] * scale for node in nodes}


def parse_mutual_count(text: str):
    numbers = [int(x.replace(",", "")) for x in re.findall(r"\d[\d,]*", text)]
    return (numbers[-1] + 2) if numbers else None


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root
    raw, out = root / "data" / "raw", root / "data" / "derived"
    out.mkdir(parents=True, exist_ok=True)
    follow = load_json(raw / "following.json", {"accounts": []})
    posts = load_json(raw / "post-features.json", {"accounts": []})
    candidates = load_json(raw / "candidates.json", {"accounts": []})
    accounts = follow["accounts"]
    by_handle = {a["handle"].lower(): a for a in accounts}
    post_by = {a["handle"].lower(): a for a in posts.get("accounts", [])}

    documents = {}
    for handle, account in by_handle.items():
        words = tokens(account.get("bio", "")) * 3
        for term in post_by.get(handle, {}).get("top_terms", []):
            words.extend([term["term"]] * min(5, term["count"]))
        documents[handle] = words or ["unknown-profile"]
    vectors = vectorize(documents)
    k = max(6, min(16, round(math.sqrt(len(accounts) / 2))))
    labels = kmeans(vectors, k)
    mentions = {h: a.get("bio_mentions", []) for h, a in by_handle.items()}
    edges, adjacency = semantic_graph(vectors, mentions)
    between = sampled_betweenness(adjacency)
    max_between = max(between.values()) or 1

    weighted_degree = {h: sum(adjacency[h].values()) for h in adjacency}
    bridge_rows = []
    account_rows = []
    for handle in sorted(by_handle):
        cross = sum(w for other, w in adjacency[handle].items() if labels[other] != labels[handle])
        total = weighted_degree[handle] or 1
        bridge = 0.55 * (between[handle] / max_between) + 0.45 * (cross / total)
        account = by_handle[handle]
        post = post_by.get(handle, {})
        account_rows.append({
            "handle": account["handle"], "name": account["name"], "community": labels[handle],
            "weighted_degree": f"{weighted_degree[handle]:.4f}", "bridge_score": f"{bridge:.4f}",
            "verified": account.get("verified", False), "follows_you": account.get("follows_you", False),
            "posts_collected": post.get("post_count", ""), "latest_post_at": post.get("latest_post_at", ""),
            "bio": account.get("bio", ""), "profile_url": account["profile_url"],
        })
    write_csv(out / "accounts.csv", account_rows, list(account_rows[0]))

    cluster_data = []
    for community in sorted(set(labels.values())):
        members = [h for h in labels if labels[h] == community]
        centroid = mean_vector([vectors[h] for h in members])
        top_terms = [w for w, _ in sorted(centroid.items(), key=lambda x: (-x[1], x[0])) if w != "unknown-profile"][:8]
        central = sorted(members, key=lambda h: (-weighted_degree[h], h))[:8]
        cluster_data.append({
            "id": community, "size": len(members), "label": " / ".join(top_terms[:4]) or "low-information",
            "top_terms": top_terms, "central_accounts": [by_handle[h]["handle"] for h in central],
        })
    (out / "communities.json").write_text(json.dumps(cluster_data, indent=2) + "\n")

    bridge_rank = sorted(account_rows, key=lambda r: (-float(r["bridge_score"]), r["handle"].lower()))[:30]
    write_csv(out / "bridges.csv", bridge_rank, list(bridge_rank[0]))

    weak = []
    account_bridge = {r["handle"].lower(): float(r["bridge_score"]) for r in account_rows}
    for (left, right), weight in edges.items():
        if labels[left] == labels[right]:
            continue
        weak.append({
            "left": by_handle[left]["handle"], "left_community": labels[left],
            "right": by_handle[right]["handle"], "right_community": labels[right],
            "similarity_or_mention_weight": f"{weight:.4f}",
            "structural_score": f"{weight * (account_bridge[left] + account_bridge[right]):.4f}",
        })
    weak.sort(key=lambda r: (-float(r["structural_score"]), r["left"].lower(), r["right"].lower()))
    write_csv(out / "weak-ties.csv", weak[:50], list(weak[0]))

    today = datetime(2026, 8, 16, tzinfo=timezone.utc)
    review = []
    for row in account_rows:
        handle = row["handle"].lower(); post = post_by.get(handle)
        reasons = []
        if post and post.get("latest_post_at"):
            date = datetime.fromisoformat(post["latest_post_at"].replace("Z", "+00:00"))
            age = (today - date).days
            if age >= 365: reasons.append(f"latest collected post is {age} days old")
            if post.get("post_count", 0) <= 2:
                count = post.get("post_count", 0)
                reasons.append(f"only {count} {'post' if count == 1 else 'posts'} visible")
        if not by_handle[handle].get("bio") and weighted_degree[handle] < 0.25:
            reasons.append("empty bio and little semantic/mention evidence")
        if reasons:
            review.append({"handle": row["handle"], "name": row["name"], "reason": "; ".join(reasons), "profile_url": row["profile_url"]})
    write_csv(out / "review-candidates.csv", review, ["handle", "name", "reason", "profile_url"])

    candidate_rows = []
    centroids = {c: mean_vector([vectors[h] for h in vectors if labels[h] == c]) for c in set(labels.values())}
    for candidate in candidates.get("accounts", []):
        candidate_documents = dict(documents)
        candidate_documents["__candidate__"] = tokens(candidate.get("bio", "")) or ["unknown-profile"]
        vec = vectorize(candidate_documents)["__candidate__"]
        nearest = sorted(centroids, key=lambda c: (-cosine(vec, centroids[c]), c))[:2]
        candidate_rows.append({
            "handle": candidate["handle"], "name": candidate["name"].strip(),
            "mutual_follow_context": parse_mutual_count(candidate.get("mutual_context", "")) or "",
            "adjacent_communities": ",".join(map(str, nearest)),
            "community_labels": " | ".join(next(x["label"] for x in cluster_data if x["id"] == c) for c in nearest),
            "bio": re.sub(r"\s+", " ", candidate.get("bio", "")).strip(),
            "profile_url": candidate["profile_url"],
        })
    candidate_rows.sort(key=lambda r: (-(int(r["mutual_follow_context"] or 0)), r["handle"].lower()))
    write_csv(out / "nearby-people.csv", candidate_rows, list(candidate_rows[0]))

    states = Counter(a.get("load_state", "unknown") for a in posts.get("accounts", []))
    posts_collected = sum(a.get("post_count", 0) for a in posts.get("accounts", []))
    coverage = {
        "following_accounts": len(accounts), "following_collection_complete_to_ui_bottom": True,
        "post_accounts_attempted": len(posts.get("accounts", [])),
        "post_accounts_with_at_least_one": sum(a.get("post_count", 0) > 0 for a in posts.get("accounts", [])),
        "post_feature_records": posts_collected, "post_load_states": dict(states),
        "candidate_profiles": len(candidate_rows), "communities": len(cluster_data),
        "graph_edges": len(edges), "cross_community_edges": len(weak),
    }
    (out / "coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")

    lines = [
        "# Alejo's X follow graph", "",
        f"I collected all **{len(accounts)} accounts** visible in `@alejoacelas`'s Following list on 2026-08-16. "
        f"The list reached the UI bottom after six consecutive scrolls added no accounts.", "",
        "## Coverage", "",
        f"- Following: {len(accounts)}/{len(accounts)} UI-visible accounts.",
        f"- Posts: {posts_collected} feature records from {coverage['post_accounts_with_at_least_one']} accounts; "
        f"{coverage['post_accounts_attempted']} profiles attempted before X's timeline endpoint began returning “Something went wrong.”",
        "- Post text was reduced in memory to dates, URLs, repost flags, and aggregate terms; full tweet text is not stored.",
        "- No likes, follows, unfollows, messages, or other X mutations were made.", "",
        "## Communities", "",
        "Communities come from deterministic TF–IDF k-means over bios plus available post terms. The graph overlays six-nearest semantic edges and explicit bio mentions; it is not a crawl of follow edges among the 443 accounts.", "",
    ]
    for cluster in cluster_data:
        lines.append(f"- **{cluster['id']} · {cluster['label']}** — {cluster['size']} accounts; central: " + ", ".join("@" + x for x in cluster["central_accounts"][:5]))
    lines += ["", "## Bridges and weak ties", "",
              "Bridge scores combine sampled betweenness with the share of a node's weighted edges that cross communities. Treat them as navigation leads, not prestige scores.", "",
              "Top bridge accounts: " + ", ".join("@" + row["handle"] for row in bridge_rank[:12]) + ".", "",
              "The account pairs in `data/derived/weak-ties.csv` are cross-community semantic or bio-mention edges. They identify where Alejo's interests overlap; they do not prove that the two accounts follow or interact with each other.", "",
              "## Review candidates", ""]
    if review:
        for row in review[:15]: lines.append(f"- [@{row['handle']}]({row['profile_url']}) — {row['reason']}.")
    else:
        lines.append("No account had enough evidence for a stale/low-signal flag. Missing post coverage is never treated as inactivity.")
    lines += ["", "These are review prompts only. No one was unfollowed.", "", "## Nearby people", "",
              "X showed these unfollowed accounts on signed-in recommendation surfaces. Mutual counts are the number of Alejo-followed accounts X displayed as following each candidate; they are context, not causal evidence.", ""]
    for row in candidate_rows:
        lines.append(f"- [@{row['handle']}]({row['profile_url']}) — {row['mutual_follow_context']} mutual-follow context; adjacent to {row['community_labels']}; {row['bio']}")
    lines += ["", "## Method borrowed from xiq", "",
              "- [A Birdseye view of your tweets](https://xiqo.substack.com/p/a-birdseye-view-of-your-tweets) embeds account history, clusters it, labels clusters, and distinguishes persistent topics from isolated events. I borrow the embed/cluster/label shape, while using reproducible TF–IDF because this dataset has only bios and partial post features.",
              "- [How to measure serendipity online](https://xiqo.substack.com/p/experiments-on-measuring-community) uses recent reciprocal exchanges, a second proxy metric, sensitivity checks, and explicit missing-data treatment. I borrow the multiple-signal and missingness discipline; this dataset cannot reproduce reciprocal-interaction metrics.",
              "- [Discovering the postrat canon](https://xiqo.substack.com/p/discovering-the-postrat-canon-in) combines quote-tweet structure with semantic matches and manual quality criteria, then spot-checks LLM summaries. I borrow its separation of structural and semantic evidence and avoid pretending semantic proximity is a social tie.",
              "- [Modelling the viability of opportunity networks](https://xiqo.substack.com/p/modelling-the-viability-of-opportunity) models friends-of-friends, calibrates on observed data, reports wide uncertainty, and stresses heterogeneity. I borrow the focus on second-order bridges and calibrated caveats, but do not import its Barabási–Albert simulated edges into this observed ego network.",
              "", "## Limits", "",
              "- X exposes an ego list here, not the full directed graph among followed accounts. Community and bridge results therefore mix semantic edges with explicit bio mentions.",
              "- X rate-limited profile timelines after a burst of profile reads. The collection stopped instead of bypassing the UI; exact post coverage is in `data/derived/coverage.json`.",
              "- Recommendation candidates came from X's opaque ranking and may reflect popularity, mutuals, or personalization. “Generative” is inferred from their stated work and adjacency, not measured output quality.",
              "- Bios and recent posts change. This is a dated snapshot, not a durable account judgment.", ""]
    (root / "report.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
