# Codex Usage Optimization + Frontend Design — Installation Handoff

**For:** OpenAI Codex CLI / Codex IDE, Windows PowerShell first, macOS/Linux supported  
**Goal:** Reduce unnecessary context/token consumption, improve frontend design consistency, and enable token-conscious browser QA without weakening testing or code quality.  
**Prepared:** 2026-10-10

> **Scope:** These tools **do not increase or bypass** Codex 5-hour/weekly allowances. Output compression benchmarks are **not** verified savings on the account quota. The frontend design skills primarily improve **UI quality**, not quota; Playwright CLI can reduce browser tool context compared with heavy MCP workflows. This document is a **handoff**, not proof of installation.

## 1. Start here: minimal setup (recommended)

Install **RTK** and keep a short **`AGENTS.md`**. Use **ccusage** only when you want a usage report. Do not install every listed tool.

### Windows PowerShell

```powershell
# Check Codex first
codex --version

# RTK: use the package manager rather than piping unknown scripts to a shell
winget install rtk-ai.rtk
rtk --version

# Configure specifically for CODEX (not the Claude default)
# FIRST back up existing ~/.codex files; the handoff prompt below does this.
rtk init -g --codex
rtk gain

# Optional: read-only usage report; requires Node/npm
npx ccusage@latest codex daily
```

Restart Codex after configuring RTK. On macOS, substitute `brew install rtk` for the `winget` command. On Linux, use a release binary or the official repository's installation instructions, review them before executing. If RTK is already installed, **do not reinstall**; check its version and integration first.

**What these commands do:** RTK filters repetitive terminal output on supported commands; `rtk gain` reports RTK-specific estimates. `ccusage` reads local Codex session logs for token/cost reporting and **does not itself reduce usage**. Verify that the Codex integration actually activates in your CLI/version; use explicit `rtk ...` commands where automatic rewriting is not active.

## 2. Efficient Codex rules (`AGENTS.md` excerpt)

Add or merge this **short excerpt** into your existing `~/.codex/AGENTS.md` (global) or the project's `AGENTS.md` (project-only). Never overwrite existing instructions or duplicate rules. Keep the global file concise; put task-specific instructions in the repository.

```md
## Token-efficient software engineering
- Inspect only files relevant to the task. Prefer scoped searches and bounded command output; avoid dumping the entire repository or long logs.
- Reuse existing code, packages, patterns, and tests. Avoid speculative features, unnecessary dependencies, and broad refactors.
- Make the smallest correct change, then run focused verification. Escalate to broader tests only when needed.
- Prefer RTK for supported noisy shell commands when installed. Retrieve raw/uncompressed output when exact errors, line numbers, or complete results matter.
- Avoid repeating file reads, large pasted outputs, or lengthy status messages. State findings, changes, tests, and blockers concisely.
- Keep MCP servers and skills to those required for the current job; preserve important context and correctness over token savings.
- For frontend work, read project `DESIGN.md` when present; use one design-direction skill at a time, then audit with web-design-guidelines and verify in Playwright CLI when installed.
```

Codex reads `AGENTS.md` as instructions, so long global instructions can themselves consume context. Never replace Codex's built-in safety/instruction prompt with a minimal custom prompt just to save tokens.

## 3. GitHub resources: name, link, function and installation decision

| # | Tool / GitHub | Function | Decision |
|---|---|---|---|
| 1 | [RTK — Rust Token Killer](https://github.com/rtk-ai/rtk) | Filters/condenses Git, test, build, Docker, search and other command output before the agent reads it. Has `--codex` integration. | **Install first** |
| 2 | [Codex Token Optimizer Skill](https://github.com/HelloWorld668/codex-token-optimizer) | Skill that guides when to apply RTK and Headroom, and how to measure targeted savings. | Optional; complements RTK |
| 3 | [ccusage](https://github.com/ccusage/ccusage) | Reads local Codex/Claude logs and reports token usage and estimated API-equivalent costs. | **Monitor only** |
| 4 | [Headroom](https://github.com/headroomlabs-ai/headroom) | MCP compress/retrieve/stats tools for large context, logs and tool outputs. | Optional for very large outputs |
| 5 | [Codex Token Saver](https://github.com/fumingyang2004/codex-token-saver) | Beta bundle with RTK, local repository search/context engine, dashboard and native hooks. | Alternative to separate tools; evaluate cautiously |
| 6 | [Codex Token Optimizer Kit](https://github.com/Creativebrook/codex-token-optimizer-kit) | Windows-friendly skills, PowerShell search helpers and session handoff templates. | Optional alternative workflow |
| 7 | [Codex Usage Statusline](https://github.com/picoSols/codex-usage-statusline) | Local companion display of context use and 5-hour/7-day rate-limit information where present in logs. | Monitor only; early-stage repo |
| 8 | [codex-usage](https://github.com/qianhaoq/codex-usage) | Simple local Codex token usage and rate-limit reporting. | Alternative to ccusage |
| 9 | [OpenAI Plugins](https://github.com/openai/plugins) | Official Codex plugin examples and curated marketplace structure. **Not a token optimizer.** | Reference when selecting skills |
| 10 | [Codex CLI](https://github.com/openai/codex) | Official Codex software and current implementation/documentation for plugins, CLI, MCP and hooks. | Reference / compatibility check |

**Do not stack** RTK hooks, Token Saver hooks, and other output-rewriting systems without validating their interactions. Large MCP configurations may increase fixed context overhead. Track actual usage across comparable tasks, not only README percentages.

## 4. Optional installation — only after inspecting your environment

### Option A — Codex Token Optimizer Skill

If your Codex build provides the `skill-installer`, use it *inside Codex*:

```text
$skill-installer install https://github.com/HelloWorld668/codex-token-optimizer/tree/main/codex-token-optimizer
```

Otherwise follow that repository's install instructions and confirm the installed skill exists in the active Codex skill directory (`$CODEX_HOME/skills`, typically `~/.codex/skills`). This skill is **instructional**: RTK/Headroom are separate dependencies. Restart or start a new Codex task to load it.

### Option B — Headroom MCP, only for large text workloads

Review [Headroom MCP documentation](https://github.com/headroomlabs-ai/headroom/blob/main/docs/content/docs/mcp.mdx). If you use Python tooling and want the MCP tools:

```bash
# Choose one isolated tool installer supported on your machine
pipx install 'headroom-ai[mcp]'

# Register its stdio MCP server for Codex (after confirming the binary is on PATH)
codex mcp add headroom -- headroom mcp serve
codex mcp list
```

Restart Codex; verify `headroom_compress`, `headroom_retrieve`, and `headroom_stats` appear. If `headroom` is installed in a virtual environment, use its **actual executable path**. MCP tools are on-demand; do **not** assume Headroom automatically compresses every Codex operation. Remove the MCP server if its startup/context cost outweighs benefits. Avoid putting sensitive text into third-party compression flows without reviewing data handling.

### Option C — Local usage reporting (no background service)

```powershell
# Requires Node/npm; Codex usage is experimental in ccusage
npx ccusage@latest codex daily
npx ccusage@latest codex session
```

The local reports may differ from your **official account usage counter**, because they reflect retained logs and estimated costs, not account-wide quota accounting. Do not treat an API-equivalent dollar estimate as a subscription charge.

### Codex plugins vs Claude plugins

Claude's `/plugin marketplace add ...` commands are **not interchangeable** with Codex commands. For eligible Codex CLI versions, the official marketplace flow is `codex plugin marketplace add <repository>` followed by `codex plugin add <plugin>@<marketplace>`—but **only for repositories actually structured as Codex marketplaces**. RTK itself is a CLI utility, not automatically a Codex marketplace plugin. Do not try `codex plugin add rtk` without a real matching marketplace entry.

## 5. Frontend design + browser QA: five requested additions

**Compatibility:** These are intended for **Codex**, not Claude's `/plugin` commands. The Skills CLI uses `-a codex` and `-g` for global installations. Require Node/npm, Git where applicable, and inspect third-party instructions before installation. **Install selectively:** `frontend-design` and Taste Skill overlap in art direction; keep both available if wanted, but apply **one as lead** for a given task.

| Addition / GitHub | Function | What to install |
|---|---|---|
| **Frontend Design** — [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Gives frontend builds intentional visual direction, typography, hierarchy, composition, responsive layout, and non-template aesthetics. | `frontend-design` skill (Codex target) |
| **Taste Skill** — [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Fine-tunes design variance, motion intensity, and visual density; aims for distinctive, polished, animated interfaces. Default v2 is experimental; `gpt-taste` is an optional more opinionated Codex variant. | `design-taste-frontend` skill (choose **one** variant) |
| **Awesome DESIGN.md** — [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | Curated design-reference Markdown files with colors, typography, components, spacing, and responsive rules. **Reference collection, not a plugin.** | Browse and copy **one** suitable `DESIGN.md` to a project's root; adapt to your own brand; do not overwrite existing files. |
| **Web Design Guidelines** — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) | Audits built UI for web UX, accessibility, forms, keyboard focus, interaction, responsiveness and performance; provides actionable code review findings. | `web-design-guidelines` skill (Codex target) |
| **Playwright CLI** — [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | Token-conscious browser interaction, screenshots, snapshots and smoke tests for responsive interfaces; often leaner than always-loaded Playwright MCP schemas. | `@playwright/cli` CLI + agent-layout skill, test on a public URL or local app. |

### Copy-paste setup — Windows PowerShell / macOS / Linux terminals

Run **in a terminal**, not as Codex `/plugin` commands. This block installs three Codex-targeted skills and Playwright CLI; it does **not** automatically select or copy a branded `DESIGN.md`. Run it after reviewing the repositories and confirming Node/npm is available. If a skill is already installed, inspect it before attempting updates.

```powershell
node --version
npm --version

# 1: Visual direction skill (Anthropic source, Codex target)
npx skills add anthropics/skills --skill frontend-design -a codex -g

# 2: Taste Skill for premium layout, motion and density (default v2 experimental)
npx skills add Leonxlnx/taste-skill --skill design-taste-frontend -a codex -g
# ALTERNATIVE (not alongside the default Taste variant):
# npx skills add Leonxlnx/taste-skill --skill gpt-taste -a codex -g

# 3: Web design/accessibility review
npx skills add vercel-labs/agent-skills --skill web-design-guidelines -a codex -g

# 4: Browser QA (Node/npm required)
npm install -g @playwright/cli@latest
playwright-cli --help
# Install cross-agent SKILL.md into ~/.agents/skills; check Codex discovers it.
playwright-cli install --skills=agents -g
```

> **Awesome DESIGN.md setup:** Browse [the available design profiles](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md), select a reference, and copy its `DESIGN.md` to **`<YOUR_PROJECT>/DESIGN.md`** only after checking for an existing design system. It is not appropriate to install one brand's design globally for every unrelated project. If you need the entire reference gallery locally, `git clone --depth 1 https://github.com/VoltAgent/awesome-design-md.git` into a *separate resources directory* (not a folder replacing your project).

### After installation: use the right tool at the right step

1. **Plan visual direction:** Read project requirements and `DESIGN.md` (if present). Use **Frontend Design OR Taste Skill** as the lead design instruction; avoid contradictory instructions from both at once. For scientific dashboards, use purposeful motion/3D without degrading information density or clarity.
2. **Build UI:** Implement complete responsive layouts, typography, state handling and appropriate animations. Preserve performance, reduced-motion preference and keyboard access.
3. **Audit:** Invoke `web-design-guidelines` for specific changed frontend files; fix meaningful accessibility/interaction issues rather than dumping a giant repo-wide audit every time.
4. **Browser QA:** Run `playwright-cli open http://localhost:3000` **only if** your application is actually running there; otherwise use its real local URL. Then run `playwright-cli snapshot` and `playwright-cli screenshot`. Verify navigation, primary flows, layouts and browser errors. If a browser binary is missing, follow CLI instructions to install it; do not bypass the check.
5. **Verify registration:** Restart Codex (or start a fresh task); confirm the three skills are discoverable and `playwright-cli --help` works. Check if `~/.agents/skills/playwright-cli/SKILL.md` (or your project-scoped location) exists. If Codex does not discover it, use its `$skill-installer` or supported skill path rather than guessing configuration changes.

**On quotas:** Design skills may **increase** per-task reasoning and output, because they demand more thorough design work. Use them only during UI tasks. Playwright CLI is designed for efficient browser automation, but **none of these five guarantees a measurable reduction of your Codex account limits**.

### Example prompt for your React / engineering dashboard work

```text
Use Frontend Design as the visual lead (or Taste Skill, but not both as competing design leads).
Read DESIGN.md if present; otherwise create a small project-specific DESIGN.md with visual tokens.
Build a polished, responsive, accessible React/Next.js engineering dashboard with clear charts,
professional typography, restrained but meaningful animations, and optional performant 3D.
After implementation, run Web Design Guidelines on the changed UI files.
Use Playwright CLI to verify desktop/mobile layouts, navigation, and critical user flows.
Keep outputs scoped and concise; preserve tests, correctness, and performance.
```

## 6. Verification checklist

- [ ] Detected OS, shell, Codex version, RTK version, existing Codex hooks/plugins/MCP and existing `AGENTS.md`.
- [ ] Backed up `~/.codex/config.toml`, `~/.codex/AGENTS.md`, and relevant hook settings **before** modifying them.
- [ ] Installed only the minimal selected tools; no other AI agent's settings altered.
- [ ] Confirmed `rtk --version`, `rtk gain`, and Codex integration behavior on a small non-sensitive repository.
- [ ] Confirmed no double execution, broken shell commands, masked failing tests, or duplicate hooks.
- [ ] Confirmed usage reporting is local/read-only and distinguished telemetry estimates from real quota.
- [ ] Recorded exact installed versions, edits, tests, failures and rollback commands.
- [ ] Checked that `frontend-design`, `design-taste-frontend`, and `web-design-guidelines` were installed into Codex-compatible locations, if selected.
- [ ] Verified Playwright CLI help, its agent skill path, and a browser smoke test if a browser is available.
- [ ] Kept `DESIGN.md` project-specific, reviewed reference provenance, and retained any existing design conventions.

## 7. READY-TO-PASTE PROMPT FOR CODEX

Copy the entire block below and attach this `.md` file to your Codex task:

```text
Read the attached CODEX_USAGE_OPTIMIZATION.md and perform a safe, minimal Codex usage optimization setup on my machine.

GOAL: Make my Codex 5-hour usage allowance more efficient during Python/data science, petroleum-engineering dashboards, React/Next.js, 3D, and full-stack development, without sacrificing correctness, security, or UI/UX quality.

1. Detect my OS/shell, Codex installation and version, current agents instructions, hooks, plugins, MCP servers, available package managers, and existing RTK/usage trackers.
2. Back up each file before changing it. Show what you plan to modify. Never overwrite my existing profile, project rules, or credentials.
3. Default to installing/configuring ONLY RTK for Codex (`rtk init -g --codex`) and merging the concise AGENTS.md excerpt. Use a verified package-manager command for my OS. Do not install duplicate copies.
4. Test the integration on small safe commands and confirm that important test failures remain visible. When rewriting is unsupported, prefer explicit RTK commands over undocumented hooks.
5. Optionally run ccusage in read-only mode to establish a local baseline if Node/npm is present. Do not confuse local usage estimates with official quotas.
6. Install the FIVE frontend additions under Section 5, using the Codex-targeted instructions and only after checking current installations:
   - Anthropic Frontend Design skill (Codex)
   - Taste Skill's default `design-taste-frontend` (do not also install `gpt-taste` unless explicitly requested)
   - Vercel Web Design Guidelines skill (Codex)
   - Microsoft Playwright CLI and its cross-agent skill
   - Awesome DESIGN.md reference library: verify the repo, but DO NOT impose a global brand style or overwrite an existing project DESIGN.md. For a project with no DESIGN.md, suggest a reference and adapt a project-specific file only when relevant.
   Review each skill before install. Do not activate conflicting frontend-design instructions simultaneously.
7. Review, but DO NOT automatically install, Headroom, Codex Token Optimizer Skill, Codex Token Saver, or other potentially overlapping context-compression systems. Recommend them only if a measurable bottleneck warrants them.
8. Keep MCP and skill registrations lean. Use design skills for UI work, Web Design Guidelines for focused auditing, and Playwright CLI for tested browser QA. Avoid unnecessary dependencies; never disable Codex safety checks or weaken tests to reduce tokens.
9. Provide a final concise report: installed versions, paths/config edits, confirmation of the five frontend resources (installed / referenced / skipped), browser smoke-test results, usage measurement method, limitations, and rollback steps.

Proceed with ordinary local setup actions after inspection. Ask before any unexpected elevated-permission, remote-script, credential, deletion, or invasive system change.
```

## Sources / current references

- [RTK installation and Codex mode](https://github.com/rtk-ai/rtk)
- [Official Codex plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Official OpenAI guidance on compact skills/instructions](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
- [ccusage Codex log support](https://github.com/ccusage/ccusage/blob/main/docs/guide/codex/index.md)
- [Headroom MCP reference](https://github.com/headroomlabs-ai/headroom/blob/main/docs/content/docs/mcp.mdx)
- [Anthropic Frontend Design skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design)
- [Taste Skill README and variant names](https://github.com/Leonxlnx/taste-skill)
- [Awesome DESIGN.md source collection](https://github.com/VoltAgent/awesome-design-md)
- [Vercel Web Design Guidelines skill](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines)
- [Microsoft Playwright CLI](https://github.com/microsoft/playwright-cli)
- [Playwright CLI agent skill installation](https://github.com/microsoft/playwright.dev/blob/main/agent-cli/skills.mdx)

**Bottom line:** Start with **RTK + concise `AGENTS.md`** for token control, and use the **five added resources** for frontend direction, style references, audits and browser QA. Run **ccusage** for observability. Add Headroom only if you find a real context bottleneck. Differentiate **design quality** gains from **token** savings.
