# 两件地质校准候选：独立 QA（一次）

**结论：适合继续给用户作 A/B 比较；本报告不批准生产换基准。** 本次仅审阅砂岩与烟囱两件候选，未改动模型、渲染、门禁或生产资产，也未合并、发布或上线。

审阅对象固定为实验源提交 `1692a5ab57b996c382fa8ed8b1bd182bd1682a92`（`experiment/two-geology-calibration-20261019`）。对比基准为生产 175 件提交 `de413ef720463a2999516faf92c606bcdf9ab1b7`。以下判断来自候选仓库内的真实 GLB 渲染；没有查看到任何外部实物照片像素，因此不对地质真实性作照片验证结论。

## 视觉判断

| 候选 | 看得见的改善 | 尚存限制 | 本轮判断 |
|---|---|---|---|
| cross-bedded-sandstone | 不规则碎块轮廓明显减轻了原来直角板材感；hero/front 仍能从斜向色带读出层理，轮廓厚度也更像一块自然碎落的岩石。 | 层理的可读性主要靠材质色带。对照 clay/front/back，新的斜层截切几何很浅且不连贯；240px 单件图与小场景里层理进一步变弱。灰模读起来更像有色面刻出的圆角块，而不是几何上明确的交错层。故“减轻板材感”通过，“保留足够强的几何层理截切”仅部分通过。 | 可供用户比较，不能称为无条件优于原版。若用户要求层理在灰模或缩略图中也清楚可辨，这一项不满足该门槛。 |
| hydrothermal-chimney | 原版明显等厚、近周期水平色带被打散为沿高度及周向变化的沉积色区；烟囱仍有宽底、较窄颈部和可见顶端开口，整体体量保留。 | 色区边界依然硬，浅赭色有几处方块状/竖向贴片；240px 图上块边仍明显。周期环带改善成立，但外观仍偏低多边形贴色，不等于自然照片级沉积。 | 主要目标达到，残留硬边是风格权衡，可直接给用户判断是否接受。 |

`comparison.jpg` 汇总图和关键视图：砂岩 [comparison](../../experiments/geology-calibration-20261019/cross-bedded-sandstone/comparison.jpg)、[front](../../experiments/geology-calibration-20261019/cross-bedded-sandstone/views/after-front.png)、[clay](../../experiments/geology-calibration-20261019/cross-bedded-sandstone/views/after-clay.png)、[240px 单件](../../experiments/geology-calibration-20261019/cross-bedded-sandstone/views/after-thumbnail-240.png)、[240px 小场景](../../experiments/geology-calibration-20261019/cross-bedded-sandstone/views/after-thumbnail-scene-240.png)；烟囱 [comparison](../../experiments/geology-calibration-20261019/hydrothermal-chimney/comparison.jpg)、[front](../../experiments/geology-calibration-20261019/hydrothermal-chimney/views/after-front.png)、[back](../../experiments/geology-calibration-20261019/hydrothermal-chimney/views/after-back.png)、[clay](../../experiments/geology-calibration-20261019/hydrothermal-chimney/views/after-clay.png)、[240px 单件](../../experiments/geology-calibration-20261019/hydrothermal-chimney/views/after-thumbnail-240.png)、[240px 小场景](../../experiments/geology-calibration-20261019/hydrothermal-chimney/views/after-thumbnail-scene-240.png)。

## 来源与公平性核验

- 两件 before 文件哈希分别为 `1a93b06b2a9a3457f0f11bff876328dc50b5d8c2f3a7a730fe411ebc200b3ac1` 与 `247577c08bfcfb0f35bf11704dd05e967c10e73789557a60f6ad2394fa00aa96`；直接从生产提交 `de413ef` 的对应 GLB blob 读取并重算，均与实验指标和渲染清单相符。因此 before 确为生产 GLB，不是重新建模的代用品。
- 每件 8 组逐视图 before/after（hero、front、back、clay、top、side、reversehero、240px 单件）均在清单中匹配相同相机、目标点、正交尺度、分辨率、引擎、采样和曝光；另有每件一组真实 240px 三件场景对比。合计核对 18 组。使用同一渲染脚本与灯光；没有按各自包围盒重缩放。
- 实验 after GLB、候选记录、指标、metadata、源 QA 和 runtime 报告中的 after SHA 一致；两次重建报告都记录字节级相同。Khronos glTF Validator 2.0.0-dev.3.10 报告两件均为 0 error、0 warning。GLB 结构检查均通过 14,000 triangles / 1,000,000 B 硬上限。
- 保留成本差异：砂岩 `588 → 2,276` triangles、`34,128 → 133,172` B，primitive `2 → 15`（每个实例基础 draw-call 潜在成本上升明显）；烟囱 `4,032 → 5,760` triangles、`150,088 → 213,240` B，primitive `3 → 4`。大小和三角形数都不是完整设备性能测量。软件 WebGL 运行记录可佐证 GLB 可加载与渲染，但不能证明真实手机 GPU 帧率。烟囱源 QA 保留了一条内壁平滑的风格提示，作为有意设计说明。
- 实验目录 `checksums.sha256` 中 99 个条目有 98 个现存文件逐项校验通过，无现存文件哈希不符；唯一缺项是列表引用了不存在的 `logs/build.log`。它不影响上述 GLB、视图和验证报告的独立哈希交叉核对，但日志本身未能复核。

完整逐文件哈希、生产 Git blob、成对参数检查及缺项记录见 [evidence.json](evidence.json)。原实验包说明外部实物照片下载遇到 HTTP 403，图片通道也只有文本占位符。本次 QA 保持该项为 **unknown**；这不是可据以宣称照片支持的科学考证结果。

## 处置

可以把两份候选与真实生产 before 图一起交给用户选择风格基准；砂岩需要特别提示“轮廓变自然、但几何层理变弱”，烟囱需要提示“减少周期条带、但色块边缘仍硬”。本轮没有足以阻止 A/B 比较的结构或渲染错误，也不据此自动替换任何生产模型。生产基准选择与真实参考照片验证仍未解决。
