# batch-13 — 仅计划，尚未派发

**当前状态：线上79已确认（main eb9153eab06f7e95235eac30611b731c8178ffb7）；16/18旧错批QA无效，16新线程01a150f1-ab04-71eb-af42-0a2fc9450036、18新线程01a150f5-9dfe-77e0-bd27-6cbc89942035审正确source；17模型QA PASS；19新QA运行、20模型QA PASS、21制作中。错批报告不计PASS，最新state/派发证明覆盖历史描述。**

**当前状态：线上67已确认（main ccf48bb446dd4d0a710ab14dfc05d6fbf7064cdb，PR9/Pages/public Chromium均PASS）；13–15全模型QA PASS、67→79发布容量失败待恢复，不影响已完成67；16–17候选完成/QA运行无结论，18独占制作。以最新state和父任务派发证明覆盖下方历史空claim/未派发/旧线上数量。**

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Cobbania与Pluricarpellatia保持淡水标签；叠层石是生态构造不是珊瑚；岩体教学露面不冒充精确古地点。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `acrocyathus` | Acrocyathus clustered rugose coral / Acrocyathus（簇生四射珊瑚） | `items/acrocyathus/` | 簇生长多边杯和放射内壁补充群体四射珊瑚，区别于蜂巢细管群体。 长多边杯成簇且内部放射隔壁可读，杯间有真实结构节奏；不要复用Favosites蜂巢只改孔数/密度。微观板壁、完整软体与精确杯数可简化。 |
| `sawdonia` | Sawdonia spiny branching shoots / Sawdonia 刺轴植物 | `items/sawdonia/` | 稀疏刺列、弯钩顶端与枝层空隙丰富早期地表植物，区别于光滑裸轴或K节点匍匐植物。 分叉轴自然衔接，少量有方向的刺列和钩曲顶端表达身份；不是对旧裸轴随机加刺。微小表皮/气孔或精确刺数不强加。 |
| `leanchoilia` | Leanchoilia whip-fingered arthropod / Leanchoilia（鞭指节肢动物） | `items/leanchoilia/` | 三指大附肢拖长丝与矛头尾提供新的小型节肢动物轮廓，区别于角棘头盾。 大附肢三指与长丝、连贯分节体和矛头尾可读；以少量有用细丝表达，不做无穷细须。小肢精确节数/软组织可合理简化。 |
| `septarian-concretion` | Septarian concretion / 龟甲石结核 | `items/septarian-concretion/` | 圆结核内部的分叉矿物填充裂隙提供近景地质结构，与泥裂地面不同。 保留圆状结核体与可见内部矿物填充网；可用一处有意教学切面显示内部，切面是展示选择不是原地自然断裂事实。不能把表面Voronoi裂纹或泥裂缩球当成结核。 |

显式采用main已合并 `static-stylized-v1` / `2026-10-18.1`，先读README的profile步骤与profile-policy.json。候选就绪后绑定真实hash生成sidecar，再显式运行新profile；默认legacy-v1不是此任务验收入口。fixed8恰好每标签一张、零转台，不伪造left/right。references.sources[].use=consulted-only、incorporated=false，每项有真实title/url/rights_note，全局no_incorporated_third_party_assets=true；不猜测第三方license。blockers用结构对象，criterion IDs从本brief派生并逐项一致。profile合同兼容PASS不等于valid/approved/model QA/发布PASS；历史legacy_result保留。
