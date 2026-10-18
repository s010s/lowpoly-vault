# 第二轮v002：优先海底与六种珊瑚，批次04–06

**当前状态：线上67已确认（main ccf48bb446dd4d0a710ab14dfc05d6fbf7064cdb，PR9/Pages/public Chromium均PASS）；13–15全模型QA PASS、67→79发布容量失败待恢复，不影响已完成67；16–17候选完成/QA运行无结论，18独占制作。以最新state和父任务派发证明覆盖下方历史空claim/未派发/旧线上数量。**

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

**仍然只规划，未领取/派发/生产。** 父任务确认CI完成于main `643534830397824dfd46990485bd16ad66ecf9ce`；01–03已经独占派发，本次没有改动首轮目录内任何文件。按用户最新海底优先要求，调整尚未派发的04–06。

实际清单统计与两轴解释先见 [INVENTORY-STATS.md](INVENTORY-STATS.md)；机器重计数见 [INVENTORY-STATS.json](INVENTORY-STATS.json)：17个珊瑚概念、七大物体类合计1000，并非17个已完成珊瑚模型。

## 当前三批分工

| 任务 | 精确inventory ID | 清单原名 | 选择理由 |
|---|---|---|---|
| [batch-04](batch-04-TASK.md) | `calceola` | Calceola slipper coral / Calceola（拖鞋珊瑚） | 单体拖鞋杯与单盖提供低矮有盖珊瑚，区别于块状和枝状群体。 |
| [batch-04](batch-04-TASK.md) | `favosites` | Favosites honeycomb tabulate coral / Favosites（蜂巢床板珊瑚） | 蜂巢状紧排多边管群体，提供厚实圆块礁体，与链状珊瑚不同。 |
| [batch-04](batch-04-TASK.md) | `opabinia` | Opabinia five-eyed swimmer / Opabinia（五眼古生动物） | 五眼、单根长吻和侧叶形成游泳主体；区别于已有鱼、蟹、双瓣甲动物。 |
| [batch-04](batch-04-TASK.md) | `choia` | Choia radial-disc sponge / Choia（放射盘状海绵） | 扁盘与放射骨针丰富海底低矮层，不是海胆的球壳长刺变种。 |
| [batch-05](batch-05-TASK.md) | `goniophyllum` | Goniophyllum four-lidded coral / Goniophyllum（四盖珊瑚） | 方锥体和四片三角盖形成与Calceola不同的有盖单体珊瑚。 |
| [batch-05](batch-05-TASK.md) | `halysites` | Halysites chain coral / Halysites（链珊瑚） | 开放环链式直立管壁形成通透礁体，区别于Favosites实心蜂巢群体。 |
| [batch-05](batch-05-TASK.md) | `marrella` | Marrella fork-spined arthropod / Marrella（叉棘节肢动物） | 头盾双组长棘和细分节躯干形成新的小型底栖轮廓。 |
| [batch-05](batch-05-TASK.md) | `proteroctopus` | Proteroctopus finned octopod / Proteroctopus（有鳍八腕动物） | 柔软外套膜、成对鳍和八腕补充海生软体动物，避免全是硬甲。 |
| [batch-06](batch-06-TASK.md) | `aulopora` | Aulopora trumpet-network coral / Aulopora（喇叭网珊瑚） | 低矮附生管网与上翘喇叭口丰富岩面覆盖层，不是大块礁体缩放版。 |
| [batch-06](batch-06-TASK.md) | `thamnopora` | Thamnopora porous branch coral / Thamnopora（孔枝珊瑚） | 粗指状分枝和向外孔口增加海底竖向层次，区别于低矮管网和链状/块状珊瑚。 |
| [batch-06](batch-06-TASK.md) | `hallucigenia` | Hallucigenia spiny lobopodian / Hallucigenia（背棘叶足动物） | 细长体、背棘和软足形成低位行走生物，与硬壳蟹和海星不同。 |
| [batch-06](batch-06-TASK.md) | `fenestella` | Fenestella windowed fan bryozoan / Fenestella（窗格扇苔藓动物） | 开窗网格扇形增加海底竖向背景，区别于海绵盘和分枝腕动物；是苔藓动物而非植物。 |

真正珊瑚6项：`calceola`、`goniophyllum`、`favosites`、`halysites`、`aulopora`、`thamnopora`；单体一盖/四盖、密实蜂巢、开放链、低矮管网、粗指枝，结构差异明确，不用密度变种凑数。配套6项海生动物保留游动、甲棘、软体与底栖轮廓；其中Choia明确为海绵，Fenestella明确为苔藓动物，不能充作珊瑚。

原04–06中尚未制作的`meganeura`、`cooksonia`、`mongolarachne`、`salvinia`、`leclercqia`、`montsechia`延后，原冻结包保存在`deferred-items/<ID>/`，不在当前12项执行队列。原计划完整可从提交`07cf1981b4e95eb7f1f101ebac533132d598b712`恢复；变化映射见`superseded-plan.json`。归档共享policy哈希对应旧提交，不是当前活跃输入。

## 可直接使用的路径与状态

每项计划目录 `production/continuous-small-life-round02-20261018/items/<ID>/` 含中英原名/完整inventory-record、brief、build-config、references和freeze。脚本/执行记录放本目录`work/<batch>/<ID>/r001/`；待审包放`assets/candidates/continuous-small-life-round02-20261018/<batch>/<ID>/r001/`；仅QA通过后由父任务串行整合到`assets/additions/<ID>/continuous-small-life-v1/`。queue.json列出每项精确路径、预算、尺度、理由和制作/QA模型。

`state.json`仍是planned_awaiting_parent_dispatch，claims为空、没有attempt或QA结果。父任务先核对最新远端/发布/候选和实时会话，再登记独占claim、实际thread/branch/base SHA；没有owner不代表maker可抢占。本planning分支不合main。去重快照包含新抓取的首轮batch03候选分支、三件组发布分支及原排除项，首轮12项全部排除；路径扫描不保证发现未推送工作或共享生成器内部函数。

## 参考与标签

11项原inventory为reference-ready；新增Thamnopora保留needs-specific-reference。其原来源是床板珊瑚类群页，只需有界核对可靠基础指枝/向外管口形态，合理风格化做inspired-by教学道具；不要求属级微孔、精确孔数和种级鉴别，不伪造来源支持。Favosites/Halysites/Aulopora现有来源同样有类群范围限制，reference-ready也不表示所有属级细节已经证实；以所查到的基本形态为界。

Calceola/Goniophyllum共有具名有盖珊瑚参考入口，区分一盖拖鞋杯和四盖方锥杯；盖开合姿态是静态美术选择，不做软体/运动机制复原。Proteroctopus及Fenestella继续使用基本类群形态支持的描述性inspired-by标签，不新增无依据的精确属级断言。所有来源历史access如实继承，本轮未重新打开外部页面。微观解剖、软组织、色彩、精确尺寸和同地点共存不是必需验证；可靠基本形态和实际输入权限足够即可继续。

参考仅查阅、模型贴图原创；consulted-only不是源媒体的开放许可，不搬运图/扫描/第三方网格。需要收录才检查真实许可与署名。保留事实标签、来源和美术选择，不造参考或事实PASS。海底风格化目录跨时代；不是这些生物同域共存的科学复原。

## 制作、预算与独立QA

制作GPT-6.1 Sol medium；独立QA由父任务新派GPT-6 Luna xhigh，制作自检不能替代。沿用已认可v002 `c8514b8c348777c9a2d81c6c0bbd9cf02cdb5184` 的自然精致、可信比例、柔和衔接，适度卡通；80–240px通常观看、约480px中近距离。

14,000三角形、1,000,000GLB bytes都是上限而非目标；通常争取100–500KB、更小同样可以。增加面数须对轮廓/比例/衔接有可见收益，未超硬上限则记录收益，不为软目标破坏造型。≤6材质/≤30 primitives；最多1张≤256px原创贴图，编码总计≤65,536 bytes、解码预算≤524,288 bytes，不用大贴图凑精细。分别报告源/求值/导出顶点、三角形、GLB字节、贴图与场景实例，不凭面数声称质量或设备性能。

可编辑Blend、独立GLB、可重建generator/config与依赖哈希、中英metadata/来源/许可/署名、透明封面、八固定QA视图和实际GLB多角度运行时证据；零转台序列，有实际问题才加针对性视图。源重开、两次语义重建、Khronos/project、目标loader、功能渲染和简化多实例场景都绑定精确GLB哈希；软件渲染不能冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；不为微观复原不确定反复研究返工。真实必需技术/基本形态/授权缺陷没解决交父任务裁决，新模型hash使旧受影响verdict失效。用户已授权QA通过分批直接push/merge无需逐模型审批；发布整合由父任务串行协调。本planner不生产、不上传Google Drive、不改权限、不强推。

## 恢复

运行 `python3 production/continuous-small-life-round02-20261018/verify_plan.py` 只检查规划。详细流程见[首轮恢复说明](../continuous-small-life-20261018/README.md)和仓库[runner契约](../../skills/blender-lowpoly-pipeline/references/parallel-queue.md)。queue是初始计划，state/events是动态真相，由父任务串行协调写入。使用最新main的独立branch/worktree，避免整体挑入旧分支CI/site/release代码。未完成、输入/工具配置不同或完整输出hash不符都不能复用成功；新尝试新目录，保留失败日志。

实际generator出现后才创建全部语义inputs、必需outputs、timeout等齐全的runner manifest；本队列不是可直接执行的manifest。build/preview/render分lane，默认共享协调池1worker×2threads，不让每批各占满主机。冻结输入改动提高版本并重算freeze/checksums；state/events由Git追踪。首轮任务/状态/输入完全不动。
