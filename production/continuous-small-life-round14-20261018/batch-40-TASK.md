# batch-40 — 仅计划，尚未派发

**当前父任务进度：线上确认163；37–39目标175发布中，未记为上线；40–42独立QA全PASS排队；43QA进行中、44/45制作中。一轮独立QA、必修处差异复核、发布必要上线检查。双栏网站仅PRD讨论，未批准实现，不改UI或信息架构。最新state/派发覆盖旧空claim。**

**当前父任务进度：线上163已完成，34–36已发布；37/38QA通过，39仅aa-lava-front需外轮廓必修；40QA通过，41/42制作中。只一轮独立全批QA，必修处差异复核，发布必要上线检查，不重复全批验收。见round15/review-policy.json；以最新state及父任务派发为准。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Botrychium仅育性残片，不拼未相连营养片；Dicroidium仅Y叉叶，不外推整株或混合羽片。两件遗迹均原结构剖面，不指定制造者；自然物不指定实际古地点。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

按用户最新要求只进行一轮独立模型QA，由父任务总协调。发布复用相同hash已接受证据，只做必要上线检查，不新增重复模型验收；真实缺陷/模型hash变化交父任务针对性处理，不自动再开整轮QA，不伪造或复用不匹配PASS。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `sidneyia` | Sidneyia broad-bodied hunter / Sidneyia（宽体节肢动物） | `items/sidneyia/` | 宽叠甲躯干突然收为窄环尾和尾桨，补充底栖猎食节肢动物，区别于双瓣甲游泳体。 宽躯干叠甲—窄腹环—尾桨过渡有整体比例和自然关节，不是Asaphus加尾或Waptia放大甲。肢组经济可读，不强求微毛/关节计数或捕食动画。 |
| `botrychium` | Botrychium fertile-frond specimen / Botrychium 阴地蕨类化石 | `items/botrychium/` | 育性残片上的成簇圆孢子囊补充植物繁殖器官，不再增加整株蕨冠。 仅一件有记录育性枝浅浮雕，孢子囊簇与枝轴连续；未相连营养片段不得拼成整株，不添加未知根茎/叶丛，非现代种完整复原。 |
| `barrier-island` | Barrier island / 障壁岛 | `items/barrier-island/` | 离岸长条沙岛将外海与潟湖分隔，为岸边增加内外水域关系，区别于连岛细颈。 长岛与大陆之间保留潟湖通道、面向外海另一侧岸线清楚；不能把tombolo剪断一端或sand-spit换方向。20m仅代表教学裁片非实测全岛，水/灯光另作展示不计新资产。 |
| `diplocraterion-spreite-burrow` | Diplocraterion spreite burrow / Diplocraterion 蹼状U形潜穴 | `items/diplocraterion-spreite-burrow/` | U管间连续叠层片补充向上/下迁移的潜穴结构，区别于简单U形管。 原sectional-structure：U形管两臂之间必须有真正可读连续叠层片，不能只复制Arenicolites加表纹或多摆一条U管。灰色内部剖面检查，不指定造迹物种、事件时间或复制标本。 |

采用static-stylized-v1 / 2026-10-18.1。publication_authority=separate，授权policy单独pin；profile-policy.json仅规划说明，真实candidate就绪才生成sidecar，显式校验新profile，最终加--require-approved。fixed8/零转台；额外诊断另存。来源consulted-only/incorporated=false/非空rights_note，实际素材须真实授权，原创贴图自带provenance。结构化blockers及criterion ID匹配brief；legacy_result照实保留，profile兼容不等于valid/approved、模型QA或发布。
独立QA优先新上下文，先填核batch-40-QA-SCOPE.json真实source/逐项GLB hash及恰好四ID，错对象invalid_review_wrong_subject，不计PASS、不据其修错模型。catalog_facets原样保留，research pack不是已发布pack。

详读review-policy.json：用户最新一轮独立QA规则优先于历史模板的重复验收解释。
