# batch-18 — 仅计划，尚未派发

**当前状态：线上79已确认（main eb9153eab06f7e95235eac30611b731c8178ffb7）；16/18旧错批QA无效，16新线程01a150f1-ab04-71eb-af42-0a2fc9450036、18新线程01a150f5-9dfe-77e0-bd27-6cbc89942035审正确source；17模型QA PASS；19新QA运行、20模型QA PASS、21制作中。错批报告不计PASS，最新state/派发证明覆盖历史描述。**

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
| `spinolestes` | Spinolestes / Spinolestes（古哺乳形类） | `items/spinolestes/` | 紧凑有毛小兽与局部棘皮区补充陆地近景，区别于蛙和蝙蝠。 头躯、短肢和局部棘皮区柔和连接，有安静毛面与识别重点；不要随机满身长刺或现代刺猬换色。颜色/软体轮廓为教学美术，不承诺严格皮毛组织复原。 |
| `odontogriphus` | Odontogriphus smooth-bodied grazer / Odontogriphus（光背软体动物） | `items/odontogriphus/` | 无壳扁椭圆体、宽腹足与边缘鳃带补充低位软体海生动物。 扁椭圆体与宽腹足、克制边缘鳃带有整体连续性；区别于八腕动物、叶足动物和鱼。细齿舌/鳃片数等微观部分可省，不贴现代蛞蝓的无依据触角。 |
| `trapa` | Trapa harpoon-horned fruit / Trapa 菱属四角果化石 | `items/trapa/` | 紧凑果体与四条反向角臂补充果实器官展示，区别于球果/蕨叶。 仅化石果实器官：紧凑中央体、四角与克制倒刺方向清楚；不添加未知叶茎根或现代整株。末端不需危险尖锐，颜色和名义尺寸是美术选择。 |
| `flint-nodule` | Flint nodule / 燧石结核 | `items/flint-nodule/` | 白垩状外皮与贝壳状断口提供小型岩石材质/结构差异，区别于矿物充填结核。 不规则圆钝结核、浅色外皮和一处可读贝壳状断面；这是断口形态，不是贝壳动物。只计一种构图，不以完整/破损另增ID，不把断面随机三角噪声当结构。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。
