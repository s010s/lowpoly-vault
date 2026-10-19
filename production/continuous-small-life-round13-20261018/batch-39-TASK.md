# batch-39 — 仅计划，尚未派发

**当前round17观察：main提交175（37–39发布描述符），planner未核公网；163仅历史已确认公网checkpoint。父任务明确46–48制作中，全部保留独占，不因已有候选/handoff/QA分支推断新结论或重复领取。一轮独立QA、必修处差异复核；本任务不改网站、模型、CI。**

**当前父任务进度：线上确认163；37–39目标175发布中，未记为上线；40–42独立QA全PASS排队；43QA进行中、44/45制作中。一轮独立QA、必修处差异复核、发布必要上线检查。双栏网站仅PRD讨论，未批准实现，不改UI或信息架构。最新state/派发覆盖旧空claim。**

**当前父任务进度：线上163已完成，34–36已发布；37/38QA通过，39仅aa-lava-front需外轮廓必修；40QA通过，41/42制作中。只一轮独立全批QA，必修处差异复核，发布必要上线检查，不重复全批验收。见round15/review-policy.json；以最新state及父任务派发为准。**

**当前父任务进度：34–36独立QA全PASS；37候选完成正在QA，38/39制作中。main manifest观察151，planner未核公网。用户最新规则：一轮独立QA，父任务总协调，发布仅必要上线检查、不重复模型验收；详见round14/review-policy.json。最新state和派发覆盖历史空claim。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Schizoneura仅分节枝段、Nelumbo仅盾叶浮雕；Diplomoceras/Clavagella仅原壳体/钙质管标本，不外推完整生物。遗迹保留原剖面/凸浮雕，不指定制造者；自然物不指定实际古地点。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `clavagella` | Clavagella bottle-tube bivalve / Clavagella（瓶管双壳类） | `items/clavagella/` | 小壳瓣融入膨大钙质管和长颈，补充底栖管壳标本，区别于钩曲牡蛎。 仅保存的壳瓣/钙质管结构标本：膨大部、嵌入小壳瓣和长颈有自然连续关系，不是瓶子加普通贝壳。不补未知虹吸管/软体/生活姿态，细管数量和种级尺寸不外推。 |
| `aa-lava-front` | Aa lava front / 渣状熔岩前缘 | `items/aa-lava-front/` | 连续熔岩体上覆盖角砾状渣块，提供与绳状及枕状熔岩不同的前缘结构。 可读连续基体和不等尺度渣块覆盖前缘，重量/堆积有逻辑；不是给pahoehoe加均匀噪声、散布等大石块或把枕瓣锐化。只计一个构图，无火/烟/模拟或指定海岸火山事件承诺。 |
| `native-copper-dendrite` | Native copper dendrite / 自然铜枝晶 | `items/native-copper-dendrite/` | 金属分枝晶与不规则扁平端部丰富小型自然标本，区别于立方或十字晶簇。 不等粗连续分叉、扁平端部与适度金属响应共同识别，不是Vauxia/陆生枝条换铜色或工业导线；形态在灰色也可读。非精确矿点标本，微枝数量不强求，展示支点另记。 |
| `nereites-lobed-meander` | Nereites lobed meander / Nereites 叶瓣曲行迹 | `items/nereites-lobed-meander/` | 曲行轴管两侧交替交叠叶瓣补充取食迹，区别于网格迹和双叶爬行沟。 原raised-fossil-relief：轴管曲行、两侧交替重叠叶瓣为真实起伏，不是涂曲线或Cruziana加密。内部灰色顶/斜视读结构，不指定造迹生物；不把Neonereites/Scalarituba另计新对象。 |

采用static-stylized-v1 / 2026-10-18.1。publication_authority=separate，授权policy单独pin；profile-policy.json仅规划说明，真实candidate就绪才生成sidecar，显式校验新profile，最终加--require-approved。fixed8/零转台；额外诊断另存。来源consulted-only/incorporated=false/非空rights_note，实际素材须真实授权，原创贴图自带provenance。结构化blockers及criterion ID匹配brief；legacy_result照实保留，profile兼容不等于valid/approved、模型QA或发布。
独立QA优先新上下文，先填核batch-39-QA-SCOPE.json真实source/逐项GLB hash及恰好四ID，错对象invalid_review_wrong_subject，不计PASS、不据其修错模型。catalog_facets原样保留，research pack不是已发布pack。
