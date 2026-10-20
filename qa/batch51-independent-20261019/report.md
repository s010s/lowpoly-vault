# Batch 51 独立 QA 报告

**结论范围：独立阶段检查，不是正式候选批准。** 核对对象锁定在候选 handoff `6b5bc2793572361242544f7a19afd6bbd71243ab`，资产字节来自材料 commit `ee4e37b3c1cc49ab5e41c807c6ca8e1a155bbc6b`。候选分支为 `candidate/small-life-batch51-concept-20261019`；本报告单独保存在 `qa/batch51-independent-20261019`。

四件模型的标准视图、形体与事实范围通过；GLB 格式、Blender 重开一致性、预算、Khronos 验证和独立软件 WebGL 重放通过。Calcite 与 lapilli 的**名义尺寸字段互相矛盾**，因此规格未通过。所有四件当前 `--require-approved` 都失败；`--require-complete` 也都因精确 ImageGen 生成时间未知而失败。没有改候选、冻结、模型、验证器或生产数据。

## 逐件裁决

| 资产 / 修订 | 视觉 | 事实范围 | 规格 | 格式与预算 | 当前正式批准 |
|---|---|---|---|---|---|
| `dicranurus` r001 | 通过 | 通过 | 通过 | 通过 | 未批准 |
| `calcite-raft-deposit` r002 | 通过 | 通过 | **未通过：0.42 m brief 与 0.32 m 构造计划冲突** | 通过 | 未批准 |
| `accretionary-lapilli-bed` r002 | 通过 | 通过 | **未通过：0.60 m brief 与 0.28 m 构造计划冲突** | 通过 | 未批准 |
| `conichnus-conical-burrow` r001 | 通过 | 通过 | 通过 | 通过 | 未批准 |

视觉判断针对 handoff 锁定的 `candidate-proof` 八视图，不是旧 `proof/` 图。四件都检查了 hero、reversehero、front、side、rear、top、clay、silhouette。概念图、最终视图、模型和运行时截图的完整哈希索引在 [verified-inputs.json](evidence/verified-inputs.json)；机读裁决在 [results.json](evidence/results.json)。

| 资产 | 最终 GLB SHA-256 | 原始概念图 SHA-256 | 导出尺寸 XYZ（m） | 三角面 / bytes / 材质 / primitives |
|---|---|---|---|---|
| Dicranurus | `ffe61e0340399eb1bd41cb198ba5abc20edae439db44e3c21d4cf6d9e032bd65` | `a8c8eaf0df9efe39148dc92ac980a5f2d64fd34c529cf4e94166be83f3055932` | 0.05222 × 0.03639 × 0.06083 | 9,016 / 481,424 / 3 / 8 |
| Calcite rafts | `fdbad4c14684a3af5940199f422ee3c605d00bf997649738a85fe0082eb4fd22` | `07140bd478b0f36c4e97281d70559f392010bbb6e9f50830da31e07e41368cfa` | 0.33594 × 0.02607 × 0.25429 | 1,400 / 79,228 / 4 / 4 |
| Accretionary lapilli | `61b2ae162930e8b8221e0f3cad27dd3e044a99ba6883db299dbe041231711cf3` | `0a71d024dd5550445c94a54204b3cdcce3e8ef8d9ce2d541ff7c4c325b2ad5e7` | 0.28450 × 0.11560 × 0.20509 | 5,496 / 291,392 / 5 / 7 |
| Conichnus | `34948b0738264195544dd24ff377a1b0f3b92a93a1e34ab07d66647235388042` | `7c2cb8dd3ba7578ffe702e2818b2cc33abb6ec6a297b31c08895dd9654a80585` | 0.24000 × 0.14070 × 0.20000 | 1,790 / 86,088 / 3 / 3 |

静态 profile 硬上限是 14,000 三角面、1,000,000 GLB bytes、6 材质、30 primitives；四件都在限制内，且均未使用图像或纹理。Calcite 和 Conichnus 小于通常约 100–500 KB 的制作区间，但这不是最低门槛；模型都以几何形体为主，没有为凑体积增加贴图。

### 真实概念调用与查看顺序

四件的 `generation-record.json` 都保留 ImageGen 工具名、实际 prompt、输出接收记录和概念图哈希。记录的接收时间均为 **2026-10-19 22:45:37 UTC**；同图哈希的 `view_image` 检查记录约在 **22:47:36 UTC**；首次建模分别在 **22:49:00、22:52:23、22:55:56、22:58:32 UTC**。保存的 prompt、原图、检视记录与建模收据一致，因此足以支持“生成结果被接收并查看后才开始建模”的顺序。

工具没有单独披露生成瞬间。`concept_generated_at` 保持 `null`，没有用接收时间或文件时间代替。四件的 `validate_concept_evidence.py --require-complete` 均返回 **1**，唯一 blocker 是：`concept_generated_at: unknown; do not reconstruct times from file mtimes`。这份顺序证据不能补出精确生成时间，也不能把概念证据完整性门禁变成通过。

### 形体、尺寸与元数据

- **Dicranurus：** 两支有空气间隙的后弯环角、紧凑头盾、叠甲与长侧刺在多个视图都清晰可辨。brief 的名义角体跨度为 0.065 m，实测对应跨度约 0.06083 m，低约 6.4%；构造计划也为 0.065 m，brief 没有规定更严容差，不要求重做。
- **Calcite raft deposit：** 断裂多边薄片覆盖在可见的旧池底基质上，前/侧低视图能确认薄片厚度；无水体模拟或具体洞址误称。候选 brief 写 0.42 m，concept prompt 和冻结构造计划写 0.32 m，最终长跨度为 0.33594 m。应先澄清尺寸规格，不能把这当成美术缺陷。
- **Accretionary lapilli bed：** 连续灰层基质、嵌入的圆团粒和三个显露的同心剖面符合已冻结的教学块构造；团粒层纹明确是放大的讲解特征，不是实测微观尺度。候选 brief 写 0.60 m，概念 prompt 与冻结计划写 0.28 m，最终宽度为 0.28450 m。这是 brief 与构造输入不一致，不是当前形体需要反复润色。
- **Conichnus：** 标准俯视与斜视显示块体上的圆形负腔；灰模剖面显示腔壁往下明显收窄，末端是小圆钝底，不是浅 slab 轮廓或正锥体。灰色 section 是仅用于解释的副本切面，交付 GLB 未被切开或改变。对精确 GLB 独立重跑了 Blender 向下射线：六个 X 采样点 0、0.01、0.02、0.03、0.04、0.05 m 的击中高度依次约为 0.0275、0.0470、0.0770、0.1079、0.1350、0.1400 m；腔中心深 0.11250 m，底下仍有 0.02750 m 基质。负腔与向底部收窄均得到直接验证。

最小的规格修复是**新建版本化的 brief/derived-freeze**，不覆盖原始冻结：若保持当前两个模型，则把 Calcite 名义尺寸定为 0.32 m、lapilli 定为 0.28 m，并重跑绑定新 brief 的规格/候选校验；当前 GLB 无需因尺寸问题重建。若原 brief 的 0.42/0.60 m 才是权威目标，则按其重缩模型并重生受影响的视图和技术证据。

四件 `metadata.json` 都有中英文名称、representation/claim scope、facet、来源与素材许可字段；模型都标为 stylized/inspired teaching art，引用材料为 consulted-only，没有携入第三方图像或网格。Dicranurus、calcite、Conichnus 的实际形态来源可打开并与窄化后的声明相符。Lapilli 的 USGS 摘要支持球状火山灰团粒与围绕核的细灰累积；它不支持该教学块的实测尺寸，因此模型没有作尺寸或具体喷发地点声称。

## Blender、GLB 与运行时

独立 Blender 4.3.2 重开每件 `.blend`（脚本自动执行关闭），再把导出集合的三角面数和轴转换后的边界与 handoff 指定 GLB 对比：四件都匹配，边界误差为 0 m，报告无错误/警告，源文件未保存。每件另用官方 Khronos `gltf-validator 2.0.0-dev.3.10` 对精确 GLB 独立检查，均为 **0 errors / 0 warnings**。详细原始结果见 [Blender source/export reports](evidence/replay/blender-source-export/) 和 [Khronos reports](evidence/replay/khronos/)；候选完整性检查均 `valid=true`，但该状态不等于审批。

用原批次 runtime 脚本独立重跑每个精确 GLB：Chromium 154.0.8037.57、Three.js 180、ANGLE SwiftShader。解析三角面、材质、边界与 handoff runtime report 一致；无浏览器或 WebGL 错误；四件各自的 7 张 runtime PNG（含 near 与九实例场景）都与候选图逐像素哈希一致。此为**软件 WebGL 功能通过**。它不代表实体 GPU 性能验证。

批次任务与选定 brief 只要求带真实实例/工作量记录的 neutral multiple-copy teaching-prop benchmark，没有规定 128/8/32 数量。现有并独立重放的是每件精确 GLB 的 3×3 九副本场景，符合这个单资产基准要求；真实父场景/博物馆集成没有验证。硬件 GPU 未验证。

## 来源核实

- [AMNH《Trilobite Hall of Fame》](https://www.amnh.org/content/download/432038/6245021/file/trilobites-hall-of-fame.pdf) p.31 描述 Dicranurus 的 ram-horn 形态及标本背景；只支持基础弯角识别，不据此声称严格种级复原。
- [NPS Wind Cave：Calcite Rafts](https://www.nps.gov/wica/learn/nature/cave-formations-speleothems.htm) 说明薄方解石片在水面形成并漂浮，沉底后也可作为旧淹水通道的证据；足以支撑本件薄片沉积形态。
- [USGS Bohor & Triplehorn (1984)](https://www.usgs.gov/publications/accretionary-lapilli-altered-tuffs-associated-coal-beds) 支持火山灰团粒近球形、细灰围绕核累积的基本形态。
- [Kansas Geological Survey：Conichnus](https://www.kgs.ku.edu/Publications/Bulletins/245/04_ichno.html) 将属级形态描述为圆锥至近柱形、圆底、无装饰；`Conichnus conicus` 的具体描述指出垂直圆截面潜穴和可能的平小底盘。本次模型按教学解释塑为负腔，并避免声称特定造迹生物。
- **单独标记、非阻塞：** NPS Hawaiʻi 的 Keonehelelei 火山地质 PDF (`EN-VO3B`) 当前访问失败（internal error / proxy 403），仍只保留 inherited search result，未称其已核实。lapilli 的基础事实由可访问的 USGS 原始来源支持，故该 PDF 不阻塞本轮其他形体与格式检查。

## 正式门禁当前缺项

四件的 `validate_candidate.py --require-approved` 均返回 **1**，`approved_for_brief=false`；候选记录仍是 `approval=pending`，并有 `independent-qa-pending` 与 `imagegen-exact-generation-time-unavailable` 两个 open blocker。其余候选侧独立 review/functional stage 记录仍显示 unknown，包括 visual、factual、specification、GPU 和 scene。本报告是在 QA 分支中独立保存的结论，不修改这些候选状态。

当前门禁需要：

1. 一个真实且可审计的 provider generation timestamp，或上游明文支持该时间。现在没有，必须继续保持 unknown；不能用本轮截图或文件时间填补。
2. 在版本化 brief 中裁决 Calcite 与 lapilli 的名义尺寸矛盾，再绑定对应的规格判定。
3. 候选侧按确切 GLB/brief hash 记录正式 stage review，并重新运行 `--require-approved`。本独立有限 QA 不代替这个候选侧记录。
4. 如需声明硬件性能或真实父场景验收，须在可用硬件及目标父场景中另行验证；当前不能由 SwiftShader 九副本预览推导。

目前没有需要重做的视觉缺陷，也不建议继续做无目的美术微调。仅 Calcite/lapilli 的尺寸规格决策需要版本化修正；精确 ImageGen 时间与正式审批仍受当前证据门禁阻塞。

## 可重放证据

- [验证 pinned source/candidate 与所有交接、冻结、概念、候选八视图及 runtime 哈希](evidence/verify_inputs.py)
- [可独立重跑的 Conichnus GLB 射线检查](evidence/replay/probe_negative_cavity.py)
- [候选 integrity / `--require-approved` / `--require-complete` 输出与退出码](evidence/replay/candidate-checks/)
- [Blender 重开 source/export 原始报告](evidence/replay/blender-source-export/)
- [官方 Khronos 原始报告](evidence/replay/khronos/)
- [独立 runtime 报告及逐图哈希比较](evidence/replay/runtime/runtime-replay-summary.json)
- [Conichnus 独立射线输出、maker 灰模诊断清单和射线记录](evidence/replay/conichnus/)

`verify_inputs.py` 运行结果通过，并确认候选交接 commit 之后没有改动模型或 production 树。此分支只保存独立 QA 与可重放证据；未修改 main、生产 catalog、模型、PR20/PR28，未创建或合并 PR。
