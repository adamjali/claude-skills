#!/usr/bin/env python3
"""Build an explicit publish directory, and refuse to ship build artefacts.

Deploying a project root once published a client's HOME ADDRESS (research/BRIEF.md) and a
tracker PASSWORD (tracker.py). `.netlifyignore` does NOT stop this: it is not honoured by
`netlify deploy --dir`. The only reliable fix is to publish a directory that never contained
those files in the first place.

    python3 make-dist.py <project-dir>        # writes <project-dir>/dist
    netlify deploy --prod --dir dist
"""
import pathlib, shutil, sys

KEEP_EXT = {'.html','.css','.js','.mjs','.xml','.txt','.toml','.webp','.jpg','.jpeg','.png',
            '.svg','.gif','.ico','.mp4','.webm','.woff','.woff2','.ttf','.pdf','.vtt','.mp3','.avif'}
KEEP_NAME = {'_headers','_redirects','netlify.toml','robots.txt','sitemap.xml','favicon.ico',
             'site.webmanifest','manifest.json'}
SKIP_DIR = {'node_modules','.git','.netlify','__pycache__','dist','research','ledger',
            '.impeccable','out','src','.vscode','notes','scratch'}
BLOCK_NAME = {'package.json','package-lock.json','tsconfig.json','yarn.lock','.env',
              'ogcard.html'}   # social-card SOURCE: renders the card, must not be published
BLOCK_SUFFIX = ('.py','.md','.sh','.log','.srt','.bak','.frag','.ts','.tsx','.map')


def build(root: pathlib.Path):
    dist = root / 'dist'
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir()
    kept, blocked = [], []
    for p in root.rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(part in SKIP_DIR for part in rel.parts):
            continue
        if p.name in BLOCK_NAME or p.name.endswith(BLOCK_SUFFIX) or '.bak' in p.name:
            blocked.append(str(rel)); continue
        if p.suffix.lower() in KEEP_EXT or p.name in KEEP_NAME:
            t = dist / rel
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, t)
            kept.append(str(rel))
        else:
            blocked.append(str(rel))
    fn = root / 'netlify'                      # serverless functions must ship
    if fn.exists():
        shutil.copytree(fn, dist / 'netlify', dirs_exist_ok=True)
    return kept, blocked


if __name__ == '__main__':
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.').expanduser().resolve()
    kept, blocked = build(root)
    if not (root / 'dist' / 'index.html').exists():
        sys.exit("ABORT: dist has no index.html. Check the project layout before deploying.")
    print(f"dist ready: {len(kept)} files published, {len(blocked)} withheld")
    notable = [b for b in blocked if b.endswith(('.py', '.md')) or 'package' in b][:10]
    if notable:
        print("withheld (build artefacts):", ", ".join(notable))
