# 第三轮07–09：海底多样性规划，12项

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

**仅计划，尚未派发制作；不启动Blender、不自行发布、不合并main。** 当前父任务要求只保存第三轮；01–03全独立QA PASS且交唯一release child排队但尚未确认发布，04独立QA中，05–06已正式独占派发。旧空claim快照不能阻塞已有父任务派发的worker。

制作固定GPT-6.1 Sol medium；独立QA由父任务新任务派GPT-6 Luna xhigh。所有条目取自原1000清单已有ID，不编造或增加inventory条目。

## 三批各四项

| 可直接派发的任务文件 | 精确inventory ID | 原始中英名 | 选择理由 |
|---|---|---|---|
| [batch-07](batch-07-TASK.md) | `syringopora` | Syringopora organ-pipe coral / Syringopora（管风琴珊瑚） | 分离直立细管与稀疏横桥提供通透管风琴群体，不重复蜂巢块或开放链壁。 |
| [batch-07](batch-07-TASK.md) | `vauxia` | Vauxia branching fibrous sponge / Vauxia（分枝纤维海绵） | 反复分枝的细管海绵提供灌丛式立体空间，区别于扁盘Choia。 |
| [batch-07](batch-07-TASK.md) | `halimeda` | Halimeda articulated calcified thallus / Halimeda 仙掌藻类 | 关节相连扁平节片链，补充活体概念的钙化海藻形态，与管状/丝状藻不同。 |
| [batch-07](batch-07-TASK.md) | `isoxys` | Isoxys double-spined swimmer / Isoxys（双棘甲游泳动物） | 双瓣凸甲、前后相对长棘及突眼，丰富水层小型游泳动物。 |
| [batch-08](batch-08-TASK.md) | `heliophyllum` | Heliophyllum ribbed horn coral / Heliophyllum（肋角珊瑚） | 弯角单体和深放射杯丰富单体珊瑚，区别于一盖/四盖珊瑚。 |
| [batch-08](batch-08-TASK.md) | `pirania` | Pirania spine-covered sponge / Pirania（长刺海绵） | 粗基部分枝和疏布长刺提供有刺管状海绵，不是Choia扁盘放大。 |
| [batch-08](batch-08-TASK.md) | `bosworthia` | Bosworthia ribbon-branch thallus / Bosworthia 带枝藻化石 | 扁平带状分叉藻体片段丰富藻类展示轮廓，不重复钙化节片海藻。 |
| [batch-08](batch-08-TASK.md) | `haplophrentis` | Haplophrentis hyolith with support rods / Haplophrentis（支杆锥壳动物） | 渐细锥壳、盖板和两根外弯支杆形成新的低位海底主体。 |
| [batch-09](batch-09-TASK.md) | `thecosmilia` | Thecosmilia branch-tube reef coral / Thecosmilia（枝管造礁珊瑚） | 直立厚管枝末端的独立深杯补充枝管珊瑚，区别于Thamnopora指枝侧孔。 |
| [batch-09](batch-09-TASK.md) | `meandrina` | Meandrina maze-ridge coral / Meandrina（迷宫脊珊瑚） | 连续蜿蜒沟壁与迷宫脊增加低丘礁体结构，区别于Favosites离散蜂巢孔。 |
| [batch-09](batch-09-TASK.md) | `leptomitus` | Leptomitus wrinkled tube sponge / Leptomitus（褶纹管海绵） | 高窄褶纹管体提供安静竖向海绵层，与Vauxia分枝及Pirania带刺管不同。 |
| [batch-09](batch-09-TASK.md) | `buthograptus` | Buthograptus curved-pinna thallus / Buthograptus 羽状绿藻 | 弯曲渐细侧元组成羽状/梳状藻体片段，与Bosworthia连续带枝不同。 |

四种真正珊瑚：管风琴式分离竖管+横桥、弯角深杯、枝管末端深杯、迷宫沟壁丘体，分别区别于前轮六种珊瑚。三种海绵分别为分枝细管、带刺粗管、高窄褶管，不以颜色/密度变种计数。Halimeda是完整钙化节片海藻概念；Bosworthia/Buthograptus是两种藻体标本结构片段。海绵不是珊瑚，海藻不是海草/陆生植物。

## 两项藻体片段的范围

Bosworthia与Buthograptus在原清单均为`category=plants`、`subcategory=alga`、`representation=fossil-specimen`、`reconstruction_type=specimen`，限定保存的thallus。按其原modeling_brief做浅浮雕/浅厚度结构片段教学展示，不加未知根系、固着器、完整母体或活体冠；不把这两件说成海底植被已经重建。可以不导出展示岩板，省略岩板也不把片段变成完整活体。它们丰富藻类形态/博物馆近景教学，Halimeda才是本轮完整海藻造型候选。

没有用Hydropteris、Salvinia、Montsechia等淡水条目冒充海底植物。整轮跨地质时期，不声称同域共存生态复原。名义尺度是明确记录的美术起点，不是化石新测量；过小标本需前景/标注展示比例，不承诺远岛视点可读。

## 参考门槛、权利和风格

`reference-policy.json`逐项列出边界。本轮7项原reference-ready；Syringopora、Heliophyllum、Thecosmilia、Meandrina及Halimeda五项保留needs-specific-reference，现有来源支持类群/局部基础形态。派发后做有界基础形态核对，可靠入口足以支撑所画轮廓即可继续inspired-by教学风格，不要求精确属级微孔、隔壁数、软组织或生活运动复原；不把泛类群页说成具名特征已验证，也不把现代Halimeda种无证据指派给白垩纪概念。需要时缩窄标签/省略无支持细节，不为不确定复原反复返工。

来源只继承真实inventory记录，本轮未重新打开论文或网页，access如实标历史。仅查阅事实并原创建模不赋予复制图/网格的许可；不收录来源媒体、扫描、第三方网格/纹理。确需使用须先记录真实许可/授权与署名，优先原创避免依赖。不伪造来源、PASS或精确尺寸。

延续已认可v002 `c8514b8c348777c9a2d81c6c0bbd9cf02cdb5184`：自然精致、可信比例、柔和衔接、适度卡通，80–240px通常观看与约480px中近景可看；避开机械拼接、大贴图假精细与单纯面数评判。

每项14,000三角形、1,000,000 GLB bytes为硬上限而非目标；通常约100–500KB，更小同样可以。增加面数须有轮廓/比例/衔接的可见收益，超通常区间但在上限内记录具体收益即可，不为软目标伤害造型。≤6材质/≤30 primitives；最多1张≤256px原创贴图，总编码≤65,536 bytes、解码预算≤524,288 bytes。顶点三种口径、三角形、材质/primitive、GLB/贴图大小与场景实例分开报告，不把primitive数当真实draw calls。

## 输出与QA

每项完整计划在 `items/<ID>/`：brief.json、build-config.json、references.json、原始inventory-record.json、freeze.json。queue.json有精确全路径：

- 制作脚本/执行记录：`production/continuous-small-life-round03-20261018/work/<batch>/<ID>/r001/`。
- 冻结待审包：`assets/candidates/continuous-small-life-round03-20261018/<batch>/<ID>/r001/`。
- QA通过后父任务整合位置：`assets/additions/<ID>/continuous-small-life-v1/`。

交付可编辑Blend、独立GLB、可重建generator/config与全部语义依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创地图、透明封面，八固定视图hero/reversehero/front/side/rear/top/clay/silhouette及实际GLB多角度运行时证据。零转台序列，有实际问题才补针对性视图。源重开、两次语义重建、Khronos/project、目标loader、功能渲染和简化多实例场景结果绑定精确GLB hash；软件渲染不冒充真实设备性能，不承诺动画就绪。

Maker正常push冻结candidate并回报精确commit/GLB/brief/reference/evidence hashes，由父任务新派独立Luna xhigh QA，先不提供maker自评分。一次汇总QA、至多一次计划内外观修复；真实必需缺陷没解决交父任务决定，修复新revision/hash使旧受影响verdict失效。不因未保存软体/微观细节不确定反复返工。通过全部必需QA后用户已授权分批push/merge，无需逐模型审批，但发布仍由父任务唯一release协调，不把QA PASS写成已发布。

## 去重、恢复与授权

`dedup-snapshot.json`记录全部已抓取分支SHA、当前main、选中ID模型/具名脚本路径扫描及release描述符。01–06的24个ID及其claims全部排除，发布十六项、Dapedium/Callichimaera候选和三件组也排除；未将首轮QA通过12件误计成已经发布。当前远端没发现所选12项模型/具名generator；共享脚本内部函数、未推送工作与实时会话仍由父任务领取前统一核对，路径扫描不是全局锁。

`queue.json`是初始计划；`state.json`和父任务明确派发是当前授权证据。07–09当前无owner/attempt/QA；父任务先核对实时占用，记录独占thread/branch/base SHA再派发，本planner不得启动。父任务已明确独占派发的既有worker，不因旧副本claim为空、冻结config写未派发或旧queue状态而停工；保留派发消息作为授权证据并正常补记最新state，未知时间/分支/哈希留空不捏造。

实际执行从届时最新main独立branch/worktree，只携带必要规划输入/helpers，不整体挑入旧CI/site/release变更。build/preview/render分lane；共享协调池默认1worker×2threads，实际CPU/配额/并发由父任务分配，不能每批各占整台。实际generator出现后才创建完整runner inputs/outputs/timeout等manifest；当前queue并不可执行，不含虚构脚本路径。

失败/中断/缺文件/不同输入工具配置与完整输出hash不能复用成功；新attempt/revision隔离，保留日志；resume依照[仓库队列契约](../../skills/blender-lowpoly-pipeline/references/parallel-queue.md)。运行 `python3 production/continuous-small-life-round03-20261018/verify_plan.py`只核验规划。冻结输入变化提升版本并重算freeze/checksums，动态state/events由Git追踪，父任务串行协调状态写入，正常push冲突先fetch/reconcile。

沿用仓库[流水线](../../skills/blender-lowpoly-pipeline/SKILL.md)、[美术](../../skills/lowpoly-art-direction/SKILL.md)、[史前环境](../../skills/prehistoric-environment-art/SKILL.md)及[事实审查](../../skills/asset-factual-review/SKILL.md)，明确用户本轮模型/风格/practical要求覆盖旧设置。只规划，不上传Google Drive、不改权限、不强推，不合并main；署名Leon Made This <8357465+s010s@users.noreply.github.com>。
