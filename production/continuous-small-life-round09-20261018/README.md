# 第九轮25–27：海底与岸边丰富度，12项

**当前父任务进度：线上确认103，22–24发布整合中；25/26模型QA PASS、27候选完成待QA；28/29候选完成且已派独立QA、无结论，30刚独占派制作。未提供的thread/turn/审核source不猜，实际state与父任务证明优先于历史初始空claim。**

**当前父任务进度：22–24全独立模型QA PASS，23仅标签修正、模型未变；25候选完成待独立QA，26独立模型QA PASS，27制作中。此处不新增线上数量/发布确认；实际state和父任务派发证明优先于历史初始空claim/旧阶段文字。**

**仅规划，未领取/派发；不启动制作或独立QA，不合并main。** 父任务当前确认round08的22/23已交付待独立QA、24由生产者独占；它们全部排除。本轮读取最新远端/main与提交的release描述符用于去重，不重新宣称线上部署结果。旧state中live79是最后明确给到planner的父任务确认checkpoint，非本轮重新执行公开验证。

## 三批各四项

| 制作任务 | 精确inventory ID | 原始中英文名 | 选择理由 |
|---|---|---|---|
| [batch-25](batch-25-TASK.md) | `anomalocaris` | Anomalocaris grasping radiodont / Anomalocaris（奇虾类） | 渐细游泳体、弯前附肢与上扬尾扇丰富游动轮廓，区别于宽马蹄甲和小穹头奇虾类。 |
| [batch-25](batch-25-TASK.md) | `jimaodanus` | Jimaodanus two-zone algal axis / Jimaodanus 异型轮枝绿藻 | 下部细刷轮枝与上部棒瓣冠形成两区藻体标本，区别于连续带枝和羽状梳枝。 |
| [batch-25](batch-25-TASK.md) | `hydrothermal-chimney` | Hydrothermal chimney / 海底热液烟囱 | 不规则矿物塔包围窄通道，补充海底竖向岩体而非另一种石柱阵列。 |
| [batch-25](batch-25-TASK.md) | `arenicolites-u-burrow` | Arenicolites U-burrow / Arenicolites U形潜穴 | 两竖井底部相连的U形潜穴以剖面教学增加潮间带结构，而非一个新动物。 |
| [batch-26](batch-26-TASK.md) | `echinochiton` | Echinochiton spiny plated mollusk / Echinochiton（棘甲软体动物） | 连续背板两侧的大刺补充板甲软体动物，区别于前后帽壳加中段鳞片的Halkieria。 |
| [batch-26](batch-26-TASK.md) | `clypeina` | Clypeina fertile-whorl specimen / Clypeina 盾盘轮藻 | 有记录的一对轮盘与粗放射分区补充海藻繁殖结构片段，不做未知高轴。 |
| [batch-26](batch-26-TASK.md) | `tidal-flat` | Tidal flat / 潮坪 | 极缓坡与浅小排水沟为岸边小生物提供场景层次，区别于单一波痕/泥裂纹理。 |
| [batch-26](batch-26-TASK.md) | `thalassinoides-branching-burrow` | Thalassinoides branching burrow / Thalassinoides 分支潜穴网 | 粗平滑潜道与开放Y节点补充海底内部路径教学，区别于U形双井。 |
| [batch-27](batch-27-TASK.md) | `sollasina` | Sollasina plated tube-foot echinoderm / Sollasina（板甲管足棘皮动物） | 低矮板甲体与多条细长板甲管足补充棘皮动物形态，区别于长刺海胆/海星。 |
| [batch-27](batch-27-TASK.md) | `ottoia` | Ottoia ringed predatory worm / Ottoia（环纹捕食蠕虫） | 粗环纹软管体与可缩吻的基本关系补充低位蠕虫轮廓，区别于叶毛和叶足类。 |
| [batch-27](batch-27-TASK.md) | `eocladus` | Eocladus multilevel algal branchwork / Eocladus 复枝绿藻 | 多级藻体分枝与清楚粗细阶差增加标本型海藻负空间，区别于两区轮枝或带状枝。 |
| [batch-27](batch-27-TASK.md) | `limestone-pavement` | Limestone pavement / 石灰岩溶沟石面 | 近平坦石灰岩块与深溶沟增加可走近自然岩面，区别于紧接多边岩柱。 |

4项小型生物、3项保存海藻形态、3项地形/岩体、2项潜穴剖面教学道具，均为原1000稳定ID。未增加同种颜色/密度/姿态/破损变体。奇虾的渐细游泳体、侧向大刺背板、多管足板体、粗环软管分别独立；地形与遗迹增加海底/岸边空间层次，区别于只堆更多相似物种。

## 信息架构、范围与尺度

每项catalog_facets按原inventory逐字段保存worlds/packs/category/subcategory/taxon_group/eras/biomes/tags/representation/reconstruction_type；完整原行在inventory-record.json。world主题、研究pack、物体分类、时代/生境是独立轴，pack不能增加条目数或改变分类。research pack归属不等于对应发布pack已经存在，正式metadata按当前发布schema/registry核对，不把计划条目计入线上过滤/下载数量。空数组保持未指定，不变成全时代全环境通用。

Jimaodanus仅保存上下两区藻轴；Clypeina仅有记录的一对相连轮盘，不外推未知高茎；Eocladus仅保存扁平多级分枝。三者都是fossil-specimen/specimen概念，不造完整母藻、根系或整株海底植物。厚度/姿态/颜色可合理教学化，不据此升级为新测量或科学复原。Eocladus保留needs-specific-reference，有可靠基础分枝依据即可进入inspired-by制作，不强加显微枝数/精确器官复原。其他11项原reference-ready也不代表新模型QA。

Arenicolites/Thalassinoides是trace-concept/artistic-concept：两竖井底部相连且无中间蹼层的U形，与粗平滑潜道开放Y节点网络。剖切是示意，不说复制真实出土标本、不指定制造者。识别关键是灰色顶/剖面内部几何和洞腔-围岩关系，外轮廓不是识别gate；不能把悬空树枝/圆管当真实潜穴。主fixed8可通过实际露面的朝向覆盖内部结构，必要额外诊断另存，不改主清单或伪造视图标签。

潮坪为6m宽的代表性教学片区，溶沟岩面为3m宽片区；保留原scale_class=landscape，不归一化成手掌小石或声称完整地貌测绘。微缓坡/排水沟、平缓岩块/深溶沟是宏观几何，不只画贴图。Limestone pavement原biomes=cave不改为已验证海岸成因，作为独立陆上溶蚀形态素材，不把所有本轮条目硬拼成同时代同地点海岸。其他名义尺度见config，全部是美术起点，不是新量化石；微小个体近景/标注展示尺度使用，不承诺远处可辨。

热液烟囱是矿物塔与窄通道的静态岩体，烟羽/水流若展示另分，不承诺喷发模拟或其古生态共存。自然形态不是具体古地点/年代复原。只需可信基本轮廓、自然衔接和诚实标签，不为细微不确定反复研究返工。

## 冻结输入与去重

`items/<ID>/`含原始inventory-record、brief/config/references/freeze；queue.json含精确名字、理由、预算、尺度、分类轴和路径。原1000资料不改写，不新增概念。`dedup-snapshot.json`有最新抓取ref SHA、当前main、已提交release描述符hash、所选ID模型/具名generator扫描及前序状态。前二十四批96个活跃/制作/候选/发布ID全部排除，其他已发布和候选一并排除；没有因错QA或发布容量失败而重做在途项目。共享脚本内部函数、未推送工作与实时分派不能完全靠文件名证明，父任务派发前统一协调。

脚本/attempt：`production/continuous-small-life-round09-20261018/work/<batch>/<ID>/r001/`；候选包：`assets/candidates/continuous-small-life-round09-20261018/<batch>/<ID>/r001/`；QA后父任务整合：`assets/additions/<ID>/continuous-small-life-v1/`。任何修复/重试新attempt/revision隔离，不覆盖旧记录。

## 制作、预算与交付

制作必须GPT-6.1 Sol medium；独立QA由父任务新任务派GPT-6 Luna xhigh，优先全新上下文，制作自检不能代替。沿用认可v002自然精致、可信比例、柔和衔接、适度卡通，通常80–240px与约480px中近景可读，不用机械拼接、全体随机噪声或大贴图凑精细。

每项14,000三角形、1,000,000GLB bytes为硬上限而非目标；通常100–500KB，更小亦可，增加几何只为轮廓/比例/衔接的可见收益。硬上限内超通常区间记录具体收益，不为软目标破坏结构。≤6材质/≤30 primitives，最多1张≤256px原创贴图，总编码≤65,536bytes、解码预算≤524,288bytes。源/求值/导出POSITION顶点、三角形、材质/primitive、文件/纹理与实例分别计量，不用面数判美或推测设备帧率。

交付可编辑Blend、独立GLB、可重建generator/config与所有语义依赖hash、中英metadata/范围/来源/权利/署名、可选原创map、透明封面、fixed8及实际GLB多角度runtime证据。源重开、两次语义重建、Khronos/project、目标loader、功能渲染和简化多实例场景绑定实际GLB hash。软件渲染不冒充物理设备性能，不承诺动画就绪。

一次汇总独立QA、至多一次计划内外观修复；真实必需缺陷未解决交父任务决定，不为微观枝数/软组织/齿钩/板片精确计数开无限循环。新模型hash使旧受影响QA失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅唯一release协调器整合，模型QA PASS不等于生产发布。

## 完整static profile和参考规范

本轮核读当前main的profile说明/代码，版本仍为`static-stylized-v1 / 2026-10-18.1`，文件SHA及policy pin保存在profile-policy.json。该文件只是计划说明，不能当validator sidecar。机器publication_authority=separate，已有批量发布授权另pin。

- 主manifest恰好hero/reversehero/front/side/rear/top/clay/silhouette各1张，turntable_frames=0；真实相机、GLB关联、尺寸和文件hash完整。side不臆造left/right；额外诊断另存，不破坏主fixed8。
- 原来源title/url/supports/access如实继承，本轮没重开外部论文，不伪造阅读或来源。每来源use=consulted-only、incorporated=false、rights_note非空；全局no_incorporated_third_party_assets=true。实际并入素材需真实许可/署名，原创贴图有独立provenance，不以consulted引用冒充素材授权。
- candidate按最新main模板，blockers结构化，stage/criterion IDs逐项匹配本brief；实际source/generator/config和全部证据hash绑定，unknown/fail不升PASS。
- candidate真实就绪后才用scripts/candidate_profile.py生成真实sidecar，再显式调用scripts/validate_candidate.py --profile static-stylized-v1 --profile-contract <sidecar>；最终批准加--require-approved。不填假hash/假候选。
- 默认legacy-v1不是本轮入口，不为误跑旧gate补转台/左右视图或改冻结资料。legacy_result如实保留，不自动回退、不删历史错误、不伪造旧PASS。
- profile_contract_status=pass仅合同兼容，不等于valid/approved_for_brief、模型独立QA或发布；批准必须记profile/rule，执行前复核policy/tool，变化需新版本冻结。

## 独立QA对象绑定

每批有`batch-XX-QA-SCOPE.json`，queue有路径，freeze绑定hash。当前只固定batch/四ID，source及逐项GLB hash为null、ready_for_qa=false，未启动QA。父任务提供实际冻结handoff后，在新执行记录填真实source/hash，优先全新上下文独立QA。

报告必须先回显并核对batch、恰好四ID、source commit和逐项GLB hash，再审实际导出。错批/错source报告标invalid_review_wrong_subject、不计PASS，也不据其修错模型；保留无效尝试，交父任务重启正确对象。旧批正确QA不因后来错答连带撤销。

## 领取、恢复与权限

本轮planned_awaiting_parent_dispatch，claims为空、无attempt/模型/sidecar/QA。父任务先核实时占用并登记独占task/thread/branch/base SHA再派发，planner不启动；已有worker以最新state与父任务明确派发为准，不被旧副本空claim阻塞。未知线程/turn/时间/路径不猜。

执行从届时最新main独立worktree/branch起步，只携带必要规划/helpers，不整体挑入旧CI/site/release改动。共享协调池默认1worker×2threads，实际CPU/配额由父任务分配；build/preview/render分lane，实际generator出现才生成完整inputs/outputs/timeout的runner manifest，此queue不是可执行manifest。失败/中断/缺文件/输入工具配置或完整输出hash变化不能复用成功，新attempt隔离保留日志。

运行`python3 production/continuous-small-life-round09-20261018/verify_plan.py`仅核验规划。冻结输入变化提升版本重算freeze/checksums，动态state/events由Git追踪，父任务串行协调，正常push冲突先fetch/reconcile。署名Leon Made This <8357465+s010s@users.noreply.github.com>；只普通push原planning分支，不制作、不派发、不合main、不强推、不改权限、不上传Google Drive。
