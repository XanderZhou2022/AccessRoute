"""Bundle the checked-in AccessRoute core for the static teaching widgets."""
from pathlib import Path
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
esbuild = os.environ.get('ESBUILD') or shutil.which('esbuild')
if not esbuild:
    bundled = ROOT.parent / 'accessroute-showcase/node_modules/.bin/esbuild'
    if bundled.exists():
        esbuild = str(bundled)
if not esbuild:
    raise SystemExit('Set ESBUILD to an installed esbuild executable to rebuild the core bundle.')
subprocess.run([esbuild, str(ROOT/'interactive/engine.ts'), '--bundle', '--format=esm',
                '--target=es2020', '--minify',
                f'--outfile={ROOT / "dist/assets/method-engine.mjs"}'], check=True)
