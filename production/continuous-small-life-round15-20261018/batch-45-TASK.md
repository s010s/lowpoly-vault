# batch-45 — 仅计划，尚未派发

**当前父任务进度：线上确认163；37–39目标175发布中，未记为上线；40–42独立QA全PASS排队；43QA进行中、44/45制作中。一轮独立QA、必修处差异复核、发布必要上线检查。双栏网站仅PRD讨论，未批准实现，不改UI或信息架构。最新state/派发覆盖旧空claim。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/真实授权素材足够即可inspired-by风格化，继承来源不伪造已读。Dillhoffia只果体/宿存萼、Joffrea只一种成熟态的附果枝段，Yochelcionella只帽壳/管口；不外推完整生物或母株。两件遗迹保留凸起化石浮雕，不指定制造者。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

按用户最新要求只进行一轮独立模型QA，由父任务总协调。发布复用相同hash已接受证据，只做必要上线检查，不新增重复模型验收；真实缺陷/模型hash变化交父任务针对性处理，不自动再开整轮QA，不伪造或复用不匹配PASS。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `tokummia` | Tokummia pincer-bearing mandibulate / Tokummia（钳肢有颚动物） | `items/tokummia/` | 宽双瓣甲罩长躯干并伸出醒目大钳，丰富抓取型海生节肢动物，区别于短前爪体和尾桨甲体。 宽甲、长分节躯体与成对前端大钳有比例/关节关系，钳根自然且开合空隙可读；不是Waptia加夹子或Callichimaera拉长。微肢节/颚器计数可经济简化，不承诺抓取动画。 |
| `obsidian-flow-face` | Obsidian flow face / 黑曜岩流面 | `items/obsidian-flow-face/` | 流带穿过玻璃质岩面和宽贝壳状断口，补充岩体流动—断裂结构，区别于小燧石结核。 原创露面中流带和大曲面断口共同表达，断口为岩石术语不是贝壳生物；非flint-nodule放大改黑或火山渣块抛光。材质克制不依赖镜面反射/透明藏形，不冒充实地点。 |
| `helictite` | Helictite / 卷曲石 | `items/helictite/` | 细矿物管偏离竖直方向弯折并分叉，增加小型洞穴生长形态，区别于薄片帘与金属枝晶。 连续细管主次分叉、偏离重力的弯曲和附着面关系明确，不是自然铜枝晶换白或随机弯铁丝。少量有效分枝展示形态，不强求微孔/精确生长机制，挂点/支撑另记。 |
| `protovirgularia-chevron-trail` | Protovirgularia chevron trail / Protovirgularia 人字形爬迹 | `items/protovirgularia-chevron-trail/` | 沿狭窄轴迹串联V形纹补充双侧步进轨迹节奏，区别于重叠叶瓣曲迹和分叉潜穴。 原raised-fossil-relief：有几何高度的连续V纹附着于窄轴迹，V的方向与主轴连续；非Nereites叶瓣改角度或Cruziana改纹理。灰色内形可读，不指定制造者/行为速度、不复制标本。 |

采用static-stylized-v1 / 2026-10-18.1。publication_authority=separate，授权policy单独pin；profile-policy.json仅规划说明，真实candidate就绪才生成sidecar，显式校验新profile，最终加--require-approved。fixed8/零转台；额外诊断另存。来源consulted-only/incorporated=false/非空rights_note，实际素材须真实授权，原创贴图自带provenance。结构化blockers及criterion ID匹配brief；legacy_result照实保留，profile兼容不等于valid/approved、模型QA或发布。
独立QA优先新上下文，先填核batch-45-QA-SCOPE.json真实source/逐项GLB hash及恰好四ID，错对象invalid_review_wrong_subject，不计PASS、不据其修错模型。catalog_facets原样保留，research pack不是已发布pack。

详读review-policy.json：用户最新一轮独立QA规则优先于历史模板的重复验收解释。

必修处只差异复核，发布不额外重复全批模型验收。
