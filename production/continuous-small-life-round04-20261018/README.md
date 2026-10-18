# 第四轮10–12：珊瑚、植物和岸边环境，12项

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

**仅计划，未派发、未制作；不合并main。** 最新父任务确认的发布总数为31（main `ab11dfe622682b75b86a8dd29c48c650e5e5a5c2`）。04–06模型QA PASS，显式candidateprofile兼容/合批发布仍在处理，未确认43；07–09候选完成，当前独立QA进行中且没有结论。最新state与父任务派发证明优先于历史空claim。

## 三批各四项

| 可直接派发的任务 | 精确inventory ID | 清单中英原名 | 类型与选择理由 |
|---|---|---|---|
| [batch-10](batch-10-TASK.md) | `flabellum` | Flabellum fan-wedge coral / Flabellum（扇楔珊瑚） | 侧扁扇楔单体珊瑚补充宽刃杯轮廓，区别于先前圆杯/管枝/迷宫群体。 |
| [batch-10](batch-10-TASK.md) | `horneophyton` | Horneophyton corm-based shoots / Horneophyton 角蕨类植物 | 膨大基体与分叉孢子囊带来小型直立早期植物，区别于首轮根茎拱。 |
| [batch-10](batch-10-TASK.md) | `wave-ripple-surface` | Wave ripple surface / 波浪波痕面 | 对称波脊与圆钝波谷提供浅水/岸边可走近地表，不增加水体贴图负担。 |
| [batch-10](batch-10-TASK.md) | `gogia` | Gogia brachiole-crowned eocrinoid / Gogia（腕丝冠始海百合类） | 短基部梨形板杯与取食腕丝冠丰富小型固着海底生物，区别于Saccocoma无柄开放分枝。 |
| [batch-11](batch-11-TASK.md) | `micrabacia` | Micrabacia radial-disc coral / Micrabacia（放射盘珊瑚） | 自由扁盘与放射肋带来低平珊瑚轮廓，区别于丘状迷宫和深角杯。 |
| [batch-11](batch-11-TASK.md) | `sengelia` | Sengelia K-branching ground plant / Sengelia 匍匐早期植物 | 连续K形匍匐节点补充贴地早期植物，区别于直立轴丛和蕨类叶冠。 |
| [batch-11](batch-11-TASK.md) | `coquina-outcrop` | Coquina outcrop / 贝壳灰岩露头 | 可见贝壳碎片构成多孔固结岩，增加岸边材质与结构差异，不重复层理崖或自然拱。 |
| [batch-11](batch-11-TASK.md) | `naraoia` | Naraoia two-shield arthropod / Naraoia（双甲节肢动物） | 两块背甲下藏细足的小型底栖轮廓，区别于前轮封闭双瓣甲泳体。 |
| [batch-12](batch-12-TASK.md) | `cystiphyllum` | Cystiphyllum blister-cup coral / Cystiphyllum（泡杯珊瑚） | 膨大弯曲单杯和宽浅泡状杯内结构补充厚实低杯，区别于Heliophyllum细弯角深放射杯。 |
| [batch-12](batch-12-TASK.md) | `limnobiophyllum` | Limnobiophyllum stolon-linked leaf rosettes / Limnobiophyllum 浮生天南星类 | 匍匐茎连接叶丛与下垂根束丰富淡水岸边漂浮层，区别于成对浮叶水蕨。 |
| [batch-12](batch-12-TASK.md) | `wielandiella` | Wielandiella divaricate shrub / Wielandiella 本内苏铁类灌木 | 叉枝灌木骨架与叶丛丰富岸边/陆地中层，不增加另一种大树冠密度变体。 |
| [batch-12](batch-12-TASK.md) | `desiccation-crack-surface` | Desiccation crack surface / 干裂泥面 | 相接泥片和收窄裂缝提供干露岸面，与波浪波痕湿浅水区域形成不同地表结构。 |

共3种真正珊瑚、4种植物、3种岸边地表/岩体、2种小型海生动物，没有大恐龙，也没有同种颜色/密度/冠层变体。扇楔杯、低放射盘、膨大浅泡杯是不同inventory形态；若实现后轮廓只剩旧珊瑚改比例，先修结构差异，不计作新形态完成。四种植物分别是膨大基体轴丛、K节点匍匐植物、匍匐茎叶丛浮生植物、叉枝灌木；不是继续堆大树。

Limnobiophyllum是淡水湿地浮生植物，不用于海水海底，不误标海草；其他植物为陆地/岸边教学素材，未承诺精确耐盐性或同地点共存。波痕、贝壳灰岩、泥裂分别表达浅水纹理、固结岩体、干露岸面；泥裂不宣称永久水下形成。批次是制作分工，不是一个同时代同地点生态复原。

## 输入、尺度与目录

`queue.json`有每项精确目录、名义尺寸、理由和预算；`items/<ID>/`保存原始inventory-record、brief、build-config、references、freeze。所有ID均来自原1000清单，不增条目。原形态范围如实保留：生物是whole-organism教学概念，3个地质体是artistic-concept过程道具，不把它们当化石标本。

- 制作脚本/attempt：`production/continuous-small-life-round04-20261018/work/<batch>/<ID>/r001/`。
- 待审包：`assets/candidates/continuous-small-life-round04-20261018/<batch>/<ID>/r001/`。
- QA通过后整合：`assets/additions/<ID>/continuous-small-life-v1/`，由唯一release协调器处理。

名义尺度是美术起点，不是新量化石：地表波痕块宽1.5m、干裂块宽1.2m、贝壳灰岩宽0.8m；Wielandiella高0.8m；其余生物尺度见每项config。资产保留米制与可记录挂点，不能统一归一化成单位立方体。地表块边缘是明确裁切边界，不承诺任意重复无缝；真实拼接需求另检查接缝。

## 参考只要求基本辨识

3项珊瑚原needs-specific-reference，其他9项reference-ready；这些是历史研究状态，不是制作或QA结果。珊瑚基础类群资料可支撑相应杯/盘结构时，按inspired-by教学标签合理风格化继续，不要求属级微孔、隔壁/器官精确数量、软组织、真实尺寸或生活机制复原。来源不能支持的精确特征不添加，标签可缩窄，不为不确定细节反复查证返工。

引用访问方式均继承真实清单，本轮没有重新打开外部论文/页面，不伪造阅读、支持范围或参考。Gogia按所查类群/具名图示范围做基本梨形杯与腕丝冠，不强求精确微板；Coquina只用EN-RK2支持贝壳碎片岩，EN-RK2B在原清单讲燧石/晶洞，保留原始引用记录但不能冒充贝壳灰岩形态证据。字段映射见references和brief的required_sources。

模型与可选贴图原创；consulted-only不是来源图片/网格开放许可。仅查阅事实无需再分发素材，但确需并入外部媒体/资产时须先核实真实许可、署名与授权。保留中英名称、事实边界和美术选择，不制造参考或PASS。

## 相同制作、预算与QA标准

制作必须 **GPT-6.1 Sol medium**；独立QA由父任务在新任务派 **GPT-6 Luna xhigh**，制作自查不能替代。沿用认可v002 `c8514b8c348777c9a2d81c6c0bbd9cf02cdb5184`：自然精致、可信比例、柔和衔接、适度卡通，80–240px正常观看和约480px中近景，不追求显微科考。

每项14,000三角形、1,000,000 GLB bytes为硬上限而非目标，通常约100–500KB，更小同样可以。只为轮廓、比例或衔接的可见收益增加面数；在硬上限内超通常区间记录收益即可，不为软目标破坏造型。≤6材质/≤30 primitives，最多1张≤256px原创贴图，总编码≤65,536bytes、解码预算≤524,288bytes。不靠大贴图凑精细，源/求值/导出POSITION顶点、三角形、材质/primitive、GLB/纹理和实例分别计量，不凭面数判美或性能。

可编辑Blend、独立GLB、可重建generator/config与依赖哈希、中英metadata/来源/权利/署名、可选原创maps、透明封面、八固定QA视图及实际GLB多角度runtime证据。视图是hero/reversehero/front/side/rear/top/clay/silhouette，零转台，有实际问题才补针对性视角。源重开、两次语义重建、Khronos/project、目标loader、功能渲染和简化多实例场景需实际记录并绑定精确GLB hash，软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务决定，不为微观复原不确定反复返工。新模型hash使旧受影响verdict失效。用户已授权QA通过分批push/merge，无需逐模型审批，但模型QA、完整candidate/profile合同、整合发布分别记录，PASS不能跨层冒用。

## 当前显式candidate profile

本轮读取了当前main新增的 `docs/candidate-profile-compatibility.zh-CN.md` 和 `schemas/templates/static-profile-contract.template.json`，只把选择与policy哈希保存在本目录`profile-policy.json`，没有改CI/validator/release代码。新brief机器字段用 `publication_authority: separate`，批量发布授权单独pin。实际候选依照届时最新main的模板填写结构化blockers与匹配criterion IDs；没有模型证据前不得制作假sidecar或填假hash。

明确使用 `static-stylized-v1`（当前规则2026-10-18.1），实际candidate就绪后用 `scripts/candidate_profile.py` 生成绑定真实candidate/原输入/policy的sidecar，再显式调用 `scripts/validate_candidate.py ... --profile static-stylized-v1 --profile-contract ...`。兼容不能删旧错误或自动降级；若仍有结构/criterion/evidence错误，记录并修复真实问题，不能把模型QA PASS当完整candidate gate PASS。保存的policy pin和版本在执行时复核，变化则新版本记录，不静默换哈希。

## 去重、领取与恢复

`dedup-snapshot.json`保存全部抓取分支SHA、当前main、所选ID模型/具名generator扫描、发布描述符哈希。前九批36项全部排除，加上原发布资产/已有候选；没有把QA中的07–09或待兼容发布的04–06当成可重做项目。当前远端未发现本轮12项模型/具名generator，但共享脚本内函数、未推送工作和实时会话仍由父任务派发前协调。

本轮state为planned_awaiting_parent_dispatch，claims为空、无attempt或QA结论，planner不自行派发或制作。父任务的明确独占派发和最新state才是现时授权证据；既有worker不因旧副本空claim而停工。未知实际任务/时间/路径/哈希留空，不编造。父任务串行登记状态并追加events，常规push冲突先fetch/reconcile，禁止force。

执行从届时最新main的独立worktree/branch起步，只带必要规划与helpers，不整体挑入旧分支CI/site/release改动。build/preview/render分lane，共享协调池默认1worker×2threads，父任务分配实际CPU/配额；不让每批各占满主机。实际generator出现后才生成完整runner manifest；此queue非可执行manifest，不含不存在的generator命令。新attempt/revision隔离、保留失败记录；未完成/缺文件/输入工具配置或完整输出hash变化不能复用成功。

运行 `python3 production/continuous-small-life-round04-20261018/verify_plan.py`只核验规划，不启动生产。完整runner规则见[仓库队列契约](../../skills/blender-lowpoly-pipeline/references/parallel-queue.md)。变更冻结输入提升版本并重算freeze/checksums；state/events作为动态Git记录。

常规checkpoint/no-reply push，署名Leon Made This <8357465+s010s@users.noreply.github.com>。不合并main、不生产、不上传Google Drive、不改权限、不强推。
