# Alejo's X follow graph

I collected all **443 accounts** visible in `@alejoacelas`'s Following list on 2026-08-16. The list reached the UI bottom after six consecutive scrolls added no accounts.

## Coverage

- Following: 443/443 UI-visible accounts.
- Posts: 512 feature records from 28 accounts; 56 profiles attempted before X's timeline endpoint began returning “Something went wrong.”
- Post text was reduced in memory to dates, URLs, repost flags, and aggregate terms; full tweet text is not stored.
- No likes, follows, unfollows, messages, or other X mutations were made.

## Communities

Communities come from deterministic TF–IDF k-means over bios plus available post terms. The graph overlays six-nearest semantic edges and explicit bio mentions; it is not a crawl of follow edges among the 443 accounts.

- **1 · policy / future / google / risks** — 165 accounts; central: @jasonhausenloy, @GovAIOrg, @arcinstitute, @PeterMcCrory, @coeff_giving
- **2 · anthropicai / trying / training / philosophy** — 42 accounts; central: @bcherny, @AvitalBalwit, @jkcarlsmith, @AmandaAskell, @divyasiddarth
- **3 · ai-safety / assistant / systems / company** — 35 accounts; central: @AnthropicAI, @FabienDRoger, @rohinmshah, @EthanJPerez, @METR_Evals
- **4 · director / health / professor / dad** — 30 accounts; central: @JacobSteinhardt, @natliml, @goodside, @bscwang, @sj_manning
- **5 · models / deep / tech / scientists** — 27 accounts; central: @80000Hours, @ARIA_research, @MariusHobbhahn, @fish_kyle3, @aengus_lynch1
- **6 · low-information** — 27 accounts; central: @pawtrammell, @repligate, @richardhatchett, @SemiAnalysis_, @tkuiken
- **7 · openai / harvard / science / lead** — 26 accounts; central: @OpenAI, @gdb, @JacobTref, @jxnlco, @sharifshameem
- **8 · founders / cursor_ai / spacexai / agent** — 23 accounts; central: @pmcntyr, @amanrsanger, @ben_j_todd, @StartupArchive_, @jasoncrawford
- **9 · biosecurity / pandemics / emerging / focused** — 15 accounts; central: @RyanGreenblatt, @Convergent_FROs, @JacobSwett, @JaimeYassif, @kprather88
- **10 · engineer / product / codex / london** — 13 accounts; central: @lvcadeleo, @OpenAIDevs, @skirano, @kevinweil, @saadiq
- **11 · work / resolution_org / cofounder / arcinstitute** — 10 accounts; central: @patrickc, @abhinadduri, @alexalbert__, @_catwu, @jacob_pfau
- **12 · futures / bio / nabla / biosecurity** — 10 accounts; central: @deanwball, @jackclarkSF, @kenzasaml, @guynamedjoshl, @joshgans
- **13 · effective / events / altruism / academic** — 7 accounts; central: @bellaforristal, @Ollie_Base, @willmacaskill, @Turn_Trout, @ReflectiveAlt
- **14 · tools / insight / focus / memory** — 7 accounts; central: @catherineols, @charliermarsh, @zeynep, @vibeshipco, @visakanv
- **15 · guy / economy / political / bias** — 6 accounts; central: @BharatKChandar, @danielrock, @haththerescuer, @JasonDClinton, @BertuzLuca

## Bridges and weak ties

Bridge scores combine sampled betweenness with the share of a node's weighted edges that cross communities. Treat them as navigation leads, not prestige scores.

Top bridge accounts: @AnthropicAI, @model_thinking, @EthanJPerez, @DuncanMcClement, @BharatKChandar, @80000Hours, @PeterMcCrory, @ARIA_research, @TechEmails, @RylanSchaeffer, @alexolegimas, @kprather88.

The account pairs in `data/derived/weak-ties.csv` are cross-community semantic or bio-mention edges. They identify where Alejo's interests overlap; they do not prove that the two accounts follow or interact with each other.

## Review candidates

- [@aghyadd98](https://x.com/aghyadd98) — latest collected post is 551 days old; only 2 posts visible.
- [@AHT_SBD](https://x.com/AHT_SBD) — only 1 post visible.

These are review prompts only. No one was unfollowed.

## Nearby people

X showed these unfollowed accounts on signed-in recommendation surfaces. Mutual counts are the number of Alejo-followed accounts X displayed as following each candidate; they are context, not causal evidence.

- [@ilyasut](https://x.com/ilyasut) — 191 mutual-follow context; adjacent to policy / future / google / risks | anthropicai / trying / training / philosophy; SSI @SSI
- [@_sholtodouglas](https://x.com/_sholtodouglas) — 161 mutual-follow context; adjacent to anthropicai / trying / training / philosophy | policy / future / google / risks; Scaling RL @AnthropicAI , ex @DeepMind - working towards intelligence too cheap to meter
- [@LauraDeming](https://x.com/LauraDeming) — 109 mutual-follow context; adjacent to founders / cursor_ai / spacexai / agent | policy / future / google / risks; CEO of @untillabs I enjoy helping new technologies into the Overton window of acceptable discourse
- [@SamoBurja](https://x.com/SamoBurja) — 82 mutual-follow context; adjacent to founders / cursor_ai / spacexai / agent | tools / insight / focus / memory; There's never been an immortal society. Figuring out why. Founder @bismarckanlys .
- [@Meaningness](https://x.com/Meaningness) — 76 mutual-follow context; adjacent to engineer / product / codex / london | tools / insight / focus / memory; Better ways of thinking, feeling, and acting—around problems of meaning and meaninglessness; self and society; ethics, purpose, and value.
- [@BraunJoschka](https://x.com/BraunJoschka) — 8 mutual-follow context; adjacent to ai-safety / assistant / systems / company | openai / harvard / science / lead; AI safety researcher @ApolloResearch | Science of Scheming | prev. @MATSprogram @kasl_ai @health_nlp @uni_tue

## Method borrowed from xiq

- [A Birdseye view of your tweets](https://xiqo.substack.com/p/a-birdseye-view-of-your-tweets) embeds account history, clusters it, labels clusters, and distinguishes persistent topics from isolated events. I borrow the embed/cluster/label shape, while using reproducible TF–IDF because this dataset has only bios and partial post features.
- [How to measure serendipity online](https://xiqo.substack.com/p/experiments-on-measuring-community) uses recent reciprocal exchanges, a second proxy metric, sensitivity checks, and explicit missing-data treatment. I borrow the multiple-signal and missingness discipline; this dataset cannot reproduce reciprocal-interaction metrics.
- [Discovering the postrat canon](https://xiqo.substack.com/p/discovering-the-postrat-canon-in) combines quote-tweet structure with semantic matches and manual quality criteria, then spot-checks LLM summaries. I borrow its separation of structural and semantic evidence and avoid pretending semantic proximity is a social tie.
- [Modelling the viability of opportunity networks](https://xiqo.substack.com/p/modelling-the-viability-of-opportunity) models friends-of-friends, calibrates on observed data, reports wide uncertainty, and stresses heterogeneity. I borrow the focus on second-order bridges and calibrated caveats, but do not import its Barabási–Albert simulated edges into this observed ego network.

## Limits

- X exposes an ego list here, not the full directed graph among followed accounts. Community and bridge results therefore mix semantic edges with explicit bio mentions.
- X rate-limited profile timelines after a burst of profile reads. The collection stopped instead of bypassing the UI; exact post coverage is in `data/derived/coverage.json`.
- Recommendation candidates came from X's opaque ranking and may reflect popularity, mutuals, or personalization. “Generative” is inferred from their stated work and adjacency, not measured output quality.
- Bios and recent posts change. This is a dated snapshot, not a durable account judgment.
