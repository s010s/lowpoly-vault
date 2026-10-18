# batch-31 — 仅计划，尚未派发

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Baculites/Mucrospirifer只做保存壳体，不生造软体；潜迹只按原阴/阳浮雕教学、不指定制造者；海岸地形保留米制代表片区，不假称古地点测绘。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `asaphus` | Asaphus eye-tower trilobite / Asaphus（高眼柱三叶虫） | `items/asaphus/` | 椭圆三叶虫甲体与高眼柱补充贴底动物轮廓，区别于两盾甲和大眼游泳蟹。 光滑椭圆甲体、头部附近高眼柱和基本轴向层次连续自然；不是把蟹眼或Naraoia拉长改色。限定原高眼柱形态的inspired-by，不宣称整个属都如此，微环节/软体可简化。 |
| `hazelia` | Hazelia open-shield sponge / Hazelia（开盾形海绵） | `items/hazelia/` | 薄宽杯壁展开不规则盾面，补充海底竖向屏风式海绵，区别于管状/带刺/扁盘海绵。 宽薄杯壁与盾面连续、有克制放射纤维脊和真实内外表面，基部支撑可信；不做漏孔平板或旧海绵仅改变密度。微纤维/骨针不强求。 |
| `sea-cave` | Sea cave / 海蚀洞 | `items/sea-cave/` | 岩壁底部横向浪蚀开口与内部空间增加岸边遮蔽结构，区别于独立海蚀柱和穿透石拱。 选一段岩壁与有厚度洞腔，入口/顶壁/侧壁/短腔背面可读；可选盲腔作为美术布局，不声称所有海蚀洞如此。不能只画黑洞或把旧石拱封一面当新形态，水场景另分。 |
| `cruziana-crawling-furrow` | Cruziana crawling furrow / Cruziana 双叶爬行沟 | `items/cruziana-crawling-furrow/` | 长条双沟与重复斜刮痕补充潮间带表面潜迹，区别于U/Y管道剖面。 按原凹陷印迹：成对沟槽与方向一致的斜向刮痕在灰色顶/斜视可读，底板不是识别依据。示意布局，不复制出土标本，也不因为邻近Asaphus就指定制造者。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。

独立QA优先新上下文，先填/核对batch-31-QA-SCOPE.json实际source/逐项GLB hash与恰好四ID；错批/错source即invalid_review_wrong_subject，不计PASS或据其修错模型。当前scope未就绪，planner不启动QA。catalog_facets按原字段，research pack不是已发布pack。壳体只标本；潜迹保留凹/凸显示方式，不指定制造者；岩层/槽模按灰色露面检查而非外轮廓。
