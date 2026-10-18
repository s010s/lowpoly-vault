# Batch 19 独立 QA 复核

**源候选：** `candidate/small-life-batch19-20261018` @ `5d137441d8ee2a20fcf5ef96a98e3e1c2ec178dc`  
**检查规则：** `static-stylized-v1` / `2026-10-18.1`  
**复核结论：** 四项均通过各自冻结 brief 范围内的视觉、结构、尺度、固定视图和实际 GLB 运行时核验。风格按自然、精致的低多边形教学美术评估，不作严格科考复原结论。

## 核验方法与结果

- 在只读源资产的独立 worktree 中复算各 `.blend`、`.glb`、`candidate.json` hash；Blender 4.3.2 fresh reopen 核对单位比例 1、identity root、三角面、变换，以及每个导出网格的 boundary / non-manifold edge。
- 对每件 8 张固定源图逐图核对文件名、manifest SHA-256、字节数和实际尺寸。八图为 hero/reversehero/front/side/rear/top/clay/silhouette；除 128×128 的 silhouette 外均为 512×512；没有转台帧。
- 重跑 `scripts/validate_candidate.py --profile static-stylized-v1`，以 Khronos glTF Validator 2.0.0-dev.3.10 独立验证各选中 GLB：均为 0 errors / 0 warnings。
- 用 Three.js 0.180.0 `GLTFLoader` 在 Chromium ANGLE SwiftShader WebGL2 独立重载并渲染精确 GLB：单件七向、80/160/240px 和六实例场景 hero/top 均通过；检查的关键新截图与冻结 runtime 截图 SHA 完全一致。

| 资产 | 版本 | 名义尺度 | 实测 GLB bounds (X×Y×Z m) | 三角面 / GLB | 六实例场景 draw calls / triangles | QA |
|---|---:|---:|---:|---:|---:|---|
| cooksonia | r001 | 0.07 m (shoot cluster height) | `[0.05499999783933163, 0.0701957773999311, 0.02404000051319599]` | 5,888 / 114,504 bytes | 18 / 35,328 | **PASS** |
| cambroraster | r002 | 0.12 m (shield body span) | `[0.12813019752502441, 0.024888877291232347, 0.11309130489826202]` | 9,588 / 192,668 bytes | 66 / 57,528 | **PASS** |
| bedrock-pothole | r001 | 0.8 m (rock patch width) | `[0.7994612455368042, 0.3083689510822296, 0.6394271552562714]` | 6,840 / 141,884 bytes | 24 / 41,040 | **PASS** |
| quartz-prism-cluster | r001 | 0.2 m (crystal cluster span) | `[0.1720000058412552, 0.1877751499414444, 0.12823480367660522]` | 972 / 58,392 bytes | 24 / 5,832 | **PASS** |

## 逐件结论

### cooksonia / r001 — PASS

- 单件 checkpoint：`8c9272b6efc97db5ba2e6f6cde7129032989b0c0`
- `candidate.json` SHA-256：`dd0f86d7c38a75e183aeafa0fefae7f51637447c199c3385e865f492ff307106`
- 源 `.blend` SHA-256：`b296dd083342a3134e933d252a8a77faf900e75a0b8dd57fbe7377be3f03cf18`
- 选中 `.glb` SHA-256：`9f0a98a40646df280257f0f0049dd71a260d0c05056d2e97383f45f974fbb5c0`
- 名义尺度 0.07 m（shoot cluster height）；实测 bounds X/Y/Z `[0.05499999783933163, 0.0701957773999311, 0.02404000051319599]` m。源网格 2,966 verts / 5,888 triangles；3 materials / 3 primitives / 114,504 bytes。
- 视觉结论：Y形分叉茎与末端孢子囊读得清楚，分枝节奏稀疏但有层次；70 mm 目标高与实测 70.196 mm 相符。固定视角和 GLB 中未见断茎、错误开口或缺面。80 px 近缩略图细枝变弱，160/240 px 轮廓仍明确。
- 源网格核验：2 个导出 mesh，全部 boundary edge 和 non-manifold edge 为 0；源 tri 与最终 GLB tri 对齐。
- runtime：3 draw calls / 5,888 单件 triangles；六件场景 18 calls / 35,328 triangles；所有视图无运行错误/失败请求。

### cambroraster / r002 — PASS

- 单件 checkpoint：`b55970770d407e7449e7ebf9ff33b178830c89a9`
- `candidate.json` SHA-256：`8e289be06eb3c68edb299f71ac4394322ff2186cf5cc186e38694f844e8f7965`
- 源 `.blend` SHA-256：`921bf7ed3788c150ba90254b408ae5e28f7155f485520b9895b99c800eddf7b9`
- 选中 `.glb` SHA-256：`c8662370a1b676ee7f2b0c12c8b93e8aa8f38a867b375001ac4cb7c5b3f1e86e`
- 名义尺度 0.12 m（shield body span）；实测 bounds X/Y/Z `[0.12813019752502441, 0.024888877291232347, 0.11309130489826202]` m。源网格 4,902 verts / 9,588 triangles；5 materials / 11 primitives / 192,668 bytes。
- 视觉结论：只评 r002。r001 的侧视腹侧附肢连接缝仍可见；r002 的新腹侧头部体块与抬高的附肢根在源图和独立重载 GLB 侧视/腹视中连续衔接。马蹄形背甲、深眼缺口和眼部轮廓清楚；其余腹部/附肢仍是明确简化，不主张精确复原。
- 源网格核验：6 个导出 mesh，全部 boundary edge 和 non-manifold edge 为 0；源 tri 与最终 GLB tri 对齐。
- runtime：11 draw calls / 9,588 单件 triangles；六件场景 66 calls / 57,528 triangles；所有视图无运行错误/失败请求。

Cambroraster 只审最终 r002；r001 没有继承任何通过结论。repair 记录将 r001 侧视缺口绑定到新的侧视图与 GLB。直接对比旧/新侧视，再查看 r002 精确 GLB 的 side/bottom runtime：腹侧头部体块与抬高的附肢根已连续衔接，原缺口消失。
- r001 旧 GLB SHA-256：`1fa6443375920d2acc1160f57c6f64d022d4a1255ff5f95a88a3e36e9e4582e3`；r002 新侧视 SHA-256：`38243ac30301e5e18dccdea1471e554a8caade60445ecae53f42a63ba83224c4`；r002 GLB SHA-256：`c8662370a1b676ee7f2b0c12c8b93e8aa8f38a867b375001ac4cb7c5b3f1e86e`。

### bedrock-pothole / r001 — PASS

- 单件 checkpoint：`af3e0711b5e43675fc7e7b3212a05b47f7a96d8b`
- `candidate.json` SHA-256：`a7c46b2e4696413325300acc3ca5a434471438a8b19ab845c11224b67631af1a`
- 源 `.blend` SHA-256：`d33e12bd47d92e3fee7ead0caf9c8d6a3748b5a8ad228eac144c32492b0fda01`
- 选中 `.glb` SHA-256：`182f30ba029ddf8acb131c82018613178f40f447582baac16d37513600e78420`
- 名义尺度 0.8 m（rock patch width）；实测 bounds X/Y/Z `[0.7994612455368042, 0.3083689510822296, 0.6394271552562714]` m。源网格 3,424 verts / 6,840 triangles；3 materials / 4 primitives / 141,884 bytes。
- 视觉结论：约 0.8 m 宽的限定展示岩块中，圆深穴与穴底圆砾清楚；俯视、斜视和侧视没有意外开口或缺面。平直外缘是有边界的教学切块，不应标作可无缝拼接地形。
- 源网格核验：2 个导出 mesh，全部 boundary edge 和 non-manifold edge 为 0；源 tri 与最终 GLB tri 对齐。
- runtime：4 draw calls / 6,840 单件 triangles；六件场景 24 calls / 41,040 triangles；所有视图无运行错误/失败请求。

### quartz-prism-cluster / r001 — PASS

- 单件 checkpoint：`da4a0627f8d651c4ca1734822d9753720239f936`
- `candidate.json` SHA-256：`4ac19a0f4baae2be138f6bd59039f7e0871b65a439972b6d12b250aa789563c9`
- 源 `.blend` SHA-256：`aedb083438c72ccea5c8326be631f54d7398de1be79d8745c3679b08f597df75`
- 选中 `.glb` SHA-256：`6efded4938f08ad789a4a3f409a45b6e178c243d998aa6ae50b72bef02b17044`
- 名义尺度 0.2 m（crystal cluster span）；实测 bounds X/Y/Z `[0.1720000058412552, 0.1877751499414444, 0.12823480367660522]` m。源网格 506 verts / 972 triangles；4 materials / 4 primitives / 58,392 bytes。
- 视觉结论：约 0.2 m 的晶簇有明显主次高度、不同倾角、六方柱体与尖端，晶体扎根于安静基质；俯视和斜视均可读。没有把它标成特定矿区、年代或化学测定样品。
- 源网格核验：2 个导出 mesh，全部 boundary edge 和 non-manifold edge 为 0；源 tri 与最终 GLB tri 对齐。
- runtime：4 draw calls / 972 单件 triangles；六件场景 24 calls / 5,832 triangles；所有视图无运行错误/失败请求。

## 记录边界

- 四件 profile 复验均 `valid=true`、`profile_contract_status=pass`；原始 `candidate.json` 仍 `approved_for_brief=false`，七个正式阶段还保留 `unknown`。本复核记录给出独立 QA 结果，但没有改写冻结候选状态。
- 本次 runtime 使用 SwiftShader 软件 WebGL2。目标硬件 GPU 和真实设备性能仍为 `unknown`；没有从软件渲染推断硬件性能。
- 旧 `legacy-v1` 对 consulted-only 引用缺少 license 文本的错误原样保留；当前 `static-stylized-v1` 合同通过。引用只作查阅，未并入参考媒体或网格，也没有推断第三方权利。
- 未改模型、阈值、CI、权限、发布清单或其他批次；未 merge、发版或写入 Drive。

机器可读的逐项 hash、视图清单、source/runtime 测量、validator 与限制见同目录 [`review.json`](./review.json)。
