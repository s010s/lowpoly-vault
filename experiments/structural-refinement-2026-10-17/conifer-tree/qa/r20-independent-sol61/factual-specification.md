# r20 factual / specification 独立补充审查

日期：2026-10-17。对象保持固定 commit `265b47eed899307228d609355cc46c6d6992f61d`，未对候选作任何修改。

GLB SHA-256 `c3a215eda3ceb3e4ec95bdb31446e180fd9f9d1f7eaa24131459a0db6fa56b40`；brief SHA-256 `50466e78d5da46f10532b601cc2d4ea15ef2fae44c2881a8b8e0e01c15e99a5e`；references SHA-256 `6f1ff6cb8fa57c8aec580945eaa04ee141240988cfbdc90b075007d8d9afbe4a`。

结论：**factual-acceptance = pass，严格限于冻结的通用风格化针叶树概念；honest-concept = pass。specification-acceptance = fail（交付说明/指针有可修复不一致），模型与数值规格子项通过；实际GPU/scene仍unknown。** 不代签其他任务尚未运行的证据，也不组装最终总通过记录。此前报告里的“本次未完成全面factual源核查”由此补充审查推进，不追溯修改历史报告。

## 事实特征与来源逐项对照

本次在线阅读所有必需的植物参考相关段落，并对照此前实际打开的53张当前r20图片；不需要再次渲染同一模型。

| 特征或声明 | 公开证据、具体位置 | 当前模型/文字对照与结论 |
|---|---|---|
| 连续主轴与从属侧枝 | [PRI Digital Atlas, Branching](https://www.digitalatlasofancientlife.org/learn/embryophytes/tracheophytes/branching/)，Lateral/Axillary branching及Monopodial growth：主顶端延伸、侧芽产生侧枝；页面也明确针叶树有腋生分枝 | 主干连续、侧生弯枝和细枝层级可读。pass，支持一般结构，不认证每个节点的植物发育过程。 |
| 水平/下垂、羽状侧枝类比 | [HK Herbarium 2018 Third Revision](https://herbarium.gov.hk/en/publications/books/book7/book7-2018-third-revision/index.html)，印刷页17 Features for Identification。该表同时列2014/2015/2018修订列，异叶南洋杉与柱状南洋杉不能混为一个物种 | 对应条目支持平展/下垂小枝及羽状侧枝；可支持风格化架构。pass（仅一般形态）。现代Araucaria结构与Metasequoia式叶组组合是艺术概括，不是已验证的单一物种。 |
| 狭长、对生/近对生、柔软羽状针叶 | [NC State Metasequoia](https://plants.ces.ncsu.edu/plants/metasequoia-glyptostroboides/)，Quick ID、Leaves/Leaf Description：针形、线形、对生及柔软羽状外观 | 当前窄片沿细轴成对组织，符合采用的类比；开放表面和106三角形/束属于实现方式。pass，不证明实际触感。 |
| 扁平、梳状排列和轻微弯曲 | [C.J. Earle, Description](https://www.conifers.org/cu/Metasequoia.php)，叶生于相对枝叶单元、叶列呈梳状，叶线形扁平、可略弯；原文还给出现生树的实际尺寸、短尖/钝叶端 | 支持A羽状窄叶的概括。12对加短终端、放大的宽长、尖端角度、149束数量不等于该物种测量值；brief已明确为艺术选择。pass within concept。 |
| 史前设计语境 | [NHM, How to grow a dinosaur garden](https://www.nhm.ac.uk/discover/how-to-grow-a-dinosaur-garden.html)，Fossil forests、Plants of the Jurassic Period；讨论化石证据与现代类比、侏罗纪针叶植物 | 只支持宽泛的史前灵感语境，不支持该形状存在于某个具体地层/地区。brief的Jurassic-Cretaceous inspired context作为艺术语境可接受；不能改写成“侏罗纪/白垩纪该种树的准确复原”。 |
| 化石例证的时代边界 | PRI页首Metasequoia occidentalis，Yale YPM PB005960的说明明确是Eocene / Washington | 这是始新世例证，不能充作中生代该模型身份、尺度或叶形的证明。当前模型未作这项声称，故不形成未满足的物种复原门禁。 |
| 既有结构目标 | 固定工作区 `docs/case-studies/lightweight-triceratops.md` 的First-ten triage，Conifer行：原始宽叶壳、旧版板状连接/星爆叶簇是失败目标 | 当前图像已独立审查，不再是这些形式。该内部来源只支持设计目标，不当作植物学证据。 |
| 概念标签 | brief.claim_scope、metadata.scientific_status、metadata.description、README的Reference and license | 都保留非命名灭绝种、现代类比、艺术尺度与分组的限制。pass。 |

可保留的准确描述：“约7米的风格化针叶乔木概念；以现代针叶植物的主轴/侧枝与羽状窄叶结构为类比，具有分离细针、轻透冠层和自然天窗。”

属于艺术概括的内容：26主枝、149喷束、每束12对叶条加终端、106三角形/束、具体枝条弧度、枝距和位置、绿色/木色、7米尺寸、缺失下枝、天窗与局部搭接。它们无需伪造化石来源，但交付文字必须继续明确其艺术性质。双面开放叶面是低模表示，不是真实叶厚和组织解剖。

**本结论不允许声称**：这是Metasequoia glyptostroboides、Araucaria heterophylla/columnaris或某个已命名灭绝种的精确模型；来自特定中生代地点/地层；7米及每叶尺寸由化石测量；现代物种从中生代至今形态完全不变。未建球果、芽、真实树皮/叶背细节不违反当前通用环境道具brief，但也不能借此作为物种鉴定模型使用。

照片与权利边界：NCSU页面为Francois Gulbert叶片照片列有署名/许可链接。此次点击该单独图片返回检索错误，未把maker曾查看照片的说法冒充为本次独立实际照片检查；以上判定依赖已读的NCSU文字、Earle与HK条目以及已看候选像素，照片不是冻结brief的必需独立事实来源。原始照片未下载进QA或候选，不嵌入交付物。现有纹理/图像数为0、生成输入为代码与已记录木质快照，符合consulted-only记录；不是对所有创作历史作超出证据的权利保证。

## 已核实的规格子项

| 子项 | 结论与证据 |
|---|---|
| 约7m、米单位、静态道具 | pass。Three.js独立解析尺寸 `[4.661952019,7.042110443,5.167210817]` m，地面最小Y=0。7.042m符合“约7m”；不是生物测量。 |
| 根节点、变换及展示场景分离 | pass。GLB场景只有identity根 `conifer-tree` 及两个mesh节点，共3 primitive；没有灯光、相机、动画、skin、外部纹理或演示地台。根extras声明米与原作署名。画面根部落地；实际组合场景接地仍须另测。 |
| 几何/材料/纹理上限 | pass。19,052≤19,500 tri；3 materials /3 primitives；715,500≤1,000,000 B；0 textures，符合冻结brief。上限合规不是GPU性能通过。 |
| NORMAL16交付profile | pass。FLOAT32位置/index次序/材质/变换精确保留；SHORT normalized VEC3法线8-byte stride、required KHR_mesh_quantization，最大误差0.001443162°≤0.001444°。由独立audit与parser/validator证据支持。 |
| 六项required_deliverables | pass。source、generator、config、wood-source、core-generator、pack-generator文件存在，六项SHA-256均与brief匹配；GLB/brief/reference hash也匹配。 |
| 编辑/重现输入 | 文件完整性pass。源blend与生成/打包脚本、木质快照/config及既有helper依赖有记录；既有重建输出字节一致已核对。没有假称此次再次启动Blender。 |
| 诊断图片覆盖 | pass。24个不同方位、0–345°每15°，另必需front/rear/left/right/top/bottom/clay/clayalt/wire/detail均存在并在上一轮实际打开；37+7+9=53 raw，manifest绑定相同模型/brief/references。 |
| A用途与可用尺度 | pass（当前CPU像素）。128px保留树形/层级，512px可近看细羽束；没有逐针128px保证。用途仍是孤立展示与声明的稀疏林组，非密林性能承诺。 |
| GPU与scene运行规格 | unknown。固定Three.js0.180.0、1/16/32 independent clones、16.7ms目标已声明；此次不填入未执行的设备、画面和计时。无LOD声明，不额外要求必须制作LOD。 |

## 规格失败项：有限的文档修复，无需重做模型

1. **S1 metadata.preview失效**：`metadata.json` 指向 `candidate-r20/rebuild-runs/local-rebuild-01/outputs/conifer-tree/preview-hero.png`，实际不存在。应指向已存在且确认用途的当前preview，并明确当前诊断图不是尚未生产的24alpha发布预览；不能保留不存在的资源作为已交付内容。
2. **S2 metadata.delivery_storage.equivalence_report失效**：值为 `../normal16-equivalence.report.json`，从metadata所在目录解析至 `conifer-tree/normal16-equivalence.report.json`，不存在。当前真实等价报告为候选内 `geometry-equivalence.report.json`；由maker在可审计的新文档检查点修正绑定，勿改模型。
3. **S3 brief预算增幅算错对象**：`budget_rationale` 把19,500 guard写成相对r12实际18,706增加1.85%。实际 **19,052模型值**相对18,706增加1.8497%；**19,500 ceiling**相对18,706增加4.2446%。数字上限和模型计数各自合规，但这句理由必须如实区分，不能用1.85%为更高上限背书。
4. **S4 references.study_scope遗留描述**：含“two secondary fans”，来自r17 A/B研究，不是当前冻结的单轴A叶构造。应明确这是历史被比较方案，或用准确当前范围取代；不能让最终reference ledger误述当前模型。该项是记录准确性问题，不要求改变已选A形态。

metadata里的GLB/blend路径虽仍指向build-run目录，但目前文件存在且hash与声明一致；此次没有把它们误报为丢失。交付/集成时仍应使用最终约定的相对路径，避免将内部重建目录当成唯一公开资产位置。

以上修复属于记录修正。应保留265b47e原冻结检查点，在新检查点更正并更新所有受影响的brief/reference/metadata/freeze/candidate evidence绑定。GLB和图片字节若不变，不要求为文字修正重新跑全部渲染；独立核对新旧GLB/图片hash、变更语义和subject绑定即可。此前视觉结论仍指向原始受审hash，不可静默修改或冒充已复核新brief。

## 最小剩余门禁清单

最终接受前只有以下工作组需要闭合，勿重复为已通过叶型启动制作：

1. **四项文档/指针修复并重绑证据**：S1–S4；独立复查实际文件/正确计算及新subject哈希。此项完成前specification不能pass。
2. **指定独立运行任务的GPU与scene**：同一精确GLB；真实renderer/device/是否software fallback、错误、当前画面/运动闪烁检查；1/16/32 independent-clone场景的真实比例、落地、材质、分辨率/DPR/阴影设置、draw工作量和warmup/采样帧时，比较16.7ms目标。不能用Node parse、Blender PNG、算术或仅instancing替代。
3. **最终独立记录组装和完整性验证**：以上证据齐后，由协调者合并technical、visual、factual、specification、runtime_parse、gpu、scene七stage；保留本次来源映射与警告审查，关闭有真实证据的blocker，运行candidate完整性和`--require-approved`。本补充报告只签factual/规格子项，不预填GPU/scene通过。必要时由独立审查者核对最终引用没有掉项。

发布阶段另有既定工作，不能混同QA门禁：取得发布授权；生成并检查24alpha正式预览与实际站点显示profile；集成到最新main时核对相同GLB/source身份、元数据/许可/归属/概念标签；运行集成检查后才发布。上述发布物不属于当前GPU/scene任务自动交付，也尚未完成。本次没有发布或main修改。
