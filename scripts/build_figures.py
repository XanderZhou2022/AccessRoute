"""Compile the TikZ method figures and package their editable sources."""
from pathlib import Path
import shutil
import subprocess
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('route-planning', 'visual-localization', 'rag-retrieval')

def main():
    output = ROOT / 'dist/assets/methods'
    output.mkdir(parents=True, exist_ok=True)
    latex = shutil.which('pdflatex') or '/Library/TeX/texbin/pdflatex'
    svg = shutil.which('pdftocairo')
    if not svg:
        raise RuntimeError('Install Poppler (pdftocairo) to export SVG figures.')
    for name in NAMES:
        source = ROOT / 'figures' / name / 'main.tex'
        with tempfile.TemporaryDirectory(prefix='accessroute-figure-') as tmp:
            result = subprocess.run(
                [latex, '-no-shell-escape', '-halt-on-error', '-interaction=nonstopmode',
                 f'-output-directory={tmp}', str(source)],
                cwd=source.parent, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(result.stdout[-7000:] + result.stderr)
            if 'Overfull' in result.stdout:
                raise RuntimeError(f'{name}: overflowing TeX content\n{result.stdout}')
            pdf = Path(tmp) / 'main.pdf'
            shutil.copyfile(pdf, output / f'{name}.pdf')
            subprocess.run([svg, '-svg', str(pdf), str(output / f'{name}.svg')], check=True)
        print(f'Built {name}: PDF + SVG')
    archive = ROOT / 'dist/downloads/method-figures-source.zip'
    with ZipFile(archive, 'w', ZIP_DEFLATED) as bundle:
        for name in NAMES:
            bundle.write(ROOT / 'figures' / name / 'main.tex', f'{name}/main.tex')
        bundle.write(ROOT / 'figures/README.txt', 'README.txt')

if __name__ == '__main__':
    main()
