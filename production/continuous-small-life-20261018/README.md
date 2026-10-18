# 可恢复持续制作队列：首轮 12 项

**当前状态：线上67已确认（main ccf48bb446dd4d0a710ab14dfc05d6fbf7064cdb，PR9/Pages/public Chromium均PASS）；13–15全模型QA PASS、67→79发布容量失败待恢复，不影响已完成67；16–17候选完成/QA运行无结论，18独占制作。以最新state和父任务派发证明覆盖下方历史空claim/未派发/旧线上数量。**

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

**当前状态：父任务已确认 CI 完成（main `643534830397824dfd46990485bd16ad66ecf9ce`），首轮三批已独占派发；实际线程和领取信息以 state.json 为准。此 planning 会话未启动 Blender、QA、发布或合并。queue.json 中初始 blocked 状态是历史计划快照，不覆盖当前 state。**

计划分支：`planning/recoverable-small-life-12-20261018`。本目录是可以恢复、分派和核对的制作 backlog，不是 `run_asset_queue.py` 可直接运行的 manifest。三批互不共享模型输出；实际 Blender 并发仍受同一云环境资源协调限制。

## 首轮分工

所有 ID 都来自真实 `research/prehistoric-1000-v1/inventory.json`。英文、中文原名和完整 inventory 行保存在 `items/<ID>/inventory-record.json`。不是新增 12 个概念，也不增加研究清单总数。

| 批次 / 制作任务 | 精确 inventory ID | 名称 | 计划目录 | 选择理由 |
|---|---|---|---|---|
| [01](batch-01-TASK.md) | `archaeopteryx` | Archaeopteryx / 始祖鸟 | `items/archaeopteryx/` | 长羽尾与翼爪，补充鸟类轮廓 |
| 01 | `canadaspis` | Canadaspis / 甲壳底栖动物 | `items/canadaspis/` | 双瓣甲与分节躯体丰富海底层 |
| 01 | `ceratomyrmex` | Ceratomyrmex / 角颚蚁类 | `items/ceratomyrmex/` | 头角与上举颚区别于已有飞虫 |
| 01 | `hydropteris` | Hydropteris / 羽叶水蕨 | `items/hydropteris/` | 羽状水蕨的根叶关系丰富浅水层 |
| [02](batch-02-TASK.md) | `longipteryx` | Longipteryx / 长翼鸟类 | `items/longipteryx/` | 长吻短尾小鸟；不安排捕鱼叙事 |
| 02 | `urasterella` | Urasterella / 细腕海星类 | `items/urasterella/` | 放射腕形补充海底低位主体 |
| 02 | `alienopterus` | Alienopterus / 短前翅化石昆虫 | `items/alienopterus/` | 短前翅与六足结构补充地表昆虫 |
| 02 | `aglaophyton` | Aglaophyton / 裸轴植物 | `items/aglaophyton/` | 低矮裸轴和分叉，不重复星木 |
| [03](batch-03-TASK.md) | `cephalaspis` | Cephalaspis / 头甲鱼类 | `items/cephalaspis/` | 宽头盾与细尾区别于现有鱼 |
| 03 | `saccocoma` | Saccocoma / 游泳海百合类 | `items/saccocoma/` | 小杯体分枝腕，补充悬浮形态 |
| 03 | `archaeocidaris` | Archaeocidaris / 原始长棘海胆 | `items/archaeocidaris/` | 球壳长刺补充海底立体结构 |
| 03 | `onoclea` | Onoclea / 球子蕨类 | `items/onoclea/` | 营养叶与生殖结构，不以冠密度变体计数 |

表格中文为便于阅读的简称；精确双语原名见 queue.json，ID 是唯一键。批次不是同年代、同地点共存的生态组合。海底、浅水和陆地素材分别使用，不给出虚假的完整生境复原承诺。

每项输出位置已固定在 `queue.json`：

- 生产脚本和执行记录：`production/continuous-small-life-20261018/work/<batch>/<ID>/r001/`。
- 待审包：`assets/candidates/continuous-small-life-20261018/<batch>/<ID>/r001/`。
- 仅在通过 QA 后由父任务整合：`assets/additions/<ID>/continuous-small-life-v1/`。
- 新的重试使用独立 attempt 目录；修改已冻结模型使用 r002 等新版本，禁止覆盖旧证据。

## 已做去重和未确定事项

`dedup-snapshot.json` 保存全部远端分支 SHA、主分支快照、排除项和检查边界。已读取原 24 项 backlog 与 remaining-20 分批计划：本轮重排其中未制作的 12 项，不创建平行重复任务。余下一项 `pycnodus` 暂缓，为不同轮廓腾出位置。

已发布的初始十项及 `asteroxylon`、`bothriolepis`、`confuciusornis`、`ichthyornis`、`juracimbrophlebia`、`waptia` 全部排除。最新提交的发布依据为 `assets/releases/small-life-six-20261018.json`，main 快照为 `0d22f06124a8dbac40ca7e0e4570aa44659dc3d2`。这是仓库发布记录，不宣称重新检查了线上部署。

`dapedium` / `callichimaera` 属于 `candidate/fish-crab-pair-20261018`，SHA `5f912df345a39549ef8eb1a9cf0783e055314b0e`。该远端仅保存 `scripts/models/build_small_fish_crab.py`，没有这两项的 GLB；父任务已说明存在候选，必须保留他人制作占用，不能因远端缺少导出文件就重做。

`diplomystus` / `burgessomedusa` / `kalligramma` 已有 v002：`candidate/small-fauna-trio-20261018`，SHA `c8514b8c348777c9a2d81c6c0bbd9cf02cdb5184`。本轮用户已认可风格并授权发布；旧 README 中“user acceptance pending”是历史状态，不能覆盖本次父任务提供的授权。此处不接管三件组发布。

全部抓取分支中，没有发现首轮 12 项的 .blend/.glb 或按这些 ID 命名的生成器。旧队列中的 brief-ready 仅表示等待制作，不能当作正在制作。当前连接器 open-PR 查询返回空。路径扫描仍无法证明共享生成器、未推送工作或另一个会话没有占用；父任务启动前必须统一确认 claim。不能把本快照当全局任务锁。

五项旧 inventory gate 为 `needs-specific-reference`：`longipteryx`、`ceratomyrmex`、`urasterella`、`saccocoma`、`archaeocidaris`。其后已有 practical inspired-by brief/reference，随本目录保存，但本轮没有重新打开外部论文，也没有宣布清除这些 gate。这些旧 gate 不再作为严格科考复原的自动停工令：见 [五项处理说明](REFERENCE-GATES.md) 和 `reference-gate-policy.json`，只确认可靠基础参考支持可辨识形态，输入原创或有真实使用授权，之后即可合理风格化继续；不为软组织、精确齿数/板列/羽序或微观复原细节反复研究返工。没有可靠基本形态依据或标签声称超过依据时，先缩窄 inspired-by 标签或交父任务调整，不能伪造来源或事实 PASS。其他七项 reference-ready 也不是 QA PASS。

## 当前规范和预算

遵循仓库：

- [Blender 流水线](../../skills/blender-lowpoly-pipeline/SKILL.md)、[标准流程](../../skills/blender-lowpoly-pipeline/references/standardized-pipeline.md)、[可恢复队列契约](../../skills/blender-lowpoly-pipeline/references/parallel-queue.md)。
- [美术](../../skills/lowpoly-art-direction/SKILL.md)、[预算](../../skills/lowpoly-art-direction/references/asset-budgeting.md)、[史前环境](../../skills/prehistoric-environment-art/SKILL.md)、[事实审查](../../skills/asset-factual-review/SKILL.md)。

当前用户指令优先于 skill 或归档文件：制作 **GPT-6.1 Sol medium**；独立 QA 由父任务在新任务派发 **GPT-6 Luna xhigh**。本轮未派发任何制作或 QA。自然精致、可信比例、柔和衔接、适度卡通；关注 80–240 px 正常视图与约 480 px 中近距离。不能靠低面数宣称质量，不用不必要大贴图补救机械拼接或比例问题。

12 项均复用上述已认可 v002 的现行预算，而不是旧 remaining-20 的 2 MiB / 1K 贴图预算：

| 项目 | 每模型预算 |
|---|---|
| 导出三角形 | ≤14,000，上限而非目标 |
| 材质 / primitive | ≤6 / ≤30；不等同实际 draw calls |
| GLB | 通常争取约 100,000–500,000 bytes，硬上限 1,000,000 bytes |
| 可选原创建色贴图 | ≤1 张，单边 ≤256 px，总编码 ≤65,536 bytes |
| 贴图解码内存 | ≤524,288 bytes；另记录是否含 mip，不冒充 GPU 实测 |

单独报告源顶点、求值顶点、导出 POSITION-stream 顶点、三角形、材质/primitive、GLB 字节、贴图解码估算、源归档大小和场景实例数。现行 v002 没有独立顶点硬上限，不捏造一个。8,000/10,000/12,000 旧三角形阈值仅在 upstream 中归档，当前统一采用 v002 上限，不填满预算。14k 和 1MB 都是上限而非目标；通常争取约 100–500KB，更小同样可接受。只在轮廓、可信比例或衔接有明显收益时增加面数，不以大贴图凑精细。超过通常区间但仍在上限内，记录具体收益即可，不为软目标破坏造型。若必须提高硬上限，先给出命名的可见改善证据交父任务协调，不静默超限。

交付：可编辑 .blend、独立 GLB、可重建脚本/配置/依赖哈希、中英 metadata/不确定性/来源/许可/署名、透明封面，八个有意义的固定 QA 视图（hero/reversehero/front/side/rear/top/clay/silhouette），实际 GLB 多角度运行时证据。默认零转台序列；真正问题加针对性视图。源重开、两次语义重建对比、Khronos 验证与项目检查、精确 GLB 的 loader/功能渲染/简化多实例场景检查都必须记录。软件渲染不能冒充真实设备性能。

历史 `validate_candidate.py` 与此 practical 零序列配置可能冲突；不得为了通过旧 schema 编造转台证据。使用当前适用记录检查；把范围与缺项交独立 QA，任何本 brief 必需的未知项均阻止接受。制作会话的自查不构成独立 QA。

## 恢复、领取和执行

1. 正常 fetch 全部分支和最新 main，再读本目录 `queue.json`、`state.json`、`events.jsonl`、`dedup-snapshot.json`。运行 `python3 production/continuous-small-life-20261018/verify_plan.py` 只校验规划，不执行 Blender。
2. **等父任务明确确认 CI 精简完成。** 父任务记录确认来源/时间/相关 SHA 到 `state.json.ci_confirmation`，随后重查最新发布、候选分支、PR 和父任务实时分工。CI 工作流或 release 文件有变动本身不是确认。没有确认不开始建模。CI 确认后，五项旧参考 gate 按 REFERENCE-GATES.md 的有界基础检查处理，不额外要求严格科考复原。
3. 父任务作为单一协调者先领取独占 ID，再派发对应 batch TASK。把 owner、任务 ID、时间、工作分支与起点 SHA 写入 claims，并追加 events。队列中的 immutable 初始状态仍为 blocked；以已提交 state/events 为动态真相。不由三个 maker 各自假设自己先拿到 claim；常规 Git push 冲突须 fetch/reconcile，绝不 force push。过期 claim 必须由父任务明确释放，不能仅凭超时抢占。
4. 每批独立 branch/worktree，从届时最新 main 起步，只带入本 planning 目录。模型/脚本/证据按本批隔离，不覆盖已发布素材；不顺带 cherry-pick 旧分支的 CI、站点、发布代码。规划分支不合 main。原子更新 state 由父任务串行完成；并行 maker 返回各自结果文件供其归并。
5. 沿用 `planned → brief_ready → building → candidate → reviewing → repair → reviewing → accepted_for_brief`，另记 blocked/failed/cancelled/superseded/released。每个 attempt 保存输入/脚本/工具/参数哈希、资源、日志、返回码、输出哈希和路径，失败不覆盖、不当成功。
6. 实际 generator 出现以后再生成 `run_asset_queue.py` manifest。inputs 必须列全部语义依赖，outputs 列全部必需文件，build/preview/render 分 lane；默认 **1 worker × 2 threads**，与父任务协调 CPU share。先探测配额与已有进程，不能三个批次各自把整台机器额度用满。显式 timeout、可校准 memory；不杀他人进程。此处不写不存在的脚本/输出到假可执行 manifest。
7. 恢复时仅复用输入/工具/配置 fingerprint、完成状态和整个输出目录哈希一致的成功 attempt。中断、取消、缺文件、旧哈希、未知 gate 一律重试或补证据，不把现有文件名当完成。使用 runner 的 `--resume`，新尝试新目录。
8. Maker 推送候选与 SHA 后，父任务派新 GPT-6 Luna xhigh 任务，供应冻结 brief/reference、实际 GLB 和完整视图/报告，先不提供 maker 自评分。独立 QA 绑定当前 GLB hash；修复后旧 verdict 标 stale。通过全部必需检查后，用户已授权分批直接推送/合并，不需逐模型审批；由父任务串行整合 release/site 到最新 main，避开 CI/release 任务冲突。

恢复日志至少记录：ID、revision、attempt、状态、owner、branch/commit、输入/输出哈希、QA task/model/verdict、阻塞原因、release commit。`queue.json` 是初始计划，`state.json` 是当前状态，`events.jsonl` 追加记录；不得只改文字 README 就宣称模型完成。

每项 upstream 是原冻结输入的原字节归档；`freeze.json` 固定更新后的本轮 brief/config/reference/inventory 行。归档中的旧模型/批号/预算不是当前要求。变更本轮冻结输入须提高计划或模型版本并重新生成 freeze/checksums 后正常提交。动态 state/events 不计入静态文件清单哈希，仍由 Git 版本追踪。

许可沿用仓库；正常 commit/push 署名 `Leon Made This <8357465+s010s@users.noreply.github.com>`。不上传 Google Drive、不改权限、不强推。

下一轮12项已另存到 [round02，批次04–06](../continuous-small-life-round02-20261018/README.md)，尚未领取/派发。不得重领首轮ID。
