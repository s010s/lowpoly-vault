# batch-27 — 仅计划，尚未派发

**当前父任务进度：main已推进127，公网证据核对中（此前确认115）；31–33独立模型QA全PASS；34制作中、35候选完成待QA、36已派制作。模型QA/正式profile/提交发布/公网确认分别记录，当前state及父任务派发覆盖历史空claim。**

**当前父任务进度：线上确认115、22–24已发布；25–27发布整合中（27报告内容PASS与其正式profile阻塞分开保留）；28–30模型QA均PASS；31–33候选全完成且已派独立QA、无结论。最新state/父任务派发证明覆盖历史初始空claim，不从模型QA推断发布。**

**当前父任务进度：线上确认103，22–24发布整合中；25/26模型QA PASS、27候选完成待QA；28/29候选完成且已派独立QA、无结论，30刚独占派制作。未提供的thread/turn/审核source不猜，实际state与父任务证明优先于历史初始空claim。**

**当前父任务进度：22–24全独立模型QA PASS，23仅标签修正、模型未变；25候选完成待独立QA，26独立模型QA PASS，27制作中。此处不新增线上数量/发布确认；实际state和父任务派发证明优先于历史初始空claim/旧阶段文字。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。海藻限原保存藻轴/轮盘/扁平分枝；潜穴限示意剖面且不指定制造者；潮坪和溶沟岩面是代表性片区，不归一化成小石或假称实测古地点。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `sollasina` | Sollasina plated tube-foot echinoderm / Sollasina（板甲管足棘皮动物） | `items/sollasina/` | 低矮板甲体与多条细长板甲管足补充棘皮动物形态，区别于长刺海胆/海星。 身体与管足连续、有主次间隙，管足不是随机刚刺；颜色/姿态为教学美术，微板/管足精确数量不强求，不作运动机制复原。 |
| `ottoia` | Ottoia ringed predatory worm / Ottoia（环纹捕食蠕虫） | `items/ottoia/` | 粗环纹软管体与可缩吻的基本关系补充低位蠕虫轮廓，区别于叶毛和叶足类。 柔和环纹躯体、克制吻端和后部小钩提示，不做满口尖牙捕食场景；保持自然弯曲和粗细过渡，不用等径圆筒机械堆叠。微钩数/软组织可简化。 |
| `eocladus` | Eocladus multilevel algal branchwork / Eocladus 复枝绿藻 | `items/eocladus/` | 多级藻体分枝与清楚粗细阶差增加标本型海藻负空间，区别于两区轮枝或带状枝。 只做原保存扁平分枝布局，多级枝序以粗细层次表达，简化末枝数量；保留needs-specific-reference，可靠基础分枝资料足够即可，不虚构具名图、未知整株或根系。 |
| `limestone-pavement` | Limestone pavement / 石灰岩溶沟石面 | `items/limestone-pavement/` | 近平坦石灰岩块与深溶沟增加可走近自然岩面，区别于紧接多边岩柱。 平缓岩块之间的深溶蚀裂隙有连续性/排水逻辑，不是工业地砖或泥裂缩放。代表性露头片区而非完整古地貌；原biomes cave不改成已验证海岸，不声称海水侵蚀成因。 |

新任务明确采用main static-stylized-v1 / 2026-10-18.1。publication_authority机器字段为separate；本目录profile-policy.json是规划说明，不是validator sidecar。真实candidate出现后才生成真实hash sidecar，显式调用新profile。fixed8每标签一张、零转台，side不伪造left/right；额外诊断另存。references每来源use=consulted-only、incorporated=false、title/url/rights_note非空，全局no_incorporated_third_party_assets=true；不猜license。blockers用结构对象，criterion IDs匹配brief。legacy_result如实保留，profile兼容不等于valid/approved、模型QA或发布PASS。

独立QA优先新上下文；先填/核对同目录batch-27-QA-SCOPE.json的真实source/逐项GLB hash及恰好四ID，报告回显相同对象，错批/错source即invalid_review_wrong_subject、不计PASS。当前scope为未就绪规划，不启动QA。metadata依原worlds/分类等facet，research pack不自动成为已发布pack。潜穴检查灰色内部剖面，不按外轮廓判识别；海藻仅原标本范围，地形保留明确米制代表片区。
