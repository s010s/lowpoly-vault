# r20 GPU / scene 独立复核：范围通过，动态证据仍有一个小缺口

只读审查运行分支 `render/conifer-r20-runtime-20261017` 固定 commit **`c92f41539448758817635d0e8b5a4701e12fdfe2`**，路径为旁边 `asset-refinements/qa/conifer-r20-runtime-20261017/`。

输入候选固定 commit `265b47eed899307228d609355cc46c6d6992f61d`，revision `structure-r20-A-normal16`，GLB `c3a215eda3ceb3e4ec95bdb31446e180fd9f9d1f7eaa24131459a0db6fa56b40`。原brief `50466e78d5da46f10532b601cc2d4ea15ef2fae44c2881a8b8e0e01c15e99a5e`，references `6f1ff6cb8fa57c8aec580945eaa04ee141240988cfbdc90b075007d8d9afbe4a`。

## 门禁结论

- **GPU实际加载/着色/背面正确性：pass within observed contexts。** 已有Apple M5 Pro/ANGLE Metal真实硬件报告与SwiftShader软件路径各自成功画面；不把SwiftShader称物理GPU。当前A细针造型未因SHORT法线在目标渲染器中回退。
- **M5 Pro/Metal固定场景采样性能与场景布置：pass，明确限定本次1200×900/DPR1、无阴影、完整林组自适应取景、1/16/32独立clone。** 六种clone/instance样本均低于16.7ms，实例化结果附加记录而不替代clone基线。
- **SwiftShader性能：fail，保留失败。** 16/32棵远超预算；严格按冻结16.7ms阈值，单棵rAF p95=16.8/16.9ms也不算通过。加载正确性通过与性能失败可以同时成立。
- **细叶连续运动/缩放质量：unknown，尚不能签“全交互无闪烁”。** 12帧/尺度的42°–44.2°离散微转动不是只有固定视图，但覆盖有限，没有连续rAF时序和缩放穿越证据。可认可已看局部微转动没有整束大块跳失，不能从静止byte-stable推导整个可用相机范围的动态稳定。
- 因最后一项，本报告**不签完整无条件gpu/scene最终通过或总candidate通过**。无需返工模型；最小补证见下。已有固定场景性能无需因此重复全部跑一遍。

## 实际检查与图像

独立读取README、两个runtime-report、producer gpu/scene报告、probe原代码、supplemental diagnostics代码/执行记录、输入与图像清单。没有再次运行浏览器、Blender或探针，也未修改运行分支或候选；只写当前QA目录。

- `SHA256SUMS.json` **180个文件逐一独立核对，0 mismatch**；输入GLB/brief/references身份与上面的冻结subject吻合。
- 从raw arrays独立重算各场景p95（nearest rank）、max、样本数和disjoint标记；未用`gl.finish` CPU返回时间作为GPU或帧率证明。
- 实际打开两个profile全部 **12张scene**（1/16/32 × clones/instanced）、全部 **8张diagnostics**（under/high、正反branch detail）、4张512px normal对照（132°、r19/r20各一）、4张alpha原帧（各profile frame000/012）、**30张原始motion PNG**（各profile全部12张128px，512px分别00/05/11），以及两张24帧联系表和四张motion样本条，共64个原始证据文件。没有声称逐张打开全部48张768px发布帧或48张motion原图。
- 另外独立Pillow解码两套 **48张WebP**，核对尺寸、hash、透明/实心/部分透明像素数与manifest一致；poster字节等于frame0。
- 对两个profile、128/512、42/132/222°共 **12组r19/r20 RGBA对照**独立重新计算差异，结果与producer一致。三组512px在Metal改变7/9/10像素，SwiftShader改变3/11/12像素；最大通道差≤4。个别128px对照可能完全相同，整体不是数学无损或所有图像相同。

画面证据：clone场景中根部与网格地面接触，树高保持约7.04m的原始米尺度，1/16/32棵一致，未见缺失个体或材料替换。16/32全景里细针较淡，是A与投影尺度的表现，不以缺少B连面块否决；没有看到新硬叶壳、绿色管或大面积背面缺失。正反branch detail显示窄叶沿细轴排列，木质接合与冻结造型一致；under/high证据能看见薄叶两侧。GPU颜色比CPU诊断更亮，属于此次实际renderer/preset的结果，不声称跨渲染器全像素一致。

WebP在通用透明图查看器中一度呈现方块状灰色，已通过独立解码并合成至深灰/浅底排除文件缺陷，派生诊断图 `metal-frame000-dark.png`、`metal-frame000-light.png`、`swiftshader-frame000-dark.png` 已实际打开：透明边缘与细针正常。该现象不列为模型/预览失败。

## 原始采样复核

Metal六例：每例60个有效elapsed timer样本、30个rAF间隔，disjoint=false。所有Metal rAF单样本也低于16.7ms，最大10.3ms。

| copies / mode | 实测calls | 实测triangles | Metal GPU p95 ms | Metal rAF p95 ms | SwiftShader rAF p95 ms |
|---|---:|---:|---:|---:|---:|
| 1 clones | 5 | 19,054 | 2.392374 | 8.9 | 16.8（fail） |
| 1 instanced | 5 | 19,054 | 2.374625 | 9.1 | 16.9（fail） |
| 16 clones | 50 | 304,834 | 0.624375 | 9.6 | 133.4（fail） |
| 16 instanced | 5 | 304,834 | 1.412583 | 9.6 | 133.4（fail） |
| 32 clones | 98 | 609,666 | 0.433124 | 9.5 | 259.7（fail） |
| 32 instanced | 5 | 609,666 | 0.900708 | 9.7 | 266.5（fail） |

两项reference drawables是floor/grid，floor多2三角形；单独网站ModelStage测量为3calls /19,052tri。可见clone数分别为1/16/32，与记录一致。Instancing仅减少提交calls，不保证更低GPU耗时。

多棵Metal GPU耗时低于单棵不是“更多树更快”的普遍结论：每组相机重新适配完整林组、单树屏幕投影与覆盖量变化，不能把不同取景的GPU值作线性扩展规律。该测试不证明近距离32棵、阴影、多种植被混合、其他设备或长时热负载性能。

**producer文案需要准确保留的一个采样细节：** README说每例60个non-disjoint query样本，但SwiftShader的16/32棵四例实际仅各10个GPU query结果，30个rAF仍完整。Metal六例确为60。原代码查询等待有10秒截止，只收集截止前available的query；证据不能写“全部场景60个有效GPU样本”。SwiftShader32例原始rAF还保留约10,124.6ms /10,091.3ms的最大间隔，p95不能掩盖这些异常长间隔。它们不改变已明确失败的软件性能结论，无需为得出失败而重跑。

probe确实在rAF回调里渲染静态相机场景；这与motion目录中单次setView/toDataURL的离散帧是两套过程。不能把静态相机的rAF性能样本当作运动时序捕获。shader/console/page错误记录为空，双导入Three同版本warning和SwiftShader readPixels stall有保留；未把warning清空冒充无日志。图片证明shader实际画出，但不额外声称已采集全部program编译内部诊断。

本轮producer使用isolated headless Chromium141，Metal设备是驱动返回值，并非同等于headed交互测试；本审查只读这些既有结果，没有启动该浏览器。后续补录应使用工作区允许的headed/in-app路径，不能因此启动被禁止的headless浏览器。

## 最小动态补证，仅一次受限补录

现有证据已足够证明加载和静态场景采样性能，不需要为凑“全通过”改变标准或模型。只缺一段代表性交互连续记录：

1. 同一GLB、Three0.180.0/preset和Metal设备，保留相机/显示尺寸信息，用实际rAF绘制并按顺序记录时间戳；做约5–8秒缓慢20–30°orbit，加一次从全树到声明近景范围再返回的缩放。覆盖128px和512px使用尺度，可在一段或两段短录制中完成。
2. 看是否只有细针正常的亚像素边缘变化，还是出现整束突失、反复大片明暗跳变、显著摩尔纹/持续闪烁。当前12帧微转动没有证明后一类缺陷，也没有充分排除更宽角度/缩放中的问题。不要预先要求“任何单像素都不变化”。
3. 提交短视频或带真实时序/相机轨迹的连续帧与hash，独立看过后关闭动态unknown；若没有可见结构/稳定性问题，可保留轻微边缘采样作为明确限制。此处没有要求新增LOD或重做细针、重跑六场景计时。

## 规格、身份与发布剩余项

- 前述S1–S4四项文档修复尚未在此次固定265b47e对象中复核；maker新检查点完成后，需核对GLB/source/图片不变和brief/reference/metadata绑定。不能把运行证据旧brief hash静默换成新hash。
- 运行报告只支持明确的 **M5 Pro/Metal sampled profile pass**，并保留SwiftShader软件预算失败，不能写成无设备范围的“性能pass”或删掉failed software evidence。固定brief此前gpu_device为pending，本次填入实际设备范围不等于把原16.7ms改低；目标不变。若发布另行承诺软件/低端设备达标，该新增承诺当前不满足。
- 冻结ID **`structure-r20-A-normal16`** 与发布小写路由冲突真实存在：旁边运行分支的 `site/refined-release.mjs` 第106行要求小写安全slug、第133行要求accepted candidate revision与发布revision精确相同；`site/turntable-delivery.mjs` 第20行也要求小写。不能简单在release JSON中lowercase后称通过，不能改原冻结证据ID。
- 由父任务选择并记录可追溯方案：创建明确supersedes原ID的全新小写“包装/发布revision”，证明同一GLB/source且按受影响范围重新绑定文档/预览和接受记录；或者明确设计、审查并测试区分candidate identity与release slug的映射机制。**当前gate不支持直接加alias绕过**，本审查未改gate或命名。
- 动态补证、四文档修复复核及身份处理完成后才组装七stage最终记录和`--require-approved`。48预览已做独立解码但未逐张完成发布视觉批准；选定其中一个renderer profile后，还需完整发布预览/元数据/站点集成检查与单独发布授权。不得混用Metal/SwiftShader帧且宣称一个可复现profile。

无新的模型修复要求；当前最小阻塞是动态补证、文档/identity可追溯闭合和最终记录/发布检查。原始GPU/scene有效证据不必丢弃或无限重跑。
