# Batch 21 独立 QA

**审查者 / Git 作者：** Leon Made This `<8357465+s010s@users.noreply.github.com>`
**日期：** 2026-10-18
**范围：** 仅审查 `montsechia`、`dollocaris`、`coelurosauravus`、`columnar-jointed-outcrop`。
**规则：** `static-stylized-v1`, `2026-10-18.1`；handoff 锚点 [`f78c364`](https://github.com/s010s/lowpoly-vault/tree/f78c36446e13cf12e335c152a37096e53859813a/production/continuous-small-life-round07-20261018/work/batch-21)，其中 `final-handoff.jsonl` SHA-256 为 `be0d64cf314dab339f3bb9c8435be327cf3c055de4fed04503f181dc6f0cb6a0`。

## 结论

**独立审查通过：** 四项的对象与 handoff source commit、Blend、GLB 均对应；静态固定 8 视图与精确 GLB 的实际浏览器渲染均已查看。比例、关键部件衔接与面连续性符合各自 brief，未见明显意外缺面、断接或尺度归一化问题。整体达到自然、精致的风格化低模教学资产观感；结论限于 brief 所述的启发式形态，不作严格微观复原判断。

这不是 profile 的最终发布批准。源记录仍为 `approved_for_brief=false`：目标硬件 GPU 与实际代表性场景尚未证实。本审查没有更改任何候选记录、模型、阈值、CI、权限或发布状态。

## 对象身份与证据绑定

候选分支与 source commit 取自指定 handoff 的四条记录；下表哈希分别核对 handoff、源文件与候选分支内容。固定视图 manifest 与 runtime evidence manifest 也逐一核对。

| 对象 / 候选 source | GLB SHA-256；尺寸 / 三角面 | Blend SHA-256 | 固定 8 视图 manifest SHA-256 | Maker runtime evidence manifest SHA-256 |
|---|---|---|---|---|
| **Montsechia** · [`candidate/batch21-montsechia-20261018`](https://github.com/s010s/lowpoly-vault/tree/86038ef0274924cb2315057500b481fdda8d8ec6/assets/candidates/continuous-small-life-round07-20261018/batch-21/montsechia/r001) @ `86038ef0274924cb2315057500b481fdda8d8ec6` | `5ce96a830ddd499881f9aac0c5d261a80b1436c79935e85965c7777ffaf28d6b` · 92,544 B / 3,140 tris | `dbd160b8c67d69cc6cab2c5e547e2ea2ad8438c0a20c7de02af79544142a3d4f` | `1b2b5f270ae447558dfe2f2265890cfb3babc7e039e76d09d0adc33a7dab0428` | `b377258ef0d691d1b6608b76adf81394dd6eb2409dc64b4a018a11f3df386483` |
| **Dollocaris** · [`candidate/batch21-dollocaris-20261018`](https://github.com/s010s/lowpoly-vault/tree/76872051f73176326d40df9ac4dafbc0dcc9583c/assets/candidates/continuous-small-life-round07-20261018/batch-21/dollocaris/r001) @ `76872051f73176326d40df9ac4dafbc0dcc9583c` | `5ea5da44c0b7fb0f22110ba5d86686863d67c260802700c9d1dd8a542f58c284` · 124,824 B / 6,504 tris | `32474bf5cba324bc487e8ba73fdbb2e077211b219a09521dd6b809c584ac40d1` | `003b46b801cf84edd51a3ebc628a346edd03916fa978867f99410dd8143eea1d` | `526fcffeb6fd9cdca67722e9a4a3e11d992680447f1f4e11098edf64ea5adf39` |
| **Coelurosauravus** · [`candidate/batch21-coelurosauravus-20261018`](https://github.com/s010s/lowpoly-vault/tree/8d223a9bd8eb46478bfee41b7c091ca0456b925b/assets/candidates/continuous-small-life-round07-20261018/batch-21/coelurosauravus/r001) @ `8d223a9bd8eb46478bfee41b7c091ca0456b925b` | `7cee9840fa5dc80192df77f9b2486a926aa17f9d9bbf2ae282f0dfa900fb750e` · 126,560 B / 6,628 tris | `c2ede59ba2df6695113ac23416023b5eed2b16c6c95de9390fd46b57e1fb9124` | `a5f035502ef907db7e7d5abca1ae8359a8c713657b14bac9e567ce0e55606643` | `ab76d02fc225c689b1ef0285c0b976575102a8b443ca894837189c30c4d30ad8` |
| **Columnar-jointed outcrop** · [`candidate/batch21-columnar-jointed-outcrop-20261018`](https://github.com/s010s/lowpoly-vault/tree/49ecdbd68c9f93e8cd9566a837937c5cf588f9f9/assets/candidates/continuous-small-life-round07-20261018/batch-21/columnar-jointed-outcrop/r001) @ `49ecdbd68c9f93e8cd9566a837937c5cf588f9f9` | `c7fe274488d63ad1df65c0e68362104271c47f9629d95e1abd9c83adfa723f96` · 38,692 B / 614 tris | `ff91872ca1b1bdb1019d78f909708742c91303656210694138bea0128be16385` | `6c1adb05c7719dd35291a9a830c9e6f5d88ac1c5b18babb61e278926df317970` | `0d77c75d802b232aaf4d6d13cf4acb693edc03141b6f49ac9eaacbd3852b52a2` |

## 检查方法与结果

- **固定视图：** 对照各自的 `views/render-manifest.json` 实际查看 `hero, reversehero, front, side, rear, top, clay, silhouette` 八张图。每项各视图恰好一次，turntable 为 0；标准视图为 512×512，silhouette 为 128×128。图像 SHA 与 manifest 相符。
- **源模型与导出：** 以 Blender 4.3.2 重新打开四个精确 `.blend`；独立 source mesh measurements 显示单位比例 1.0、根变换为 identity，原始源网格没有非有限法线、非正面积面、开放边界或非流形边。对照 `source-export.report.json`、Khronos GLB Validator 和 `check_glb_roundtrip.py`，GLB 哈希、三角面数、边界尺寸与来源一致，边界最大误差为 0；四个 Khronos 报告均为 0 errors / 0 warnings。
- **精确 GLB 运行时：** 将 handoff 指定的四个 GLB 分别重新送入候选 `runtime.mjs`，用 Chromium 154.0.8037.57、Three.js 0.180.0、ANGLE SwiftShader software WebGL 实际加载，并重新渲染 hero、reversehero、front、side、top、near、scene-9-copies。四项 runtime status 均为 `pass`；运行时重新计算的 GLB SHA、三角面数与上表相同；每视图均有前景像素、`gl_error=0`，无浏览器/控制台错误。九实例结果只验证本地功能显示，不代表实际目标硬件性能。
- **圆整说明：** Blender 导入 round-trip 对平滑面及因平面着色法线拆点产生的部分导入边界计数给出 `pass_with_warnings`。原始 Blend 网格边界审计为零；结合 GLB validator 与全部视图像素复核，未发现可见开洞或断开的柱体/叶片。没有把这种导入拆点计数误判成模型缺面。

## 逐项视觉、比例与形态

| 对象 | 目检结论；GLB 全对象包围盒（X × Y × Z，m） |
|---|---|
| **Montsechia** | 轻巧的分叉柔性枝条、小叶与成对顶生卵形果实读形明确，果实和枝梢、叶片和枝轴衔接自然；top 视图显得细长扁平，符合纤细枝条设定。包围盒 `0.11311 × 0.15000 × 0.01944`；brief 的标称枝条跨度 0.15 m 与长轴相符。 |
| **Dollocaris** | 深椭圆双瓣甲壳包住身体；两只放大的前部眼有连续基座，三对前部抓握肢与后部短附肢可辨。侧面和反面未见肢体断接；顶面甲壳中缝表现为有意的双瓣接缝。眼睛比例是温和的风格化强调。包围盒 `0.07199 × 0.07809 × 0.13226`；brief 标称 0.10 m 是甲壳长度，不是含附肢全对象长。 |
| **Coelurosauravus** | 低伏躯干、长尾、四肢与两侧带独立放射支杆的翼膜在 hero/top/reversehero 均连贯；side 很薄，符合扁平滑翔体的设计且没有缺面。支杆起点、数量与飞行机制仍按 brief 视作艺术化/不确定，没有扩张成精确解剖主张。包围盒 `0.20076 × 0.02642 × 0.32000`；brief 的 0.32 m 为吻端至尾端，不含展示翼幅。 |
| **Columnar-jointed outcrop** | 不规则多边形柱紧密相接并连到低矮岩体，顶端高低错落；top 明确呈现柱状节理，side 的块状轮廓与 hero 中可见的断裂层次一致。柱间线是意图表现的节理，未见宽阔空洞。包围盒 `0.90000 × 0.38985 × 0.68571`；宽度与 brief 标称 0.90 m 相符。 |

共同观感为克制的低面数形体、柔和自然色与清楚的关键轮廓。尺度按各 brief 的对象基准核对；没有将局部翼展、附肢或装饰跨度误当作标称身体长度，也没有观察到单位立方体式归一化。

## 事实范围与未覆盖项

审查按 brief 的“受启发的风格化教学资产”范围判断：Montsechia 的无根分枝柔性枝轴、简单小叶与成对顶生果实；Dollocaris 的双瓣甲、成对大眼、三对头部附肢；Coelurosauravus 的扁平滑翔体与翼膜；柱状节理的多边形柱体。参考：[Montsechia 原始论文](https://www.pnas.org/doi/10.1073/pnas.1509241112)、[Dollocaris 形态论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC4735654/)、[自然历史博物馆的 Coelurosauravus 概述](https://www.nhm.ac.uk/discover/news/2022/september/gliding-reptiles-have-been-taking-to-skies-for-260-million-years.html) 与 [期刊论文 DOI](https://doi.org/10.1080/02724634.2022.2108713)、[美国国家公园管理局柱状节理说明](https://www.nps.gov/subjects/volcanoes/columnar-jointing.htm)。Coelurosauravus 期刊全文本次无法直接读取，因此该项只按宽泛、启发式形态审查；不推断精确支杆位置/数目、单一遗址、严格尺寸或行为。

Maker 记录中的 `profile_contract_status=pass`、`candidate_record_valid=true` 与 `approved_for_brief=false` 仍各自独立。本报告不替代其余尚未完成的 profile 阶段，特别是目标 GPU 与实际代表性场景检查。
