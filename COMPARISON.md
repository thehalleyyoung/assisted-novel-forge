# Comparison vs marketplace members

| Area | Typical incumbent | assisted-novel-forge |
|---|---|---|
| Scope | Single phase (outline OR chapter OR craft) | End-to-end assisted/autonomous novel pipeline |
| Handoff | Implicit chat memory | Filesystem handoff-pack with schema validate |
| Done gate | Chat self-grade | verify_gate.py scripts + evals |
| Continuity | Ad-hoc | continuity_bridge.py ledger merge |
| Wrong-sense | Over-triggers on Storybook/user-stories | assist_mode_router ABSTAIN |
| Modes | One style | assisted (AskUser) vs autonomous (checkpointed) |

| E2E smoke | none | run_pipeline_smoke + evals |
| Wrong-sense guard | rare | assist_mode_router |

| Band filter | middling 80–8k | **all installs** (25–8200+) |
| Members | 10 | 41 upgraded dirs |

| Anti-AI tells | ad hoc craft | 10-skill ensemble + lexicon gate |

| Composition | Linear skill list | Pressure-driven compose + adversarial pairs + voice coupling |
| Done metric | Member self-grade | compound_pressure + verify_gate |
| Anti-AI tells | Run all 10 | detect≠scrub pair chosen by tell family |
