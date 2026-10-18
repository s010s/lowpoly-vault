# batch-17 — 仅计划，尚未派发

**当前状态：线上67已确认（main ccf48bb446dd4d0a710ab14dfc05d6fbf7064cdb，PR9/Pages/public Chromium均PASS）；13–15全模型QA PASS、67→79发布容量失败待恢复，不影响已完成67；16–17候选完成/QA运行无结论，18独占制作。以最新state和父任务派发证明覆盖下方历史空claim/未派发/旧线上数量。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Matonidium只做蕨叶、Araucaria mirabilis只做附枝球果、Trapa只做果实，不凭单器官扩写整株；岩体/矿物只作过程教学概念。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `isastraea` | Isastraea polygon-cup reef coral / Isastraea（多边杯造礁珊瑚） | `items/isastraea/` | 低块体与相接星隔大杯补充造礁珊瑚，区别于长杯簇与细蜂巢管。 低块群体、相接大多边杯及清楚星状隔壁；不把Favosites单纯扩大杯口当新形态，也不复制Acrocyathus长管簇。微孔/隔壁精确数不强求。 |
| `araucaria-mirabilis` | Araucaria mirabilis attached cone specimen / Araucaria mirabilis 南洋杉类球果 | `items/araucaria-mirabilis/` | 单枝附生球果的鳞片浮雕丰富植物器官展示，区别于另一个整树冠。 仅原清单器官范围：一段有依据的短枝与附生圆形镶嵌鳞片球果，不外推整棵树、树皮大贴图或无依据母体结构；鳞片数/颜色可简化。 |
| `onychonycteris` | Onychonycteris / Onychonycteris（古哺乳形类） | `items/onychonycteris/` | 宽早期蝙蝠翼与翼指爪提示补充小型飞行哺乳动物，不再增加鸟类换色。 紧凑哺乳动物身体、可读宽翼膜和指骨支撑自然连贯，保留可见翼指爪提示；不逐微骨精确复原，不把它做成鸟翼或现代种确定复原。友善静态展示，不承诺飞行动画。 |
| `pillow-lava-outcrop` | Pillow lava outcrop / 枕状熔岩露头 | `items/pillow-lava-outcrop/` | 膨鼓枕瓣、细颈和冷却外壳为海底/自然场景提供新的过程岩体。 不等大枕状叶瓣用细颈连贯，外壳起伏支持凝固逻辑；不是等大球体机械相切堆叠。代表性露头裁切边界明确，不把尺寸/地点/年代当实测。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。
