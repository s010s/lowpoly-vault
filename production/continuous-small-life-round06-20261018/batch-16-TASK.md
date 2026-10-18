# batch-16 — 仅计划，尚未派发

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Matonidium只做蕨叶、Araucaria mirabilis只做附枝球果、Trapa只做果实，不凭单器官扩写整株；岩体/矿物只作过程教学概念。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `pleurodictyum` | Pleurodictyum low cup-disc coral / Pleurodictyum（低杯盘珊瑚） | `items/pleurodictyum/` | 低穹盘与几个较大相邻杯提供低矮珊瑚轮廓，区别于Micrabacia单杯放射盘。 小穹盘上的多杯关系可读；不是旧圆块珊瑚缩小或换孔密度，整体低盘及少量大杯需共同表达。微观板壁与软组织可简化。 |
| `matonidium` | Matonidium comb-ray frond / Matonidium 掌状蕨 | `items/matonidium/` | 放射叶轴与成对羽片形成掌状蕨叶展示，区别于旧羽状整丛。 仅保存叶片器官：细放射叶轴、成对块状羽片和射线间空隙。不能凭叶片添加未知干根或整株蕨冠；叶厚、少量叶片弯曲可合理风格化。 |
| `yohoia` | Yohoia elbow-clawed arthropod / Yohoia（肘爪节肢动物） | `items/yohoia/` | 方形头甲和成对肘爪提供新的前肢轮廓，区别于Leanchoilia长丝三指附肢。 方形头甲、自然连接的肘状前爪与末端长指组可读；以原参考基本形态为界，不把现有长丝动物剪短改色。细肢节/软组织可经济简化。 |
| `gypsum-desert-rose` | Gypsum desert rose / 石膏沙漠玫瑰 | `items/gypsum-desert-rose/` | 交叠含沙板晶构成放射集合体，为近景自然物增加矿物形态。 有主次尺度的板状晶体交叠成玫瑰状，保持晶片厚度与夹角；不是花朵或等距机械齿轮。颜色/晶片数量属美术，不作矿点精确复原。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。
