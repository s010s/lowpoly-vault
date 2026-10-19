# batch-36 — 仅计划，尚未派发

**当前父任务进度：线上163已完成，34–36已发布；37/38QA通过，39仅aa-lava-front需外轮廓必修；40QA通过，41/42制作中。只一轮独立全批QA，必修处差异复核，发布必要上线检查，不重复全批验收。见round15/review-policy.json；以最新state及父任务派发为准。**

**当前父任务进度：34–36独立QA全PASS；37候选完成正在QA，38/39制作中。main manifest观察151，planner未核公网。用户最新规则：一轮独立QA，父任务总协调，发布仅必要上线检查、不重复模型验收；详见round14/review-policy.json。最新state和派发覆盖历史空claim。**

**当前父任务进度：main已推进127，公网证据核对中（此前确认115）；31–33独立模型QA全PASS；34制作中、35候选完成待QA、36已派制作。模型QA/正式profile/提交发布/公网确认分别记录，当前state及父任务派发覆盖历史空claim。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Cooperoceras/Gryphaea仅保存壳、Sabalites仅扇叶；遗迹限凹印/木质剖面，不指定制造者或树种；自然地貌/矿物不宣称共存古地点。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `gryphaea` | Gryphaea curved oyster fossil / Gryphaea（弯曲牡蛎化石） | `items/gryphaea/` | 深钩状下壳与较平盖壳补充不对称双壳标本，区别于横向长翼壳和盘卷壳。 仅壳体标本，钩曲下壳与上盖边缘/铰接关系自然，不加无依据软体/足。不是把普通贝壳压弯改色，主下壳体积与小盖关系是结构重点。 |
| `folded-strata-outcrop` | Folded strata outcrop / 褶皱地层露头 | `items/folded-strata-outcrop/` | 连续岩层弯曲成背斜/向斜，补充与截切交错层不同的内部结构。 几条主要岩层连续弯曲、厚度/转折有逻辑，灰色露面和轮廓都有信息；不能只旋转旧层崖或贴弯条纹。剖面/层数为教学选择，不声称精确应变、古地点或年代。 |
| `volcanic-bomb` | Volcanic bomb / 火山弹 | `items/volcanic-bomb/` | 选一件流线梭形凝固喷出块，补充不同于圆钝燧石结核的火山自然物。 本次仅选梭形构图，连续粗细变化与克制冷却壳结构；不另计面包壳/破损/颜色变体。不要做现代炸弹或爆炸场景，名义尺寸与表面起伏属美术。 |
| `teredolites-wood-boring-cast` | Teredolites wood-boring cast / Teredolites 木质钻孔铸型 | `items/teredolites-wood-boring-cast/` | 木化石块内棒端膨大的钻孔/铸填结构补充木质内部生态遗迹，区别于泥中U/Y潜道。 按原结构剖面显示木质宿主与棒端膨大的钻孔/铸型关系，不能只给旧枯木贴黑孔；剖切示意非真实标本复制。不指定树种或制造者，不另计一件完整枯木或活体动物。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。

独立QA优先新上下文，先填/核对batch-36-QA-SCOPE.json真实source/逐项GLB hash和恰好四ID，错批/错source即invalid_review_wrong_subject、不计PASS且不据其修错模型。scope当前未就绪。shell/frond只原标本范围；遗迹检查灰色内部/剖面、不指定制造者；catalog_facets原样保留，research pack非已发布pack。
