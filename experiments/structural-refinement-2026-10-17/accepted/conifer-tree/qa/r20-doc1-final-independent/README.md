# doc1 最终独立接受记录

**`structure-r20-a-normal16-doc1` 已在冻结brief及下述明确设备范围内通过七门禁独立验收。不是全设备性能通过，不是发布授权。**

受审文档提交 `062be906210f34f206748a313e288934a52a2c4f`；GLB SHA-256 `c3a215eda3ceb3e4ec95bdb31446e180fd9f9d1f7eaa24131459a0db6fa56b40`；blend `04c20d19354455e57bbc70a8cced6308d9020e02ff057996bfde7c585a7acbef`；brief `092af4c3259156cd4a8a357df6e0151a1ec08fdd53fd7a351d162a6ed7561031`；references `18062b9ea882d531834240554f764a8a0818b83efd5e6f8afde2bbb77326119a`。

机器记录：`candidate.independent.json`，与maker的候选文件分开；七份 `*.report.json` 记录各自方法、范围、警告与subject。旧QA、candidate-r20及doc1候选均未修改。`assemble.py`只在本目录创建独立记录与必要证据副本，不重写冻结输入。

## 最后动态判定

新增运行证据固定提交 `b3107dc7a5e04c2fd1cb0031ebb1bdb4f8cdfc17`，基于原实测 `c92f41539448758817635d0e8b5a4701e12fdfe2`。录像保留原始身份并以相同GLB与doc1已审映射复用；没有把旧执行日期/subject改写成新运行。

我实际用ffmpeg独立解码原始 `orbit-zoom.webm`，并用ffprobe核对409个单调PTS；核对视频/trace SHA，trace有821次真实draw。按时间顺序查看全部409帧的11张联系页，另打开19张768px实际解码原帧，其中199–204为连续近景帧。**这是实际解码/抽帧核查，不冒称实时播放观看或逐张全分辨率查看409张。** 视频原件和来源记录在 `support/motion/`；独立样本、顺序联系页和逐帧统计保存在support。

记录wall时长7003.8ms（约7.004秒），视频PTS从0到6.965秒，409帧不等于821次绘制。首段最大PTS间隔195ms，录像有编码/采样间隔变化，不能用本视频宣称无丢帧或60fps性能通过；帧预算仍依据原始场景采样。独立全帧前景检测范围25,133–126,941像素，0个全背景/空帧。轨道实际42.0206°→402°，zoom scale约0.45→1.1，覆盖全树与近景后返回；最近处画面裁切树顶/根部是相机缩放构图，不是模型突然消失。

**动态质量通过，带明确aliasing边界。** 全段顺序图及近景连续样本中，枝轴与整束叶片沿相机运动连续，没有整束突失/闪回、明显法线反转或大片明暗闪烁。细针在远处、斜侧和交叠区域可见像素级点线强弱变化、细碎边缘跳动及VP9软化；这正是薄小几何的亚像素采样限制，当前程度没有破坏用户选择A的轮廓、枝叶层级或近景使用。结论不承诺零aliasing，也不证明所有DPR、光照、相机速度及未测设备稳定。原128/512小角度证据与本768px连续orbit/zoom互补，原来的动态unknown可关闭，不需修改叶型或反复追加测试。

## 七门禁范围

| stage | 通过范围 |
|---|---|
| technical | 精确模型/预算/法线误差、独立validator、已核对的source/export与hash-bound重建输出；不伪称本审查又执行了一次Blender |
| visual | 用户A：分离细针、轻透羽状、自然天窗；53张CPU全方向诊断与目标GPU/动态证据，无粗管/宽硬片回退 |
| factual | 通用风格化针叶树概念，现代结构类比；7m、叶数、冠层位置/配色为艺术概括，非命名物种/年代/地区精确复原 |
| specification | 六项交付物、53图覆盖、尺寸/上限、S1–S4修复、小写doc1及显式证据复用映射均满足；没有放宽16.7ms目标 |
| runtime_parse | Three.js0.180.0，required KHR_mesh_quantization，三组normalized Int16Array法线，无外部decoder |
| gpu | 实际Metal/WebGL2加载/着色、正反/上下视图及连续运动通过；保留细针aliasing，非普遍无闪烁保证 |
| scene | **仅Apple M5 Pro/ANGLE Metal、Chromium141、DPR1、1200×900、无阴影、全林组适配取景、1/16/32 independent clones**的记录条件满足16.7ms；instanced仅补充对比 |

Metal六例rAF p95为8.9–9.7ms；clone calls5/50/98含floor/grid，单体网站渲染3calls/19,052tri。没有将三角算术或CPU gl.finish时间写成实测GPU时间。

**SwiftShader不接受为性能通过profile：** 单棵p95=16.8/16.9ms也超过严格16.7ms；16/32棵为133.4–266.5ms。软件正确性成功不消除性能失败。新README已纠正有效query数，原raw arrays未改：Metal每例60，SwiftShader单棵60、16/32棵各10有效query。原软件32棵的约10秒最大rAF间隔也保留。以上失败是已观察限制，不得在后续发布文案中隐藏或改成全设备pass；若另行要求SwiftShader/低端设备满足同一目标，该额外用途当前不通过。

## 验证与检查点

独立记录按conifer-tree作为bundle root验证：

    python3 scripts/validate_candidate.py qa/r20-doc1-final-independent/candidate.independent.json --root experiments/structural-refinement-2026-10-17/conifer-tree --json
    python3 scripts/validate_candidate.py qa/r20-doc1-final-independent/candidate.independent.json --root experiments/structural-refinement-2026-10-17/conifer-tree --previous candidate-r20-a-normal16-doc1/candidate.json --require-approved --json

输出分别保存在 `integrity-result.json`、`require-approved-result.json`。检查不会自动证明艺术或科学真伪；这些判定来自上文实际独立审查，机器检查负责哈希/范围/记录完整性。接受记录独立reviewer与maker身份不同。

## 仍需发布阶段完成

无新增模型或QA阻塞。发布仍需独立授权；选定一个renderer profile后完成整套24alpha发布视觉批准、poster/manifest的doc1身份与正式路由绑定、release metadata、站点集成与最新main检查。当前CPU诊断metadata不是发布预览；Metal与SwiftShader序列不可混为一个可复现profile。本次只保存独立QA检查点，不改main、不集成、不发布。
