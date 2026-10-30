# Repository task entrypoint

For repository tasks, report the actual checkout commit and read the relevant
Skill from this checkout; a skill name or acknowledgment alone is not evidence
that it was read. `skills/` contains the production Skills; `.agents/skills/`
contains separately scoped tooling. Do not assume either is in an agent catalog.

## Creature generation and refinement

For Meshy creature base generation or subsequent Blender refinement, read
[skills/meshy-blender-creatures/SKILL.md](skills/meshy-blender-creatures/SKILL.md).
Read its linked references when their stage applies, not all references by default.
Reuse existing applicable research and briefs. This route supplements existing
art direction, export and factual checks; it does not certify an external service
output as a deterministic from-scratch build.

Delegated tasks should name the exact repository commit and Skill path, the current
stage, inputs, accepted simplifications and authorized scope. The executor reports
its actual commit, Skill/reference paths read and the constraints applied, together
with observable work or the exact blocker. Do not claim a pinned version was read
when the checkout differs; reconcile the mismatch first. A supplied workflow pack
is usable only with its source commit and file hashes verified against that handoff.

For multi-species generation, isolate each species' execution context, inputs and
state; do not inherit the entire parent conversation by default. A focused handoff
contains that species' brief/accepted simplifications, input hashes, candidate
revision, commit/Skill path, stage, remaining authorization and required outputs.
For continuation, privately include the actual existing service task ID and known
attempt state. Keep one coordinating budget ledger with spent and unknown charges;
context isolation does not reset usage. Reconcile uncertain POSTs before moving
work or creating a new attempt. Shared research or safe batch tooling may still be
reused when appropriate; isolation is not a ban on every batch operation.

Track generation, refinement and QA separately with the optional
[production provenance contract](docs/production-provenance.md). Missing historical
provenance is unknown, not proof that an asset was or was not generated/refined.
Exact revision/hash bindings prevent a newer candidate's QA from relabeling an old
published model. Skill installation and task assignment grant no additional paid
calls, environment access, push, merge or deployment authority. Current task
authorization and remaining budget control those actions; keep private operational
records out of public files.
