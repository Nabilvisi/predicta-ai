"""Non-mutating, best-effort check for Codex tool availability and source artifacts.

Usage: python -m scripts.codex_readiness
This does NOT prove a skill is loaded by Codex, permissions, or deployment.
"""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
TOOL_NAMES = ("codex", "rtk", "playwright-cli", "gh", "git", "streamlit")
SKILLS = ("frontend-design", "design-taste-frontend", "gpt-taste", "web-design-guidelines", "playwright-cli")

def main() -> int:
    print("PREDICTA AI / Codex read-only readiness audit")
    print(f"Python: {sys.version.split()[0]} (deployment recommended: 3.12)")
    print(f"Repository files: {'PASS' if all((ROOT / name).is_file() for name in ('AGENTS.md','DESIGN.md','app.py','requirements.txt')) else 'INCOMPLETE'}")
    for name in TOOL_NAMES:
        found = shutil.which(name)
        print(f"CLI {name}: {'found' if found else 'not found on PATH'}")
    home = Path.home()
    roots = (home / '.codex' / 'skills', home / '.agents' / 'skills')
    for name in SKILLS:
        locations = [root / name for root in roots if (root / name).exists()]
        print(f"Skill directory {name}: {'present in '+', '.join(str(p) for p in locations) if locations else 'not found in common locations'}")
    print("Note: Codex host registration, MCP connections and authentication must be verified INSIDE Codex; missing paths do not prove absence.")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
