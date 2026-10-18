# batch-12 — 仅计划，尚未派发

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。本轮Limnobiophyllum只作淡水岸边植物；波痕、贝壳灰岩和泥裂是地表/岩体过程概念，不伪称精确史前地点；珊瑚只需可靠基础辨识，不强加显微复原。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `cystiphyllum` | Cystiphyllum blister-cup coral / Cystiphyllum（泡杯珊瑚） | `items/cystiphyllum/` | 膨大弯曲单杯和宽浅泡状杯内结构补充厚实低杯，区别于Heliophyllum细弯角深放射杯。 膨大弯杯、宽浅顶部与少量泡状内起伏共同区分形态；不能只改变Heliophyllum比例或配色。不做夸张随机疙瘩、微观隔壁全复原。 |
| `limnobiophyllum` | Limnobiophyllum stolon-linked leaf rosettes / Limnobiophyllum 浮生天南星类 | `items/limnobiophyllum/` | 匍匐茎连接叶丛与下垂根束丰富淡水岸边漂浮层，区别于成对浮叶水蕨。 少量分枝匍匐茎、清楚的叶丛与简化垂根束；是淡水湿地浮生植物，不当海草或海底植被。叶间距/根束数属构图，种级细脉或精确果序不强加。 |
| `wielandiella` | Wielandiella divaricate shrub / Wielandiella 本内苏铁类灌木 | `items/wielandiella/` | 叉枝灌木骨架与叶丛丰富岸边/陆地中层，不增加另一种大树冠密度变体。 重点为叉枝的支撑骨架与叶丛关系，采用原清单修订整株概念，不套用旧花形图或现有苏铁莲座。末级叶数/颜色可简化，不用叶片密度替代分枝结构。 |
| `desiccation-crack-surface` | Desiccation crack surface / 干裂泥面 | `items/desiccation-crack-surface/` | 相接泥片和收窄裂缝提供干露岸面，与波浪波痕湿浅水区域形成不同地表结构。 多边形泥片拼合与渐窄真实裂缝，节奏有主次；不是Voronoi噪声贴图。不额外命名干燥气候/地质年代，不将这种干露形成纹理当永久水下成因。 |

新候选采用最新main的显式 `static-stylized-v1` profile（规则2026-10-18.1），机器字段 `publication_authority: separate`；用户批量发布授权另pin到profile-policy.json的policy。实际candidate生成后再用scripts/candidate_profile.py生成绑定真实hash的sidecar；不得预填假hash或称profile PASS。保留legacy错误，blockers用结构对象、criterion IDs与brief一致；模型QA PASS、candidate/profile PASS和发布状态分别记录。
