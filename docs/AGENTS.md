# AGENTS.md for `docs/`

Read the [root `AGENTS.md`](../AGENTS.md) first. This file adds how to write the documents in this folder. `PVSURPLUS.md` is the user documentation of the PV blueprint: change it only for a change that users see.

## General

- English, short, concrete. Update the document that exists; do not add a new one for what fits into an old one.
- A statement that the code does not do something needs the lines you read and the whole path of the data (read, store, show), not only a search for a name. Say which decision does not use a value, not that the code "does not read" it.
- A count or a share in a document (number of risks, tests, files) names what was counted and how; recount it when you change the document. Do not count boilerplate that every file contains.
- Mark where a statement comes from: `[Code]` (read from the source, with file and line), `[Docs]` (official or project documentation) or `[Inference]` (derived, not stated by the author). Nothing in these documents was checked on a real charger unless it says so.
- Do not renumber sections of `architecture/arc42-ha-goecharger-api2.md`; other documents refer to them.

## `architecture/arc42-ha-goecharger-api2.md`

- Diagrams are Mermaid. Put labels with brackets, commas or colons in quotes. Open the page after a change; a broken diagram shows as an error, not as a build failure (`python tests/tools/build_site.py <dir> --docs docs`).
- Chapter 9 lists the decisions and chapter 11 points to the risks; both only link, the content is in `adr/` and `risks/`.

## `architecture/adr/`: decisions

- One file per decision, `NNNN-short-title.md`, the next free number. Copy [`architecture/adr/_template.md`](architecture/adr/_template.md): Status, Context and reasoning, Decision, Consequences, Origin. Its comment lists the rules; delete it when done.
- A decision that is replaced stays: set its status to `Superseded by ADR-NNNN`. Add the entry to the table in `adr/README.md` and in chapter 9 of the arc42 document.
- Write who decided and when only if you know it. A decision rebuilt from code is marked `[Inference]` and "reconstructed".

## `architecture/risks/`: risks

- One file per risk, `RNNN-short-title.md`, **three-digit id** (`R031`, not `R31`), the number after the highest in the register. Copy [`architecture/risks/_template.md`](architecture/risks/_template.md); its comment explains the front matter and the rules, delete it when done.
- The file starts with a front matter block. Copy a neighbouring file and set: `id`, `date`, `category` (`ARCH`, `SEC`, `INT`, `QA`, `DOC`, `MAINT`), `probability` and `impact` (1 to 5), `residual_probability` and `residual_impact`, `strategy` (`mitigate`, `accept`, `avoid`, `transfer`), `status` (`open`, `fixed`, `settled`, `superseded`, `note`), `owner` (empty until the maintainer names one), `review`.
- Write the description as "If cause, then event, which leads to impact", then the finding in detail with its evidence and the countermeasure.
- **Run `python tests/tools/build_risk_register.py` after every change.** It writes the assessment table, the status line, the heat maps, the overview and the links for references like `R015`. Never edit the blocks between `<!-- risk:... -->` markers by hand. CI runs it with `--check`.
- Probability, impact and strategy are assessments. Do not present them as measured.
- A fixed risk is not deleted: set `status: fixed` and name the change that fixed it. Never change the original assessment of a closed risk; write what was done and which residual risk remains (accepted or not) under "Countermeasure" and "Status and history".
- An open risk may be reassessed when new facts justify it. Add a "Reassessment" entry under "Status and history" with the date, the old and the new values and the reason; never overwrite an assessment silently. Do not inflate a risk: close it and record what remains as a new risk.

## `quality/testkonzept-ha-goecharger-api2.md`: test concept

Update the numbers, the risk coverage table and the list of gaps when you add or change tests. The figures come from a run, not from memory; say which run.
