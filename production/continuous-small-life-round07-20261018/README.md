# 第七轮19–21：恢复延后植物并补充小型生物/自然物，12项

**只规划，未派发制作；不启动Blender、不合并main。** 线上67已由父任务明确确认，main `ccf48bb446dd4d0a710ab14dfc05d6fbf7064cdb`，PR9/Pages/public Chromium全部通过。13–15全模型QA PASS、下一次67→79发布任务容量失败待恢复；该失败不撤销已完成的67。16–17候选完成且独立QA运行无结论，18已独占制作。最新state与父任务派发证明优先于历史空claim/旧线上数量。

## 三批各四项

| 可直接使用的任务文件 | 精确inventory ID | 原始中英文名 | 选择理由 |
|---|---|---|---|
| [batch-19](batch-19-TASK.md) | `cooksonia` | Cooksonia sporangial shoots / Cooksonia 裸轴植物 | 简单Y分叉与扁平顶囊补充稀疏低位植物，区别于刺轴、K节点与膨大基体。 |
| [batch-19](batch-19-TASK.md) | `cambroraster` | Cambroraster horseshoe-shield radiodont / Cambroraster（马蹄甲奇虾类） | 宽马蹄甲、后掠侧翼与深眼切口提供新的近底轮廓，区别于双瓣甲和角棘头盾。 |
| [batch-19](batch-19-TASK.md) | `bedrock-pothole` | Bedrock pothole / 河床壶穴 | 裸露河床岩石中的深圆穴增加自然物的内部空间，与外部风化小孔不同。 |
| [batch-19](batch-19-TASK.md) | `quartz-prism-cluster` | Quartz prism cluster / 石英柱晶簇 | 六方柱和尖端从天然基质生长，区别于石膏玫瑰板晶。 |
| [batch-20](batch-20-TASK.md) | `leclercqia` | Leclercqia divided-leaf shoot / Leclercqia 裂叶石松类植物 | 分裂叶单元与回曲中央尖端丰富小型石松形态，区别于裸轴/刺轴植物。 |
| [batch-20](batch-20-TASK.md) | `canadia` | Canadia leaf-bristled annelid / Canadia（叶毛环节动物） | 扁长虫体、叠覆宽刚毛与两根头须丰富海底柔软小生物。 |
| [batch-20](batch-20-TASK.md) | `salvinia` | Salvinia paired floats and submerged leaf / Salvinia 槐叶萍类水蕨 | 成对宽浮叶和沉水分叉叶丰富淡水表层，区别于基囊浮生莲座或有根叶柄。 |
| [batch-20](batch-20-TASK.md) | `load-cast-bedding` | Load-cast bedding / 负载构造岩层 | 上层鼓状下垂叶瓣进入下方软层，补充地层内部几何，区别于表面泥裂和波痕。 |
| [batch-21](batch-21-TASK.md) | `montsechia` | Montsechia flexible fine-leaf shoots / Montsechia 水生早期被子植物 | 细分叉茎、小叶与成对卵形果补充淡水水下植物，区别于浮生水蕨。 |
| [batch-21](batch-21-TASK.md) | `dollocaris` | Dollocaris giant-eyed arthropod / Dollocaris（巨眼甲壳动物） | 深罩甲、两枚大眼与三对捕捉足补充罩甲生物，区别于大眼游泳蟹。 |
| [batch-21](batch-21-TASK.md) | `coelurosauravus` | Coelurosauravus / Coelurosauravus（史前爬行类） | 小型爬行体与侧方骨杆支撑滑翔膜丰富陆地上方层，区别于鸟和蝙蝠。 |
| [batch-21](batch-21-TASK.md) | `columnar-jointed-outcrop` | Columnar jointed outcrop / 柱状节理岩体 | 紧接多边岩柱与台阶状断端补充自然岩体竖向节奏，区别于矿物尖晶簇。 |

总体4植物、4小型动物、4自然物，不追加同种颜色/密度/损伤变体。没有再做大型恐龙：宽马蹄甲、叶毛虫体、深罩大眼、小爬行体侧膜分别有不同轮廓；深圆穴、六方尖晶、下垂负载层、多边台阶岩柱表达不同结构和过程。

## 四项延后计划的唯一恢复

Cooksonia、Leclercqia、Salvinia、Montsechia最初在round02未派发版本中规划，后来按海底珊瑚优先要求移到 `production/continuous-small-life-round02-20261018/deferred-items/<ID>/`，不属于当前round02的12个活跃job。此次检查前十八批72项活跃/已制作ID、最新state和所有抓取ref模型/具名generator，未发现这四项已有模型或占用。它们是同一稳定ID恢复计划，不是新增概念或重复制作。

每项 `planning_lineage` 指向旧包；`items/<ID>/upstream-deferred/` 原字节保存旧输入，`upstream-deferred-hashes.json`绑定全部文件，freeze再绑定该manifest。旧包含旧规范/初始未派发描述，只作来源，不能作为第二个执行任务。新brief/config/reference/freeze是当前唯一版本。旧round02 state的`deferred_plan_transfers`与追加event已登记新批次位置，原round02模型job/发布状态不变。

没有修改原1000资料，也没有把旧archive加入当前模型计数；本轮4项恢复仍无owner/attempt/QA。若父任务掌握未推送工作，派发前重新协调，而非仅凭路径扫描抢占。

## 范围和生境

Salvinia和Montsechia只作淡水湿地植物：Salvinia下垂分叉束是沉水叶不是根，Montsechia不添加原资料未支持的根/大花。Cooksonia顶囊裸轴与Leclercqia分裂叶均是各自整株教学概念，不复用旧植物只改变密度。海生三动物、陆地滑翔爬行类、淡水与早期陆地植物分区使用；不从同一批次推断同地点同时代共存。

Coelurosauravus突出侧方杆支撑膜与四肢的区别，不做鸟翼或蝙蝠手翼，不承诺飞行动画；Dollocaris眼大但仍需可信比例。河床壶穴是有深度的几何，不画黑圆假穴；负载层是上层向下鼓入软层，不是表面岩石噪声；石英晶簇的天然基质和不同朝向区别于紧接的节理岩柱。所有自然物只是过程/形态教学，不宣称精确古地点、年代或实测参数。

## 真实输入、预算与目录

所有ID来自原1000清单，本轮12项原research gate均reference-ready，但不等于模型QA/科学复原或权利审计。`items/<ID>/`包含原inventory-record、当前brief/config/references/freeze；queue.json有精确原名、理由、预算、名义尺度与输出路径。尺度是美术起点，不是新量化石；不统一缩为单位立方体，展示放大另标，微小对象不承诺远处可读。

制作脚本/attempt：`production/continuous-small-life-round07-20261018/work/<batch>/<ID>/r001/`；候选：`assets/candidates/continuous-small-life-round07-20261018/<batch>/<ID>/r001/`；QA后父任务整合：`assets/additions/<ID>/continuous-small-life-v1/`。

GPT-6.1 Sol medium制作；父任务新派GPT-6 Luna xhigh独立QA，制作自检不能代替。自然精致、可信比例、柔和衔接、适度卡通，通常80–240px观看与约480px中近景；不用机械拼接或大贴图假精细。14,000三角形/1,000,000GLB bytes是硬上限，不是目标；通常100–500KB、更小亦可，只为轮廓/比例/衔接可见收益增加几何，硬上限内超通常区间记录收益即可。≤6材质/≤30 primitives，最多1张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。源/求值/导出POSITION顶点、三角形、材质/primitive、字节/纹理和实例分开记录，不凭面数判美或设备性能。

基础可靠参考能支撑辨识形态且素材原创/有实际授权即可风格化继续。原title/url/supports/访问等级如实保留，本轮未重开外部论文；不伪造已读图/来源或属级强断言。微观计数、未保存软组织、真实尺寸/运动机制不额外强求，不为不确定复原细节反复返工。一次汇总独立QA、至多一次计划内外观修复；真实必需缺陷未解决交父任务裁决，模型新hash使旧受影响QA失效。

交付可编辑Blend、独立GLB、可重建generator/config及语义依赖hash、中英metadata/范围/来源/权利/署名、可选原创map、透明封面、固定视图与实际GLB runtime证据。源重开、两次语义重建、Khronos/project、目标loader、功能渲染及简化多实例场景绑定精确GLB hash；软件渲染不冒充物理设备性能。

## static profile完整要求

当前main文档/代码哈希固定在profile-policy.json，使用`static-stylized-v1 / 2026-10-18.1`。profile-policy.json是计划说明，不能当validator sidecar。机器publication_authority为separate，已有批量发布授权另pin。

- 主fixed8恰好hero/reversehero/front/side/rear/top/clay/silhouette各1张，转台0；记录真实相机、GLB关联、文件hash和尺寸。side不伪造left/right；额外诊断另存，不能破坏主fixed8。
- references每来源use=consulted-only、incorporated=false、title/url/rights_note真实非空，全局no_incorporated_third_party_assets=true。查阅不等于外部媒体授权；实际并入内容须真实许可/署名，原创贴图有自己的provenance，不能用consulted来源当并入纹理出处。
- candidate按最新main模板，blockers是结构对象，stage/criterion IDs逐项匹配本brief；source/generator/config和所有必需证据实际hash绑定，unknown/fail不改写成PASS。
- candidate真实存在后才用scripts/candidate_profile.py生成真实sidecar，再显式运行scripts/validate_candidate.py --profile static-stylized-v1 --profile-contract <sidecar>，最终需要批准时用--require-approved，不填假hash/假候选。
- 默认legacy-v1不是此任务验收入口；不为误跑旧gate补无意义转台/左右视角或改冻结原文。新profile中的legacy_result如实保留，不自动回退、不删旧错误、不伪造旧PASS。
- profile合同兼容、valid/approved_for_brief、模型独立QA和生产发布是不同结果；profile_contract_status=pass不替代其余任何门槛。批准明确记profile/rule，执行前复核policy/tool，变化需新版本冻结。

## 去重、领取、恢复

`dedup-snapshot.json`保存全部抓取ref SHA、72个前序ID的状态/claim、选中ID模型/具名generator扫描与release描述符。已发布/已有候选一并排除，不能因为QA或容量失败就重做在途项目。共享脚本内部函数、未推送工作与即时会话不由文件名扫描完全证明，父任务派发前统一核对。

本轮planned_awaiting_parent_dispatch，claims为空、无attempt/模型/sidecar/QA。父任务登记独占task/thread/branch/base SHA再派发，planner不启动；既有worker以最新state及父任务明确派发为授权，历史副本空claim不阻塞工作。未知任务/时间/路径留空不猜。

从届时最新main的独立worktree/branch起步，仅带必要规划/helpers，不整体挑旧CI/site/release改动。共享协调池默认1worker×2threads，实际CPU/配额父任务分配，build/preview/render分lane；实际generator就绪才生成完整inputs/outputs/timeout的runner manifest，本queue不可直接执行。新attempt/revision隔离且保留失败日志，未完成/缺文件/输入工具配置或完整输出hash变化不能复用成功。

运行 `python3 production/continuous-small-life-round07-20261018/verify_plan.py`仅检查规划。输入变更提高版本重算freeze/checksums；动态state/events由Git追踪，父任务串行协调，正常push冲突先fetch/reconcile。用户已授权QA通过分批push/merge无需逐模型审批，但只有唯一release协调器执行发布，本planner不自行制作或合main。

署名Leon Made This <8357465+s010s@users.noreply.github.com>；常规checkpoint/no-reply push，不强推、不改权限、不上传Google Drive。
