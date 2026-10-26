"""Adds content-hash version tags to the site's own CSS and JS, so a change shows
as soon as the page is reloaded instead of after the browser cache expires
(GitHub Pages lets browsers keep files for 10 minutes).

    python tools/asset_versions.py        (also run by tools/build_pages.py)

For each page it:
  - rewrites assets/css/*.css and assets/js/*.js links to file.css?v=<hash>;
  - adds an import map before the first module script, so modules imported
    from main.js (./motion/core.js, the 3D bundle, ...) get the same tags.
The hash comes from the file's contents, so it only changes when the file does.
Vendor files already carry their version in the file name and are left alone.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_SKIP = ("design/", "tools/", "e-invoice-checker/", "node_modules/")
REF = re.compile(r'(?P<attr>href|src)="(?P<path>/?assets/(?:css|js)/[^"?#]+\.(?:css|js))(?:\?v=[0-9a-f]+)?"')
IMPORT_MAP = re.compile(r'[ \t]*<script type="importmap">.*?</script>\r?\n', re.S)
FIRST_MODULE = re.compile(r'([ \t]*)<script type="module"')


def version(path):
    # Line endings normalised, so a Windows checkout gives the same hash as the repo.
    data = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()[:10]


def import_map():
    modules = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "assets" / "js").rglob("*.js"))
    return json.dumps({"imports": {f"/{m}": f"/{m}?v={version(m)}" for m in modules}}, separators=(",", ":"))


def stamp(page, imports):
    raw = page.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    s = REF.sub(lambda m: f'{m["attr"]}="{m["path"]}?v={version(m["path"].lstrip("/"))}"', raw)
    s = IMPORT_MAP.sub("", s)
    first = FIRST_MODULE.search(s)
    if first:
        tag = f'{first[1]}<script type="importmap">{imports}</script>{nl}'
        s = s[:first.start()] + tag + s[first.start():]
    if s != raw:
        page.write_bytes(s.encode("utf-8"))
        return True
    return False


def stamp_all():
    imports = import_map()
    pages = [p for p in ROOT.rglob("*.html")
             if not p.relative_to(ROOT).as_posix().startswith(PAGES_SKIP)]
    return [p for p in sorted(pages) if stamp(p, imports)]


if __name__ == "__main__":
    for p in stamp_all():
        print("versioned", p.relative_to(ROOT).as_posix())
