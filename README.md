# AccessRoute HK

Project website for HumanRoute's accessible first and last mile navigation system.

**Website:** https://xanderzhou2022.github.io/AccessRoute/

## Explore

- [Journey](https://xanderzhou2022.github.io/AccessRoute/journey.html): product screens, route choices and the Kowloon Tong field video.
- [Technology](https://xanderzhou2022.github.io/AccessRoute/technology.html): map contracts, AI workflows and deterministic routing.
- [Validation](https://xanderzhou2022.github.io/AccessRoute/validation.html): dated regression results and scene coverage.
- [Resources](https://xanderzhou2022.github.io/AccessRoute/resources.html): manual, presentation, videos and technical references.

Navigation application source: [AccessRoute_small_demo](https://github.com/XanderZhou2022/AccessRoute_small_demo).

## Technical method pages

- `routing.html`: feasible-graph formulation, objective weights and numbered lexicographic Dijkstra pseudocode.
- `localization.html`: map indexing, bounded retrieval, evidence scoring and graph-node coordinate resolution.

Both pages are linked from Technology. `scripts/methods.py` maintains the page content and selectable equations / algorithms; `dist/assets/methods.css` supplies their paper-style layout. The TikZ projects in `figures/` generate the main figures, with PDF / SVG exports and a downloadable source ZIP.

The localization page also includes an expanded RAG data-flow figure (`figures/rag-retrieval/`), showing node-linked map records, retrieved candidates, structured model input, evidence pairs, ranking and coordinate lookup.

Both pages now open with interactive explanations. The route widget lets readers change mobility, weather, route objectives and lift closures. The localization walkthrough reveals observation, retrieval, evidence validation, ranking and a confirmable map anchor. It uses clearly labelled synthetic records and prepared visual/model outputs; route planning, spatial retrieval and scoring run through a checked-in snapshot of the application core. See `interactive/README.txt` for source provenance and rebuilding.

Validate the interactive behavior with:

```bash
node scripts/check_interactive.mjs
node --check dist/assets/method-interactive.mjs
```

The Pages workflow checks all static references and 108 combinations of teaching-widget settings before deployment. No model credentials or backend are required by these explanations.

Regenerate figures with a local TeX installation (`pdflatex`, standalone, newtxtext/newtxmath, TikZ) and Poppler (`pdftocairo`):

```bash
python3 scripts/build_figures.py
python3 scripts/build.py
python3 scripts/check.py
```

Ordinary content edits require only the last two commands. The committed vector exports let GitHub Pages publish without a TeX installation. On narrow screens, figures and long formulas scroll inside their own regions; the rest of each page reflows.

## Website source

The static site is in `dist/`. It uses HTML, CSS and a small JavaScript menu. All sections have direct URLs and work as ordinary links.

Preview from this directory:

```bash
python3 -m http.server 8798 --directory dist
```

`scripts/build.py` generates the HTML pages. Edit its English content or update files in `dist/assets/` and `dist/downloads/`, then run:

```bash
python3 scripts/build.py
python3 scripts/check.py
```

GitHub Actions publishes `dist/` to GitHub Pages on pushes to `main`.

## Materials

Product screenshots and the two videos come from the AccessRoute project materials. The English manual and technical presentation are available under `dist/downloads/`.

The regression summary records the 18 October 2026 run against the local `accessroute-hk` source: 132 tests across 16 files. Test cases and outcomes are listed in the downloadable JSON record.

Map from Lands Department © Government of the Hong Kong Special Administrative Region. Official map and transit data retains its source terms. See the website's [technical references](https://xanderzhou2022.github.io/AccessRoute/resources.html#references).

## API cost and timing page

`service-budget.html` reproduces the technical report’s section 23 tables and links the dated timing evidence. The page distinguishes historical price snapshots, token workload budgets, observed timing, request deadlines and acceptance targets. `dist/downloads/service-budget.json` holds the data; `scripts/service_budget.py` generates the tables, and `dist/assets/service-budget.mjs` calculates adjustable workloads locally without model calls. JSON, CSV and a report extract are downloadable.

Run `node scripts/check_service_budget.mjs` to check all per-call arithmetic, report journey workloads and calculator edge cases.
