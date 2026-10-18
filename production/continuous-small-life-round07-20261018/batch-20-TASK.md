# batch-20 — 仅计划，尚未派发

**当前状态：线上79已确认（main eb9153eab06f7e95235eac30611b731c8178ffb7）；16/18旧错批QA无效，16新线程01a150f1-ab04-71eb-af42-0a2fc9450036、18新线程01a150f5-9dfe-77e0-bd27-6cbc89942035审正确source；17模型QA PASS；19新QA运行、20模型QA PASS、21制作中。错批报告不计PASS，最新state/派发证明覆盖历史描述。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Salvinia沉水部分是叶而非真根；Montsechia不添无依据根，二者只作淡水植物；早期陆地植物/海生动物/滑翔小爬行动物分区使用。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `leclercqia` | Leclercqia divided-leaf shoot / Leclercqia 裂叶石松类植物 | `items/leclercqia/` | 分裂叶单元与回曲中央尖端丰富小型石松形态，区别于裸轴/刺轴植物。 几片主要叶的分裂轮廓和较长中央部可读，叶基自然接茎；远侧重复叶经济简化。恢复同一延后ID，不以密度变体计数，不强求每叶细脉。 |
| `canadia` | Canadia leaf-bristled annelid / Canadia（叶毛环节动物） | `items/canadia/` | 扁长虫体、叠覆宽刚毛与两根头须丰富海底柔软小生物。 虫体与宽叶状背刚毛成组衔接，头须克制；不是Aysheaia加毛或整身细刺噪声。细刚毛/体节数可合理简化，软组织色彩为艺术。 |
| `salvinia` | Salvinia paired floats and submerged leaf / Salvinia 槐叶萍类水蕨 | `items/salvinia/` | 成对宽浮叶和沉水分叉叶丰富淡水表层，区别于基囊浮生莲座或有根叶柄。 两片浮叶与下垂分叉沉水叶分层，后者必须标为叶而非真根。淡水不是海水，叶毛/细脉和对数可简化；只恢复原延后ID。 |
| `load-cast-bedding` | Load-cast bedding / 负载构造岩层 | `items/load-cast-bedding/` | 上层鼓状下垂叶瓣进入下方软层，补充地层内部几何，区别于表面泥裂和波痕。 两层连续岩体中上层向下鼓入的叶瓣可读，教学侧面显露过程结构，不堆离散球体。裁切与色层为美术，不能声称精确古地层或实时变形动画。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。
