"""Check static routes and assets without a browser or third-party packages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import json

ROOT=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls=[];self.ids=set();self.h1=0;self.lang=None;self.image_alt=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if 'id' in a:self.ids.add(a['id'])
        if tag=='img':self.image_alt.append(a.get('alt'))
        for key in ['href','src','poster']:
            if key in a:self.urls.append(a[key])

pages={}
for file in ROOT.glob('*.html'):
    page=Page();page.feed(file.read_text());pages[file]=page
    assert page.lang=='en',f'Language: {file}'
    assert page.h1==1,f'Heading: {file}'
    assert all(page.image_alt),f'Image descriptions: {file}'
    text=file.read_text().lower()
    for banned in ['[add link','workbuddy','n = 110','does not claim','not intended','only a prototype','lorem ipsum']:
        assert banned not in text,f'Unwanted copy in {file}: {banned}'

count=0
for file,page in pages.items():
    for url in page.urls:
        parsed=urlparse(url)
        if parsed.scheme or parsed.netloc:continue
        target=(file.parent/unquote(parsed.path)).resolve() if parsed.path else file
        assert target.is_relative_to(ROOT.resolve()),f'Outside site: {url}'
        assert target.exists(),f'Missing asset: {file.name} {url}'
        if parsed.fragment and target in pages:assert parsed.fragment in pages[target].ids,f'Missing anchor: {url}'
        count+=1

report=json.loads((ROOT/'downloads/regression-report.json').read_text())
assert report['success'] and report['testsPassed']==132 and report['testsFailed']==0
assert len(json.loads((ROOT/'assets/scenes.json').read_text()))==12
assert not any(p.name.startswith('.env') for p in ROOT.rglob('*'))
print(f'PASS: {len(pages)} pages, {count} internal references, English copy, image descriptions, 12 scenes and the regression record.')
