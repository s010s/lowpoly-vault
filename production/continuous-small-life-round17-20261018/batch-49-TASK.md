# batch-49 — 仅计划，尚未派发

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态和原创/真实授权素材足够即可inspired-by风格化；继承来源不伪造本次已读，微观未知如实标注，不追加耗时科研gate。Belosaepia仅内壳，Czekanowskia仅叉叶短枝，Tempskya仅假干切面，不补完整生物。两件遗迹保持原negative-impression，不指定制造者。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

按用户最新要求只进行一轮独立模型QA，由父任务总协调。发布复用相同hash已接受证据，只做必要上线检查，不新增重复模型验收；真实缺陷/模型hash变化交父任务针对性处理，不自动再开整轮QA，不伪造或复用不匹配PASS。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `diania` | Diania cactus-limbed lobopodian / Diania（仙人掌足叶足动物） | `items/diania/` | 细躯干下的粗壮多刺叶足补充底栖动物重心，区别于裸长躯干/前部集中细臂。 细连续躯干与粗叶足形成鲜明比例，叶足基部自然有负空间；非Hallucigenia加粗腿或Facivermis移腿。保留主要刺节奏，微刺/细软体可省，不作已解决系统发育或行走动画断言。 |
| `czekanowskia` | Czekanowskia forked-thread short shoots / Czekanowskia 茨康叶植物 | `items/czekanowskia/` | 短枝上的细带反复二叉叶补充线性叶器官，区别于羽片叶和缩叶分节枝。 仅原短枝/叶标本，细角状带片从紧凑短枝长出、主要二叉可读；不是针叶丛贴图或Pseudofrenelopsis加叶数。不假设整树冠、繁殖联系或现代银杏物种。 |
| `natural-levee` | Natural levee / 天然堤 | `items/natural-levee/` | 沿河槽两侧低沉积堤脊补充水边微地形，区别于单条海岸脊及扇形沉积面。 同一裁片包含主河槽、近岸成对低堤与向后低平面，高差服从河岸结构；非beach-ridge复制一条或河道简单加墙。14m为教学裁片非全河测绘，不承诺水动力/泛滥事件，水灯另展示。 |
| `lockeia-resting-trace` | Lockeia resting trace / Lockeia 杏仁状停栖迹 | `items/lockeia-resting-trace/` | 两端尖收的紧凑杏仁凹印补充静止印迹，区别于双列步迹和浅星状腕印。 原negative-impression：杏仁形浅凹有明确两端收尖、内部凹度与边缘过渡，不是涂黑叶形或完整贝壳压入。不指定双壳物种/制造者，灰色顶斜视检查内部形态，不以外底板识别。 |

采用static-stylized-v1 / 2026-10-18.1。publication_authority=separate，授权policy单独pin；profile-policy.json仅规划说明，真实candidate就绪才生成sidecar，显式校验新profile，最终加--require-approved。fixed8/零转台；额外诊断另存。来源consulted-only/incorporated=false/非空rights_note，实际素材须真实授权，原创贴图自带provenance。结构化blockers及criterion ID匹配brief；legacy_result照实保留，profile兼容不等于valid/approved、模型QA或发布。
独立QA优先新上下文，先填核batch-49-QA-SCOPE.json真实source/逐项GLB hash及恰好四ID，错对象invalid_review_wrong_subject，不计PASS、不据其修错模型。catalog_facets原样保留，research pack不是已发布pack。

详读review-policy.json：用户最新一轮独立QA规则优先于历史模板的重复验收解释。

必修处只差异复核，发布不额外重复全批模型验收。

双栏网站仅PRD讨论、未批准实现，不改UI或信息架构。

本轮仅规划：不改网站/信息架构、模型或CI，不用Mac/Drive。
