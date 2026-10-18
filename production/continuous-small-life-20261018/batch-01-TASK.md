**最新进度：04–06已发布，父任务确认总数43/main 0bd62cda92814af5ac781e1a706bba6310cecc35；07–09独立模型QA PASS、profile发布记录适配中，未确认55；10–11独立QA进行中无结论，12已独占制作。现state与父任务派发证明优先于下方历史规划/空claim。**

**当前授权以最新state和父任务明确派发证明为准；旧queue/config/工作副本的空claim或未派发文字是历史快照，不得阻塞已被父任务独占授权的worker。以下旧阶段文字不覆盖当前状态。**

当前 `batch-01`：`published`。详情及精确source/QA/发布pins见state.json。

**状态与派发授权：以本目录最新 `state.json` 和父任务明确派发证明为准。`queue.json`/冻结config/旧工作副本中的空claim或“尚未派发”是历史快照，不能阻塞父任务已经独占派发的worker；父任务消息是有效授权证据。未知真实分支/时间/哈希不编造，新任务仍由父任务统一领取，不能由未派发者自行认领。**

当前 `batch-01`：`release_queued`；原制作线程 `01a15039-c422-75bb-bd79-136370f9a010`。12件已交唯一release child `01a1502d-a2f1-74aa-adef-d04595fe501c` 排队，尚未确认发布。

**当前独占领取：父任务已派发到 `01a15039-c422-75bb-bd79-136370f9a010`；CI 已确认 main `643534830397824dfd46990485bd16ad66ecf9ce`。以下初始等待描述为历史，现以 state.json 为准；不要再次派发或重新领取同一批。**

# batch-01 — maker task (do not start before parent CI confirmation)

制作模型必须 GPT-6.1 Sol，reasoning medium。先读同目录 README.md、queue.json、state.json 和每项 freeze/brief/config/references。父任务尚未确认 CI 精简，本文件只是待派发任务。

Only inventory IDs: archaeopteryx, canadaspis, ceratomyrmex, hydropteris.

Confirm parent CI completion evidence and exclusive coordinator claims for these IDs before any Blender invocation. Use a separate branch/worktree based on current main, copy only the planning directory from this planning branch, and keep every attempt isolated. Never cherry-pick entire stale production branches into main.

Follow v002 natural/refined style: credible proportions, soft transitions, deliberate low-poly structure, restrained original small textures, child-friendly normal-view readability. Use queue budgets unchanged: 14k triangles and 1,000,000 GLB bytes are hard ceilings, not targets. Usually aim about 100–500 KB (smaller is fine). Add geometry only for visible silhouette/proportion/connection improvement; do not pad counts or enlarge textures to fake refinement. Read reference-gate-policy.json. Reliable basic recognizable form and original/authorized inputs suffice for this stylized-inspired static prop. Keep source labels and uncertainty honest; fine reconstruction uncertainty does not require repeated research or repair.

Required per ID: editable .blend, standalone GLB, deterministic generator/config/helper hashes, bilingual metadata/provenance/attribution, original maps if used, transparent cover, eight fixed QA views and exact-GLB runtime views at normal/near scale, Khronos/project validation, source reopen and deterministic rebuild, candidate artifact hashes. No full turntable campaign. Record bounds/scale, triangles, source and exported vertices, materials/primitives, bytes/texture memory, visible copies and declared runtime. Do not infer beauty from counts.

Freeze candidate SHA and file digests, commit/push this batch branch normally, record state and notify parent with the exact bundle paths and hashes. Parent dispatches GPT-6 Luna xhigh in a fresh task for independent QA. Maker checks cannot substitute. Repair into a new revision/attempt and invalidate old affected verdicts. QA PASS permits parent-coordinated release/merge without per-model user approval; this task must not edit CI, unrelated site code or release other batches.

Prior backlog upstream files are archived under items/<id>/upstream/. They may contain obsolete Astra/xhigh, old budgets and old batch letters; current brief/config/README and the current user request govern.

| ID | 名称 | 选择理由 | 计划目录 |
|---|---|---|---|
| `archaeopteryx` | 始祖鸟（Archaeopteryx） / Archaeopteryx | 长羽尾、翼爪与站姿补足鸟类轮廓；区别于已发布孔子鸟和鱼鸟。 | `items/archaeopteryx/` |
| `canadaspis` | Canadaspis（甲壳底栖动物） / Canadaspis shielded bottom crawler | 双瓣甲与分节躯体形成近底小型海生轮廓；不重复 Waptia 的成品。 | `items/canadaspis/` |
| `ceratomyrmex` | Ceratomyrmex（角颚蚁类） / Ceratomyrmex horn-jawed ant | 头角与向上颚提供清晰昆虫辨识点；与蝶蛉和悬蝇不同。 | `items/ceratomyrmex/` |
| `hydropteris` | Hydropteris 羽叶水蕨 / Hydropteris rooted pinnate water fern | 羽状水蕨的根叶关系丰富浅水层，不以叶片密度变体计数。 | `items/hydropteris/` |

For the five historical reference gates, see [REFERENCE-GATES.md](REFERENCE-GATES.md). Keep the inherited one consolidated independent review / at most one planned cosmetic repair bound. Real technical/basic-form defects remain actionable; uncertain soft tissue, color, microscopic anatomy, exact plate/feather counts and unclaimed fossil measurements are advisory. Preserve source access truth; no third-party asset or image reuse without actual rights.
