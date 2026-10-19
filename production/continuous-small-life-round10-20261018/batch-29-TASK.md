# batch-29 — 仅计划，尚未派发

**当前父任务进度：线上确认115、22–24已发布；25–27发布整合中（27报告内容PASS与其正式profile阻塞分开保留）；28–30模型QA均PASS；31–33候选全完成且已派独立QA、无结论。最新state/父任务派发证明覆盖历史初始空claim，不从模型QA推断发布。**

**当前父任务进度：线上确认103，22–24发布整合中；25/26模型QA PASS、27候选完成待QA；28/29候选完成且已派独立QA、无结论，30刚独占派制作。未提供的thread/turn/审核source不猜，实际state与父任务证明优先于历史初始空claim。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Marsilea/Azolla仅淡水岸边；Pachypteris仅叶器官、Peltaspermum仅盾籽盘，不推断整株。海岸地形保留米制片区，矿物/熔管不是植物或具体古地点。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `azolla` | Azolla scale-leaved floating mat / Azolla 满江红类水蕨 | `items/azolla/` | 连续分枝单元上的阶梯状叶瓦形成细密浮生水蕨，区别于Salvinia两片大浮叶。 叶瓦与分枝结构有清楚层次，覆盖范围只算一种构图；不做Salvinia缩小增密变体。保持淡水标签与needs-specific-reference，不把类群/标本页当所有古种细节已验证。 |
| `odaraia` | Odaraia tube-carapace swimmer / Odaraia（筒甲游泳动物） | `items/odaraia/` | 两端开口筒甲、大眼和三叶尾提供新的游动外形，区别于封闭双瓣甲或侧向长棘。 筒甲开口、眼位与三叶尾有整体衔接，不把Dollocaris或Isoxys换色。眼睛大但比例可信；小肢、体节细节及游泳机制可合理简化。 |
| `pachypteris` | Pachypteris thick-pinnule frond / Pachypteris 厚叶种子蕨 | `items/pachypteris/` | 厚而全缘的小羽片与分枝叶轴补充种子蕨叶器官，区别于薄羽片掌状蕨。 仅保存叶器官，羽片有浅体积、圆钝多边尖与叶轴分枝；不推断灌木/母树，也不把旧蕨叶仅加厚复制。细脉和原始颜色不强求。 |
| `sand-spit` | Sand spit / 沙嘴 | `items/sand-spit/` | 一端连岸的狭长沙舌补充岸线轮廓与遮蔽浅水空间，区别于潮坪排水面。 连岸端和伸出狭长沙舌关系清楚，不做独立小岛或两端连接的连岛沙洲；宏观轮廓而非波纹噪声。原landscape类别保留，12m名义片区不代表整条真实海岸，水场景另分。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。

独立QA优先新上下文，先填/核对batch-29-QA-SCOPE.json实际source/逐项GLB hash与恰好四ID；错批/错source报告invalid_review_wrong_subject，不计PASS且不据其修错模型。scope当前未就绪，planner不启动QA。metadata保留原worlds/分类/eras/biomes，research pack不是已发布pack；两种水蕨只淡水。海蚀柱/沙嘴保持明确米制地形尺度，不单位化。
