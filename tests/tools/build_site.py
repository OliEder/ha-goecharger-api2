"""Builds the static site for GitHub Pages from the latest results.

Usage: python build_site.py <site dir> --report <dir with testreport.md and html-all> \
           --testcases <testcases.md> [--regression <summary.md>] [--docs <dir with arc42 and test concept>]
Needs the package `markdown`. Every input is optional except the site directory; a missing part is left out.
"""
import argparse
import html
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import markdown

CSS = """
:root{--bg:#fff;--fg:#1f2328;--muted:#59636e;--line:#d1d9e0;--head:#f6f8fa;--link:#0969da}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--muted:#9198a1;--line:#3d444d;--head:#151b23;--link:#4493f8}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif}
main{max-width:60rem;margin:0 auto;padding:1rem 16px 4rem}
nav{border-bottom:1px solid var(--line);background:var(--head)}
nav div{max-width:60rem;margin:0 auto;padding:.7rem 16px;display:flex;gap:1.2rem;flex-wrap:wrap}
a{color:var(--link)}h1,h2,h3{line-height:1.25}
table{border-collapse:collapse;display:block;overflow-x:auto;max-width:100%}
th,td{border:1px solid var(--line);padding:.3rem .6rem;text-align:left;vertical-align:top}
th{background:var(--head)}code{background:var(--head);padding:.1rem .3rem;border-radius:4px}
footer{color:var(--muted);font-size:.9rem;margin-top:3rem}
"""
PAGES = [("index.html", "Übersicht"), ("testreport.html", "Testbericht"), ("testcases.html", "Testfälle"),
         ("testkonzept.html", "Testkonzept"), ("arc42.html", "Architektur (arc42)"),
         ("adr.html", "Entscheidungen (ADR)"),
         ("testkonzept-en.html", "Test concept (EN)"), ("arc42-en.html", "Architecture (arc42, EN)"),
         ("adr-en.html", "Decisions (ADR, EN)"), ("coverage/index.html", "Abdeckung im Detail")]
# the diagrams of the arc42 document are Mermaid; the library is loaded from a CDN with a fixed version
MERMAID = ('<script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.4.0/dist/mermaid.esm.min.mjs";'
           'mermaid.initialize({startOnLoad:true,theme:matchMedia("(prefers-color-scheme: dark)").matches?"dark":"default"});</script>')
# page -> (title, file relative to the docs directory); the documents are looked up by their folder
# (architecture, quality) and, for older layouts, directly in the docs directory
DOC_FILES = {"arc42.html": ("Architektur (arc42)", "architecture/arc42-ha-goecharger-api2.md"),
             "testkonzept.html": ("Testkonzept", "quality/testkonzept-ha-goecharger-api2.md"),
             "arc42-en.html": ("Architecture (arc42, English)", "architecture/arc42-ha-goecharger-api2.en.md"),
             "testkonzept-en.html": ("Test concept (English)", "quality/testkonzept-ha-goecharger-api2.en.md")}
# the architecture decision records: one page per language, built from the files in docs/adr
ADR_PAGES = {"adr.html": ("Architekturentscheidungen (ADR)", "adr"), "adr-en.html": ("Architecture decisions (ADR, English)", "adr/en")}
LINK_TARGETS = {"arc42-ha-goecharger-api2.md": "arc42.html", "arc42-ha-goecharger-api2.en.md": "arc42-en.html",
                "testkonzept-ha-goecharger-api2.md": "testkonzept.html", "testkonzept-ha-goecharger-api2.en.md": "testkonzept-en.html"}


def find_doc(docs, rel):
    root = Path(docs)
    for candidate in (root / rel, root / Path(rel).name):
        if candidate.exists():
            return candidate
    return None


def adr_files(docs, folder):
    directory = Path(docs) / folder
    if not directory.is_dir():
        return []
    return sorted(f for f in directory.glob("*.md") if f.name != "README.md")


def adr_anchors(docs):
    """File name -> heading id on the ADR page (the first line of each file is its heading)."""
    from markdown.extensions.toc import slugify
    anchors = {}
    for folder in ("adr", "adr/en"):
        for f in adr_files(docs, folder):
            anchors[(folder.endswith("en"), f.name)] = slugify(f.read_text().splitlines()[0].lstrip("# ").strip(), "-")
    return anchors


def rewrite_links(md_text, page, anchors):
    """Links between the Markdown documents point to the generated pages."""
    english_adr = page == "adr-en.html"

    def fix(m):
        path, name, frag = m.group(1), m.group(2), m.group(3) or ""
        if name in LINK_TARGETS:
            return f"]({LINK_TARGETS[name]}{frag})"
        is_en = "adr/en/" in path or english_adr
        if name == "README.md":
            return f"](adr-en.html{frag})" if is_en else f"](adr.html{frag})"
        key = (is_en, name)
        if key in anchors:
            return f"](adr{'-en' if is_en else ''}.html#{anchors[key]})"
        return m.group(0)
    return re.sub(r"\]\(([^)#]*?)([A-Za-z0-9_.-]+\.md)(#[^)]*)?\)", fix, md_text)


def render(site, name, title, body_md, available, toc_levels=False):
    english = name.endswith("-en.html")
    nav = "".join(f'<a href="{href}">{label}</a>' for href, label in PAGES if href in available)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])
    body = md.convert(body_md)
    mermaid = '<code class="language-mermaid">' in body
    if mermaid:
        body = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', r'<pre class="mermaid">\1</pre>', body, flags=re.S)
    if toc_levels:
        entries = [t for top in md.toc_tokens for t in (top["children"] if top["level"] == 1 else [top])]
        items = "".join(f'<li><a href="#{t["id"]}">{html.escape(t["name"])}</a></li>' for t in entries)
        body = body.replace("</h1>", f"</h1><details><summary>{"Contents" if english else "Inhalt"}</summary><ol>{items}</ol></details>", 1)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if english:
        footer = (f"Generated {stamp}. The tests and documents were written with AI assistance (Claude Code) and reviewed by a human. "
                  'Source: <a href="https://github.com/marq24/ha-goecharger-api2">marq24/ha-goecharger-api2</a> (tests/, docs/quality).')
    else:
        footer = (f"Erzeugt am {stamp}. Die Tests und Dokumente wurden mit KI-Unterstützung (Claude Code) erstellt und von einem Menschen geprüft. "
                  'Quelle: <a href="https://github.com/marq24/ha-goecharger-api2">marq24/ha-goecharger-api2</a> (tests/, docs/quality).')
    (site / name).write_text(
        f'<!doctype html><html lang="{"en" if english else "de"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body><nav><div>{nav}</div></nav>"
        f"<main>{body}{MERMAID if mermaid else ''}<footer>{footer}</footer></main></body></html>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--report")
    ap.add_argument("--testcases")
    ap.add_argument("--regression")
    ap.add_argument("--docs")
    a = ap.parse_args()
    site = Path(a.site)
    site.mkdir(parents=True, exist_ok=True)
    pages = {}
    if a.report and (Path(a.report) / "testreport.md").exists():
        pages["testreport.html"] = ("Testbericht", (Path(a.report) / "testreport.md").read_text())
        if (Path(a.report) / "html-all").exists():
            shutil.copytree(Path(a.report) / "html-all", site / "coverage", dirs_exist_ok=True)
    if a.testcases and Path(a.testcases).exists():
        pages["testcases.html"] = ("Testfälle", Path(a.testcases).read_text())
    anchors = adr_anchors(a.docs) if a.docs else {}
    for name, (title, filename) in DOC_FILES.items():
        found = find_doc(a.docs, filename) if a.docs else None
        if found is not None:
            pages[name] = (title, rewrite_links(found.read_text(), name, anchors), True)
    for name, (title, folder) in ADR_PAGES.items():
        files = adr_files(a.docs, folder) if a.docs else []
        index = (Path(a.docs) / folder / "README.md") if a.docs else None
        if files and index is not None and index.exists():
            parts = [index.read_text()] + [f.read_text() for f in files]
            pages[name] = (title, rewrite_links("\n\n---\n\n".join(parts), name, anchors))
    index = ["# Regressionstests für ha-goecharger-api2", "",
             "Tests und Berichte zur Home-Assistant-Integration [marq24/ha-goecharger-api2](https://github.com/marq24/ha-goecharger-api2) "
             "(go-eCharger). Die Tests liegen im Repository unter `tests/integration`; diese Seite wird aus einem Fork heraus gebaut. Die Tests ändern den Code nicht.", ""]
    if a.regression and Path(a.regression).exists():
        index += ["## Letzter Lauf gegen eine Version des Original-Repos", "", Path(a.regression).read_text().replace("\n## ", "\n### ")
                  .replace("## Regression", "### Regression", 1), ""]
    index += ["## Seiten", "", "- [Testbericht](testreport.html): Zeilen-, Zweig- und Pfadabdeckung, Kritikalität",
              "- [Testfälle](testcases.html): jede Testfunktion in einer Zeile",
              "- [Abdeckung im Detail](coverage/index.html): Zeile für Zeile",
              "- [Testkonzept](testkonzept.html): Ziele, Methoden, Kennzahlen und ihre Grenzen",
              "- [Architektur (arc42)](arc42.html): Aufbau der Integration, Abläufe, Risiken",
              "- [Entscheidungen (ADR)](adr.html): Architekturentscheidungen, je eine mit Begründung und Folgen",
              "- English: [Test concept](testkonzept-en.html), [Architecture (arc42)](arc42-en.html), [Decisions (ADR)](adr-en.html)"]
    available = set(pages) | {"index.html"} | ({"coverage/index.html"} if (site / "coverage").exists() else set())
    for name, (title, body, *toc) in pages.items():
        render(site, name, title, body, available, bool(toc))
    render(site, "index.html", "Regressionstests", "\n".join(index), available)
    (site / ".nojekyll").write_text("")
    print("site written to", site)


main()
