# batch-23 — 仅计划，尚未派发

**当前父任务确认：batch22/23已交付、待独立QA，batch24生产者独占制作。实际state及父任务派发证明覆盖下方初始未分派/空claim；交付不等于QA PASS或已发布。22/23来源SHA为本次远端头观察值，派QA前核对实际冻结handoff。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Florissantia只做五萼花器官，Metasequoia只做化石枝，Nordenskioldia只做果序轴，Williamsonia只做种子球果，均不能外推未知整株。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `metasequoia` | Metasequoia opposite-leaf fertile branch / Metasequoia 水杉类化石枝 | `items/metasequoia/` | 对生交互排列的小叶/球果化石枝补充植物器官，不增加另一种完整树冠。 只做保存枝条器官，突出成对着生和拓扑间隔；不扩写整棵红杉，也不把现有针叶树冠减少密度。未关联器官不加，叶数/厚度可简化。 |
| `ovatiovermis` | Ovatiovermis unarmoured filter lobopodian / Ovatiovermis（无甲滤食叶足动物） | `items/ovatiovermis/` | 裸躯前举滤食臂与后部固着爪足提供不同姿态的软体小生物。 裸躯、前长臂和后部较粗爪足的连接/支撑可读；不是Hallucigenia去棘或人形手臂。细滤毛可经济简化，姿态是静态美术，不承诺完整取食力学。 |
| `nordenskioldia` | Nordenskioldia radial-fruit axis / Nordenskioldia 轮列果序化石 | `items/nordenskioldia/` | 细轴上的放射果环补充果序结构，区别于单果角臂或球果鳞片。 仅保存果序枝/轴，少量放射分段小果环边界清楚；不另计种子资产，不添加未知整树、花或叶冠。果数和间距为教学简化。 |
| `waterfall-ledge` | Waterfall ledge / 瀑布岩阶 | `items/waterfall-ledge/` | 突出上岩缘与下退软层补充地形高差和岸边遮蔽空间。 上下抗蚀差异形成连续岩阶/下方退缩区，不能用两块松散方砖假装地层。只导出岩阶，水体/灯光若作展示另分，不承诺水流模拟或精确古地点。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。

独立QA优先由父任务创建全新上下文，先核对同目录batch-23-QA-SCOPE.json中batch/四ID，填真实source commit及逐项GLB hash再开始。报告必须回显相同对象，旧线程回错批次/ID/source的报告标invalid_review_wrong_subject，不得计PASS，也不能据此修错模型。当前scope仅计划，source/hash为空不代表QA就绪。
