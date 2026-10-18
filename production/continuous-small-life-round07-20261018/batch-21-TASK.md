# batch-21 — 仅计划，尚未派发

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Salvinia沉水部分是叶而非真根；Montsechia不添无依据根，二者只作淡水植物；早期陆地植物/海生动物/滑翔小爬行动物分区使用。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `montsechia` | Montsechia flexible fine-leaf shoots / Montsechia 水生早期被子植物 | `items/montsechia/` | 细分叉茎、小叶与成对卵形果补充淡水水下植物，区别于浮生水蕨。 细茎、小简单叶和成对末端果自然衔接，不加原资料缺乏依据的根或大型花。只恢复同一延后计划，微果脉和精确枝数不强求。 |
| `dollocaris` | Dollocaris giant-eyed arthropod / Dollocaris（巨眼甲壳动物） | `items/dollocaris/` | 深罩甲、两枚大眼与三对捕捉足补充罩甲生物，区别于大眼游泳蟹。 罩形甲壳和可读眼位、捕捉足基部有整体结构；眼睛虽大仍可信，不做浮着的机械球。无捕食演示，细复眼/肢节微观部分可简化。 |
| `coelurosauravus` | Coelurosauravus / Coelurosauravus（史前爬行类） | `items/coelurosauravus/` | 小型爬行体与侧方骨杆支撑滑翔膜丰富陆地上方层，区别于鸟和蝙蝠。 侧方滑翔膜及支撑杆布局与四肢区分，身体/尾自然衔接，不把膜做成鸟翼或蝙蝠手翼；在基础参考范围内标inspired-by，不强求骨杆逐根精确或滑翔机制/动画。 |
| `columnar-jointed-outcrop` | Columnar jointed outcrop / 柱状节理岩体 | `items/columnar-jointed-outcrop/` | 紧接多边岩柱与台阶状断端补充自然岩体竖向节奏，区别于矿物尖晶簇。 相互紧接的多边柱群和不齐台阶在整体岩体中成立，不是空隙很大的水晶阵列。柱截面/节理简化服务轮廓，不能把任意柱径当实地测量。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。
