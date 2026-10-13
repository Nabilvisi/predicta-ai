# Codex skill/plugin playbook — PREDICTA AI

This project draws from `docs/CODEX_USAGE_OPTIMIZATION_UPDATED.md`, supplied as the user's intended Codex skill/usage handoff. **That document is not proof that the skills or plugins are installed on the Codex host.** Probe the environment first; do not reinstall automatically.

| Tool/resource in supplied handoff | Use in this project | Requirement / fallback |
|---|---|---|
| RTK / Rust Token Killer | Compress noisy Git, tests, or CLI output *after* confirming Codex integration | Optional; raw logs for genuine errors |
| `AGENTS.md` | Scoped project instructions and token-efficient work | Included at root; do not override global rules |
| `frontend-design` skill | Lead visual hierarchy and charts, adapted to Streamlit | Use **instead of** Taste as lead; fallback `DESIGN.md` |
| `design-taste-frontend` skill | Alternative lead for refined motion and density | Do not activate as a conflicting second lead |
| Awesome DESIGN.md | Design reference and style tokens | An adapted `DESIGN.md` is included; no global brand override |
| `web-design-guidelines` | Accessibility/responsiveness audit of changed UI | If not installed, manual targeted review |
| Microsoft Playwright CLI | Browser navigation, mobile checks, snapshots/screenshots | Use real Streamlit URL `http://localhost:8501` if port 8501 is bound |
| Codex GitHub plugin/MCP (if present) | Authorized repo creation/update, PRs and workflow runs | Alternative: authenticated GitHub CLI; confirm scope before writes |
| ccusage | Optional local token-usage observability | Not a quota augmenter or official quota report |
| Headroom / token-saver hooks | **Do not use by default** | Add only after measured bottleneck and safe overlap audit |
| Python 3.15 `lazy import` | Experimental targeted compatibility work | Keep actual training/serving on 3.12 until verified |

## Discovery first: safe, read-only examples

**Windows PowerShell**

```powershell
codex --version
codex mcp list
rtk --version
playwright-cli --help
gh auth status
python --version
python -m scripts.codex_readiness
```

**macOS / Linux**

```bash
command -v codex rtk playwright-cli gh python || true
codex mcp list
python -m scripts.codex_readiness
```

Commands may be unavailable: a missing tool is not a reason to install everything. Avoid displaying or pasting credential values. `gh auth status` displays account/scope state; don't save authentication details into the repo.

## Browser procedure (Streamlit)
1. Start `streamlit run app.py --server.port 8501 --server.headless true`, after validated model artifacts are available for actual inference.
2. Use Playwright CLI to open `http://localhost:8501` (or actual bound address), then capture a snapshot and screenshot. Consult installed `playwright-cli --help` for exact command options.
3. Test all seven pages, metric/chart loading, upload validation, prediction, RUL confidence/coverage explanations, planner export, desktop/mobile layout and browser errors.
4. On hosted URL, rerun the same smoke tests and retain evidence in a release report. Do not claim browser coverage unless it actually ran.

## Publishing contract
Use the connected GitHub plugin/MCP if discovered and writable, otherwise use `gh`/Git only when signed in and repository destination is confirmed. GitHub and Streamlit Cloud are distinct authentication steps. **Neither an installation handoff nor the presence of a GitHub CLI verifies permission to deploy to Streamlit Cloud.**

Streamlit Community Cloud deployment: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
