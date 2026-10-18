# Batch 13 独立 QA

**结果：四项均 PASS；无必须返工项。** 判定针对静态风格化、基本形态可辨、低模连接自然的教学道具要求；不代表严格古生物复原认证。

- 审核模型：GPT-6 Luna xhigh；日期：2026-10-18 UTC
- 审核基点：c173fe4666939005f1617e7be46cdbba6b4cef89
- 批次 handoff：production/continuous-small-life-round05-20261018/work/batch-13/final-handoff.jsonl，SHA-256 083c194d9177be95b08879bff21ce6deed6e548b096bc7b152e8283d65ec376f
- 四项 source commit、分支、GLB / Blend SHA 均见下表；每条结论只适用于对应精确资产哈希。
- 汇总图：[固定八视角联系表](all-fixed-views-contact-sheet.png)、[精确 GLB runtime 联系表](all-runtime-contact-sheet.png)。完整单图仍在各 candidate source commit 内。
- 结构化证据：[review-evidence.json](review-evidence.json)；新跑的 GLB、Blend 对照与 Blender reimport 报告见本目录 fresh-* 子目录。

| 项目 | candidate 分支 @ 精确 source commit | GLB（bytes / triangles / SHA-256） | Blend SHA-256 |
|---|---|---|---|
| acrocyathus | candidate/batch13-acrocyathus-20261018 @ 284891f1444356f74e2363c27f8bd66e5f6bc1e1 | 137,920 / 4,340 / 85c65487af8ddb08595248c5dfda912ddfdc3a1d9e22116177937d848b08400c | c7aaed77606f061bd626b99ace2bd60657327dfb371f1f47390635c3edd198c2 |
| sawdonia | candidate/batch13-sawdonia-20261018 @ 61cace55d96184ec66a7f0cb7306d667f7d7492e | 231,164 / 12,456 / 6d8ef1cccefd269ff7f1715828c949e8a466a18ee04ebfc2249d52ad55ee212c | e73eb1d1fefd2fe032e16751bcb5191e515d55ec89f2d6bb1ccdcbdf2013b55d |
| leanchoilia | candidate/batch13-leanchoilia-20261018 @ 810977ed98e8350948b236755a90e4509f4c652e | 137,092 / 6,980 / e328011f4d9df45eeaa4b1abc94111c6145b2dc9b49b9396bde92e02940ada86 | e4aab6687efa0b9b819baa0d5c881bfe9b2ea67db589c99849f5e037963cd15e |
| septarian-concretion | candidate/batch13-septarian-concretion-20261018 @ e82773c763817a9b9ccd7eacbfa0a266d7e7c30b | 343,052 / 7,548 / 399ce37d67c905c0ce0f08802c1206307570d39cead72aa68defa9ebaf737c6d | cc9e73a01e8800699adc30b8c355007c757ec8ceab09e2885a3462d0add8f573 |

## 独立核验摘要

我把 handoff 当作待核验的索引，而不是 PASS 依据。批次 scope.json 只列这四个 asset ID；逐个以 planning/base 提交 0bd62cda92814af5ac781e1a706bba6310cecc35 对比 candidate tip，四项所有改动路径都在各自 asset 工作目录与对应 work 目录内。路径数量和 SHA 与 scope 完全一致（前三项各 105 项，Septarian 117 项）；shared_changes=false、制作方未合并。

我复算了每项 checksums.sha256 的 58/58 项及 candidate artifact pins。四份 references profile 均与冻结 references 字节一致，引用全标为 consulted-only、未并入来源媒体；我没有推测或补写许可。Handoff 也明确最终 evidence 绑定精确 source tip；Septarian 制作过程有一次短时 preview/build 调度重叠，随后暂停编排、完成最终修正后按序生成证据。此处不作“始终单 worker”的声明；没有看到最终证据之后还有模型改动。

### Blend / GLB 与运行检查

我用 Blender 4.3.2 独立打开每个 Blend，读取 EXPORT 中 evaluated meshes；将顶点从 Blender Z-up (x,y,z) 转为 glTF Y-up (x,z,-y)，再与对应 GLB 的实际位置流对照。四项按 1e-6 m 坐标精度均得到相同唯一顶点集合、完全相同的三角数和包围盒；GLB 没有退化三角形。唯一位置数依次为 Acrocyathus 2,482、Sawdonia 6,354、Leanchoilia 3,626、Septarian 3,638。对应完整结果见 [fresh Blend-to-GLB reports](fresh-blend-glb-compare/)；我另以项目 qa_glb.py 按各自 brief 上限复核 GLB，无错误或警告。Khronos validator 2.0.0-dev.3.10 的现有报告都与精确 GLB SHA 相符，均为 0 errors / 0 warnings。

四个 GLB 还分别由 Blender glTF importer 重新打开；三角数一致、包围盒最大误差 0 m、无导入错误。导入检查会报告平滑面，以及少数材质/硬边分割后的 boundary-edge 提示；原 Blend 各源 mesh 的独立测量是 0 boundary / 0 non-manifold，位置集和渲染图均无缺面或裂缝。这些提示被保留并审阅，没有更改阈值或从报告中抹去。

实际 Chromium 154 / Three.js r180 / ANGLE SwiftShader 图像由 GLTFLoader 直接载入对应 GLB 生成。每项的 7 个视图——hero、reversehero、front、side、top、near、scene-9-copies——均 gl_error=0、无运行错误。它只证明软件 WebGL 功能，不代表实体 GPU 或目标设备性能。九件场景采用 runtime 脚本的 1.38 × 4.7 正交视锥；最长标称轴在 512px 画布约为 512/(1.38×4.7)=79px，处于 brief 的约 80px 典型下沿；九件轮廓仍分开可读。单件近看投影约 300–350px，低于 480px 近看上限。细小刺/旗丝只在近看更清楚，但不影响基本轮廓。

### Profile 与历史 checker

临时 sidecar 由 candidate_profile.py 按各候选实际字节生成，并在 candidate root 内运行 validate_candidate.py --profile static-stylized-v1：四份均为 profile contract pass、record valid。--require-approved 仍按设计返回失败，因为 candidate 自身的七个独立阶段和 approval 仍是 unknown/pending；我只提交独立审查报告，没有改写 candidate record。默认 legacy-v1 checker 四项仍失败于 consulted-only reference 缺历史 license 字段。此项属于已记录的旧合同差异，不是造型问题；不凭空填许可。

## 逐项判定

### acrocyathus — PASS

- **形体观察：** 八视图与 GLB 运行图呈现紧簇的长多边珊瑚杯、杯口和内部放射隔壁；杯间节奏可辨，正、侧、背与反向视图没有明显破面、断接或穿插。九件场景里单簇仍可分辨，近看可读内部隔壁。
- **必须问题：** 无。
- **非阻塞建议：** 无需改模。80px 场景里的细隔壁比单件/近看低调，是预期的尺度收缩。
- **来源范围：** Digital Atlas 页面收录了 Acrocyathus floriformis 的殖民型 rugose coral 化石，可支持“簇生珊瑚”这一基本启发范围；本次 PASS 不延伸为严格物种鉴定或微结构认证。[Digital Atlas of Ancient Life](https://www.digitalatlasofancientlife.org/vc/cnidaria/anthozoa/rugosa/)
- 证据：[固定八视图](../../../../../assets/candidates/continuous-small-life-round05-20261018/batch-13/acrocyathus/r001/qa-contact-sheet.png)、[GLB runtime 图](../../../../../assets/candidates/continuous-small-life-round05-20261018/batch-13/acrocyathus/r001/runtime-contact-sheet.png)、[near](../../../../../assets/candidates/continuous-small-life-round05-20261018/batch-13/acrocyathus/r001/runtime/near.png)。

### sawdonia — PASS

- **形体观察：** 直立分枝轴、弯曲/回卷的枝端和沿轴稀疏分布的小刺在固定视图与 GLB runtime 中保持连贯。正侧轮廓细长但不散架；80px 九件场景依然读得出分枝植株形。近看能看到小刺，未见明显枝轴断口、浮刺或穿插。
- **必须问题：** 无。
- **非阻塞建议：** 若展示重点是小刺，选更接近 240px 的呈现尺寸；无需为了 80px 缩图把枝条加粗或重做拓扑。
- **来源范围：** University of Alberta 的古植物实验材料列出 Sawdonia，并明确标记 Sawdonia 的显著刺，支持该模型的基本分枝/有刺方向；本次不认证精确物种复原。[Paleobotany Lab 03](https://grad.biology.ualberta.ca/paleobotany/?page_id=28)
- 证据：[固定八视图](../../../../../assets/candidates/continuous-small-life-round05-20261018/batch-13/sawdonia/r001/qa-contact-sheet.png)、[GLB runtime 图](../../../../../assets/candidates/continuous-small-life-round05-20261018/batch-13/sawdonia/r001/runtime-contact-sheet.png)、[near](../../../../../assets/candidates/continuous-small-life-round05-20261018/batch-13/sawdonia/r001/runtime/near.png)。

### leanchoilia — PASS

- **形体观察：** 单一头盾、分节躯干、两侧附肢、尾端和前方多指大附肢在 hero、top、side 与反向图中都能区分；三指/鞭丝读法在 80px 场景较细，near 图中清楚。连接处没有显眼脱节、穿插或比例断层。
- **必须问题：** 无。
- **非阻塞建议：** 无需改模。远景缩小后旗丝会弱化；目标尺寸仍能辨出节段躯干和前方附肢。
- **来源范围：** ROM 的 Leanchoilia superlata 页面描述三枚长爪状前附肢与鞭状 flagella，也标出躯干分区和分节，足以支持基本形态对照；不把它扩大成精确软组织重建。[Royal Ontario Museum — Leanchoilia superlata](https://burgess-shale.rom.on.ca/fossils/leanchoilia-superlata/)
- 证据：[固定八视图](../../../../../assets/candidates/continuous-small-life-round05-20261018/batch-13/leanchoilia/r001/qa-contact-sheet.png)、[GLB runtime 图](../../../../../assets/candidates/continuous-small-life-round05-20261018/batch-13/leanchoilia/r001/runtime-contact-sheet.png)、[near](../../../../../assets/candidates/continuous-small-life-round05-20261018/batch-13/leanchoilia/r001/runtime/near.png)。

### septarian-concretion — PASS

- **形体观察：** 圆润结核外形与向上展示的切面区分明确；切面中的径向和同心矿物填充网络比表面裂泥/Voronoi 图案更像教学剖面。多角度 GLB 画面、top view 和 [重新导入 GLB 的 wireframe](septarian-glb-wireframe.png) 均未显示缺面、裂缝或明显 z-fighting。
- **历史迭代复核：** prototype-01-regular-network 被保留并注明纹路太规则；failed-attempt-02 的实际 source QA 曾发现 host-rock 12 个、mineral-cement 1 个退化三角，失败记录和日志保留；prototype-03-coplanar-junctions 因 coplanar junction 触发修正；最终 generator SHA 为 6214aff2cf59ecc5d235c8ef6e76c1a50d25d98a57b1afba353646f49fd01e1c，最终模型 0 个退化面，两次重建与最终 GLB 字节一致。最终迭代索引只把 final GLB 作为验收目标。
- **附加拓扑观察（非门槛）：** 我对 GLB position 按 1e-7 m 合并后做了不设失败阈值的 edge-incidence 诊断：boundary edge 0、退化三角 0，但有 257 条边被超过两张三角形引用，主要位于 host-rock / mineral-cement 接口和 cement 网络内部。源 mesh 分件本身 closed / manifold；当前静态 GLB 的实际视图中这些位置没有可见洞、断缝或闪烁，所以不构成当前使用的必须返工项。若未来要做变形、碰撞或实体布尔操作，再单独清理统一拓扑。
- **必须问题：** 无。
- **非阻塞建议：** 保持切面朝向展示相机，径向/同心网络是识别线索；当前模型无需改动。
- **来源范围：** 冻结来源表中的 USGS PDF 本次未能打开；为核对非常宽泛的 septarian 形态，我另开了 PRI 的文本页面：它描述了向内放大的放射裂隙、与同心裂隙相交及方解石/硅质胶结。这只支持基本教学概念，不是某一地点/标本复原。[Paleontological Research Institution — Concretions](https://www.priweb.org/blog-post/concretions)
- 证据：[固定八视图](../../../../../assets/candidates/continuous-small-life-round05-20261018/batch-13/septarian-concretion/r001/qa-contact-sheet.png)、[GLB runtime 图](../../../../../assets/candidates/continuous-small-life-round05-20261018/batch-13/septarian-concretion/r001/runtime-contact-sheet.png)、[near](../../../../../assets/candidates/continuous-small-life-round05-20261018/batch-13/septarian-concretion/r001/runtime/near.png)、[wireframe](septarian-glb-wireframe.png)。

## 实际执行命令

以下命令对四个 ID 各执行一次；candidate_profile.py 生成的 sidecar 临时放在对应 root 内供路径合同检查，检查后删除，没有改写 candidate、Blend 或 GLB。

    # 先固定 handoff worktree；四个源快照分别从 scope.json 的精确 tip 创建
    git fetch origin c173fe4666939005f1617e7be46cdbba6b4cef89
    git worktree add -b qa/s010s/small-life-batch13-20261018 /tmp/batch13-qa c173fe4666939005f1617e7be46cdbba6b4cef89
    git worktree add --detach /tmp/batch13-source-acrocyathus 284891f1444356f74e2363c27f8bd66e5f6bc1e1
    git worktree add --detach /tmp/batch13-source-sawdonia 61cace55d96184ec66a7f0cb7306d667f7d7492e
    git worktree add --detach /tmp/batch13-source-leanchoilia 810977ed98e8350948b236755a90e4509f4c652e
    git worktree add --detach /tmp/batch13-source-septarian-concretion e82773c763817a9b9ccd7eacbfa0a266d7e7c30b

    # 在 /tmp/batch13-qa 仓库根目录，以每个 ID 执行
    id=acrocyathus  # 依次替换为 sawdonia、leanchoilia、septarian-concretion
    root=/tmp/batch13-source-$id
    candidate=assets/candidates/continuous-small-life-round05-20261018/batch-13/$id/r001/candidate.json
    contract=$root/assets/candidates/continuous-small-life-round05-20261018/batch-13/$id/r001/.independent-review-profile-contract.json
    python scripts/candidate_profile.py "$candidate" --root "$root" > "$contract"
    python scripts/validate_candidate.py "$candidate" --root "$root" --profile static-stylized-v1 --profile-contract "$contract" --json
    python scripts/validate_candidate.py "$candidate" --root "$root" --profile static-stylized-v1 --profile-contract "$contract" --require-approved --json
    python scripts/validate_candidate.py "$candidate" --root "$root" --json
    rm "$contract"

    # 每个 GLB 使用其 brief 中的 14,000 / 6 / 30 几何上限；无纹理
    python scripts/qa_glb.py --report /tmp/b13-checks/$id/glb-audit.json --max-triangles 14000 --max-materials 6 --max-primitives 30 /tmp/batch13-source-$id/assets/candidates/continuous-small-life-round05-20261018/batch-13/$id/r001/$id.glb
    blender -b --factory-startup --threads 2 --python-exit-code 1 --python scripts/check_glb_roundtrip.py -- /tmp/batch13-source-$id/assets/candidates/continuous-small-life-round05-20261018/batch-13/$id/r001/$id.glb --output-dir /tmp/b13-checks/$id/roundtrip --no-render
    blender -b --factory-startup --threads 2 --python-exit-code 1 --python /tmp/b13-checks/independent_blend_glb_compare.py -- /tmp/batch13-source-$id/assets/candidates/continuous-small-life-round05-20261018/batch-13/$id/r001/$id.blend /tmp/batch13-source-$id/assets/candidates/continuous-small-life-round05-20261018/batch-13/$id/r001/$id.glb /tmp/b13-checks/$id/independent-blend-glb-compare.json

Septarian 最终 GLB 另渲染一次 wireframe 供查看：

    blender -b --factory-startup --threads 2 --python-exit-code 1 --python scripts/check_glb_roundtrip.py -- /tmp/batch13-source-septarian-concretion/assets/candidates/continuous-small-life-round05-20261018/batch-13/septarian-concretion/r001/septarian-concretion.glb --output-dir /tmp/b13-checks/septarian-concretion/roundtrip-rendered
