# batch-10 — 仅计划，尚未派发

**当前状态：线上67已确认（main ccf48bb446dd4d0a710ab14dfc05d6fbf7064cdb，PR9/Pages/public Chromium均PASS）；13–15全模型QA PASS、67→79发布容量失败待恢复，不影响已完成67；16–17候选完成/QA运行无结论，18独占制作。以最新state和父任务派发证明覆盖下方历史空claim/未派发/旧线上数量。**

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。本轮Limnobiophyllum只作淡水岸边植物；波痕、贝壳灰岩和泥裂是地表/岩体过程概念，不伪称精确史前地点；珊瑚只需可靠基础辨识，不强加显微复原。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `flabellum` | Flabellum fan-wedge coral / Flabellum（扇楔珊瑚） | `items/flabellum/` | 侧扁扇楔单体珊瑚补充宽刃杯轮廓，区别于先前圆杯/管枝/迷宫群体。 侧扁楔形单体杯与宽刃状上口可读；保持厚度和自然杯壁，不是圆锥杯压扁缩放变体。内部隔壁只做有用节奏，不要求种级微观计数。 |
| `horneophyton` | Horneophyton corm-based shoots / Horneophyton 角蕨类植物 | `items/horneophyton/` | 膨大基体与分叉孢子囊带来小型直立早期植物，区别于首轮根茎拱。 膨大基体清楚可见，直立分叉轴与孢子囊柔和连续连接；不是简单Aglaophyton换密度。保留原清单器官区别，不另强求组织切片或孢子微观结构。 |
| `wave-ripple-surface` | Wave ripple surface / 波浪波痕面 | `items/wave-ripple-surface/` | 对称波脊与圆钝波谷提供浅水/岸边可走近地表，不增加水体贴图负担。 连续对称波脊和圆钝波谷，用有秩序但非机械完全等间距的几何表达；地表块有浅厚度和明示边界，不把波纹误称单向流水纹或装饰噪声。场景需要拼接时另核接缝，不承诺所有地块无缝。 |
| `gogia` | Gogia brachiole-crowned eocrinoid / Gogia（腕丝冠始海百合类） | `items/gogia/` | 短基部梨形板杯与取食腕丝冠丰富小型固着海底生物，区别于Saccocoma无柄开放分枝。 短基部、梨形小杯和细腕丝冠自然衔接；用少量清楚的冠枝表达，而非完整显微板列/腕丝计数。不把它做成海星或植物花朵，颜色/名义高度为美术选择。 |

新候选采用最新main的显式 `static-stylized-v1` profile（规则2026-10-18.1），机器字段 `publication_authority: separate`；用户批量发布授权另pin到profile-policy.json的policy。实际candidate生成后再用scripts/candidate_profile.py生成绑定真实hash的sidecar；不得预填假hash或称profile PASS。保留legacy错误，blockers用结构对象、criterion IDs与brief一致；模型QA PASS、candidate/profile PASS和发布状态分别记录。
