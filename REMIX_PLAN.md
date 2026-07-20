# REMIX PLAN — assisted-novel-forge

## Thesis
Compose 10 middling fiction skills into one assisted/autonomous novel forge: shared project pack, continuity bridge, and verify-gate so marketplace phase skills stop false-doing manuscripts.

## Members (buffs)
| Skill | Priority | Why |
|---|---|---|
| `danjdewhurst/story-skills@chapter-writing` | **heavy** | Chapter prose is where false-done hides; needs verify + evals + handoff I/O. |
| `haowjy/creative-writing-skills@story-review` | **heavy** | Critique without independent checks rubber-stamps drafts. |
| `4444j99/a-i--skills@creative-writing-craft` | **medium** | Craft pass must read pack + write revision_targets.json. |
| `haowjy/creative-writing-skills@story-architecture` | **medium** | Map story-planning resources into pack architecture.md. |
| `yangsonhung/awesome-agent-skills@novel-writer` | **medium** | EN novel-writer as alternate planner; demote overlap with novel-creator via router. |
| `danjdewhurst/story-skills@plot-structure` | **medium** | Add schema export into handoff-pack; light verify for beat coverage. |
| `danjdewhurst/story-skills@worldbuilding` | **medium** | Export world canon files the chapter skill already expects. |
| `haowjy/creative-writing-skills@writing-principles` | **light** | Already resource-rich; add non-triggers + pack voice_contract.md writer. |
| `mave99a/novel-skill@novel-creator` | **heavy** | Full-novel path must emit pack + refuse done without verify-gate. |
| `greyhaven-ai/claude-code-config@creative-writing` | **light** | Assisted coach only; install UX + non-triggers + pack hook. |

## Subskills
- **handoff-pack** — Materialize a fiction project pack (brief.json, bible.md, world/, plot/, chapters/, continuity/ledger.json) with schema validate so phase skills share one filesystem contract.
- **verify-gate** — Independent false-done gate: required artifacts exist, claims coverage, min word counts, continuity ledger dirty=false, AI-sermon heuristics optional — scripts decide PASS/FAIL, not chat self-grade.
- **continuity-bridge** — Diff and merge continuity ledgers across world/plot/chapter/review stages; block superskill advance when unresolved contradictions remain.
- **assist-mode-router** — Route autonomous vs assisted creative writing: gate AskUserQuestion, default lengths, and which member skill owns novel planning (novel-creator vs novel-writer) without Storybook/user-story misfires.

## Superskill phases
- 0. intake + mode (autonomous|assisted) + non-trigger guard (not Storybook UI, not agile user-stories, not scientific manuscripts)
- 1. writing-principles — craft constraints / voice contract
- 2. worldbuilding — canon places/rules/factions
- 3. plot-structure — arc beats + stakes ladder
- 4. story-architecture (story-planning) — chapter/scene architecture
- 5. novel-creator OR novel-writer — full-novel plan (assisted asks; autonomous generates)
- 6. chapter-writing — outline-then-prose per chapter
- 7. creative-writing-craft — prose craft pass
- 8. story-review — critique + revision targets
- 9. greyhaven creative-writing — optional assisted coach pass
- 10. verify-gate + metric rollup — refuse done until pass

## Round map
- rounds 1–3: `buff` → `danjdewhurst/story-skills@chapter-writing`
- rounds 4–6: `buff` → `haowjy/creative-writing-skills@story-review`
- rounds 7–9: `buff` → `4444j99/a-i--skills@creative-writing-craft`
- rounds 10–12: `buff` → `haowjy/creative-writing-skills@story-architecture`
- rounds 13–15: `buff` → `yangsonhung/awesome-agent-skills@novel-writer`
- rounds 16–18: `buff` → `danjdewhurst/story-skills@plot-structure`
- rounds 19–21: `buff` → `danjdewhurst/story-skills@worldbuilding`
- rounds 22–24: `buff` → `haowjy/creative-writing-skills@writing-principles`
- rounds 25–27: `buff` → `mave99a/novel-skill@novel-creator`
- rounds 28–30: `buff` → `greyhaven-ai/claude-code-config@creative-writing`
- rounds 31–34: `subskill` → `handoff-pack`
- rounds 35–38: `subskill` → `verify-gate`
- rounds 39–42: `subskill` → `continuity-bridge`
- rounds 43–46: `subskill` → `assist-mode-router`
- rounds 47–50: `superskill` → `assisted-novel-forge`

## Non-triggers
- Storybook / React component "stories"
- Agile user stories / acceptance criteria
- Scientific manuscript review
- Pure marketing copy without fiction brief
