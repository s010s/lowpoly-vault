# Batch 48 独立模型 QA — continuous-small-life round 16

- Reviewer: Leon Made This <8357465+s010s@users.noreply.github.com>
- 结论：**四件均 PASS（仅针对冻结的风格化教学 brief）；必修项：无。**
- 候选 handoff commit：`04a4bee524379fa0022bbfc7133fa9640bfa6fdc`。
- Maker model source commit：`cab25e85d03a742b4eaea3b01a4c691363d92613`，与 `QA-HANDOFF-SCOPE.json` 的 source pin 一致。报告分支以 handoff commit 为父提交。
- handoff 与 scope 文件 SHA256、四件 candidate checkpoint、交付 GLB/Blend、source export、rebuild record、固定视图和运行像素证据均已复核。逐项哈希与结果见 [`results.json`](results.json)、[`verification-summary.json`](evidence/verification-summary.json)、[`source-fixed-view-hashes.json`](evidence/source-fixed-view-hashes.json)、[`runtime-pixel-hashes.json`](evidence/runtime-pixel-hashes.json) 和 [`source-export-and-rebuild.json`](evidence/source-export-and-rebuild.json)。

## 逐件判定

| Asset ID | 判定 | 三角面 | 精确 GLB SHA256 | 视觉观察 |
|---|---|---:|---|---|
| `facivermis` | **PASS** | 8,636 | `4f0f5c232ae02717a1a1b160b9a9639539e5d07ec26f454621170206d16abd54` | 五对前部成对附肢与刺列能从多方向区分，主躯干保持长而裸露，后部膨大清楚；头部与附着点刻画克制。 |
| `cave-pearl-pool` | **PASS** | 4,096 | `251ccacbf304eb285233f8f1122436a4a7ba09c83fa97b43379bdd0b38d66abb` | 浅矿物杯的真实凹面和八个分离、不等尺寸圆结核在顶视及斜视可读；呈矿物展示道具，不暗示蛋巢。 |
| `lava-tree-mold-crust` | **PASS** | 4,352 | `5e48537aaaf7e26323d26f76c5fef29bbb35c0191df511f5cd8238be98222258` | 连续外壳与树干形负空间的口沿可读；近侧口沿在常规英雄视图遮挡腔深。精确 GLB 的中性剖切诊断显示深盲腔、内衬与壁面起伏。 |
| `treptichnus-serial-probe-burrow` | **PASS** | 11,712 | `ad906a4701463c1b9b313e0629a7abbc34142cf37ab7aca2281eab3f8a6af734` | 纵向切开沉积块中的连续凹槽在英雄/正视可读，呈主走向加串联 J 形探槽；顶部作为切面板的轮廓视图不承载识别，不影响核心结构。 |

每件模型的 source 固定视图为 `hero/reversehero/front/side/rear/top/clay/silhouette` 共 8 张，零 turntable；清单中 8 张 source 帧 SHA 已逐张对照候选 commit 重算。每件精确 GLB 的运行证据有 10 个单件视图和 2 个场景视图，所有运行 JSON 均为 `pass`、错误和失败请求为空，运行图 SHA 与 manifest 相符。接触表可在 [`evidence/contact-sheets/`](evidence/contact-sheets/) 查看。

## 技术与来源证据

四个 Khronos glTF Validator 报告均为 0 errors / 0 warnings。冻结的 source-export 记录均 `pass_with_warnings`、无 errors，source 与 GLB 三角数一致，边界最大偏差为 0 至 `2.33e-10 m`；警告为平滑面是否符合预期风格，已结合灰模、固定视图和运行像素检查。每件保存的两次实际重建均报告 GLB 字节和语义摘要与交付 GLB 相同。这里复核了原始报告哈希与其具体摘要；按用户要求未再运行完整制作检查器或重复重建。

运行像素来自 Chromium / Three.js 0.180.0 / ANGLE SwiftShader **software WebGL2**。这证明软件 WebGL 路径加载与像素输出正常；**没有测实体 GPU 或硬件性能**。正式 `static-stylized-v1 / 2026-10-18.1` 记录为 contract pass、record valid，但 `approved_for_brief=false`，各正式阶段仍为 unknown、approval pending。legacy gate 对空 consulted-only license 文本报错的原状态保留，不猜许可、不改候选记录。

## 范围边界

本轮审核自然、儿童场景友好的静态低模教学道具，不要求标本级科研复原。四件均按已声明的 inspiration/process/trace-concept 范围呈现；报告不证明准确物种、洞穴年代、古熔岩地点、造迹生物或形成机制。没有发现必要模型修复。此报告不改变正式审批，不授予发布权，不执行 merge 或发布。
