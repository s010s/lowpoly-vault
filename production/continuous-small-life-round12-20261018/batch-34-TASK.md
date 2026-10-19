# batch-34 — 仅计划，尚未派发

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
| `takakkawia` | Takakkawia eight-fin sponge / Takakkawia（八翼海绵） | `items/takakkawia/` | 渐细锥杯与纵向放射翼补充立体有翼海绵，区别于开盾杯/细管/刺管形态。 杯口外张、锥杯与八片纵翼自然连续，翼不是随机插片或海星臂；八翼属基本轮廓提示，微骨针/组织不强求。避免把旧杯形海绵仅加密度。 |
| `sabalites` | Sabalites costapalmate fan frond / Sabalites 扇叶棕榈化石 | `items/sabalites/` | 延伸中肋和手风琴式扇叶补充棕榈叶器官，区别于离散羽片的掌状蕨。 只保存costapalmate叶器官，主肋与长褶区连贯、化石外形有限保留；不添加假定树干、整株或现代海滩棕榈树冠。不以旧蕨叶改叶数计数。 |
| `river-dominated-delta` | River-dominated delta / 河流主导型三角洲 | `items/river-dominated-delta/` | 多个分流沉积叶瓣伸出岸线，补充不同于单一展宽河口的河海过渡空间。 连续河口片区形成分流与沉积叶瓣，不能把estuary-basin放大或增加随机沟数。20m为名义教学片区，保留原landscape类别，不声称完整真实三角洲测绘；水/灯光另分。 |
| `asteriacites-resting-impression` | Asteriacites resting impression / Asteriacites 星状停栖迹 | `items/asteriacites-resting-impression/` | 中央体区与五条展开腕迹形成浅星形凹印，补充表面停栖迹而非新活体海星。 原凹陷印迹，灰色顶/斜视要看清中央区与腕印深度，不用黑色星形贴图。布局是示意、非出土标本复制，不指定海星物种或因为邻近棘皮动物就指定制造者。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。

独立QA优先新上下文，先填/核对batch-34-QA-SCOPE.json真实source/逐项GLB hash和恰好四ID，错批/错source即invalid_review_wrong_subject、不计PASS且不据其修错模型。scope当前未就绪。shell/frond只原标本范围；遗迹检查灰色内部/剖面、不指定制造者；catalog_facets原样保留，research pack非已发布pack。
