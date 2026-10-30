# AGENTS.md for `docs/`

Read the [root `AGENTS.md`](../AGENTS.md) first. This file adds how to write the documents in this folder. `PVSURPLUS.md` is the user documentation of the PV blueprint: change it only for a change that users see.

## General

- English, short, concrete. Update the document that exists; do not add a new one for what fits into an old one.
- Mark where a statement comes from: `[Code]` (read from the source, with file and line), `[Docs]` (official or project documentation) or `[Inference]` (derived, not stated by the author). Nothing in these documents was checked on a real charger unless it says so.
- Do not renumber sections of `architecture/arc42-ha-goecharger-api2.md`; other documents refer to them.

## `architecture/arc42-ha-goecharger-api2.md`

- Diagrams are Mermaid. Put labels with brackets, commas or colons in quotes. Open the page after a change; a broken diagram shows as an error, not as a build failure (`python tests/tools/build_site.py <dir> --docs docs`).
- Chapter 9 lists the decisions and chapter 11 points to the risks; both only link, the content is in `adr/` and `risks/`.

## `architecture/adr/`: decisions

- One file per decision, `NNNN-short-title.md`, the next free number. Copy the last one: Status, Context and reasoning, Decision, Consequences, Origin (and Alternatives or Evidence where they exist).
- A decision that is replaced stays: set its status to `Superseded by ADR-NNNN`. Add the entry to the table in `adr/README.md` and in chapter 9 of the arc42 document.
- Write who decided and when only if you know it. A decision rebuilt from code is marked `[Inference]` and "reconstructed".

## `architecture/risks/`: risks

- One file per risk, `RNNN-short-title.md`, **three-digit id** (`R031`, not `R31`), the number after the highest in the register.
- The file starts with a front matter block. Copy a neighbouring file and set: `id`, `date`, `category` (`ARCH`, `SEC`, `INT`, `QA`, `DOC`, `MAINT`), `probability` and `impact` (1 to 5), `residual_probability` and `residual_impact`, `strategy` (`mitigate`, `accept`, `avoid`, `transfer`), `status` (`open`, `fixed`, `settled`, `superseded`, `note`), `owner` (empty until the maintainer names one), `review`.
- Write the description as "If cause, then event, which leads to impact", then the finding in detail with its evidence and the countermeasure.
- **Run `python tests/tools/build_risk_register.py` after every change.** It writes the assessment table, the status line, the heat maps, the overview and the links for references like `R015`. Never edit the blocks between `<!-- risk:... -->` markers by hand. CI runs it with `--check`.
- Probability, impact and strategy are assessments. Do not present them as measured.
- A fixed risk is not deleted: set `status: fixed` and name the change that fixed it.

## `quality/testkonzept-ha-goecharger-api2.md`: test concept

Update the numbers, the risk coverage table and the list of gaps when you add or change tests. The figures come from a run, not from memory; say which run.
