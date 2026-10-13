# PREDICTA AI — Engineering UI Design System

**Product type:** rigorous engineering analysis software, not marketing, a candidate profile, or an interview showcase. Maintain the existing Streamlit implementation for this release.

## Approved revision: Paper Atlas (2026-10-13)

The user approved concept 02 and requested more graphics, interactive 3D motion, and less visible text. This revision supersedes the original dark visual tokens below while retaining the scientific and serving contract. Keep Streamlit and the existing trusted model.

- Warm paper `#F4F2EA`, panel `#FDFCF8`, ink `#17292D`, muted text `#546966`, cobalt `#234FCC`, dividers `#CFD5C9`.
- IBM Plex Sans for controls and analytical content; Instrument Serif for the editorial overview headline. Bundle open-source fonts and licenses.
- Horizontal seven-tab navigation, compact source/model/calibration ribbon, overview split between a short headline and a 3D cutaway illustration, followed by actual charts and numeric alternatives.
- The procedural turbine is explicitly **schematic / illustration**, not observed geometry, telemetry, a digital twin, a health indicator, or a fault reconstruction.
- Motion: one finite entrance; rotation and exploded view respond to controls. Honor reduced motion, pause hidden/offscreen rendering, limit pixel ratio, release WebGL resources, and supply a static SVG fallback. No remote graphics libraries or new application framework.
- Short visible caveats near scientific outputs; full methodology and raw schema in expandable sections. Preserve engine/cycle/source/model identity, cycle units, prediction intervals, and the non-causal sensitivity warning.

## Original identity and visual tokens (superseded palette)
- Brand: PREDICTA AI / Engine Health Intelligence.
- Background `#081421`; sidebar/panels `#13243A`; foreground `#ECF4FF`; teal accent `#4BD5CA`.
- Status colors: green for successful validation, amber for evidence/attention, red for actual errors. Do not present unvalidated model predictions as green/healthy.
- Typography: legible sans serif with tabular numbers in metrics. Preserve contrast and avoid tiny chart labels.
- Layout: side navigation; top context ribbon with data provenance/model state; KPI row; primary charts; supporting engineering tables; expandable methodology/limitations.
- Spacing: balanced cards and consistent panel alignment, no gratuitous decorative borders or animation.

## Information architecture (existing target)
1. Overview — availability and experimental model status; fleet summary and RUL distributions.
2. Sensor Explorer — real sensor time-series, comparisons, distribution and statistical deviation screens.
3. RUL Prediction — selected engine, observation window, predicted RUL with uncertainty and limitations.
4. Maintenance Planner — relative policy-driven ranking, adjustable assumptions, exportable worklist.
5. Sensitivity Lab — one-at-a-time numerical input perturbation (NOT a causal counterfactual).
6. Model Diagnostics — actual measured evaluation metrics, errors, permutation importance and stability caveats.
7. Data Contract — input schema, dataset source/provenance, version and upload requirements.

## Interaction and accessibility
- Display engine ID, cycle, input source, model version and data assumptions near predictions.
- Clear loading/empty/error states. Show model-not-trained state if release artifacts are absent.
- Give every interactive chart a useful label and numeric/table alternative where reasonable.
- Keyboard-focus and responsive width should work on typical mobile/desktop viewports.
- Honor reduced-motion preference in any custom HTML/CSS; avoid infinite nonfunctional 3D effects.
- Chart tooltips must identify sensor channels and unit uncertainty; do not invent physical units.

## Skill usage
`frontend-design` can lead layout/typography, or `design-taste-frontend` can lead motion/density, but never mix contradictory art direction in one pass. Audit with `web-design-guidelines` if installed, then Playwright CLI on Streamlit's actual port. The approved Paper Atlas request authorizes the isolated procedural WebGL illustration; no application framework migration is needed.
