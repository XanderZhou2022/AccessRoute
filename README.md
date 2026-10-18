# AccessRoute HK

Project website for HumanRoute's accessible first and last mile navigation system.

**Website:** https://xanderzhou2022.github.io/AccessRoute/

## Explore

- [Journey](https://xanderzhou2022.github.io/AccessRoute/journey.html): product screens, route choices and the Kowloon Tong field video.
- [Technology](https://xanderzhou2022.github.io/AccessRoute/technology.html): map contracts, AI workflows and deterministic routing.
- [Validation](https://xanderzhou2022.github.io/AccessRoute/validation.html): dated regression results and scene coverage.
- [Resources](https://xanderzhou2022.github.io/AccessRoute/resources.html): manual, presentation, videos and technical references.

Navigation application source: [AccessRoute_small_demo](https://github.com/XanderZhou2022/AccessRoute_small_demo).

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
