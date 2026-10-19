# Batch 38 独立 QA

本报告只覆盖 `batch-38` 的 **diplomoceras、nelumbo、marine-terrace、angular-unconformity-outcrop**，并绑定到冻结 source 与四个精确 GLB 哈希。审查依据为 `static-stylized-v1` / `2026-10-18.1`，以及用户接受的自然、精致低模教学场景范围。没有要求严格科学复原，也没有进行无边界微观返工。

## 决定

**内容与本轮独立技术检查：四件全部 PASS；模型必修项：无。正式 candidate/profile acceptance：仍 BLOCKED。** 候选记录原样保持 `approved_for_brief=false`，且多个生产阶段仍记录为 `unknown/pending`。本轮 Chromium 的 WebGL2 renderer 是 ANGLE SwiftShader 软件渲染；它证明固定 GLB 可被 Three.js 载入并绘制，不代表硬件 GPU 性能。报告也不改变 candidate 的阶段值或审批状态。

handoff 指定 reviewer 为 GPT-6 Luna / xhigh，但执行环境没有提供可独立核验的 backend model/reasoning 元数据。因此本报告将实际 reviewer identity 标为 **not independently verified**；没有根据通用 assistant 身份推断，也没有因此追加重复 QA。

## 输入与固定身份

- 候选分支：`candidate/small-life-batch38-20261018`
- handoff commit：`70abb5ec41aadd31d56ac9f0d1890ad708afc6da`
- handoff：`production/continuous-small-life-round13-20261018/work/batch-38/HANDOFF.json`；SHA-256 `87a48ec9cf4f4688d28994f5aa028c3322cdcd265723ca801709c33eae0b4589`
- `QA-HANDOFF-SCOPE.json` SHA-256：`53d27281319c5691f5fe4a7ce1ba1028cfb824d812caaf4de377733169b5b0ea`
- 四件模型源 commit：`27075cfa9989c751263ea18c583c11f3007095b5`
- 独立 QA 分支基于 handoff commit；报告未修改模型、profile thresholds、CI、权限、发布或 main。

已复算 161 个 handoff 路径/哈希/字节数引用，并直接从模型源 commit 核对每个冻结 Blend 与 GLB blob。四个 ID、attempt 和 GLB pin 与 `QA-HANDOFF-SCOPE.json` 一致。详见 [`source-integrity.json`](evidence/source-integrity.json)。

## 四件资产结论

尺寸按 GLB X × Y × Z、单位米。表中 SHA 均为完整 SHA-256。

| 资产 | attempt / 三角形 | Blend SHA-256 | GLB SHA-256 | 内容结论 / 必修 |
|---|---:|---|---|---|
| `diplomoceras` | `attempt-01` / 10,604 | `e7ea84a2a77f7ecb715d73b318b1eb3c8f985d6f34c05a5aff184b3e5f9f8107` | `6dad0da9076f6b7afbfc22c578f8886801c17639c5cb138aeb99074bdaca9a67` | PASS：连续渐粗壳管、开敞发夹弯与凹入末端壳口在固定图和 runtime 图中均可读。按保存壳体原创概念处理；不宣称软体、腔室细节或物种实测尺寸。必修：无。 |
| `nelumbo` | `attempt-01` / 6,426 | `a7461ebcbefa76fb004bcec61b173a079b2ccedd80fa52d3bc3e3c4182c3f029` | `ae8b16b920153a1f7c65675bcea268f0733d24402aaed09789ef422bccafea42` | PASS：浅浮雕圆叶、近中央着生痕及放射叶脉清楚；侧视仍保留浅起伏。限定为独立盾状叶片，不推断花、莲蓬、根系或整株。必修：无。 |
| `marine-terrace` | `attempt-01` / 1,744 | `f6ed51e416f0584e725ad44e219a40e6d3c997fe43a066957e39b962b0f13a2d` | `f4e52291f8f0fa573980568414d84f42c7ec7876a26c63f6b8656c96925f0c63` | PASS：抬升台面、后侧废弃海崖和向海前缘在 hero/side/top 可辨；16 m 为示意裁片尺度。展示平面不是 GLB 地形的一部分，不主张水体模拟、具体地点、年代或抬升速率。必修：无。 |
| `angular-unconformity-outcrop` | `attempt-03` / 616 | `b590067de70307b6e78435b147c5ef28f35ffa19c01345a3cbd81df95565062c` | `205f8d59a815eae3865bdb7bed752275cd8e3056bb6ea9cb05ba66bf2b44eded` | PASS：倾斜下伏层在接触面截切，上覆近平层保持连续；结构在彩色、灰模与 runtime 视角均可读。限定为 0.85 m 原创教学剖面，不指定地点或地层年代。必修：无。 |

四个 frozen GLB 字节数依次为 192,456、118,892、95,356、44,032；对应 Blend 为 817,224、697,280、563,084、570,040。详见 [`review.json`](review.json)。

## 独立检查与像素证据

- **Profile**：四个 `validate_candidate.py --profile static-stylized-v1` 检查均为 `profile_contract_status=pass`、`valid=true`，但仍是 `approved_for_brief=false`。每件都保留原记录中各 stage `unknown` 与 `approval pending`。合同固定八视图和零 turntable 视图；这不是模型批准。记录在 [`profile-checks`](evidence/profile-checks/)。
- **Blend 源场景**：Blender 4.3.2 读取冻结文件；四件均是单位比例、identity root、无 source scene 相机/灯。源场景与 exact GLB 三角数匹配；轴转换后包围盒误差分别为 `1.72e-8 m`、`0 m`、`1.79e-7 m`、`0 m`，均低于 `1e-4 m`。逐件检查在 [`evidence/blender`](evidence/blender/)；两次重建的 Blend/GLB 配对报告在 [`evidence/rebuilds`](evidence/rebuilds/)。
- **实际重建**：每件都用冻结的 generator/config 在 Blender 4.3.2 下全新构建两次，共八次。八个输出 GLB 都与对应冻结 GLB **字节级完全相同**，两次 decoded geometry/material/scene digest 也都一致。重建源 Blend 与各自 GLB 的三角数、包围盒检查均通过。重建日志与 digest 汇总在 [`rebuild-summary.json`](evidence/rebuilds/rebuild-summary.json)。
- **GLB 格式**：Khronos validator 对四个 exact GLB 各报 0 error、0 warning。报告以副本验证，原候选文件未被写入。
- **固定图**：核对冻结八视图 manifest 与哈希，并由冻结 Blend 独立重渲染八视图；新输出已逐像素打开检查。四件实际固定图与 `GLTFLoader` runtime 截图对照收录在 [`contact-sheets`](evidence/contact-sheets/)。原始像素覆盖统计和图像 SHA 在 [`visual-inspection.json`](evidence/visual-inspection.json)。
- **Runtime 像素**：新 Chromium `154.0.8037.57` + Three.js r180 / WebGL2 实际载入四个精确 GLB；每件 10 张单模型视角/尺寸图与 2 张六实例场景图，console/runtime errors 与 failed requests 均为 0。Renderer 为 `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)`。截图和逐视角计数在 [`evidence/runtime`](evidence/runtime/)；这是软件渲染功能/像素证据，不是 GPU 性能证据。

Diplomoceras 与 Nelumbo 的源审计提示 smooth-shaded faces 需人工复核；已结合 clay、silhouette、侧/顶视图检查，圆形壳体与浅叶浮雕的平滑着色是有意选择，不构成缺陷。

## 正式状态与未完成项

本轮对四个对象的内容判断和 Blend/GLB、重建、格式及浏览器功能检查均通过，**没有模型级 must-fix**。正式 profile acceptance 仍 blocked：候选记录未更新，多个必需 stage 仍是 `unknown/pending`；尤其没有真实硬件 GPU 证据。完成正式接受流程时需按 exact GLB hashes 取得硬件 GPU evidence，并由正常的 candidate gate/release 流程显式记录所有必需阶段。该 QA 报告本身不会把候选提升为已批准。

适用仓库指引已阅读：`skills/blender-lowpoly-pipeline`、`skills/lowpoly-art-direction`、`skills/asset-factual-review`、`skills/prehistoric-environment-art`，以及 `.agents/skills/emil-animation/*`（静态资产 QA 不涉及动画）。profile 规则依据 `docs/candidate-profile-compatibility.zh-CN.md` 与 `schemas/README.md`。
