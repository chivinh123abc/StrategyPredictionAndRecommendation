# LoL Esports & Solo Queue Data Science Assistant Constitution

## Core Principles

### I. Zero-Hardcode & 100% Algorithmic / Data-Driven Execution (NON-NEGOTIABLE)
- AI agents and developers MUST NEVER fabricate statistics, subjective assumptions, or hardcode case-specific `if/else` patches (e.g., for specific champion pairs or teams).
- Every prediction, ban/pick recommendation, tier rating, and matchup evaluation MUST operate strictly through generalizable mathematical and statistical algorithms queried from the normalized SQLite database (`data/database/lol_live_data.db`).

### II. Mandatory GPU-First Model Training
- Every machine learning training pipeline (`--train` in `src/06_machine_learning/` and `src/07_recommender/`) MUST execute using GPU acceleration (`device='cuda'`, `tree_method='hist'` on NVIDIA GeForce RTX 4070 CUDA) combined with multi-threaded execution (`n_jobs=-1`) and SQLite composite indexes (`idx_tp_game_pos_side`, `idx_tp_game_side_pos`).

### III. Real-Time Documentation & State Synchronization (`AI/` & `.specify/`)
- After every code change, algorithm update, model re-training, or infrastructure setup, all governance files in `AI/` (`AI/PROJECT_STATE.md`, `AI/TASKS.md`, `AI/CHANGELOG.md`, `AI/DECISIONS.md`, `AI/ARCHITECTURE.md`, `AI/DATABASE.md`) MUST be updated immediately in the same session to reflect 100% of the actual project state.

### IV. Strict Git Control Protocol
- Never automatically execute `git commit` or `git push`. All version control commits and pushes are strictly controlled by the User and only executed when explicitly commanded.

### V. End-to-End Verification & Isolated `.venv` Execution
- All Python execution, testing, and model packaging MUST run inside the local virtual environment (`.venv\Scripts\python.exe`).
- Verification MUST match the change: code/data/model changes require relevant execution checks; regenerate `.pkl` artifacts when the model itself changes. Documentation-only changes require content/link/format checks, not unrelated retraining or database mutation. Record actual checks before claiming `VERIFIED` or `DONE`.

### VI. Mandatory Knowledge and Output Traceability
- Follow [AI/KNOWLEDGE_RULES.md](../../AI/KNOWLEDGE_RULES.md). The central knowledge register is [docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md](../../docs/TONG_HOP_KIEN_THUC_VA_MO_RONG_BAO_CAO.md).
- Every new or changed method, feature, scientific assumption, evaluation policy, dataset scope, or output MUST update that register in the same change. Record stable ID, MH/UD/MR/NV classification, chapter/page or extension source/self-designed policy, code/module/function, purpose, artifact path and reproduction command, status/evidence and limitations.
- Specifications and plans MUST map knowledge to implementation and outputs; tasks MUST include register updates and verification. Implementations are not documentation-complete while that mapping is absent or stale. Existing read-only commands MUST report gaps without modifying files; checklist review ownership remains unchanged.
- Planned opponent modeling, search and BO5 planning MUST remain explicitly planned until implemented and verified. Five legal Fearless drafts do not establish full-series optimization. Do not fabricate chapter references, artifacts, results or winrate gains.
- Changes with no knowledge/method/function impact MAY record a reasoned no-impact note instead of inventing a new register entry. Do not create routine approval requests or retrain unchanged models to satisfy this principle.
- Project template overrides under `.specify/templates/overrides/` and root agent instructions MUST carry this rule; verify preservation after SpecKit upgrades. Installation manifests are metadata, not the policy location.

### VII. Course-Sized Scope and Explainable Extensions
- Prioritize Chapters1–6 and a small set of necessary, explainable extensions, following [the current scope](../../docs/PHAM_VI_DO_AN_VUA_SUC.md).
- Reuse existing pipelines and methods. Do not automatically add models, frameworks, strategies or research tracks; do not restore removed lookahead/global BO5 search. Keep legacy/contextual and existing draft/Fearless interaction without claiming optimality.
- Preserve historical prototypes/evaluators for provenance rather than treating all of them as mandatory product work. Runtime custom formulas remain extensions when used; do not relabel them as course material.
- Record the reason, course mapping or extension source, implementation, output and evidence for changes. This scope rule does not add routine approval requests for already assigned work.

## Architecture & Scope Constraints

- **Current Deliverable**: Executable Python CLI/notebooks, data/statistical outputs and a course report. Following explicit user authorization on 2026-11-24, `src/api/` and `web/` implement a small local FastAPI + React/TypeScript draft UI reusing the existing engine. This is NV-21 engineering support; a full production Web platform, new learning algorithm or global BO5 optimization is not mandatory. See `docs/UI_REACT_TYPESCRIPT.md` and knowledge ledger section 27.
- **Database Standard**: SQLite 3 (`data/database/lol_live_data.db`) normalized to 1NF and 3NF (`matches_10min`, `tournament_matches`, `tournament_players` — 37,009 total rows).
- **Regional Meta Segmentation**: Full support for `LCK`, `LPL`, `LCP`, `WLDS` (Worlds/CKTG), `MSI`, `EWC`, `INTERNATIONAL`, and `ALL`.

## Governance

- This Constitution and `AI/AI_RULES.md` supersede all ad-hoc practices.
- Priority hierarchy: `ALGORITHMIC GENERALITY > STATISTICAL RIGOR > CORRECTNESS > CONSISTENCY > TRACEABILITY > SPEED`.

**Version**: 1.3.0 | **Ratified**: 2026-11-23 | **Last Amended**: 2026-11-24
