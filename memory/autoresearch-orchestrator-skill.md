# autoresearch-orchestrator skill

Created: 2026-04-03

## Installed skill location
- `~/.agents/skills/autoresearch-orchestrator/`

## Packaged skill
- `dist-skills/autoresearch-orchestrator.skill`

## Purpose
Capture the reusable orchestration pattern from `karpathy/autoresearch`:
- fixed-budget experiment loops
- immutable evaluation harness
- narrow editable surface
- keep/discard ledger
- `program.md` style human-written research policy

## Bundled resources
- `SKILL.md`
- `references/autoresearch-patterns.md`
- `scripts/check_autoresearch_setup.py`

## Notes
The original repo shape is valid, but local cache for `~/.cache/autoresearch/{data,tokenizer}` is not present yet, so actual training runs still require `prepare.py` first.
