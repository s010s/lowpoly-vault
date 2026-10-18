# Batch 01 精确源提交独立 QA

**审阅源提交：** `e6391cd3d1059f39feba4dc88a18544cbeebfee6`  
**结果：** 4 项均 **PASS**；无必修项。  
**范围：** 仅验收该提交中的四个静态风格化候选。不是严格科研复原、实机 GPU 性能证明或发布授权。

## 精确资产身份

| 资产 | GLB 字节 / 三角形 | GLB SHA-256 | `.blend` SHA-256 |
|---|---:|---|---|
| Archaeopteryx | 141,564 / 3,776 | `2f74e3b9620ec72ae02f6e9a986a6e8593519aca7287c1ed7351f30c279d1a04` | `7ac64cd8b03b65f09b51b1b40d668f32d672b9d13bfd90352c7f623fa0b90257` |
| Canadaspis | 112,708 / 4,276 | `08619d89a3ef455b9612b0c55575de2abe84ec161c06ef072f38cf7e0d9e98b1` | `a3fe0904a5f8be7d6b205f47c22a4890360fde1711ffa1f6b5f83280e6451522` |
| Ceratomyrmex | 43,596 / 1,856 | `41ffc10021d27f7cf799d854076a6dd32ae657f2487dc28f601602a436761c3c` | `b1dfa3c851f188cd874f6f8ef75e3a47e4a24416d8b82b9984c8c5320be5240b` |
| Hydropteris | 234,596 / 5,332 | `629e4313bd5c2102135a1809b6be8f778e510d6e928a01a60d8a58152369b125` | `df1b33c1140050cd2d04de155e00f64d22a0e7f645b7ce9bb48758189e14e032` |

以上值逐项对照 e639 `handoff-hashes.json`，并重新计算磁盘文件 SHA/字节数。四包共 170 个 `checksums.sha256` 条目全部匹配；每项八张固定角度图和原有精确 GLB 运行图也都与各自 GLB SHA 和图像 SHA 匹配，详情见 [哈希及运行证据审计](independent-evidence/e639-refresh/e639-hash-runtime-audit.json)。

## 独立视觉与结构判定

- **Archaeopteryx — PASS。** 八视图和精确 GLB 正反、前侧、顶底图中，两翼、两腿、长尾羽轴、喙齿和翼指爪的主体关系完整；翼与尾羽连接连续。未见明显缺面、意外穿插或断开的主要结构。像素证据：[80 px](independent-evidence/e639-refresh/fresh-runtime/archaeopteryx/hero-80px.png)、[反向 360 px](independent-evidence/e639-refresh/fresh-runtime/archaeopteryx/reversehero-360px.png)。
- **Canadaspis — PASS。** 双瓣椭圆背甲和背缝、外露前端、成对侧肢、分节且带刺的裸露腹部与末端突起可从顶、侧、底视图区分。外肢未延伸成尾部步足；未见明显穿插或主体缺面。像素证据：[顶视](independent-evidence/e639-refresh/fresh-runtime/canadaspis/top-360px.png)、[底视](independent-evidence/e639-refresh/fresh-runtime/canadaspis/bottom-360px.png)。
- **Ceratomyrmex — PASS。** 六足蚁形身体、触角、窄腰、额角和上弯大颚在前、顶和斜角图中可辨，头部关键间隙仍可读。80 px 时大颚细节自然减弱，但整体轮廓保留；240–360 px 图足以辨认角颚关系。没有猎物或行为声明。像素证据：[240 px](independent-evidence/e639-refresh/fresh-runtime/ceratomyrmex/hero-240px.png)、[前视近看](independent-evidence/e639-refresh/fresh-runtime/ceratomyrmex/front-360px.png)。
- **Hydropteris — PASS。** 分枝根茎、下方根、羽状叶片和根茎/叶轴交界附近的孢子果状圆体在顶、底、侧图中仍相连并可辨。叶片有意采用简化的交替/近对生节奏；未见明显缺片、悬空叶轴或意外穿插。像素证据：[顶视](independent-evidence/e639-refresh/fresh-runtime/hydropteris/top-360px.png)、[侧视](independent-evidence/e639-refresh/fresh-runtime/hydropteris/side-360px.png)。

按同一画面检查 80、160、240 px 主体视图及 360 px 多方向近看，主体识别保持稳定。另检查每项三实例的中性场景截图；它是道具重复基准，不代表博物馆整合测试。整体风格与已接受的 `small-fauna-trio-v2`（参考图像提交 `c8514b8c348777c9a2d81c6c0bbd9cf02cdb5184`）在自然主形、克制色彩和轮廓可读性上相容；这批的调色板表面比参考组更朴素，属于本批 palette-only brief 的风格差异，无需为追求纹理而返工。

新跑的三实例场景图：[Archaeopteryx](independent-evidence/e639-refresh/fresh-runtime/archaeopteryx/scene-hero-480px.png)、[Canadaspis](independent-evidence/e639-refresh/fresh-runtime/canadaspis/scene-hero-480px.png)、[Ceratomyrmex](independent-evidence/e639-refresh/fresh-runtime/ceratomyrmex/scene-hero-480px.png)、[Hydropteris](independent-evidence/e639-refresh/fresh-runtime/hydropteris/scene-hero-480px.png)。

## 复跑技术证据

我在 detached e639 checkout 中独立重开四份 `.blend`，将导出集合与精确 GLB 比较；Blender 4.3.2 报告三角形数匹配，坐标轴转换后的包围盒最大误差均为 **0.0 m**。四个 GLB 的静态审计无错误/警告；Khronos glTF Validator 2.0.0-dev.3.10 对四个精确文件均报告 **0 errors / 0 warnings**。再次在干净 Blender 进程中导入 GLB 后，三角形数仍匹配、包围盒误差为 **0.0 m**，无导入错误。

Blender 导入检查提示一些开放边界：Archaeopteryx 的 flight/tail-feather 薄片，Canadaspis 的 outer-branches，Hydropteris 的 pinnae 薄片；它们在实际底视图、反向图和侧视图中呈现为连续的预期薄表面，而非缺失躯干/叶片。另有 smooth-face review 提示，属于有意平滑的有机面。源文件自身的四项部件审计均为 0 边界边、0 非流形边。按本 brief 和已核看像素，这些是**非阻塞警告**。

我另把 e639 的精确 GLB、原 viewer 和 `browser_qa.mjs` 复制到隔离临时目录，用 Three.js r180 / Chromium 重新渲染。每项七个方向、80/160/240 px 尺度与 360 px 方向图，以及两张三实例场景图，合计 48 张新运行截图，均绑定对应 GLB SHA；四项均无浏览器错误、失败请求或加载异常。使用的是 ANGLE/Vulkan SwiftShader 软件渲染，不构成实体 GPU 性能数据。

可复核材料：

- [重跑命令](independent-evidence/e639-refresh/commands.txt)
- [新运行图与渲染摘要](independent-evidence/e639-refresh/fresh-runtime-summary.json)
- 每项新截图位于 `independent-evidence/e639-refresh/fresh-runtime/<asset>/`
- 每项独立 GLB 审计、Blend/GLB 对比和 Blender 导入报告位于 `independent-evidence/e639-refresh/<asset>/`
- [Khronos 验证重跑](independent-evidence/e639-refresh/khronos-validator-rerun.json)
- [bundle integrity 重跑](independent-evidence/e639-refresh/bundle-validation-rerun.json)；[可复跑 Khronos 检查脚本](independent-evidence/e639-refresh/validate-khronos-batch01.cjs)

## 基础形态核对与边界

本结论只覆盖 brief 明确要求的命名类群启发式基础形态。NHM 对 Archaeopteryx 支持羽毛、齿、长骨尾和手爪，并提示其“鸟”归类与飞行能力仍有讨论；本件标为静态风格化启发式，没有飞行或严格分类声明（[NHM](https://www.nhm.ac.uk/discover/what-were-the-first-birds-like.html)）。ROM 对 Canadaspis 描述了覆盖身体前半的双瓣甲、分节无足且边缘有刺的腹部，以及成对末端突起；这些宽泛识别特征与模型一致（[ROM 形态条目](https://burgess-shale.rom.on.ca/fossils/canadaspis-perfecta/)）。Ceratomyrmex 原始论文摘要支持明显的头角与高耸镰状大颚；论文全文在本次审阅环境中无法读取，因此只判定基本角颚关系，不推断精确比例、微结构或捕食行为（[Perrichot、Wang 与 Engel 2016](https://doi.org/10.1016/j.cub.2016.03.075)）。Hydropteris 的 1994 原始描述支持分枝根茎、根、羽状叶、交替至近对生的小叶及根茎/叶轴交界的孢子果（[Rothwell 与 Stockey 1994](https://www.researchgate.net/publication/240820777_The_Role_of_Hydropteris_pinnata_gen_et_sp_nov_In_Reconstructing_the_cladistics_of_Heterosporous_Ferns)）。

**非阻塞命名备注：** 2025 年一篇命名学论文认为 `Hydropteris` 是不能使用的同名，并采用 `Dorfiella knowltonii`；2026 年一篇北美化石蕨类研究的数据表仍保留 `Hydropteris pinnata` 并写明不建议修改。当前对该名称不作裁决。候选只写 `Stylized Hydropteris`，brief 也明确为 stylized-inspired、非严格复原，因此我不把这个命名分歧扩大成几何返工项（[Hermsen 2025](https://phytotaxa.mapress.com/pt/article/view/phytotaxa.733.1.8)，[Holian 等 2026](https://doi.org/10.1002/ajb2.70243)）。

## 结论

四项均满足本次冻结的基础识别、结构连接、精确 GLB、8 个固定视图、80–240 px 场景尺度和适度近看要求。**无必修项；非阻塞备注仅供发布文案/运行环境说明使用。** 本报告不修改候选模型或验收阈值，也不合并、不发布。
