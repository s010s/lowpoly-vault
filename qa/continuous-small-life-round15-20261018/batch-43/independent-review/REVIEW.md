# Batch 43 独立静态资产 QA：lowpoly-vault / s010s

**总体结论：四件均 PASS；必修项：无。** 结论仅覆盖 `static-stylized-v1` / `2026-10-18.1` 冻结 brief 定义的自然、精致低模儿童教学艺术范围。它不是严格标本复原、候选正式批准、发布许可或硬件性能认证。

- 审查日期：2026-10-19 UTC。范围：`kootenayscolex`、`dillhoffia`、`beach-ridge`、`phycodes-palmate-burrow`。
- 候选源分支 `candidate/small-life-batch43-20261018` 的本地独立检出和远端 ref 均为 `5163f72e8d32fc4a8eefd2f191dc46d9956feeb7`；冻结 HANDOFF 与 QA-HANDOFF-SCOPE 中的模型源提交一致，均为 `4951bdbb5e0ab0b5f7fb3b115326c1ced7f7f35d`。四个 ID、GLB pins 和批次均匹配范围文件。
- 交接文件：[HANDOFF.json](../../../../production/continuous-small-life-round15-20261018/work/batch-43/HANDOFF.json)、[QA-HANDOFF-SCOPE.json](../../../../production/continuous-small-life-round15-20261018/work/batch-43/QA-HANDOFF-SCOPE.json)。适用仓库标准：[视觉验收规则](../../../../skills/lowpoly-art-direction/references/visual-acceptance.md)、[Blend→GLB 生产合同](../../../../skills/blender-lowpoly-pipeline/references/production-contract.md)、[事实范围指引](../../../../skills/asset-factual-review/SKILL.md)。
- 审查按一轮独立 QA 完成。调用上下文未提供可验证的精确模型子类型或 reasoning 元数据，因此本报告不声称 reviewer 实际身份已证实为 HANDOFF 所请求的 GPT-6 Luna xhigh，也不以该元数据缺失为由重复 QA。

## 逐件结果

| 资产 / 检查点 | Blend SHA-256 | GLB SHA-256 | triangles / materials / primitives / GLB bytes | 结论 / 必修 |
|---|---|---|---:|---|
| `kootenayscolex` / `3ea6a84be7397441f2f5736bfa47e11afe180685` | `0059843c57b8b434a13f1a419e5aea21e107a01619f5e8e018aabd30433fec5a` | `0dc9a5fa202a7f36dc39671d77dd2b876b34cb336b0efc5826c445dd7a6156d5` | 11,918 / 4 / 6 / 228,408 | PASS / 无 |
| `dillhoffia` / `9f6b36c6691977e034f923a86bb68db948ca63c8` | `b7fb48ea0b6743c04b2cd54b63ddadb99a40f760f3479e764d94553c8ff748f9` | `cbaa5715b560533f0068e228b9df3a67ae6e564edb252feedd814e54b5ed116b` | 3,164 / 3 / 3 / 64,188 | PASS / 无 |
| `beach-ridge` / `1735935c80f46d7c16e6ec6f3c7b2065ec8ab73` | `bb84bb12deff39ef40cf593578f4b446783233ed2f8607446c06b5bca7395426` | `a4c9d912ab9c4055e36a847067121f747c743475dd78a01d8aae30cec0dd0060` | 4,774 / 3 / 3 / 256,496 | PASS / 无 |
| `phycodes-palmate-burrow` / `4951bdbb5e0ab0b5f7fb3b115326c1ced7f7f35d` | `932258980e345e7d909ea905ff884113788c26a9264923c36e7c6d545d23fbc2` | `711e8a32a739fdf3f9b44fee08955c87059ecdcf579e64dfcc4cce012f36ace4` | 12,566 / 2 / 2 / 237,364 | PASS / 无 |

所有模型低于冻结硬上限：14,000 triangles、1,000,000 GLB bytes、6 materials、30 primitives；均无纹理。四个确切 Blend 均已用 Blender 4.3.2 在 autoexec 关闭情况下只读打开。每件 8 个 source 固定视图、10 个单件精确 GLB runtime 视图及 2 个六实例 runtime 场景视图，共 80 张固定图像的哈希/字节数均与各自 manifest 相符；图像逐张清单、SHA 与尺寸列于 [review.json](./review.json)。

### `kootenayscolex` — PASS

连续的柔和分节躯干中段较宽、两端收细；顶视及斜视能读出侧肢/刚毛列，头部触须和短中央结构保留。形态符合 Kootenayscolex 启发式教学件范围，不要求刚毛微观标本级复原。基础形态交叉核对：[Royal Ontario Museum](https://burgess-shale.rom.on.ca/fossils/kootenayscolex-barbarensis/)。

### `dillhoffia` — PASS

单一细长果体连到浅外张、无裂的萼盘；主要放射脊在反向/上视和灰模中可辨。没有加入母株或其他器官。该造型保持为保存果/萼教学件，不作花朵、莲蓬或精确物种复原主张。基础形态交叉核对：[RockRoom, Specimen MB302d](https://rockroom.evolvingearth.org/Home/Specimen/325)。

### `beach-ridge` — PASS

单一连续裁片表现活动前滨、其后低岸平行脊及陆侧缓坡。俯视的高程/颜色过渡克制，但侧剖面清楚显示低脊，符合 brief；它没有读成障壁岛、波纹或悬崖。14 m 只是教学裁片名义宽度。一般地貌背景：[Michigan State University](https://project.geo.msu.edu/geogmich/beach_ridges.html)。

### `phycodes-palmate-burrow` — PASS

灰模及顶视表现一条连续凸起主管，末端紧凑分成掌状扫帚末枝，枝管嵌在基岩板上且连接连续。没有声称特定造迹生物或复制标本。基础痕迹形态交叉核对：[Kansas Geological Survey](https://www.kgs.ku.edu/Publications/Bulletins/245/04_ichno2.html)。

## 技术和图像证据

- 按冻结 handoff 的精确路径重算 GLB、Blend、candidate、source-export、reproducibility、view-manifest、runtime/source contact-sheet 文件 SHA-256 和字节数，均相符；view-manifest 的 GLB hash 等于 QA scope 的 GLB pin。
- 四个 Blender 4.3.2 只读重开结果：Kootenayscolex 4 个 mesh / 6,299 vertices；Dillhoffia 2 / 1,584；beach-ridge 1 / 2,389；Phycodes 2 / 6,287。导出记录 source 与 GLB 三角数匹配、轴换算 bounds 匹配、无错误。最大 bounds 偏差分别低于 `4.5e-8 m`。Kootenayscolex、Dillhoffia、Phycodes 的 source-export 报告有 smooth-face style review 提示；这些已在对应 clay、八视角及精确 GLB 运行像素中复核，属于柔和有机表面的有意处理，没有导致结构消失或破碎高光。Beach ridge 无该提示。
- 每件已有的两次实际语义重建都记录 `byte_match=true`、`semantic_match=true`，输出 GLB SHA 等于冻结交付 SHA。每个精确 GLB 的 Khronos 报告均为 0 errors / 0 warnings。本轮复核记录和逐次重建输出路径见 `review.json`，没有重复跑已可信的重建与 validator。
- runtime 固定像素来自 Chromium + Three.js `0.180.0`、ANGLE SwiftShader **software WebGL**。这是软件渲染器，不作为硬件 GPU 或实机性能依据。

## 保留状态与证据路径

候选 JSON 中正式 stage 仍是 `unknown`、approval 仍 pending；此独立 PASS 不改写候选阶段或批准，也不替代正式发布门禁。本分支仅增加本报告的 Markdown 和 machine-readable JSON，不更改模型、阈值、CI、权限或发布文件。

各件精确的 brief 与冻结 references 在 `production/continuous-small-life-round15-20261018/items/<asset-id>/{brief.json,references.json}`；制作、source-export、profile、Khronos 摘要、runtime 与重建记录在 `production/continuous-small-life-round15-20261018/work/batch-43/<asset-id>/r001/`；确切 Blend、GLB、view manifest、八张 source 固定视图、十张单件运行视图、两张场景视图及 contact sheets 位于 [candidate asset directory](../../../../assets/candidates/continuous-small-life-round15-20261018/batch-43/)。机器报告列出每项的具体文件路径和对应 hash。
