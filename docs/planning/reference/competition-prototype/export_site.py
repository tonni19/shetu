"""Export the Flask prototype as a static site in ./site (for GitHub Pages)."""
import re, shutil
from pathlib import Path
import shetu_app as A

out = Path(__file__).parent / "site"
for f in list(out.iterdir()):
    if f.name in (".git", ".nojekyll"):
        continue
    shutil.rmtree(f) if f.is_dir() else f.unlink()
shutil.copytree(Path(__file__).parent / "static", out / "static")
routes = {"/": "index.html", "/how": "how/index.html", "/employer": "employer/index.html",
          "/employer/case/nusrat": "employer/case/nusrat/index.html", "/employer/team": "employer/team/index.html",
          "/employer/report": "employer/report/index.html", "/me": "me/index.html", "/me/map": "me/map/index.html",
          "/me/hold": "me/hold/index.html", "/me/fit": "me/fit/index.html"}
c = A.app.test_client()
for r, f in routes.items():
    resp = c.get(r)
    assert resp.status_code == 200, (r, resp.status_code)
    html = resp.get_data(as_text=True)
    depth = f.count("/")
    pre = "../" * depth if depth else "./"

    def fix(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith("/static/"):
            return f'{attr}="{pre}{url[1:]}"'
        if url in routes:
            return f'{attr}="{pre}{routes[url][:-len("index.html")]}"'
        if url.startswith("/employer/case/"):
            return f'{attr}="{pre}employer/case/nusrat/"'
        return m.group(0)

    html = re.sub(r'(href|src)="(/[^"]*)"', fix, html)
    html = html.replace("Prototype · demo data · runs offline", "Prototype · demo data · AI outputs generated offline on our laptop")
    html = html.replace("Demo data · runs offline", "Demo data · AI run offline")
    p = out / f
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
print("exported", len(routes), "pages")
