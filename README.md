# UppSkillz

Curated, reviewed U++ and Skylark knowledge for people and AI agents. Each procedure
has one authoritative home here.

## Layout

- `skills/<id>/SKILL.md`: one skill per procedure. Frontmatter has `name` (the directory
  id) and `description`. Deep material goes in `skills/<id>/references/`.
- `ai/rules|skills|info/*.md`: the ecosystem method: how skills are curated and how
  repo-local policy relates to them.
- `HISTORY.md`: provenance for every skill: source path, review verdict, date.

## Policy

- Historical material (`~/Dev/ai-upp/ai/**`) is non-binding until reviewed. Each item
  records its source path, what was changed, and why.
- A skill states its own verification: what was checked against upstream or project
  code, and what rests on recorded project experience.
- Repo-specific policy stays in the repo (`ai/**` in SkylarkManager and CompanySkylark).
  Those repos point here for generic material.

## Checks

- `python3 ai/tools/check_links.py`: every relative Markdown link in the repo must resolve.
  Code spans and fenced blocks are skipped, so code such as `int(x)` is not read as a link.
