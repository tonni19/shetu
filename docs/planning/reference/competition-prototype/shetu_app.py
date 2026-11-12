"""Shetu prototype web app.   python shetu_app.py   ->   http://127.0.0.1:5050

Employer (HR + manager):  /employer   /employer/case/nusrat   /employer/team   /employer/report
Employee (the mother):    /me   /me/map   /me/hold   /me/fit
Nusrat's case shows the real outputs of the AI + rules engines (demo/results.json; POST /run re-runs them offline).
Other HR cases are illustrative demo data (demo/cases.json)."""
import json, subprocess, sys
from pathlib import Path
from flask import Flask, render_template, redirect, render_template_string

ROOT = Path(__file__).parent
app = Flask(__name__, template_folder="templates_shetu", static_folder="static")
app.config["TEMPLATES_AUTO_RELOAD"] = True


def load(name):
    return json.loads((ROOT / "demo" / name).read_text(encoding="utf-8"))


def ctx(**kw):
    return dict(case=load("nusrat.json"), res=load("results.json"), cases=load("cases.json"), **kw)


LANDING = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Shetu prototype</title>{% include "_style.html" %}<style>.land-cards a{width:280px}@media(max-width:640px){.land-cards{flex-direction:column;align-items:stretch}.land-cards a{width:auto}.land h1{font-size:30px!important}}</style></head>
 <body style="background:#BF092F;min-height:100vh;display:grid;place-items:center;color:#fff">
<div class="land" style="text-align:center;padding:30px 18px"><img src="/static/shetu_logo_white.png" style="height:110px">
<h1 style="font-size:42px;margin-top:22px">Keep the people you trained.</h1><p style="color:#F8F4EC;margin-top:8px">Prototype · demo data · runs offline</p>
<div class="land-cards" style="display:flex;gap:16px;justify-content:center;margin-top:30px;flex-wrap:wrap">
<a href="/me" class="card" style="text-align:left;color:var(--ink)"><p class="k" style="color:var(--teal-d)">Employee · phone app</p><h2 style="margin-top:6px">I'm going on leave</h2><p class="sub">Nusrat's app: Map, Hold, Fit</p></a>
<a href="/employer" class="card" style="text-align:left;color:var(--ink)"><p class="k" style="color:var(--teal-d)">Employer</p><h2 style="margin-top:6px">HR and managers</h2><p class="sub">All leaves, case view, team capacity, report</p></a>
<a href="/how" class="card" style="text-align:left;color:var(--ink)"><p class="k" style="color:var(--teal-d)">Technology</p><h2 style="margin-top:6px">How it works</h2><p class="sub">The AI pipeline and a real trace from our test</p></a>
</div></div></body></html>"""


@app.get("/")
def home():
    return render_template_string(LANDING)


@app.get("/how")
def how():
    return render_template("how.html", **ctx(nav="how", title="How it works"))


@app.get("/employer")
def employer():
    return render_template("employer_overview.html", **ctx(nav="overview", title="All leaves"))


@app.get("/employer/case/<cid>")
def employer_case(cid):
    return render_template("employer_case.html", **ctx(nav="case", title="Case"))


@app.get("/employer/team")
def employer_team():
    return render_template("employer_team.html", **ctx(nav="team", title="Team capacity"))


@app.get("/employer/report")
def employer_report():
    return render_template("employer_report.html", **ctx(nav="report", title="Report"))


@app.get("/me")
def me():
    return render_template("me_home.html", **ctx(nav="home", title="Home"))


@app.get("/me/<page>")
def me_page(page):
    return render_template(f"me_{page}.html", **ctx(nav=page, title=page.title()))


# old single-view screens, kept for the deck
@app.get("/<screen>")
def screen(screen):
    return render_template(f"{screen}.html", **ctx(screen=screen))


@app.post("/run")
def run():
    subprocess.run([sys.executable, str(ROOT / "run_demo.py")], cwd=ROOT, check=True)
    return redirect("/employer/case/nusrat")


if __name__ == "__main__":
    app.run(port=5050)
