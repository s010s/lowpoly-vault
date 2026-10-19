# 独立 QA 审查：Small Marine Quartet

**结论范围：**四件所选 GLB/Blend 的概念、风格、参考依据、尺寸/结构/色彩、重新导入、文件格式，以及软件 WebGL 场景的独立复核。它不是正式候选批准，也不是发布批准。

| 项目 | 结果 |
|---|---|
| 固定源分支 | `candidate/small-marine-quartet-concept-20261019` |
| 固定源提交 | `7c3cc658c1d10fa595e3ef7d27c6f0b17a842dd1` |
| 审查者 | GPT6LunaXHigh（独立 QA） |
| 审查分支 | `qa/s010s-small-marine-quartet-20261019` |
| 选中模型/Blend 修改 | 无；审查脚本和证据仅写入本 QA 目录 |
| 独立限定范围 | 四件视觉/事实/规格审查、Blender 重导入与 Blend/GLB 一致性、Khronos glTF 格式检查、SwiftShader 软件 WebGL 场景 |
| 正式候选验收 | **阻断**：四个选中目录均没有 `candidate.json`，正式候选检查无法执行；四个 revision-local `metadata.json` 也缺少下文列出的字段 |
| 目标 GPU/设备与已部署填充场景 | 未验证 |

## 每件结论

“独立限定审查”仅表示下面列明的审查通过；“正式候选门禁”对每件均为阻断。没有观察到需要修复模型的确切缺陷。

| ID / 版本 | 独立限定审查 | 正式候选门禁 | GLB 尺寸 X×Y×Z (mm) | GLB 面数（三角形）/位置顶点/网格对象 | GLB 字节 / 材质 / 纹理 | Blend 作者顶点 / 面数 | GLB SHA-256 |
|---|---|---|---:|---:|---:|---:|---|
| Emeraldella r002 | **通过** | **阻断** | 54.570 × 21.623 × 140.179 | 2,996 / 6,038 / 72 | 202,492 / 4 / 0 | 1,642 / 1,916 | `7c64de69f55bca9a4bb6701dce818b5fbdf4656cef18b87785d0adfb8a1d8b7c` |
| Burgessia r002 | **通过** | **阻断** | 20.955 × 5.789 × 44.137 | 1,862 / 3,695 / 42 | 124,420 / 4 / 0 | 1,015 / 968 | `e75fdf29738520f3d8a3ad3b5d50c582fabd558c086e0a817bbc7a592a315669` |
| Tuzoia r003 | **通过** | **阻断** | 69.401 × 66.010 × 153.276 | 2,176 / 4,422 / 53 | 152,604 / 6 / 0 | 1,194 / 1,167 | `9f5f09b624b2d99da6c989b0e332903904452ffa9a7f68b2e731a31fb90dfe7c` |
| Sanctacaris r002 | **通过** | **阻断** | 52.000 × 24.020 × 100.456 | 3,604 / 7,137 / 98 | 250,108 / 6 / 0 | 1,998 / 2,172 | `d51b77469b954e9adc97c48db4dcae78adc622297ab4c4ffbb124de521805a96` |

上表面数是对 GLB 的三角形数；“位置顶点”和 Blender 作者网格顶点是不同指标，不应混为一个面数。所有维度为 GLB XYZ 公尺值换算为毫米。每个模型均使用 glTF `+Y` 向上、`+Z` 向前；0 张贴图。所列网格对象数来自独立 GLB/重新导入审计。

对应 Blend SHA-256：Emeraldella `5edeb335b564c68dddb3e833e90ceb15f8b7469d3360f2a37d3f1f66e828ac60`；Burgessia `e9782d5b49947afc0233fcc52e860a51621fb97630525edc6ffef35faa3bac42`；Tuzoia `4f8d4dc532ea26234bddb88f7900b9e795fabef24eb28ae3cc5f3b1faea1501c`；Sanctacaris `1e914e0936fe8ac5e80a3df77c6c144b559a74b79c424628d9e9c621dfa3f976`。

### 逐件视觉与概念判断

- **Emeraldella r002 — 通过。** 概念匹配与新渲染中的头盾、11 节躯干、两段圆柱形后部、长连续尾刺、成对触角和附肢关系清楚。没有凭空加眼睛。四材质低模配色为肢体 `#AC8E61`、棱脊 `#4F7B79`、甲壳 `#76A7A1`、腹面 `#DFD5B8`。128 px 轮廓仍清楚。
- **Burgessia r002 — 通过。** 单一低拱半圆甲壳、无眼外观、未分节的单根后刺和下方附肢关系符合冻结 brief；没有把尾刺画成分节尾。色彩为 `#BA966C`、`#B37E4C`、`#D9A067`、`#F0D2A5`。128 px 下主轮廓可辨，但附肢细节弱；这是小尺寸可读性限制，不构成要求返工的模型缺陷。它在共用真实公尺比例的 2×2 WebGL 场景中显得最小，因为模型本身只有约 44 mm 长；场景未把资产放大，单卡片取景未测试。
- **Tuzoia r003 — 通过。** 双瓣壳、背部铰合线、侧棱/边缘刺、眼与触角、附肢及尾扇可在多角度辨认；独立检查确认前部头部体块连接眼柄/触角根部。色彩为 `#28313D`、`#B89C74`、`#7E526D`、`#AC758A`、`#D39A9A`、`#E8C6AE`。128 px 轮廓和壳瓣仍易读。
- **Sanctacaris r002 — 通过。** 宽头盾及扫掠三角形侧翼、侧眼、六对前部附肢、11 个躯干板和宽尾扇能从 hero/front/right/top 与 clay 视图辨认。色彩为 `#233340`、`#C5AA7F`、`#506F8A`、`#7799AF`、`#A4BAC7`、`#E7D5B6`。128 px 下主体形状及尾扇清楚。

四件均是适合儿童友好场景的风格化低模道具；本判断不要求科研级复原，也没有为看不出收益的细节调整提出返工。独立审查中实际查看了概念原图、生产方 concept-match 帧及绑定精确 GLB 的新多角度图。生产方自检只作为来源/完整性证据；它不替代这里的独立视觉判断。

## 事实依据与适用边界

四项事实依据均为 Royal Ontario Museum 的 Burgess Shale 页面。审查将其用于核对所声明的宽泛外部形态，不把风格化道具当作精确化石标本或科研重建：

- [Emeraldella brocki — ROM](https://burgess-shale.rom.on.ca/fossils/emeraldella-brocki/)：支持无眼头盾、躯干与后部形态、尾刺、触角和双枝附肢等宽泛地标。
- [Burgessia bella — ROM](https://burgess-shale.rom.on.ca/fossils/burgessia-bella/)：支持半圆拱形甲壳、未分节后刺以及附肢的大体安排；无复眼证据与不绘眼的处理一致。
- [Tuzoia burgessensis — ROM](https://burgess-shale.rom.on.ca/fossils/tuzoia-burgessensis/)：支持双瓣壳、背部铰合、侧棱/刺、眼/触角和附肢等。ROM 对软体细节使用多个 Burgess Shale 物种资料；本件是属级启发的组合造型，不是某一标本的精确复原。
- [Sanctacaris uncata — ROM](https://burgess-shale.rom.on.ca/fossils/sanctacaris-uncata/)：支持宽头盾及三角侧翼、六对头部附肢、11 节躯干和宽桨形尾扇等。

触肢/刚毛/细分节、刺纹、颜色与比例中的艺术选择已在原 brief/reference 中声明。没有发现把 ROM 图片、模型、材质或代码并入候选的迹象；本审查不扩展或重新授予任何许可。模型由多个闭合部件在关节处重叠，不声称是融合实体、可打印或可活动模型。

## 独立技术检查

1. **固定输入和哈希：通过。** 审查前核对 branch/commit、生产 bundle hash、四个 Blend/GLB、brief、reference、生成器/配置、概念图、concept-match 帧、sidecar 和实际构建/事件记录。`frozen-input-audit.json` 记录所有来源路径、字节数、SHA-256 与哈希比对。最终核对发现输入模型文件的审查前/后哈希不变。
2. **Blend ↔ GLB 和干净重新导入：通过。** 独立 Blender 4.3.2 中分别执行源码导出比对、四件 GLB 干净重新导入，并逐件比较边界、网格/三角形计数、材质槽和 Principled 线性色彩。源/GLB 最大边界差低于 `4e-9 m`；重新导入与源边界差为 `0 m`；每件三角形计数一致；材质名称一致、线性 base-color 最大差为 `0`（容差 `1e-6`）。不同坐标系按 Blender 导入后的坐标变换对齐后比较。该检查不证明形态科学准确性或多个部件组成封闭实体。
3. **独立真实 GLB 图像：通过。** 仓库渲染器直接干净加载每件冻结 GLB，生成 11 个 512×512 视图：hero、reversehero、front、rear、left、right、top、bottom、clay、clayalt、wire（每件）。另外生成四个 128×128 原生视图 hero/front/right/top；接触页保留原像素，不放大帧。所有渲染 manifest 都绑定表中 GLB SHA。图像与日志位于 [`evidence/renders/`](./evidence/renders/) 和 [`evidence/renders-128/`](./evidence/renders-128/)；四件 512 px 接触页为 [Emeraldella](./evidence/renders/emeraldella-review-sheet.png)、[Burgessia](./evidence/renders/burgessia-review-sheet.png)、[Tuzoia](./evidence/renders/tuzoia-review-sheet.png)、[Sanctacaris](./evidence/renders/sanctacaris-review-sheet.png)。128 px 接触页为 [Emeraldella](./evidence/renders-128/emeraldella-review-sheet.png)、[Burgessia](./evidence/renders-128/burgessia-review-sheet.png)、[Tuzoia](./evidence/renders-128/tuzoia-review-sheet.png)、[Sanctacaris](./evidence/renders-128/sanctacaris-review-sheet.png)。
4. **Khronos GLB 校验：通过。** 使用仓库固定 wrapper 与 gltf-validator `2.0.0-dev.3.10` 对哈希相同的临时副本运行，避免写入冻结资产目录。四份报告均 0 errors / 0 warnings，未截断；原始报告和输入哈希在 [`evidence/khronos/`](./evidence/khronos/)。
5. **概念证据完整性：通过，但范围有限。** 冻结概念 sidecar 哈希检查和 `validate_concept_evidence.py --require-complete` 均通过。它们证明引用链/记录完整性，不是视觉事实判断或验收批准。
6. **WebGL 场景：软件路径通过。** Chromium 154.0.8037.57、Three.js 0.180.0、ANGLE SwiftShader software WebGL2 加载四个精确 GLB，保留作者米制比例、仅用平移排成 2×2 场景；6 个视角均绘制 10,638 个预期三角形、265 draw calls、无加载/资源错误且 `gl.getError() == 0`。截图及逐项 hash 在 [`evidence/webgl/`](./evidence/webgl/)。SwiftShader 是软件渲染，不能证明物理 GPU、性能、目标设备、应用生产集成或填充后的真实 gallery 场景通过。

证据目录 [`evidence/`](./evidence/) 保存执行命令、工具版本、实际 UTC 起止时刻、单调时钟墙钟秒数、返回码、原始报告、截图与 hash。完整审查目录的文件校验和列于 [`evidence/SHA256SUMS`](./evidence/SHA256SUMS)（该清单自身由审查分支提交 SHA 绑定）。主要记录：[`blender-execution-log.json`](./evidence/blender-execution-log.json)、[`128px-render-log.json`](./evidence/128px-render-log.json)、[`khronos/summary.json`](./evidence/khronos/summary.json)、[`webgl/runtime-report.json`](./evidence/webgl/runtime-report.json) 和 [`frozen-input-audit.json`](./evidence/frozen-input-audit.json)。

审查执行时间（UTC）示例：Blender 源/导出检查及干净重新导入从 `20:53:05.831` 至 `20:53:15.963`；每件 512 px 独立渲染在 `20:53:15.975`–`20:53:50.208` 连续完成；Khronos 检查 `20:55:02.023`–`20:55:02.755`；SwiftShader 场景 `20:55:56.865`–`20:55:58.863`；128 px 检视渲染 `20:59:07.066`–`20:59:16.294`。更精确的逐项真实开始/结束时间和 monotonic seconds 见各 JSON，不将这些机器运行时间称作全部人工审查时长。

制作者记录的实际 modeling/export 执行时间为：Emeraldella `2.533 s`（20:34:14.487–20:34:17.020Z）、Burgessia `1.411 s`（20:34:17.907–20:34:19.318Z）、Tuzoia r003 `2.401 s`（20:38:34.506–20:38:36.907Z）、Sanctacaris `3.790 s`（20:34:27.071–20:34:30.862Z）。原始 build-timing、队列结果与环境都按生产 bundle SHA 固定。另有概念记录报告生成调用 `20:26:15.072–20:27:31.556Z`、像素初看 `20:27:43.080Z`，brief/modeling 在之后才冻结；这些是可哈希核对的制作者记录，不是独立证实的墙上时钟来源。生成种子/模型版本未披露，本报告不补猜。

## 阻断与未验证项

- **四件的正式候选批准均阻断。** 在冻结提交中，四个选中 revision 目录都没有 `candidate.json`，所以不能为这些对象生成 profile contract 或运行正式 `validate_candidate.py` 候选批准检查；不能把本次独立 QA PASS 变成 `approved_for_brief`、production acceptance 或 release acceptance。
- **revision-local 元数据不完整。** 每个选中 `metadata.json` 的 `dimensions_m`、`axis`、`primitives`、`textures` 值均为 `null`；`bytes` 字段未提供。GLB 字节数以 `glb_bytes` 给出，尺寸/轴、材质、网格和导出位置顶点等另在 `integration-metadata.json`、`bounds_glb_m` 与实测记录中可得。这阻断将这些 metadata 文件本身当作完整统一候选记录；本次未修改或回填它们。缺少 `candidate.json` 时没有对正式候选验证器作通过/失败推断。
- **未验证。** 物理 GPU、指定目标浏览器/设备、真实部署后的填充场景、gallery 海报/preview 生成、动画/交互、生产性能和 printability 均未在本次检查范围内。不要将 SwiftShader 功能渲染扩大为以上结论。

本分支只包含这份独立 QA 报告和证据；未修改模型、生产元数据、发布清单、站点/UI/CI，也未触碰 PR20、main 合并或发布动作。
