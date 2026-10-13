# Paper Atlas scoped interface review

Reviewed on 2026-10-13 using the current Web Interface Guidelines from https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md. Visual lead: frontend-design. Scope: app.py, predicta/ui.py, static/paper-atlas.css, static/turbine.html, .streamlit/config.toml.

- app.py:122 — PASS: semantic overview heading; truthful median, engine counts and model-derived charts; scientific caveats retained beside outputs. Detailed tables/schema/methods moved to expandable sections.
- predicta/ui.py:22 — PASS: skip-to-analysis link; dynamic source/release values escaped; trusted local illustration only.
- static/paper-atlas.css:1 — PASS: bundled licensed fonts, font-display swap, approved paper/ink/cobalt palette, numeric alignment and visible focus.
- static/paper-atlas.css:45 — PASS within tested scope: responsive content and scrollable seven-tab strip; no document horizontal overflow at 375x812. Reduced-motion CSS disables entrance/transitions.
- static/turbine.html:6 — PASS: descriptive canvas/SVG alternatives, named native buttons, keyboard view controls and live view status. Mobile controls are at least 40px tall; dragging has button/keyboard alternatives.
- static/turbine.html:35 — PASS: controllable rotation, interruptible explode/assemble, no autoplay beyond the 1.2s entrance, reduced-motion alternative, offscreen/hidden pause, DPR cap 1.5, context-loss fallback/recovery and resource cleanup.
- .streamlit/config.toml:11 — PASS: local static asset serving enabled. An older local server initially returned HTML for font URLs; final isolated server on port 8555 serves and loads all three WOFF files.

Bounds: this is a scoped source/rendered review, not full WCAG certification. Native Streamlit tabs do not persist selection to the URL; no router/framework migration is included. Streamlit's existing width arguments and components.v1.html produce nonfatal deprecation warnings; the release baseline still supports them. The turbine is a schematic illustration, never equipment geometry, measured telemetry or a health visualization.

Rendered local evidence: paper-atlas-local-final/report.json (27/27); paper-atlas-local-final/motion-report.json (11/11). Desktop/mobile images and actual downloaded CSVs are retained alongside reports. Initial diagnostic failures remain in paper-atlas-local/ and are superseded by the final run.

Final public evidence: paper-atlas-live-final/report.json (27/27) and paper-atlas-live-final/motion-report.json (11/11). All three local font faces loaded on Cloud. The observed stale CSV resource during app reruns was addressed with native on_click="ignore" downloads; the final run has no application console errors. Cloud-wrapper heap/user-details/app-open telemetry errors remain recorded separately, with media errors still treated as application failures. Modified source files use consistent LF line endings for publication.
