# batch-43 — 仅计划，尚未派发

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/真实授权素材足够即可inspired-by风格化，继承来源不伪造已读。Dillhoffia只果体/宿存萼、Joffrea只一种成熟态的附果枝段，Yochelcionella只帽壳/管口；不外推完整生物或母株。两件遗迹保留凸起化石浮雕，不指定制造者。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

按用户最新要求只进行一轮独立模型QA，由父任务总协调。发布复用相同hash已接受证据，只做必要上线检查，不新增重复模型验收；真实缺陷/模型hash变化交父任务针对性处理，不自动再开整轮QA，不伪造或复用不匹配PASS。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `kootenayscolex` | Kootenayscolex head-bristled annelid / Kootenayscolex（头部具毛环节动物） | `items/kootenayscolex/` | 中段宽、两端细并带头刚毛的环节动物丰富小型海底生命，区别于管中虫及有甲多毛动物。 连续分节躯体宽中段向两端渐细，头部刚毛束和短中央触角形成识别重点；非Canadia改色或Ottoia加均匀刺。刚毛根部自然、数量克制，不做微毛精确复原。 |
| `dillhoffia` | Dillhoffia funnel-calyx fruit / Dillhoffia 漏斗萼果化石 | `items/dillhoffia/` | 长果体外的宽圆漏斗宿存萼提供新的植物繁殖器官，区别于角果与翼果。 仅原化石果体/宿存萼标本：中央长体连至浅外张盘，主要放射脊有起止；不做莲蓬/花朵，不推断母树、叶根或不明科级形态。 |
| `beach-ridge` | Beach ridge / 海滩堤脊 | `items/beach-ridge/` | 活动前滨后方平行岸线的低沉积脊丰富陆侧岸线结构，区别于离岸沙岛与连接陆岛的细颈。 同一裁片中前滨、其后低岸平行脊与陆侧缓坡关系清楚；非barrier-island移到陆地或wave-ripple放大。14m仅教学裁片，非实测全海滩/岸线年龄，水灯另展示。 |
| `phycodes-palmate-burrow` | Phycodes palmate burrow / Phycodes 掌状潜穴 | `items/phycodes-palmate-burrow/` | 单主管末端紧凑扫帚状分支补充取食迹的终端结构，区别于连续分叉网。 原raised-fossil-relief：一根主管末端分为紧凑扫帚状末枝，管与末枝几何连贯；非Thalassinoides减少分支或藻枝改色。灰色顶斜视看内部结构，不指定制造者或复制出土标本。 |

采用static-stylized-v1 / 2026-10-18.1。publication_authority=separate，授权policy单独pin；profile-policy.json仅规划说明，真实candidate就绪才生成sidecar，显式校验新profile，最终加--require-approved。fixed8/零转台；额外诊断另存。来源consulted-only/incorporated=false/非空rights_note，实际素材须真实授权，原创贴图自带provenance。结构化blockers及criterion ID匹配brief；legacy_result照实保留，profile兼容不等于valid/approved、模型QA或发布。
独立QA优先新上下文，先填核batch-43-QA-SCOPE.json真实source/逐项GLB hash及恰好四ID，错对象invalid_review_wrong_subject，不计PASS、不据其修错模型。catalog_facets原样保留，research pack不是已发布pack。

详读review-policy.json：用户最新一轮独立QA规则优先于历史模板的重复验收解释。

必修处只差异复核，发布不额外重复全批模型验收。
