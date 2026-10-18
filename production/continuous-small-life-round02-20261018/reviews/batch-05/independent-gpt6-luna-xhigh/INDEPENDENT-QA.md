# Batch 05 独立 QA

**资产级结论：四项均 PASS；没有必须返工项。** 依据冻结的 `stylized-inspired` low-poly brief 判定，不作为严格物种复原背书。

- 审核源提交：`e968fab0544ce2dc41814c057b1f9dca43a2b22d`
- 源分支：`candidate/small-life-batch05-20261018`
- 审核分支：`qa/s010s/small-life-batch05-20261018`
- 审核模型：GPT-6 Luna xhigh；制作模型：GPT-6.1 Sol medium
- 联系表：[batch05-independent-qa-contact-sheet.jpg](batch05-independent-qa-contact-sheet.jpg)
- 联系表 SHA-256：`b61c7e50e89fd7cdbe7b1e8b7bd0c0b00ade80b5d02af2712b97f7fabbcfa31d`

## 逐项结果

| Asset | 结论 | GLB / triangles | candidate.json SHA-256 | GLB SHA-256 | Blend SHA-256 |
|---|---|---:|---|---|---|
| goniophyllum | **PASS** | 103,884 B / 5,326 | `84d4dfaabe9847455102b651d28355eab0eb4fec2daf5a7a812026b4c9cb212c` | `8f0caa08c7ac6062a68b9bfae0c7b43f8c1c919b641b7e6122fae45895972ced` | `4ed24b09e6323a04d3e3eeed3fa8ef077294249014ede95154567b515a9b5e06` |
| halysites | **PASS** | 195,220 B / 8,464 | `ff69754403fc118c23f388cfd39c224af040d2c09218915bfffb94f325b3710a` | `451a6f8e7b5f2f93c4b3108ffbf5a17cf1d1486f86b4021ee3252be0e97541ca` | `4c332648b2a299e6124948f02d589d7d9af69c01607b792cd69c8061d724c0fb` |
| marrella | **PASS** | 210,020 B / 9,948 | `189370bd57ed63152e44adbea2a23630e9b8cbc211fd6e96e443d4b776c6c2ae` | `6e6d1413149625a566b4affb144f1e1ff8713c97e1fdee53e6a2e408403e6742` | `fb8f31343cd6d43a8ec0e31298bb61b6a7d820fd6bbca495e56cf7619aeb6fc0` |
| proteroctopus | **PASS** | 180,608 B / 9,896 | `42bfa2f115d06b27893d71148f0d96eaf331823c4f584eacf3eab393a4a74d7b` | `e264e3f341ae7d9745760c4dec7c7cfc5697df2059fc9daa38d99619bd23c18b` | `fa426d4d3208c7a5b5ea768d11ce8dd6d33825c294d88878b062c834dd8be50c` |

### goniophyllum — PASS

- **必修问题：** 无。
- **非阻塞建议：** 无需改模。方锥杯体与四片盖瓣在 top、hero 和 80–240px 视图保持可读。四盖数量来自 brief 的设计要求；公开摘要能支持 Goniophyllum 的锥形形态与 opercula，不能单独证明恰为四片。[Gudo, “Structural–functional Aspects in the Evolution of Operculate Corals”](https://onlinelibrary.wiley.com/doi/abs/10.1111/1475-4983.00254)

### halysites — PASS

- **必修问题：** 无。
- **非阻塞建议：** 无需改模。顶视清楚呈现开放的管壁链环，不像实心蜂巢；连接连续，80–240px 仍读作链珊瑚。环数与配色属于原创艺术选择。[Digital Atlas of Ancient Life, Tabulate Corals](https://www.digitalatlasofancientlife.org/vc/cnidaria/anthozoa/tabulata/)

### marrella — PASS

- **必修问题：** 无。
- **非阻塞建议：** 无需改模。楔形头盾、两组明显后伸的头部棘、分节躯干与附肢流苏在多角度和 80–240px 下均成立；纤细附肢按目标比例简化合理。[Royal Ontario Museum, Marrella splendens](https://burgess-shale.rom.on.ca/fossils/marrella-splendens/)

### proteroctopus — PASS

- **必修问题：** 无。
- **非阻塞建议：** 无需改模。短圆外套膜、成对鳍和八条臂的教学道具轮廓成立；表情与材质偏友好卡通，但仍符合已接受的自然低模风格。建议继续使用 inspired-by 标签；研究支持两鳍和八臂，同时明确其系统位置仍不确定。[Kruta et al. (2016)](https://onlinelibrary.wiley.com/doi/10.1111/pala.12265)

## 独立核验

我没有把 maker 的 PASS 当作证据。`audit_hashes.py` 复算四份 candidate、GLB、blend、37 项 checksums、manifest 与图片哈希；每项 20 张源图/运行时图及两张联系图记录均匹配。绑定当前 GLB 的 Khronos 报告均为 0 errors / 0 warnings；Three.js r180 / Chromium SwiftShader WebGL2 的 exact-GLB 运行报告与九件场景均为 pass。

`audit_meshes.py` 用 Blender 4.3.2 打开源 `.blend` 的 `EXPORT` 集合并导入同一精确 GLB：三角数和以 `1e-7 m` 比较的位置集合一致，无零面积面、低于 `1e-14 m²` 的面或焊合后的边界/非流形边。Urasterella 的 GLB 有 1,680 条 raw boundary edges，是 glTF 顶点/法线拆分；位置按 `1e-8 m` 焊合后边界为 0，源 mesh 本身也闭合。它不是可见裂缝。

Proteroctopus 的 `.blend` 还包含 EXPORT 外的编辑构造集合。第一次全场景计数因此比 GLB 多；按 handoff/源 QA 指定的 `EXPORT` 集合复算后，3 个网格、9,896 triangles、5,030 个唯一位置与 GLB 一致。这是审计范围修正，不是资产差异或修复。

视觉检查覆盖 source 的八张固定图，以及精确 GLB 的 hero、reverse、front、side、rear、top、bottom、80/160/240px 图、六件场景和联系表。四项在预期尺度均有可识别轮廓，适度近看未见明显穿插、缺面或断开。GLB 文件小于 100KB 本身不作缺陷；本批 GLB 均低于 211KB、14k 三角形预算，零纹理，符合冻结合同。

## 门槛与参考图限制

- `scripts/validate_candidate.py` 的旧 profile 最少要求 2 帧 turntable，production 视图集要求 9 个视角；当前 brief 冻结为 8 张固定视图和 `turntable_frames: 0`。因此旧 gate 不能代表当前批次合同，本 QA 没有补造 turntable 或改全局阈值。
- Batch-local 小面积阈值较旧共享 checker 宽，但没有遮住此批退化面：四个 exact GLB 的最小三角面积分别为 `4.7155e-9`、`1.4715e-6`、`9.62435e-10`、`1.13786e-8 m²`，均为新阈值 `1e-14 m²` 的至少 96,000 倍。零面积及 welded topology 另行独立复算。
- `actual-reference-access.json` 记录了一些外部参考图片或 Sketchfab 页面因 403 无法取图。我只使用可访问的文字来源核对 brief 声明的基础形态，没有声称查看过被阻断图片像素，也未复制来源媒体、网格、材质或纹理。颜色、比例、姿势与细部的精确古生物学不在本 PASS 声明内。
- `legacy-gate.json` 每项实际 `FAIL` 的记录错误是参考 ledger 缺少旧 schema 强制的 `license` 字段；`references.json` 将其标为 consulted-only，本项目策略明确事实咨询不要求给被复制素材授权，而本批没有导入第三方素材。旧 gate 还与零 turntable/fixed-eight profile 不兼容。该 pipeline/schema 对接交给父任务，不是资产必修问题。未填造 license，未改 CI、权限或模型。

## 实际执行命令

从仓库根目录 `/tmp/batch05-qa` 执行：

```sh
python production/continuous-small-life-round02-20261018/reviews/batch-05/independent-gpt6-luna-xhigh/audit_hashes.py
blender --background --python production/continuous-small-life-round02-20261018/reviews/batch-05/independent-gpt6-luna-xhigh/audit_meshes.py
python production/continuous-small-life-round02-20261018/reviews/batch-05/independent-gpt6-luna-xhigh/build_contact_sheet.py
```

机器输出见 [hash-audit.txt](hash-audit.txt) 与 [mesh-audit.txt](mesh-audit.txt)。报告与联系表只在独立 QA 分支；模型、主分支、CI、权限和发布文件均未改动，未上传 Drive。
