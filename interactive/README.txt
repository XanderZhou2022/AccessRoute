AccessRoute interactive method explanations

core/ holds unmodified TypeScript snapshots from AccessRoute_small_demo,
commit 7a8024d3706c3ebfaf46163e78be988c4c501ef4:
  shared/routing/route.ts, policies.ts, metrics.ts
  backend/retrieval/map-index.ts, rank.ts

The static site bundles only the functions used by the widgets. Type-only
imports disappear during compilation; the bundle has no framework or
runtime package dependencies.

Rebuild with esbuild 0.28.2 (or a compatible installed esbuild):
  ESBUILD=/path/to/esbuild python3 scripts/build_interactive.py
  python3 scripts/build.py
  node scripts/check_interactive.mjs
  python3 scripts/check.py

The committed engine bundle lets GitHub Pages deploy without a Node or
TypeScript build. Changes to HTML prose require only scripts/build.py.

dist/assets/method-model.mjs contains the synthetic graph, synthetic map
records and prepared observations/model evidence. It calls the original
core for route planning, edge policies, spatial retrieval, candidate
ranking and decision thresholds. It does not call a live AI model.
dist/assets/method-interactive.mjs binds the model to the accessible UI.

Input changes invalidate any confirmed teaching anchor. Widgets neither
store user data nor send their inputs to a backend.
