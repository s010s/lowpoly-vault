# batch-50 — 仅计划，尚未派发

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态和原创/真实授权素材足够即可inspired-by风格化；继承来源不伪造本次已读，微观未知如实标注，不追加耗时科研gate。Belosaepia仅内壳，Czekanowskia仅叉叶短枝，Tempskya仅假干切面，不补完整生物。两件遗迹保持原negative-impression，不指定制造者。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

按用户最新要求只进行一轮独立模型QA，由父任务总协调。发布复用相同hash已接受证据，只做必要上线检查，不新增重复模型验收；真实缺陷/模型hash变化交父任务针对性处理，不自动再开整轮QA，不伪造或复用不匹配PASS。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `belosaepia` | Belosaepia pronged internal shell / Belosaepia（弯刺内壳） | `items/belosaepia/` | 厚后部弯刺与前部扩展薄板补充头足类内壳标本，区别于外帽壳/螺壳/长号管壳。 只原内骨骼标本：厚后体和长弯后刺过渡至扩展前薄板，厚薄层次清楚；非螺壳拉平或鱼骨随意拼接。省微小壳室，不凭内壳补全软体乌贼、触腕或生活比例。 |
| `tempskya` | Tempskya composite false-trunk specimen / Tempskya 假干蕨 | `items/tempskya/` | 根群包埋多小茎的切面假干补充植物内部结构，区别于单枝、叶冠与普通木段。 仅一件切面假干标本，以不规则小茎岛和交织根带表达内部复合构造；不是枯木端面打同心圆孔。不加未知活体树冠/叶序，也不把多根小茎另计多个资产。 |
| `karst-sinkhole` | Karst sinkhole / 喀斯特落水洞 | `items/karst-sinkhole/` | 封闭漏斗向地下空洞过渡，为岸边陆侧提供向下空间，区别于向明渠开口的泉口。 本次选一种封闭漏斗构图，周缘汇入中心的真实凹度及下方空腔关系可读；非karst-spring-mouth堵口或深潭无水换色。6m为名义裁片，无特定地点/塌陷事件/年代，水非必需。 |
| `fault-scarp` | Fault scarp / 断层崖 | `items/fault-scarp/` | 断层阶坎错开两侧地表，补充自然剖面的位移关系，区别于侵蚀海崖和连续折层。 两侧地面及可对照结构被一处平面阶坎错开，灰色露面有方向/高差，不是旧台阶地形换色或直线切两块石。不声称地震事件、滑移量或实际古地点，8m是示意裁片。 |

采用static-stylized-v1 / 2026-10-18.1。publication_authority=separate，授权policy单独pin；profile-policy.json仅规划说明，真实candidate就绪才生成sidecar，显式校验新profile，最终加--require-approved。fixed8/零转台；额外诊断另存。来源consulted-only/incorporated=false/非空rights_note，实际素材须真实授权，原创贴图自带provenance。结构化blockers及criterion ID匹配brief；legacy_result照实保留，profile兼容不等于valid/approved、模型QA或发布。
独立QA优先新上下文，先填核batch-50-QA-SCOPE.json真实source/逐项GLB hash及恰好四ID，错对象invalid_review_wrong_subject，不计PASS、不据其修错模型。catalog_facets原样保留，research pack不是已发布pack。

详读review-policy.json：用户最新一轮独立QA规则优先于历史模板的重复验收解释。

必修处只差异复核，发布不额外重复全批模型验收。

双栏网站仅PRD讨论、未批准实现，不改UI或信息架构。

本轮仅规划：不改网站/信息架构、模型或CI，不用Mac/Drive。
