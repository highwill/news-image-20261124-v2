// news-image-20261124, round 2: "The World — Tuesday, 24 November 2026".
// The front page is drawn by tools/draw_frontpage.py (Python + PIL) into
// entry.png beside this file; this program copies that image to the
// grader's output directory, so both runs write the same bytes.
// Node 22, standard library only. Outside the grader, MAKEFUN_OUTPUT_DIR
// stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(new URL("./entry.png", import.meta.url),
  join(outDir, "entry.png"));
