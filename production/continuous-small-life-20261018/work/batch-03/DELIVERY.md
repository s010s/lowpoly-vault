# 首轮批次 03 候选交付

基底 main `643534830397824dfd46990485bd16ad66ecf9ce`，规划输入 `ac44f7de4082fde7fada3adc0324882b80fb2bb1`。当前用户委派已明确确认 CI 完成并独占分配本批，覆盖规划快照中的旧 blocked 状态。父任务负责共享 state/events 原子更新，本分支仅提供批次结果。

分支：`candidate/small-life-batch-03-20261018`。四项均有单独正常 push checkpoint，完整 SHA 见 `result.json`。最终评审身份以最终提交中的 `freeze.json` 与 `result.json` 为准；Onoclea 当前为 r002。

| ID | revision | GLB bytes | triangles | authored/evaluated vertices | exported POSITION vertices | materials/primitives |
|---|---|---:|---:|---:|---:|---:|
| cephalaspis | r001 | 67,700 | 2,998 | 1,535 / 1,535 | 1,699 | 4 / 11 |
| saccocoma | r001 | 219,228 | 9,436 | 5,310 / 5,310 | 6,540 | 3 / 6 |
| archaeocidaris | r001 | 209,288 | 10,680 | 5,562 / 5,562 | 5,782 | 4 / 7 |
| onoclea | r002 | 260,148 | 12,776 | 6,736 / 6,736 | 7,336 | 5 / 8 |

每项均交付可编辑 `.blend`、独立 GLB、可重建 Python、原始配置与执行补充、中英 metadata/来源/不确定性、透明封面、八个精确 GLB 渲染视图、浏览器多角度与正常/近景截图、九实例场景、源重开与两次重建报告。无贴图，解码贴图内存估算为 0；不凑面数或贴图体积。场景尺寸均为米，原点与根节点经过实测，预览相机和灯光未导出。

格式、静态几何、预算、源/导出、两次重建、锁定 Three.js 载入、软件 WebGL2、九实例场景及当前证据完整性检查通过。所有 Khronos 检查为 0 errors / 0 warnings，两次重建均 GLB 字节一致。`qa/continuous-small-life-20261018/batch-03/bundle-validation.json` 提供机器可读结果。

请按 [QA-REQUEST.md](QA-REQUEST.md) 由父任务派发全新 GPT-6 Luna xhigh 独立 QA。当前独立美术/基础形态/规格验收均 pending，不冒充外部 PASS；未合并、未发布。软件 SwiftShader 证据不代表物理 GPU 或真实设备帧率。外部参考图的 shell 下载受 HTTP403 限制，实际 web 访问方式与未重新核对部分已如实记录；未收录任何第三方媒体。
