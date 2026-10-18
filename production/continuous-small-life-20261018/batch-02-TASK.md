# batch-02 — maker task (do not start before parent CI confirmation)

**当前状态：线上67已确认（main ccf48bb446dd4d0a710ab14dfc05d6fbf7064cdb，PR9/Pages/public Chromium均PASS）；13–15全模型QA PASS、67→79发布容量失败待恢复，不影响已完成67；16–17候选完成/QA运行无结论，18独占制作。以最新state和父任务派发证明覆盖下方历史空claim/未派发/旧线上数量。**

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

制作模型必须 GPT-6.1 Sol，reasoning medium。先读同目录 README.md、queue.json、state.json 和每项 freeze/brief/config/references。父任务尚未确认 CI 精简，本文件只是待派发任务。

Only inventory IDs: longipteryx, urasterella, alienopterus, aglaophyton.

Confirm parent CI completion evidence and exclusive coordinator claims for these IDs before any Blender invocation. Use a separate branch/worktree based on current main, copy only the planning directory from this planning branch, and keep every attempt isolated. Never cherry-pick entire stale production branches into main.

Follow v002 natural/refined style: credible proportions, soft transitions, deliberate low-poly structure, restrained original small textures, child-friendly normal-view readability. Use queue budgets unchanged: 14k triangles and 1,000,000 GLB bytes are hard ceilings, not targets. Usually aim about 100–500 KB (smaller is fine). Add geometry only for visible silhouette/proportion/connection improvement; do not pad counts or enlarge textures to fake refinement. Read reference-gate-policy.json. Reliable basic recognizable form and original/authorized inputs suffice for this stylized-inspired static prop. Keep source labels and uncertainty honest; fine reconstruction uncertainty does not require repeated research or repair.

Required per ID: editable .blend, standalone GLB, deterministic generator/config/helper hashes, bilingual metadata/provenance/attribution, original maps if used, transparent cover, eight fixed QA views and exact-GLB runtime views at normal/near scale, Khronos/project validation, source reopen and deterministic rebuild, candidate artifact hashes. No full turntable campaign. Record bounds/scale, triangles, source and exported vertices, materials/primitives, bytes/texture memory, visible copies and declared runtime. Do not infer beauty from counts.

Freeze candidate SHA and file digests, commit/push this batch branch normally, record state and notify parent with the exact bundle paths and hashes. Parent dispatches GPT-6 Luna xhigh in a fresh task for independent QA. Maker checks cannot substitute. Repair into a new revision/attempt and invalidate old affected verdicts. QA PASS permits parent-coordinated release/merge without per-model user approval; this task must not edit CI, unrelated site code or release other batches.

Prior backlog upstream files are archived under items/<id>/upstream/. They may contain obsolete Astra/xhigh, old budgets and old batch letters; current brief/config/README and the current user request govern.

| ID | 名称 | 选择理由 | 计划目录 |
|---|---|---|---|
| `longipteryx` | Longipteryx（古鸟类／鸟翼类） / Longipteryx | 细长吻与短尾形成第二种小鸟轮廓；不安排捕鱼叙事，保留食性来源限制。 | `items/longipteryx/` |
| `urasterella` | Urasterella（细腕海星类） / Urasterella slender-armed sea star | 放射腕形提供海底低位主体，与鱼蟹和水母形态不同。 | `items/urasterella/` |
| `alienopterus` | Alienopterus（短前翅化石昆虫） / Alienopterus short-winged fossil insect | 短前翅与六足结构补充地表小昆虫；区别于已发布叶形悬蝇。 | `items/alienopterus/` |
| `aglaophyton` | Aglaophyton 裸轴植物 / Aglaophyton rhizome arches | 低矮裸轴、分叉与顶生结构丰富早期植物地表层，不重复星木。 | `items/aglaophyton/` |

For the five historical reference gates, see [REFERENCE-GATES.md](REFERENCE-GATES.md). Keep the inherited one consolidated independent review / at most one planned cosmetic repair bound. Real technical/basic-form defects remain actionable; uncertain soft tissue, color, microscopic anatomy, exact plate/feather counts and unclaimed fossil measurements are advisory. Preserve source access truth; no third-party asset or image reuse without actual rights.
