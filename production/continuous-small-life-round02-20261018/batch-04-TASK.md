**状态与派发授权：以本目录最新 `state.json` 和父任务明确派发证明为准。`queue.json`/冻结config/旧工作副本中的空claim或“尚未派发”是历史快照，不能阻塞父任务已经独占派发的worker；父任务消息是有效授权证据。未知真实分支/时间/哈希不编造，新任务仍由父任务统一领取，不能由未派发者自行认领。**

当前 `batch-04`：`reviewing`；原制作线程 `01a15047-91cd-7261-916c-9690e749200e`。05/06已正式独占派发；04独立QA进行中，未PASS。

# batch-04 — next-round maker task; not yet dispatched

Only inventory IDs: calceola, favosites, opabinia, choia.

CI 已由父任务确认完成于 main `643534830397824dfd46990485bd16ad66ecf9ce`；这不等于本轮已派发。先由父任务统一更新本目录 state.json 的独占 claim 和实际 task/thread ID，才能开始。本 planner 不生产、不创建制作会话、不合并 main。

制作必须 GPT-6.1 Sol medium，授权云环境。读 README.md、queue.json、reference-policy.json、state.json 及每项冻结的 brief/config/references。延续 v002 自然精致、可信比例、柔和衔接和适度卡通；80–240px 普通观看，约480px 中近距离，不要求显微科考。

每项上限 14,000 三角形 / 1,000,000 GLB bytes，不是目标。通常争取约100–500KB，更小同样可；增加面数须有轮廓、比例或衔接的明显收益，记录收益即可，不为了软目标破坏造型。≤6 materials / ≤30 primitives；最多1张≤256px原创贴图，编码总计≤65,536 bytes、解码预算≤524,288 bytes，不以大贴图凑精细。

可靠基础参考支持可辨识形态即可合理风格化继续。来源访问是继承历史，不冒充本轮已重读；仅查阅不赋予复制媒体权利。模型/贴图原创，不搬运外部网格或图片。微观解剖、精确齿/板/羽/分枝数量、未保存软组织、实际尺寸和运动机制不是门槛。真实基本身份矛盾、无来源的属级强断言或无权使用的第三方素材需修正；优先缩窄 inspired-by 标签，不进行无限研究。

使用届时最新 main 的独立 branch/worktree，携带本规划目录及必要当前 helpers；不整体挑入旧制作分支，不改CI/无关站点代码。所有制作、重建、预览与QA证据按本批/ID/revision/attempt隔离。默认协调池1 worker×2 threads，三个批次不能各自抢占全机。

每项交付：可编辑Blend、独立GLB、确定性generator/config及依赖哈希、中英metadata与来源/不确定性/许可/署名、可选原创贴图、透明封面、hero/reversehero/front/side/rear/top/clay/silhouette八个固定QA视图，以及实际GLB多角度loader/功能渲染/多实例场景证据。零转台序列；有问题才加针对性视角。记录source reopen、两次语义重建、Khronos/project checks、顶点/三角形/材料/primitive/字节/贴图/场景实例计量；软件渲染不冒充物理设备性能。

冻结精确commit与GLB/brief/reference/evidence哈希，正常push本批分支，回报父任务所有路径。独立QA必须由父任务新派GPT-6 Luna xhigh，制作自查不能替代。一次汇总QA、最多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节反复返工。修复新revision/attempt，旧verdict标stale。

通过全部必需QA后用户已授权直接推送/合并，无需逐模型审批；父任务串行整合发布。这里不自行合并main，不上传Google Drive、不改权限、不强推。

| ID | 原始中英名称 | 选择理由 / 基本形态 | 计划目录 |
|---|---|---|---|
| `calceola` | Calceola（拖鞋珊瑚） / Calceola slipper coral | 单体拖鞋杯与单盖提供低矮有盖珊瑚，区别于块状和枝状群体。 扁拖鞋形杯体与一个半圆盖的基本关系；盖缝留可读层次。开合姿态和软组织是美术选择，不作活动机制精确复原。 | `items/calceola/` |
| `favosites` | Favosites（蜂巢床板珊瑚） / Favosites honeycomb tabulate coral | 蜂巢状紧排多边管群体，提供厚实圆块礁体，与链状珊瑚不同。 圆块群体和紧邻多边管口形成蜂巢节奏；选择少量足够可读的管口，不填满微小孔阵列。宏观蜂巢形态足够，具体种级管壁微孔不必复原。 | `items/favosites/` |
| `opabinia` | Opabinia（五眼古生动物） / Opabinia five-eyed swimmer | 五眼、单根长吻和侧叶形成游泳主体；区别于已有鱼、蟹、双瓣甲动物。 五个眼部突起、单根末端抓握式长吻、低矮侧叶体要清楚；精确节数、腹侧细肢和软组织可简化。 | `items/opabinia/` |
| `choia` | Choia（放射盘状海绵） / Choia radial-disc sponge | 扁盘与放射骨针丰富海底低矮层，不是海胆的球壳长刺变种。 低扁椭圆中心与伸出式放射骨针轮廓；有秩序疏密，微观骨针计数/骨架截面不作为门槛。 | `items/choia/` |
