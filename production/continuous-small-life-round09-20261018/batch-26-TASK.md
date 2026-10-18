# batch-26 — 仅计划，尚未派发

**当前父任务进度：22–24全独立模型QA PASS，23仅标签修正、模型未变；25候选完成待独立QA，26独立模型QA PASS，27制作中。此处不新增线上数量/发布确认；实际state和父任务派发证明优先于历史初始空claim/旧阶段文字。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。海藻限原保存藻轴/轮盘/扁平分枝；潜穴限示意剖面且不指定制造者；潮坪和溶沟岩面是代表性片区，不归一化成小石或假称实测古地点。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `echinochiton` | Echinochiton spiny plated mollusk / Echinochiton（棘甲软体动物） | `items/echinochiton/` | 连续背板两侧的大刺补充板甲软体动物，区别于前后帽壳加中段鳞片的Halkieria。 背板序列与侧向大刺有整体连接，刺基/背板比例可信，空心提示只保留有用局部；不精确复原微观骨片数或全软体。保留原biomes空数组，不擅自声称特定共存生境。 |
| `clypeina` | Clypeina fertile-whorl specimen / Clypeina 盾盘轮藻 | `items/clypeina/` | 有记录的一对轮盘与粗放射分区补充海藻繁殖结构片段，不做未知高轴。 只做原记录相连轮盘标本，分区、连接与有限厚度自然；不做机械齿轮、叠硬币或无限高茎，不外推未知完整藻体。 |
| `tidal-flat` | Tidal flat / 潮坪 | `items/tidal-flat/` | 极缓坡与浅小排水沟为岸边小生物提供场景层次，区别于单一波痕/泥裂纹理。 代表性潮坪片区，浅沟有连通方向、低坡连续，不靠噪声/贴图假排水；不是完整海岸测绘，尺度/沟间距为美术。原scale_class保留landscape，不归一化成手掌小石。 |
| `thalassinoides-branching-burrow` | Thalassinoides branching burrow / Thalassinoides 分支潜穴网 | `items/thalassinoides-branching-burrow/` | 粗平滑潜道与开放Y节点补充海底内部路径教学，区别于U形双井。 粗隧道通过开放Y节点相连，切面是示意。表达洞腔与围岩关系，不能把架空树枝/虫体当潜穴；灰色剖面内部结构是识别重点，不指定制造者或真实出土标本。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。

独立QA优先新上下文；先填/核对同目录batch-26-QA-SCOPE.json的真实source/逐项GLB hash及恰好四ID，报告回显相同对象，错批/错source即invalid_review_wrong_subject、不计PASS。当前scope为未就绪规划，不启动QA。metadata依原worlds/分类等facet，research pack不自动成为已发布pack。潜穴检查灰色内部剖面，不按外轮廓判识别；海藻仅原标本范围，地形保留明确米制代表片区。
