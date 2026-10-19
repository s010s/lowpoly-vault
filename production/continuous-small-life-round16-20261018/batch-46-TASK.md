# batch-46 — 仅计划，尚未派发

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态和原创/真实授权素材足够即可inspired-by风格化；来源继承不伪造已读。Ecphora只壳，保留原四翼肋参考范围；Pseudofrenelopsis仅枝段，Pteleoidea仅翼果；不扩写整株或未知软体。Diplichnites保留凹陷印迹、Treptichnus保留结构剖面，不指定制造者。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

按用户最新要求只进行一轮独立模型QA，由父任务总协调。发布复用相同hash已接受证据，只做必要上线检查，不新增重复模型验收；真实缺陷/模型hash变化交父任务针对性处理，不自动再开整轮QA，不伪造或复用不匹配PASS。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `eiffelia` | Eiffelia lattice-sac sponge / Eiffelia（格架囊海绵） | `items/eiffelia/` | 圆薄壁囊的相扣星状格面补充海绵形态，区别于纵翼锥杯、细管和分枝灌丛。 整体圆囊、薄壁与相扣星状格面保持生长逻辑，主要格架有主次；不是Leptomitus缩短、旧泡沫石换色或工业均匀网球。微骨针/精确格目数可简化，不声称生理力学复原。 |
| `pseudofrenelopsis` | Pseudofrenelopsis jointed conifer shoots / Pseudofrenelopsis 拟节柏枝 | `items/pseudofrenelopsis/` | 渐细分节针叶树枝配缩叶鞘缘，增加植物枝段结构，区别于宽对生裂鞘和羽状叶。 仅化石枝段：光滑渐细节间、清楚鞘缘和微小叶尖连续；不是Schizoneura缩叶数量或竹节换色。不推断整树冠/树干/根、现代种或完整生境。 |
| `alluvial-fan` | Alluvial fan / 冲积扇 | `items/alluvial-fan/` | 单入流沟向外展宽的扇形沉积面丰富岸边陆侧坡脚，区别于河海三角洲叶瓣。 扇顶单入流、沿坡展宽沉积面及放射浅分流有整体高差，非river-dominated-delta去水或多放几条沟。18m为教学裁片，非实测全扇；不指定海岸、年代或完整流域，水灯另展示。 |
| `diplichnites-paired-trackway` | Diplichnites paired trackway / Diplichnites 双列足迹 | `items/diplichnites-paired-trackway/` | 两列分离小足印与中央空道补充步迹结构，区别于轴上V纹和双叶连续沟。 原negative-impression：两列真正凹入的独立足印，中央留空而不添尾沟；非Protovirgularia擦掉轴线或足印涂黑。灰色顶斜视可读凹陷，不能由步迹指定Arthropleura或其他制造者。 |

采用static-stylized-v1 / 2026-10-18.1。publication_authority=separate，授权policy单独pin；profile-policy.json仅规划说明，真实candidate就绪才生成sidecar，显式校验新profile，最终加--require-approved。fixed8/零转台；额外诊断另存。来源consulted-only/incorporated=false/非空rights_note，实际素材须真实授权，原创贴图自带provenance。结构化blockers及criterion ID匹配brief；legacy_result照实保留，profile兼容不等于valid/approved、模型QA或发布。
独立QA优先新上下文，先填核batch-46-QA-SCOPE.json真实source/逐项GLB hash及恰好四ID，错对象invalid_review_wrong_subject，不计PASS、不据其修错模型。catalog_facets原样保留，research pack不是已发布pack。

详读review-policy.json：用户最新一轮独立QA规则优先于历史模板的重复验收解释。

必修处只差异复核，发布不额外重复全批模型验收。

双栏网站仅PRD讨论、未批准实现，不改UI或信息架构。
