# X follow graph

I use this dated, read-only map of the 443 X accounts I follow to see communities, bridges, weak ties, nearby people, and accounts worth reviewing; it never changes my X account.

Read [the report](report.md), then inspect `data/derived/`. Rebuild it with:

```sh
python3 scripts/analyze.py
python3 -m unittest discover -s tests -v
```

The browser collection reached the bottom of my Following list. X blocked profile timelines after 512 post-feature records from 28 accounts; the exact boundary and failed retries are documented in [`reproduce/methodology.md`](reproduce/methodology.md).

