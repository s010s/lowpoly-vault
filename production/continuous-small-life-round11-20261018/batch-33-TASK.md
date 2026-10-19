# batch-33 — 仅计划，尚未派发

**当前父任务进度：main已推进127，公网证据核对中（此前确认115）；31–33独立模型QA全PASS；34制作中、35候选完成待QA、36已派制作。模型QA/正式profile/提交发布/公网确认分别记录，当前state及父任务派发覆盖历史空claim。**

**当前父任务进度：线上确认115、22–24已发布；25–27发布整合中（27报告内容PASS与其正式profile阻塞分开保留）；28–30模型QA均PASS；31–33候选全完成且已派独立QA、无结论。最新state/父任务派发证明覆盖历史初始空claim，不从模型QA推断发布。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Baculites/Mucrospirifer只做保存壳体，不生造软体；潜迹只按原阴/阳浮雕教学、不指定制造者；海岸地形保留米制代表片区，不假称古地点测绘。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `mucrospirifer` | Mucrospirifer wing-tip brachiopod / Mucrospirifer（长翼腕足动物） | `items/mucrospirifer/` | 极长铰合翼越出短褶肋中央壳，补充横向腕足壳体标本。 仅保存壳体：长铰合翼、短中央壳与基本褶肋连续，不是Trapa四角果改材质或普通贝壳拉宽。不添加无依据活体软组织/足，微肋数可简化。 |
| `wave-cut-platform` | Wave-cut platform / 海蚀平台 | `items/wave-cut-platform/` | 退缩海崖前宽低岩台补充步行尺度岸边层次，区别于高瀑布岩阶或海蚀柱。 连续宽低磨蚀岩台与后缘退缩岩面关系可读，保留原landscape类别，不缩成小石。代表片区和名义尺寸非古地点实测，水面/岩壁裁切边界明确。 |
| `flute-cast-slab` | Flute cast slab / 槽模岩板 | `items/flute-cast-slab/` | 岩板底面同向匙状凸模补充方向性沉积浮雕，区别于波纹和凹陷爬迹。 保持原凸模而非凹沟：同向渐尖匙状隆起在灰色露面可读，可翻转露出层底作为展示选择。不是动物足迹或随机小石，不伪称真实出土标本或精确流向测定。 |
| `paleodictyon-mesh-trace` | Paleodictyon mesh trace / Paleodictyon 网格潜迹 | `items/paleodictyon-mesh-trace/` | 沉积层下六角管网的正浮雕模式补充规则闭合潜迹图案，区别于开放Y节点网络。 按原凸起化石浮雕教学显示相连细管六角网与基底关系；闭合网格结构是关键，不能只是Thalassinoides增密或把Fenestella平放。不是活体珊瑚/蜂巢，不指定制造者；示意非出土复制。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。

独立QA优先新上下文，先填/核对batch-33-QA-SCOPE.json实际source/逐项GLB hash与恰好四ID；错批/错source即invalid_review_wrong_subject，不计PASS或据其修错模型。当前scope未就绪，planner不启动QA。catalog_facets按原字段，research pack不是已发布pack。壳体只标本；潜迹保留凹/凸显示方式，不指定制造者；岩层/槽模按灰色露面检查而非外轮廓。
