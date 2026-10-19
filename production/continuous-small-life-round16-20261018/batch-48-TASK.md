# batch-48 — 仅计划，尚未派发

**当前round17观察：main提交175（37–39发布描述符），planner未核公网；163仅历史已确认公网checkpoint。父任务明确46–48制作中，全部保留独占，不因已有候选/handoff/QA分支推断新结论或重复领取。一轮独立QA、必修处差异复核；本任务不改网站、模型、CI。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态和原创/真实授权素材足够即可inspired-by风格化；来源继承不伪造已读。Ecphora只壳，保留原四翼肋参考范围；Pseudofrenelopsis仅枝段，Pteleoidea仅翼果；不扩写整株或未知软体。Diplichnites保留凹陷印迹、Treptichnus保留结构剖面，不指定制造者。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

按用户最新要求只进行一轮独立模型QA，由父任务总协调。发布复用相同hash已接受证据，只做必要上线检查，不新增重复模型验收；真实缺陷/模型hash变化交父任务针对性处理，不自动再开整轮QA，不伪造或复用不匹配PASS。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `facivermis` | Facivermis tube-dwelling lobopodian / Facivermis（管栖叶足动物） | `items/facivermis/` | 五对前臂、裸长躯干及膨大固着后端补充前部取食型叶足动物，区别于全身等间距足。 五对带刺前臂集中前部，长裸躯干过渡至膨大后端；不要把Hallucigenia移腿或Selkirkia加满触角。臂根/体连接柔和，微刺克制；不外推无依据整管/复杂软体或取食动画。 |
| `cave-pearl-pool` | Cave pearl pool / 洞穴珠穴 | `items/cave-pearl-pool/` | 浅矿物凹盆内松散圆结核丰富低位自然集合体，区别于矿物枝晶与薄片墙。 浅盆有真实凹度，几枚不等大圆整结核聚集但可辨离散/接触关系；不是蛋窝改白、球体机械排阵或晶簇换材质。微层不强求，非指定洞址/测年或活体卵。 |
| `lava-tree-mold-crust` | Lava tree-mold crust / 熔岩树模地壳 | `items/lava-tree-mold-crust/` | 连续熔岩地壳中的深树干负形空腔补充自然包埋关系，区别于木化石孔和外露熔岩柱。 原负模：连续地壳围住深树干状空腔，内壁冷凝衬层和低树皮印痕；不是木头模型涂黑、独立空心柱或Teredolites换宿主。不计第二棵树/木材资产，不指定树种/古地点，来源现代过程不外推中生代现场。 |
| `treptichnus-serial-probe-burrow` | Treptichnus serial-probe burrow / Treptichnus 串列探穴 | `items/treptichnus-serial-probe-burrow/` | 曲折路线连接连续斜向短J探穴，补充串行探掘连接关系，区别于末端扫帚和连续网络。 原sectional-structure：曲折主路线在斜向节点接连续短J形探穴，内部剖面关系真实；非Phycodes拉长散开或潜穴网改密度。布局为原创教学示意，不指定制造者/行为机制或复制标本。 |

采用static-stylized-v1 / 2026-10-18.1。publication_authority=separate，授权policy单独pin；profile-policy.json仅规划说明，真实candidate就绪才生成sidecar，显式校验新profile，最终加--require-approved。fixed8/零转台；额外诊断另存。来源consulted-only/incorporated=false/非空rights_note，实际素材须真实授权，原创贴图自带provenance。结构化blockers及criterion ID匹配brief；legacy_result照实保留，profile兼容不等于valid/approved、模型QA或发布。
独立QA优先新上下文，先填核batch-48-QA-SCOPE.json真实source/逐项GLB hash及恰好四ID，错对象invalid_review_wrong_subject，不计PASS、不据其修错模型。catalog_facets原样保留，research pack不是已发布pack。

详读review-policy.json：用户最新一轮独立QA规则优先于历史模板的重复验收解释。

必修处只差异复核，发布不额外重复全批模型验收。

双栏网站仅PRD讨论、未批准实现，不改UI或信息架构。
