# r20 doc1：文档修复、新身份与证据复用独立复核

固定 commit：`062be906210f34f206748a313e288934a52a2c4f`。新目录 `candidate-r20-a-normal16-doc1`，新 revision **`structure-r20-a-normal16-doc1`**。

新subject：GLB `c3a215eda3ceb3e4ec95bdb31446e180fd9f9d1f7eaa24131459a0db6fa56b40`；blend `04c20d19354455e57bbc70a8cced6308d9020e02ff057996bfde7c585a7acbef`；brief `092af4c3259156cd4a8a357df6e0151a1ec08fdd53fd7a351d162a6ed7561031`；references `18062b9ea882d531834240554f764a8a0818b83efd5e6f8afde2bbb77326119a`。

**结论：S1–S4文档修复、此次小写身份及受限证据复用映射通过独立复核。没有模型变化或新的视觉返工要求。** 该结论只关闭文档/身份复核本身，不是七门禁最终通过，不代签仍在进行的orbit/zoom动态检查。

## 四项修复

| 原问题 | 新记录实际检查 | 结论 |
|---|---|---|
| S1 metadata预览指向不存在文件 | 新metadata指向本新目录 `evidence/detail512/hero035.png`，文件存在且hash为`c3de24dabcee7e3486c491b8fab23f935c97bab6a0649f6110521406f814398d`。preview_profile明确是CPU诊断、非透明、非24alpha发布预览 | pass；没有伪称CPU图就是正式站点预览 |
| S2等价报告相对路径失效 | metadata与qa.json均改为 `geometry-equivalence.report.json`，相对各自目录解析可用 | pass |
| S3上限增幅文字错误 | brief区分actual19,052相对r12 18,706为+1.8497%，ceiling19,500为+4.2446%；几何上限和实际计数均未变化 | pass；不是为候选放宽预算 |
| S4两条次级羽轴描述遗留 | references.study_scope明确当前A为单羽轴、12对窄叶片加短终端，新增historical_comparison_note把双羽轴归于旧r17 B | pass；所引植物来源、概念分类与事实义务未删改 |

因此此前specification审查中的这四项fail可以关闭。冻结brief的GPU/scene及最终接受条件仍照常保留，不能把这里的文档通过扩展成所有规格已满足。

## 不变内容与历史保留

独立读取旧freeze，并逐文件与Git对象 `265b47eed899307228d609355cc46c6d6992f61d:candidate-r20/...` 比较：原目录118文件全部恢复原字节。旧模型、brief、references、原报告等没有在原位置静默覆写。旧QA目录也未改写。

将新目录同旧freeze的118个路径逐一比对：**104个相同、14个文档/绑定报告有变化、0文件缺失**。14个变化是README、brief、两个candidate-validation报告、candidate、三个当前render-manifest、gpu-scene-handoff、metadata、qa、references、runtime-parse.summary及technical.report。GLB、blend、build/config、木质输入、raw技术/重建记录、全部当前53张图、探针/比较图、render-config等均保持相同。

`evidence-reuse.json`列出的84个protected文件也逐个验证相同。这个84是显式保护子集，不是全部相同文件数；root build-config即使未列入84，独立比较也确认与原件相同。

新freeze所列文件全部存在且hash匹配。六项required_deliverables指向新目录且hash匹配；metadata glb/blend改为新目录顶层路径，真实文件及SHA一致。

## 新身份与复用范围

新revision是单独小写文档修订，满足已核对发布路径的安全小写slug形式；没有把原 `structure-r20-A-normal16` ID原地lowercase。brief.documentary_revision、metadata.source_geometry_revision/commit、evidence-reuse.source_geometry_subject/new_subject，以及新subject wrapper保留了原始/中间/当前文档链路。

`candidate.supersedes`仍是null，但上述显式来源字段与独立证据映射已足以追溯该文档修订；本次不因一个可选字段额外发明阻塞。最终组装/发布记录必须保留这条来源链，不能仅留下小写名字而丢掉映射。

三份当前render-manifest换为新subject，同时附带documentary_evidence_reuse说明；原图字节、config和时间信息不变。technical.report与runtime-parse.summary的status改为unknown，明确source_report_status=pass及“复用旧执行、没有新执行、待独立复核”。所有七个candidate stage都保持unknown，approval pending。这没有把原生产者或原独立审查者冒充为已经审过新身份。

本独立复核接受以下有限复用：

- 同一GLB/blend与无变化的渲染/数值要求，允许继续使用已经独立验证的法线误差、validator、Node parser、现有source/export/build输出与byte相等证据。不同证据仍按各自“亲自运行/读取旧输出”的范围描述，不声称此次重跑Blender。
- 53张图片全部相同，且新brief除文档解释/路径/预算文字外没有改变A艺术目标、关键视觉义务或运行要求，因此原全角度A视觉结论可在明确复用说明后沿用，不要求重渲染。
- references只有纠正当前A与历史B范围的文字变化，没有新增物种或时代主张，因此此前“通用风格化针叶树概念”factual/honest-concept判定可在新subject下沿用；仍不批准具体物种/年代/地点/化石尺寸复原。
- `evidence-reuse.runtime_source_records`固定引用运行commit `c92f41539448758817635d0e8b5a4701e12fdfe2` 的gpu/scene报告。独立以Git show读取该提交中的原报告，hash分别匹配`7c780440b3942291710cf1436e57ff3a0a8880495b513ec4026df1e5d2547922`与`1b31b07e238157fef7bbfcb913b2876e2a43ef43d29b66c3edc12a7b965b4024`。旧subject/设备/软件性能失败保留，没有修改为新实测。GLB与运行要求不变，允许在原范围复用。

**运行范围不会因doc1而扩大。** Metal的已测固定场景范围通过；SwiftShader的软件预算失败仍存在，严格阈值下单棵也略超；原运动范围仍仅42°–44.2°离散小步，本次不代签连续运动/缩放。runtime README的SwiftShader有效query数说明问题不属于S1–S4，也没有因此自动修正；最终记录须如实引用原始有效样本数（16/32棵各10，而非60）。

## 完整性检查与剩余事项

独立运行：

`python3 scripts/validate_candidate.py candidate-r20-a-normal16-doc1/candidate.json --root experiments/structural-refinement-2026-10-17/conifer-tree --json`

结果 **valid=true / approved_for_brief=false / errors=[]**。未执行最终组装、未将stage改为pass。完整validator输出保存在本目录。该记录完整性结果不替代实际独立判定。

最小剩余工作：

1. 收到并独立查看动态orbit/zoom新证据，按实际输入GLB、设备与时间序列关闭或保留动态unknown；不需要因doc1重跑已有效的全部性能样本。
2. 将本次文档/身份复核、原视觉/事实/技术范围、原运行profile与新动态结果以精确subject映射组装七stage最终记录；保留所有限制和SwiftShader失败，重新运行`--require-approved`。新candidate中的两个maker blocker由协调者按真实完成情况关闭。
3. 最终发布前，将选定renderer的24alpha预览、poster和发布metadata统一绑定小写doc1身份，保留其来源模型hash和原预览记录的继承关系；不能把原uppercase preview manifest当作已经写好了新发布路由。模型/图像字节不变的文档性重绑可复核复用，无需凭空渲染新图。

本次只新增独立QA记录，没有更改旧QA、候选、运行分支、main或发布文件；不提前给予总通过。
