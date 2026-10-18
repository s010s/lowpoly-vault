# 第六轮16–18：小动物、植物器官和自然物，12项

**仅计划，尚未领取/派发；不启动Blender、不制作、不合并main。** 最后确认live43；07–09仍在发布适配CI，10–12全独立模型QA PASS并已交release排队；13/14候选完成且独立QA进行中，14当前turn未知留空；15独占制作。历史空claim或旧queue未派发文字不否定父任务当前明确授权。

## 三批各四项

| 可直接使用的任务文件 | 精确inventory ID | 原始中英文名 | 选择理由 |
|---|---|---|---|
| [batch-16](batch-16-TASK.md) | `pleurodictyum` | Pleurodictyum low cup-disc coral / Pleurodictyum（低杯盘珊瑚） | 低穹盘与几个较大相邻杯提供低矮珊瑚轮廓，区别于Micrabacia单杯放射盘。 |
| [batch-16](batch-16-TASK.md) | `matonidium` | Matonidium comb-ray frond / Matonidium 掌状蕨 | 放射叶轴与成对羽片形成掌状蕨叶展示，区别于旧羽状整丛。 |
| [batch-16](batch-16-TASK.md) | `yohoia` | Yohoia elbow-clawed arthropod / Yohoia（肘爪节肢动物） | 方形头甲和成对肘爪提供新的前肢轮廓，区别于Leanchoilia长丝三指附肢。 |
| [batch-16](batch-16-TASK.md) | `gypsum-desert-rose` | Gypsum desert rose / 石膏沙漠玫瑰 | 交叠含沙板晶构成放射集合体，为近景自然物增加矿物形态。 |
| [batch-17](batch-17-TASK.md) | `isastraea` | Isastraea polygon-cup reef coral / Isastraea（多边杯造礁珊瑚） | 低块体与相接星隔大杯补充造礁珊瑚，区别于长杯簇与细蜂巢管。 |
| [batch-17](batch-17-TASK.md) | `araucaria-mirabilis` | Araucaria mirabilis attached cone specimen / Araucaria mirabilis 南洋杉类球果 | 单枝附生球果的鳞片浮雕丰富植物器官展示，区别于另一个整树冠。 |
| [batch-17](batch-17-TASK.md) | `onychonycteris` | Onychonycteris / Onychonycteris（古哺乳形类） | 宽早期蝙蝠翼与翼指爪提示补充小型飞行哺乳动物，不再增加鸟类换色。 |
| [batch-17](batch-17-TASK.md) | `pillow-lava-outcrop` | Pillow lava outcrop / 枕状熔岩露头 | 膨鼓枕瓣、细颈和冷却外壳为海底/自然场景提供新的过程岩体。 |
| [batch-18](batch-18-TASK.md) | `spinolestes` | Spinolestes / Spinolestes（古哺乳形类） | 紧凑有毛小兽与局部棘皮区补充陆地近景，区别于蛙和蝙蝠。 |
| [batch-18](batch-18-TASK.md) | `odontogriphus` | Odontogriphus smooth-bodied grazer / Odontogriphus（光背软体动物） | 无壳扁椭圆体、宽腹足与边缘鳃带补充低位软体海生动物。 |
| [batch-18](batch-18-TASK.md) | `trapa` | Trapa harpoon-horned fruit / Trapa 菱属四角果化石 | 紧凑果体与四条反向角臂补充果实器官展示，区别于球果/蕨叶。 |
| [batch-18](batch-18-TASK.md) | `flint-nodule` | Flint nodule / 燧石结核 | 白垩状外皮与贝壳状断口提供小型岩石材质/结构差异，区别于矿物充填结核。 |

2项珊瑚、4项小型动物、3项植物器官标本、3项自然物。模型可分别服务海洋/陆地/飞行近景和教学展示，没有同种换色、密度或损伤变体计数，也没有大恐龙。两种新珊瑚必须保留低穹盘多杯/低块体星隔大杯的结构差异，不能把旧群体珊瑚缩放改孔密度当完成。四动物分别是肘爪小节肢、宽翼早期蝙蝠、小型棘皮有毛兽、扁体无壳软体。自然物是板晶矿物集合、枕状凝固露头、外皮与断口不同的燧石结核，成因和可见构造互异。

## 三项植物严格保持器官范围

三项原清单均`representation=fossil-specimen` / `reconstruction_type=specimen`。Matonidium只做放射叶轴与羽片的保存蕨叶；Araucaria mirabilis只做有来源的短枝附生球果，不能扩为想象整树；Trapa只做四角果实，不能从果实扩出未知茎叶根。用原类别plants归档不代表已经知道完整活体。可以不带岩板自由展示，但metadata仍为保存器官教学概念，圆厚化和配色是美术，不冒充新测标本。

海洋珊瑚/小节肢/软体、陆地小兽、飞行哺乳动物及植物器官分别使用，不承诺共存生态。石膏沙漠玫瑰是矿物，不是植物花；燧石“贝壳状断口”指断裂纹理，不是贝壳化石。枕状熔岩为代表性露头块，不由此声称具体古火山地点/年代。

## 真实输入、目录和去重

`items/<ID>/`含完整原始inventory-record、brief、build-config、references、freeze；保留原1000资料不改写、不增加条目。queue.json保存精确原名、理由、名义尺度和预算。原名义尺寸均为美术起点，不是新量化石：动物体长/翼展、植物器官跨度、岩体块宽等见逐项config。不要统一缩成单位立方体；展示放大单独标识，微小个体近景使用，不承诺远处可辨。

脚本和attempt：`production/continuous-small-life-round06-20261018/work/<batch>/<ID>/r001/`；候选包：`assets/candidates/continuous-small-life-round06-20261018/<batch>/<ID>/r001/`；QA通过后父任务整合：`assets/additions/<ID>/continuous-small-life-v1/`。版本/attempt分别隔离，旧日志和hash证据保留。

前十五批60项已全部排除，含已派发13/14/15；同时排除其他已发布及既有候选。`dedup-snapshot.json`有全部抓取ref SHA、模型/具名脚本扫描和当前main的release描述符哈希。没有因QA PASS、现有文件或旧空claim重做任何在途项目。当前远端未发现这12项模型/具名generator；共享脚本内函数、未推送工作及实时会话仍由父任务正式派发前核对。

## 参考和权利

Pleurodictyum和Isastraea保留needs-specific-reference，另外10项原reference-ready；只是研究状态，不是新模型QA。可靠基础资料能支撑多杯盘/星隔杯等基本形态即可合理风格化，属级微观计数、未保存软组织、真实尺寸、行为/飞行机制不强加。蝙蝠/小兽保留核心比例和识别结构，不追求逐骨逐毛复原，不因不确定细节反复返工。

来源title/url/supports/访问方式继承真实inventory，本轮未重新打开外部论文；不声称继承opened等于本轮已读，不伪造具名图/来源或PASS。网格与可选贴图原创，参考仅查阅；consulted-only不是外部照片/扫描/模型的开放许可，实际并入内容需真实许可/署名，不能用consulted来源当并入贴图出处。

## 制作和预算

制作必须GPT-6.1 Sol medium；独立QA由父任务新任务派GPT-6 Luna xhigh，制作自检不替代独立QA。延续认可v002自然精致、可信比例、柔和衔接、适度卡通，80–240px通常观看、约480px中近景可看。避开机械拼接、随机噪声和不必要大贴图。

14,000三角形、1,000,000GLB bytes为硬上限而非目标，通常约100–500KB，更小同样可以；增加面数须有轮廓/比例/衔接可见收益，硬上限内超通常区间记录收益即可。≤6材质/≤30 primitives；最多1张≤256px原创贴图，总编码≤65,536bytes、解码预算≤524,288bytes。源/求值/导出POSITION顶点、三角形、材质/primitive、字节/纹理和实例分别报告，不凭面数宣称质量/帧率。

可编辑Blend、独立GLB、可重建generator/config及全部语义依赖hash、中英metadata/范围/来源/权利/署名、可选原创map、透明封面、fixed8及实际GLB运行时证据。源重开、两次语义重建、Khronos/project、目标loader、功能渲染和简化多实例场景均绑定精确GLB hash；软件渲染不冒充物理设备性能，不承诺动画就绪。

一次汇总独立QA、至多一次计划内外观修复，真实必需缺陷未解决交父任务决定，不为微观复原不确定开无限循环。新模型hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但只有父任务唯一release协调器整合；不能把模型QA PASS当已发布。

## 显式静态profile与references合同

本轮读取当前main已合并文档/代码并保存SHA到profile-policy.json，明确采用`static-stylized-v1 / 2026-10-18.1`。profile-policy.json是规划说明，**不是**可传给validator的sidecar。brief机器字段`publication_authority: separate`，用户发布授权另pin；不改main validator/CI。

- 主固定manifest恰好hero/reversehero/front/side/rear/top/clay/silhouette各1张，转台0；记录真实相机、GLB/file hash和尺寸。side不伪造left/right，诊断额外视图另存，不破坏主fixed8。
- 每来源use=consulted-only、incorporated=false、真实title/url及非空rights_note；全局no_incorporated_third_party_assets=true。不猜第三方license，实际贴图有独立原创/许可provenance，不能指向仅查阅来源当并入素材。
- candidate基于届时最新main模板，blockers结构化，stage/criterion IDs与本brief逐项匹配；真实source/generator/config/报告/图都绑定hash，unknown/fail不改写成PASS。
- candidate真实存在后才用`python scripts/candidate_profile.py <candidate.json> --root <repo-root>`生成sidecar，再显式`python scripts/validate_candidate.py <candidate.json> --profile static-stylized-v1 --profile-contract <sidecar> --json`；最终批准另用--require-approved，不预填假hash/假候选。
- 默认legacy-v1不是本轮验收入口，不为误跑旧要求补无意义转台/left/right或改冻结brief。显式新profile返回的legacy_result原样保存，不自动回退、不删旧错误、不伪造旧PASS。
- profile_contract_status=pass只代表兼容，不等于valid、approved_for_brief、独立模型QA或生产发布；实际批准明确记录profile/rule版本。执行前复核policy/tool，变化需新版本冻结，不静默换hash。

## 领取与恢复

本轮state为planned_awaiting_parent_dispatch、claims为空，无模型/attempt/sidecar/QA。父任务正式分工前核对实时占用，写独占task/thread/branch/base SHA并追加events；未派发者不能自认领。已有worker的父任务明确授权与最新state覆盖旧副本空claim；未知任务turn/时间/路径留空不猜。

从届时最新main独立worktree/branch起步，只带必要规划/helpers，不整体挑旧CI/site/release改动。共享协调池默认1worker×2threads，父任务分配实际CPU/配额；build/preview/render分lane，不让每批各占整机。实际generator出现才生成完整inputs/outputs/timeout的runner manifest，此queue并不可执行。新attempt/revision隔离、失败日志保留，未完成/缺文件/输入工具配置或完整输出hash不同不能复用成功。

运行`python3 production/continuous-small-life-round06-20261018/verify_plan.py`只检查规划。冻结输入改动提高版本并重算freeze/checksums，state/events为动态Git记录；父任务串行协调状态，正常push冲突先fetch/reconcile。原runner契约和skills继续沿用，本轮明确模型/风格/profile要求覆盖旧要求。

常规checkpoint/no-reply push，署名Leon Made This <8357465+s010s@users.noreply.github.com>；不合main、不制作、不派发、不上传Google Drive、不改权限、不强推。
