"""Keeps the risk documents in docs/architecture/risks consistent with their front matter.

Every risk file (R001-....md) starts with a small front matter block (id, date, category, probability, impact,
residual values, strategy, status, owner, review). This script generates everything that is derived from it:
- the assessment table and the status line inside each risk file (between the marker comments)
- the heat maps and the overview table in the README of the folder (between the marker comments)

Usage: python tests/tools/build_risk_register.py [docs/architecture/risks] [--check]
Without --check the files are rewritten. With --check nothing is written and the exit code is 1 when a file
is out of date (used in CI). The German folder and its English subfolder `en/` are handled the same way.
build_site.py imports heatmap_html() and front_matter_table() from here for the web page.
"""
import html
import re
import sys
from pathlib import Path

CATEGORIES = {
    "ARCH": ("Technologie / Architektur", "Technology / architecture"),
    "SEC": ("Security & Datenschutz", "Security & privacy"),
    "INT": ("Integration / Drittanbieter", "Integration / third party"),
    "QA": ("Qualität / Test", "Quality / testing"),
    "DOC": ("Dokumentation", "Documentation"),
    "MAINT": ("Wartbarkeit", "Maintainability"),
}
STRATEGIES = {"mitigate": ("Mindern", "Mitigate"), "accept": ("Akzeptieren", "Accept"),
              "avoid": ("Vermeiden", "Avoid"), "transfer": ("Verlagern", "Transfer")}
STATUS = {
    "open": ("Offen", "Open"), "fixed": ("Geschlossen (behoben)", "Closed (fixed)"),
    "settled": ("Geschlossen (geklärt, kein Fehler)", "Closed (settled, not a defect)"),
    "superseded": ("Geschlossen (überholt)", "Closed (superseded)"), "note": ("Akzeptiert (Hinweis)", "Accepted (note)"),
}
CLOSED = {"fixed", "settled", "superseded"}
BAND = {"low": ("niedrig", "low", "🟩"), "medium": ("mittel", "medium", "🟨"), "high": ("hoch", "high", "🟥")}
LABELS = {
    "de": dict(field="Feld", value="Wert", id="ID", date="Datum erfasst", cat="Kategorie", status="Status", owner="Risk Owner",
               review="Nächste Prüfung", owner_none="nicht benannt (vom Maintainer festzulegen)", review_v={"release": "bei jedem neuen Release"},
               w="Eintrittswahrscheinlichkeit (W)", a="Schadensauswirkung (A)", score="Score (W × A)", resid="Restrisiko nach der Gegenmaßnahme",
               assess="Bewertung", strategy="Risikostrategie",
               scale="Skala: W 1 (sehr unwahrscheinlich) bis 5 (sehr wahrscheinlich), A 1 (gering) bis 5 (schwerwiegend); Score 1 bis 5 niedrig, 6 bis 12 mittel, ab 15 hoch.",
               title="Titel", cat_h="Kategorie", strat_h="Strategie", stat_h="Status"),
    "en": dict(field="Field", value="Value", id="ID", date="Date recorded", cat="Category", status="Status", owner="Risk owner",
               review="Next review", owner_none="not named (to be set by the maintainer)", review_v={"release": "with every new release"},
               w="Probability (W)", a="Impact (A)", score="Score (W × A)", resid="Residual risk after the countermeasure",
               assess="Assessment", strategy="Risk strategy",
               scale="Scale: W 1 (very unlikely) to 5 (very likely), A 1 (low) to 5 (severe); score 1 to 5 low, 6 to 12 medium, 15 and above high.",
               title="Title", cat_h="Category", strat_h="Strategy", stat_h="Status"),
}
MARKERS = ("assessment", "status", "heatmap-current", "heatmap-residual", "table")


def band(score):
    return "low" if score <= 5 else "medium" if score <= 12 else "high"


def parse_front_matter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def load(folder):
    risks = []
    for f in sorted(Path(folder).glob("R[0-9][0-9][0-9]-*.md")):
        fm, body = parse_front_matter(f.read_text())
        if fm is None:
            raise SystemExit(f"{f}: front matter missing")
        for k in ("id", "date", "category", "probability", "impact", "residual_probability", "residual_impact", "strategy", "status"):
            if k not in fm:
                raise SystemExit(f"{f}: front matter key '{k}' missing")
        fm = dict(fm, w=int(fm["probability"]), a=int(fm["impact"]), rw=int(fm["residual_probability"]),
                  ra=int(fm["residual_impact"]), file=f.name, n=int(fm["id"][1:]), title=body.splitlines()[0].split(":", 1)[1].strip())
        risks.append(fm)
    return sorted(risks, key=lambda r: r["n"])


def lang_of(folder):
    return "en" if Path(folder).name == "en" else "de"


def idx(lang):
    return 1 if lang == "en" else 0


def front_matter_table(fm, lang):
    t = LABELS[lang]
    owner = fm.get("owner") or t["owner_none"]
    review = t["review_v"].get(fm.get("review", "release"), fm.get("review", ""))
    return (f"| {t['field']} | {t['value']} |\n|---|---|\n| {t['id']} | {fm['id']} |\n| {t['date']} | {fm['date']} |\n"
            f"| {t['cat']} | {CATEGORIES[fm['category']][idx(lang)]} |\n| {t['status']} | {STATUS[fm['status']][idx(lang)]} |\n"
            f"| {t['owner']} | {owner} |\n| {t['review']} | {review} |\n")


def assessment_block(r, lang):
    t = LABELS[lang]
    s, rs = r["w"] * r["a"], r["rw"] * r["ra"]
    return (f"| | W | A | {t['score']} | |\n|---|---|---|---|---|\n"
            f"| {t['assess']} | {r['w']} | {r['a']} | {s} | {BAND[band(s)][idx(lang)]} |\n"
            f"| {t['resid']} | {r['rw']} | {r['ra']} | {rs} | {BAND[band(rs)][idx(lang)]} |\n\n"
            f"{t['strategy']}: **{STRATEGIES[r['strategy']][idx(lang)]}**. {t['scale']}")


def status_block(r, lang):
    return STATUS[r["status"]][idx(lang)]


def cells(risks, residual):
    grid = {}
    for r in risks:
        if r["status"] in CLOSED:
            continue
        w, a = (r["rw"], r["ra"]) if residual else (r["w"], r["a"])
        grid.setdefault((w, a), []).append(r)
    return grid


def heatmap_md(risks, residual):
    grid = cells(risks, residual)
    rows = ["| W \\ A | 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|---|"]
    for w in range(5, 0, -1):
        line = f"| **{w}** |"
        for a in range(1, 6):
            mark = BAND[band(w * a)][2]
            ids = ", ".join(f"[{r['id']}]({r['file']})" for r in grid.get((w, a), []))
            line += f" {mark} {ids} |"
        rows.append(line)
    return "\n".join(rows)


def heatmap_html(risks, residual, link=lambda r: f"#{r['id'].lower()}", lang="de"):
    """Colour grid for the web page; link(r) gives the target of an id."""
    grid = cells(risks, residual)
    out = ['<table class="heat"><thead><tr><th>W \\ A</th>' + "".join(f"<th>{a}</th>" for a in range(1, 6)) + "</tr></thead><tbody>"]
    for w in range(5, 0, -1):
        out.append(f"<tr><th>{w}</th>")
        for a in range(1, 6):
            score = w * a
            ids = " ".join(f'<a href="{html.escape(link(r))}" title="{html.escape(r["title"])}">{r["id"]}</a>' for r in grid.get((w, a), []))
            out.append(f'<td class="{band(score)}" title="W {w} × A {a} = {score}">{ids}</td>')
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def table_block(risks, lang):
    t = LABELS[lang]
    rows = [f"| ID | {t['title']} | {t['cat_h']} | W | A | Score | {t['strat_h']} | {t['stat_h']} |", "|---|---|---|---|---|---|---|---|"]
    for r in risks:
        s = r["w"] * r["a"]
        rows.append(f"| [{r['id']}]({r['file']}) | {r['title']} | {CATEGORIES[r['category']][idx(lang)]} | {r['w']} | {r['a']} | "
                    f"{s} ({BAND[band(s)][idx(lang)]}) | {STRATEGIES[r['strategy']][idx(lang)]} | {STATUS[r['status']][idx(lang)]} |")
    return "\n".join(rows)


def replace_block(text, name, content, where):
    pattern = re.compile(rf"(<!-- risk:{name} -->\n).*?(\n<!-- /risk:{name} -->)", re.S)
    if not pattern.search(text):
        raise SystemExit(f"{where}: marker 'risk:{name}' missing")
    return pattern.sub(lambda m: m.group(1) + content + m.group(2), text)


def has_block(text, name):
    return f"<!-- risk:{name} -->" in text


def process(folder, write):
    """Returns the list of files that are (or were) out of date."""
    lang = lang_of(folder)
    risks = load(folder)
    stale = []
    for r in risks:
        path = Path(folder) / r["file"]
        text = path.read_text()
        new = replace_block(text, "assessment", assessment_block(r, lang), path)
        new = replace_block(new, "status", status_block(r, lang), path)
        if new != text:
            stale.append(path)
            if write:
                path.write_text(new)
    readme = Path(folder) / "README.md"
    text = readme.read_text()
    new = replace_block(text, "heatmap-current", heatmap_md(risks, False), readme)
    new = replace_block(new, "heatmap-residual", heatmap_md(risks, True), readme)
    new = replace_block(new, "table", table_block(risks, lang), readme)
    if new != text:
        stale.append(readme)
        if write:
            readme.write_text(new)
    return stale


def main(argv):
    check = "--check" in argv
    args = [a for a in argv if not a.startswith("--")]
    base = Path(args[0]) if args else Path("docs/architecture/risks")
    if not base.is_dir():
        print(f"{base} does not exist, nothing to do")
        return 0
    stale = []
    for folder in (base, base / "en"):
        if folder.is_dir():
            stale += process(folder, write=not check)
    if stale:
        print(("out of date: " if check else "updated: ") + ", ".join(str(p) for p in stale))
        return 1 if check else 0
    print("risk documents are up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
