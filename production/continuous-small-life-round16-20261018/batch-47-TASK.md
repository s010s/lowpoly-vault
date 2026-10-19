# batch-47 — 仅计划，尚未派发

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态和原创/真实授权素材足够即可inspired-by风格化；来源继承不伪造已读。Ecphora只壳，保留原四翼肋参考范围；Pseudofrenelopsis仅枝段，Pteleoidea仅翼果；不扩写整株或未知软体。Diplichnites保留凹陷印迹、Treptichnus保留结构剖面，不指定制造者。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

按用户最新要求只进行一轮独立模型QA，由父任务总协调。发布复用相同hash已接受证据，只做必要上线检查，不新增重复模型验收；真实缺陷/模型hash变化交父任务针对性处理，不自动再开整轮QA，不伪造或复用不匹配PASS。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `ecphora` | Ecphora flanged-rib snail / Ecphora（翼肋螺类） | `items/ecphora/` | 圆壳圈上四道宽外伸翼肋及长水管沟提供新壳轮廓，区别于帽壳管口和长号壳。 仅壳体标本，以原Miocene E. gardnerae gardnerae参考范围保留四道突出T形肋、壳圈/宽脐与长水管沟的关系。肋根自然融入壳体，不是普通螺壳加薄圆盘；不加未知软体/足或依赖棕色识别。 |
| `pteleoidea` | Pteleoidea notched winged fruit / Pteleoidea 环翅果化石 | `items/pteleoidea/` | 扁果宽环翅、顶缺口和细果柄补充翼果标本，区别于漏斗萼长果和连枝蓇葖。 仅原果形态标本：隆起籽体区由薄折面宽环翅包围，保留顶缺口和细柄；不是Dillhoffia压扁换色。母株/精确亲缘未知，不扩写叶树、不主张现代果色。 |
| `karst-spring-mouth` | Karst spring mouth / 岩溶泉口 | `items/karst-spring-mouth/` | 低洞口与流出的短明渠形成岩岸水源过渡，区别于潮蚀洞与瀑布深潭。 洞口低矮有顶厚、出水明渠和岩床自然连续；不是sea-cave缩小加蓝色条或石拱换方向。3m为名义裁片，非实测泉流/水文模拟/特定地点，水效果另展示不计新资产。 |
| `shatter-cone-rock` | Shatter-cone rock / 震裂锥岩 | `items/shatter-cone-rock/` | 嵌套锥面与放射纹丰富自然岩石断裂结构，区别于贝壳状断口和锯齿溶缝。 主要嵌套锥状断裂与放射纹方向一致、在灰色剖面有真实起伏，不只是刻几条直线或堆尖锥。原通用撞击相关过程示意，不声称出土地点、事件、压力或精确撞击年龄。 |

采用static-stylized-v1 / 2026-10-18.1。publication_authority=separate，授权policy单独pin；profile-policy.json仅规划说明，真实candidate就绪才生成sidecar，显式校验新profile，最终加--require-approved。fixed8/零转台；额外诊断另存。来源consulted-only/incorporated=false/非空rights_note，实际素材须真实授权，原创贴图自带provenance。结构化blockers及criterion ID匹配brief；legacy_result照实保留，profile兼容不等于valid/approved、模型QA或发布。
独立QA优先新上下文，先填核batch-47-QA-SCOPE.json真实source/逐项GLB hash及恰好四ID，错对象invalid_review_wrong_subject，不计PASS、不据其修错模型。catalog_facets原样保留，research pack不是已发布pack。

详读review-policy.json：用户最新一轮独立QA规则优先于历史模板的重复验收解释。

必修处只差异复核，发布不额外重复全批模型验收。

双栏网站仅PRD讨论、未批准实现，不改UI或信息架构。
