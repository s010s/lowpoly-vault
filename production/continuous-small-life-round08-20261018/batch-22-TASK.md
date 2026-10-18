# batch-22 — 仅计划，尚未派发

**当前父任务进度：线上确认103，22–24发布整合中；25/26模型QA PASS、27候选完成待QA；28/29候选完成且已派独立QA、无结论，30刚独占派制作。未提供的thread/turn/审核source不猜，实际state与父任务证明优先于历史初始空claim。**

**当前父任务进度：22–24全独立模型QA PASS，23仅标签修正、模型未变；25候选完成待独立QA，26独立模型QA PASS，27制作中。此处不新增线上数量/发布确认；实际state和父任务派发证明优先于历史初始空claim/旧阶段文字。**

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
| `florissantia` | Florissantia five-sepal flower / Florissantia 五萼花化石 | `items/florissantia/` | 五宽萼裂片与浅中央杯补充小型花器官展示，区别于果实或球果。 只做原保存五萼花器官：五宽裂片、浅杯和克制主脉；中央小器官保守，不凭化石萼扩写完整花瓣/雄蕊或整株。不是现代五瓣花套壳。 |
| `stanleycaris` | Stanleycaris three-eyed radiodont / Stanleycaris（三眼奇虾类） | `items/stanleycaris/` | 小穹顶头甲、中眼和四枚尾叶的细体提供新奇虾类轮廓，区别于宽马蹄甲。 头甲、成对眼与可读中眼、细长躯干和尾叶衔接自然；保留可见基本识别点，不精确复原神经/微齿。不得仅将既有奇虾换头色或缩放。 |
| `pahoehoe-lava-surface` | Pahoehoe lava surface / 绳状熔岩面 | `items/pahoehoe-lava-surface/` | 连续圆钝绳纹与重叠叶瓣增加地表流动节奏，区别于枕状露头。 连续熔岩壳的绳状褶皱和叶瓣方向一致、有主次；不是独立圆枕堆叠，也不随机放扭绳。代表地表块而非精确火山地点/实测流速。 |
| `staurolite-cross-twin` | Staurolite cross-twin / 十字石双晶 | `items/staurolite-cross-twin/` | 两柱贯穿连生形成十字双晶，区别于石英簇和玫瑰板晶。 柱晶与连生中心形成可信矿物实体，晶面关系有逻辑，不像两个工业杆螺丝拼接。交生区域是刻意结构，metadata标明，微晶面/精确角度不作为严格矿物学门槛。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。

独立QA优先由父任务创建全新上下文，先核对同目录batch-22-QA-SCOPE.json中batch/四ID，填真实source commit及逐项GLB hash再开始。报告必须回显相同对象，旧线程回错批次/ID/source的报告标invalid_review_wrong_subject，不得计PASS，也不能据此修错模型。当前scope仅计划，source/hash为空不代表QA就绪。
