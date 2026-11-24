# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/highwill/news-image-20261124-v2/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/highwill/news-image-20261124-v2/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper front page summing up Tuesday, 24 November 2026 — lead story: Trump, Xi and Putin to hold a historic trilateral summit in Shenzhen; plus the Banten factory fire, the Kyiv-region drone strike, COP31 in Antalya, Verstappen's Las Vegas win, and the India–Nepal Saryu-Kamala Express. Round 2 rebuild: every story now gets its own illustration (the lead panel is a dusk Shenzhen skyline with the three leaders' flags), the layout is measured so no deck line can touch a rule, and the lead deck drops the hype.

The image is drawn by `tools/draw_frontpage.py` (Python PIL, flat colours) and `main.ts` copies it to `/output/entry.png`.

## Run it

```sh
python3 tools/draw_frontpage.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
