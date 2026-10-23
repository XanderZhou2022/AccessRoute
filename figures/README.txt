AccessRoute HK: method figures

Three self-contained TikZ projects, each with main.tex:
  route-planning/        Policy-constrained lexicographic Dijkstra
  visual-localization/  Retrieval-augmented visual localization
  rag-retrieval/        Detailed records, retrieval, evidence and node lookup

Compile with pdflatex (standalone, newtxtext/newtxmath, TikZ required):
  cd route-planning
  pdflatex -no-shell-escape -halt-on-error main.tex

The website uses SVG exports with glyph outlines for consistent rendering.
PDF exports retain vector graphics and embedded fonts.
From the website repository, regenerate all exports and the source ZIP:
  python3 scripts/build_figures.py

Figures describe implemented mechanisms, with abstract symbols and no
location-specific examples or measured performance claims.
The routing figure describes the general graph engine. The Kowloon Tong
field-route wrapper additionally evaluates stored route sequences.
The localization figure describes the live backend workflow. Static
showcase presets use prepared associations rather than live inference.

Labels use 8.7 pt or larger at the native figure width (approximately 18 cm).
Use at full two-column width, or enlarge for screen viewing.

Copyright 2026 HumanRoute / AccessRoute HK.
