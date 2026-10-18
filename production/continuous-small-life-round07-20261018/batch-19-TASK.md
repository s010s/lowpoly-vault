# batch-19 — 仅计划，尚未派发

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Salvinia沉水部分是叶而非真根；Montsechia不添无依据根，二者只作淡水植物；早期陆地植物/海生动物/滑翔小爬行动物分区使用。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `cooksonia` | Cooksonia sporangial shoots / Cooksonia 裸轴植物 | `items/cooksonia/` | 简单Y分叉与扁平顶囊补充稀疏低位植物，区别于刺轴、K节点与膨大基体。 保留少量纤细分叉和可读末端囊，不加未支持的现代蕨叶或花。采用原有延后计划的同一ID，不是新物种/模型变体；枝数/布局为美术选择。 |
| `cambroraster` | Cambroraster horseshoe-shield radiodont / Cambroraster（马蹄甲奇虾类） | `items/cambroraster/` | 宽马蹄甲、后掠侧翼与深眼切口提供新的近底轮廓，区别于双瓣甲和角棘头盾。 整体甲壳宽扁且侧翼/眼切口可读，软躯体与附肢自然衔接；不靠颜色区分旧蟹模型。细滤食结构可简化，不强求显微计数。 |
| `bedrock-pothole` | Bedrock pothole / 河床壶穴 | `items/bedrock-pothole/` | 裸露河床岩石中的深圆穴增加自然物的内部空间，与外部风化小孔不同。 连续岩面和有深度的圆穴用几何表达，侧壁/底部可检查，不能只画黑圆假孔。代表性地块而非精确古河床测量，不自动承诺任意无缝拼接。 |
| `quartz-prism-cluster` | Quartz prism cluster / 石英柱晶簇 | `items/quartz-prism-cluster/` | 六方柱和尖端从天然基质生长，区别于石膏玫瑰板晶。 棱柱/尖端与基质有自然朝向和粗细层次，不均匀排成工业阵列。克制便携材质，不用复杂透明重叠掩盖造型；晶面微缺陷和化学测定不要求。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。
