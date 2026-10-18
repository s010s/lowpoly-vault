# 第八轮22–24：器官标本、小型海生生物与自然物，12项

**当前父任务进度：线上确认103，22–24发布整合中；25/26模型QA PASS、27候选完成待QA；28/29候选完成且已派独立QA、无结论，30刚独占派制作。未提供的thread/turn/审核source不猜，实际state与父任务证明优先于历史初始空claim。**

**当前父任务进度：22–24全独立模型QA PASS，23仅标签修正、模型未变；25候选完成待独立QA，26独立模型QA PASS，27制作中。此处不新增线上数量/发布确认；实际state和父任务派发证明优先于历史初始空claim/旧阶段文字。**

**当前父任务确认：batch22/23已交付、待独立QA，batch24生产者独占制作。实际state及父任务派发证明覆盖下方初始未分派/空claim；交付不等于QA PASS或已发布。22/23来源SHA为本次远端头观察值，派QA前核对实际冻结handoff。**

**本条明确派发请求为准；此前21:38 UNKNOWN请求未启动，不另建重复任务。当前只规划，无领取、制作或QA，不合并main。** 线上79已确认，main `eb9153eab06f7e95235eac30611b731c8178ffb7`。16/18旧QA分别回错02/01已无效，新独立线程审正确source；17模型QA PASS，19新独立QA运行，20模型QA PASS，21制作中。不得把错批报告计PASS或撤销原01/02历史正确QA。

## 三批各四项

| 可直接使用的任务文件 | 精确inventory ID | 原始中英文名 | 选择理由 |
|---|---|---|---|
| [batch-22](batch-22-TASK.md) | `florissantia` | Florissantia five-sepal flower / Florissantia 五萼花化石 | 五宽萼裂片与浅中央杯补充小型花器官展示，区别于果实或球果。 |
| [batch-22](batch-22-TASK.md) | `stanleycaris` | Stanleycaris three-eyed radiodont / Stanleycaris（三眼奇虾类） | 小穹顶头甲、中眼和四枚尾叶的细体提供新奇虾类轮廓，区别于宽马蹄甲。 |
| [batch-22](batch-22-TASK.md) | `pahoehoe-lava-surface` | Pahoehoe lava surface / 绳状熔岩面 | 连续圆钝绳纹与重叠叶瓣增加地表流动节奏，区别于枕状露头。 |
| [batch-22](batch-22-TASK.md) | `staurolite-cross-twin` | Staurolite cross-twin / 十字石双晶 | 两柱贯穿连生形成十字双晶，区别于石英簇和玫瑰板晶。 |
| [batch-23](batch-23-TASK.md) | `metasequoia` | Metasequoia opposite-leaf fertile branch / Metasequoia 水杉类化石枝 | 对生交互排列的小叶/球果化石枝补充植物器官，不增加另一种完整树冠。 |
| [batch-23](batch-23-TASK.md) | `ovatiovermis` | Ovatiovermis unarmoured filter lobopodian / Ovatiovermis（无甲滤食叶足动物） | 裸躯前举滤食臂与后部固着爪足提供不同姿态的软体小生物。 |
| [batch-23](batch-23-TASK.md) | `nordenskioldia` | Nordenskioldia radial-fruit axis / Nordenskioldia 轮列果序化石 | 细轴上的放射果环补充果序结构，区别于单果角臂或球果鳞片。 |
| [batch-23](batch-23-TASK.md) | `waterfall-ledge` | Waterfall ledge / 瀑布岩阶 | 突出上岩缘与下退软层补充地形高差和岸边遮蔽空间。 |
| [batch-24](batch-24-TASK.md) | `williamsonia` | Williamsonia ovulate cone specimen / Williamsonia 本内苏铁类种子球果 | 独立有柄种子生殖体与粗镶嵌表面增加植物器官类型，区别于针叶树球果。 |
| [batch-24](batch-24-TASK.md) | `halkieria` | Halkieria two-shell armoured crawler / Halkieria（双壳鳞甲爬行动物） | 长扁体前后帽壳和中段叠片骨甲形成新的近底软体动物轮廓。 |
| [batch-24](batch-24-TASK.md) | `ctenorhabdotus` | Ctenorhabdotus many-combed ctenophore / Ctenorhabdotus（多栉列栉水母） | 两端较平的短椭圆桶体与重复栉带提供新栉水母形态，区别于箱钟水母。 |
| [batch-24](batch-24-TASK.md) | `conglomerate-outcrop` | Conglomerate outcrop / 砾岩露头 | 连续细粒基质内嵌圆砾，补充与贝壳灰岩/负载层不同的岩体结构。 |

四项植物器官、四种海生小动物、四种自然物，全部原1000稳定ID，不加颜色/密度/损伤变种。短椭圆栉水母与箱钟水母、绳状连续熔岩壳与枕状露头、圆砾基质与碎壳灰岩等必须有原库存明示的结构差别，不能只改比例/配色。Halkieria的中文“爬行”是贴地运动表述，分类依原mollusk，不画成蜥蜴。

## 植物器官范围与参考

四项原representation=fossil-specimen / reconstruction_type=specimen：Florissantia是五萼花保存器官，五裂片不随意说成五花瓣；Metasequoia只做对生叶/生殖结构的保存枝，不生造完整红杉冠；Nordenskioldia只做轮列果序轴，不另计种子资产；Williamsonia是本内苏铁类有柄种子生殖体，不当被子植物雏菊或针叶树鳞片球果。可不用岩板，但不因自由展示就变成完整母体，缺失/未关联器官不添加。

本轮12项原research gate均reference-ready，不代表新模型QA或科学复原。可靠基础参考足以说明可辨识形态即可教学风格化，不强求微观计数、软体组织、真实尺寸、神经/取食/运动机制。不伪造图/来源或已读状态：title/url/supports/access继承真实inventory，本轮未重开外部论文。天然十字晶体连生、河流岩阶和圆砾成岩都是过程概念，不承诺精确古地点。生物/植物/矿物分区教学，批次不是同时代同地点共存场景。

全部名义尺寸为美术起点，不是新量化石；相机/展示放大另标，不统一归一化为单位立方体。小个体用近景展示，不承诺远处可辨。

## QA对象防错：优先新上下文

每批配有同名 `batch-XX-QA-SCOPE.json`，queue.json记录精确路径，freeze绑定scope哈希；当前只填已知批次和四ID，source/GLB hash全部为null、ready_for_qa=false，不是假QA启动。

父任务优先创建**全新独立上下文**给GPT-6 Luna xhigh。供给冻结brief/reference、实际GLB、完整证据和真实source commit，不先给maker自评分。QA必须先回显/核对：batch ID、恰好四个asset IDs、source commit、逐项GLB SHA-256，再逐项检查。实际scope准备就绪需要父任务生成绑定真实候选的新冻结执行记录，不能将当前null当作任意source。

若回复出现别批、别组ID或旧source，记录`invalid_review_wrong_subject`、verdict不接受，保留这次失败/错批尝试并向父任务回报重新审正确对象；**不得记PASS，也不得根据错批报告修错模型**。同线程被重用时更要显式标明本次任务/turn和对象，旧正确QA与新错答分开，不能连带撤销历史正确批次。

## 预算、模型与交付

制作GPT-6.1 Sol medium；独立QA GPT-6 Luna xhigh，优先新上下文，制作自检不替代。延续v002自然精致、可信比例、柔和衔接、适度卡通，80–240px通常观看和约480px中近景，避免机械拼接/随机噪声或大贴图假精细。14,000三角形和1,000,000GLB bytes为上限非目标，通常100–500KB，更小亦可；增加几何只为轮廓/比例/衔接可见收益，硬上限内超通常区间记录具体收益即可。≤6材质/≤30 primitives；最多1张≤256px原创贴图，总编码≤65,536bytes、解码预算≤524,288bytes。源/求值/导出POSITION顶点、三角形、材质/primitive、字节/纹理和实例分别计量，不凭面数判美/性能。

可编辑Blend、独立GLB、可重建generator/config与语义依赖hash、中英metadata/范围/来源/权利/署名、可选原创map、透明封面、fixed8和实际GLB多角度runtime证据。源重开、两次语义重建、Khronos/project、目标loader、功能渲染和简化多实例场景绑定精确GLB hash。软件渲染不冒充物理设备性能；Ctenorhabdotus可用克制/不透明便携材质，不能用重叠透明和大贴图掩盖造型。

一次汇总独立QA、至多一次计划内外观修复；真实必需缺陷未解决交父任务决定，不为微观复原不确定反复返工。模型新hash使旧受影响QA失效。用户授权QA通过分批push/merge无需逐模型审批，但唯父任务release协调器整合发布，不能将模型QA PASS当生产上线。

## 完整显式static profile

沿用main已合并`static-stylized-v1 / 2026-10-18.1`；读取的当前main文档/代码SHA和policy pin在profile-policy.json。该文件是规划说明，**不是validator sidecar**。publication_authority机器值为separate，已有批量发布授权另pin。

- fixed8主manifest恰好hero/reversehero/front/side/rear/top/clay/silhouette各1张，转台0；真实相机、GLB/file hash、尺寸记录完整；side不伪造left/right。针对问题的额外诊断另存，不能破坏主fixed8。
- 每来源use=consulted-only、incorporated=false、真实title/url/rights_note，全局no_incorporated_third_party_assets=true。查阅不是复制媒体许可；实际并入素材有真实许可/署名，原创贴图也有自己的provenance，不能引用consulted来源冒充并入许可。不猜license或复用外部网格。
- 按最新main模板填写candidate，blockers结构化，stage/criterion IDs完全匹配本brief；source/generator/config与所有证据实际hash绑定，unknown/fail不改写PASS。
- 真实candidate就绪后才用scripts/candidate_profile.py生成真实sidecar，再显式运行scripts/validate_candidate.py --profile static-stylized-v1 --profile-contract <sidecar>；最终批准加--require-approved。不在规划阶段填假hash、假模型或假sidecar。
- 默认legacy-v1不是本轮入口；不为旧gate补无意义转台/左右视图或改冻结资料。显式新profile返回的legacy_result如实保留，不自动回退、不删旧错误、不伪造旧PASS。
- profile_contract_status=pass仅兼容，不等于valid、approved_for_brief、独立模型QA或发布。实际批准明确profile/rule版本；执行前复核policy/tool，变化要新版本冻结而非静默换hash。

## 路径、去重和恢复

每项 `items/<ID>/`保留完整原始inventory-record、brief/config/references/freeze，queue记录原名、尺度、理由、预算与路径。脚本/attempt：`production/continuous-small-life-round08-20261018/work/<batch>/<ID>/r001/`；候选：`assets/candidates/continuous-small-life-round08-20261018/<batch>/<ID>/r001/`；QA后整合：`assets/additions/<ID>/continuous-small-life-v1/`。

`dedup-snapshot.json`保存全部抓取refs和模型/具名脚本扫描，前二十一批84项全部排除，其他已发布/既有候选排除；没有因为错QA或容量失败就重做在途ID。共享脚本内部函数、未推送工作与实时占用不能完全靠文件名扫描证明，父任务正式派发前协调。四器官的原始资料保持原字节/结构，不增加完整/切片变体计数。

当前planned_awaiting_parent_dispatch、claims为空，无模型/attempt/sidecar/QA。父任务核对占用并登记独占task/thread/branch/base SHA再派发，planner不启动；已有worker以最新state和父任务明确授权为准，历史空claim不阻塞。未知线程/turn/时间/路径留空不猜。

执行从届时最新main独立worktree/branch起步，只带必要规划/helpers，不整体挑入旧CI/site/release代码。共享协调池默认1worker×2threads、实际CPU/配额父任务分配，build/preview/render分lane；实际generator出现才生成完整inputs/outputs/timeout的runner manifest，此queue不可执行。新attempt/revision隔离、保留日志，未完成/缺文件/输入工具配置或完整输出hash变化不能复用成功。

运行 `python3 production/continuous-small-life-round08-20261018/verify_plan.py`只检查规划。冻结输入变化提高版本并重算freeze/checksums；state/events由Git追踪，父任务串行协调，正常push冲突先fetch/reconcile。署名Leon Made This <8357465+s010s@users.noreply.github.com>；只checkpoint普通push，不制作、不派发、不合main、不改权限、不强推、不上传Google Drive。
