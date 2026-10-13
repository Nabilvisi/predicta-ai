# Start here — PREDICTA AI for Codex

This is the **v3.2 Codex execution handoff**, built from the existing v3.1 Streamlit deployment kit. It contains the project files, original ML notebook, CI and training scripts, plus Codex-specific instructions. There is **no trained NASA model or live URL** in this ZIP.

## Fast path
1. Extract this ZIP to a new working folder and open **that folder** in your Codex CLI/IDE workspace.
2. Make sure Codex can read `AGENTS.md` and `DESIGN.md` from the repository root. The project's original `.ipynb` is in `notebooks/`.
3. Paste the contents of `CODEX_DEPLOYMENT_MASTER_PROMPT.md` into Codex, or tell Codex:

   **“Read `AGENTS.md`, `DESIGN.md`, and `CODEX_DEPLOYMENT_MASTER_PROMPT.md`; execute the PREDICTA AI release workflow with my installed skills/plugins. Verify available tools before using them; train on real NASA FD001 data, test the Streamlit app, then publish to my authorized GitHub and Streamlit Cloud accounts if available. Report blockers without inventing results or links.”**

4. Check tool availability locally with `python -m scripts.codex_readiness` (observational; no installs).
5. Accept deployment as complete only after strict trained-model checks, a confirmed GitHub commit and a working public Streamlit URL.

## Skills by job
- **RTK + project `AGENTS.md`**: concise terminal workflow; no quota bypass.
- **Frontend Design OR Taste Skill**: professional engineering dashboard visual direction.
- **Awesome DESIGN.md**: the project-specific reference already included as `DESIGN.md`.
- **Web Design Guidelines**: focused post-implementation UI and accessibility review.
- **Playwright CLI**: browser smoke tests on Streamlit port **8501**, not React port 3000.
- **Connected GitHub plugin / `gh`**: only for account-authorized repository and Actions tasks.
- **ccusage**: optional local usage estimates. Headroom and overlapping hook systems are not default.

See `docs/CODEX_SKILL_PLUGIN_PLAYBOOK.md` for verified-versus-assumed tool distinctions.
