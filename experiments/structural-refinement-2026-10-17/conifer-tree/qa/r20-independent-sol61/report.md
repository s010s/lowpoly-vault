# r20 独立审查：A 风格与 NORMAL16 交付方向通过，生产验收仍未闭合

审查日期：2026-10-17。固定 commit：`265b47eed899307228d609355cc46c6d6992f61d`。

候选 GLB SHA-256：`c3a215eda3ceb3e4ec95bdb31446e180fd9f9d1f7eaa24131459a0db6fa56b40`。
对照 r19：`e912444734c357017d3b839c0ba009dfc994d0e57acdb8d1d1a4fe431c0357c8`。

结论：**在已冻结的 CPU 图像范围内，r20 的用户 A 风格视觉通过；NORMAL16 误差与格式/指定加载器兼容性通过独立核查。未发现要求再改造型的阻塞。整体 production / accepted_for_brief 仍不能通过：实际 GPU、1/16/32 independent-clone 组合场景尚未完成，完整 factual/specification 也不由此次有限审查代签。**

用户已经明确选择分离细针、羽状、轻透的 A 风格。本审查接受自然天窗和远景细针变线，不把 B 连面密冠作为隐藏标准；也不把用户选风格解释为所有结构、技术和成本均已批准。r15 历史失败报告不改写。

## 独立方法与只读边界

应用此前已读的仓库 lowpoly-art-direction、asset-factual-review、blender-lowpoly-pipeline 及其 visual-acceptance、asset-budgeting、standardized-pipeline 要求。读取 r20 README、冻结文件、相关技术报告和 cost-analysis-r19；独立编写 `audit.py`，不执行候选的 packing 或 pixel-comparison 脚本来充当独立核查。

- 实际逐张打开 **53 张当前 raw PNG**，另打开 3 张 comparisons 导航/匹配图，共56张。不是仅看联系表。
- 对冻结清单 **118 文件**独立 SHA-256 检查：0 mismatch。
- 独立解包 r19/r20 GLB，比较 POSITION/index 有效字节、accessor 与非存储 JSON，按 glTF signed-normalized 公式解码法线并计算误差。
- 独立用 Pillow 比较16组匹配图像的实际 RGB 像素；未修改或重画图像。
- 使用现有依赖独立重跑 Khronos validator 与固定 Three.js 0.180.0 GLTFLoader；只写本新 QA 目录。未启动浏览器、Blender、渲染或重建进程，未安装依赖。
- 已保存的 maker rebuild/canonical GLB 哈希也独立核对，但**此次没有亲自执行新的 Blender rebuild 或 source/export 检查**。既有报告/过程记录与此次独立执行项分开。
- 未更改候选、已有证据、源模型、Git 分支或发布状态；本目录为新增报告。

## 实际打开的图片清单

路径相对 `candidate-r20/`，53张 raw 的逐图 hash/尺寸保存在 `audit-results.json` 的 `opened_raw_images`。

1. `evidence/full-angle256/turntable-000.png` 至 `turntable-023.png`：全部24帧逐张打开。
2. 同目录另外13张：`hero.png`、`reversehero.png`、`front.png`、`rear.png`、`left.png`、`right.png`、`top.png`、`bottom.png`、`clay.png`、`clayalt.png`、`wire.png`、`detail.png`、`detailclay.png`。
3. `evidence/detail512/` 七张：四张 `hero035/125/215/305.png`、`detail.png`、`detailclay.png`、`clay.png`。
4. `evidence/native128/` 九张：四张 `hero035/125/215/305.png`、`front.png`、`rear.png`、`left.png`、`right.png`、`silhouette.png`。
5. 辅助 comparisons 三张：`r19-r20-hero035.png`、`r19-r20-detailclay.png`、`full-angle256-contact-sheet.png`。未以旧 normal16-probe 代替当前全图集。

## A 风格与全方向可见质量

**visual pass，范围为当前诊断图片及其显示尺度，不包括目标 GPU 动态画面。**

- 四个512px hero与24帧转台均保持单一连续主轴、弯曲主枝、从属细羽状喷束和向上收窄的树形。不同方向有预期的冠层疏密变化，没有发现主干断裂、某一转角主冠整体坍塌或新出现的孤立大叶团。层间空白是选定风格，不作为失败项。
- `detail512/detail.png` 与 `detailclay.png`：原点左上，约 x55–225/y0–125 的弯曲羽束、x305–500/y180–320 的斜向喷束、x210–345/y330–510 的下垂喷束，都能读到沿细轴排列的窄叶片；没有恢复为粗绿色圆管、八片宽硬带或大尖菱片。窄叶局部有折面、端部尖锐，是此次尺度下可接受的低模概括。
- 同近景约 x220–310/y115–180、x220–310/y265–325 的主枝根部保持连续收接。中央下部喷束有交叠，但仍可分辨轴向关系，未见需要返工的明显漂浮大块或破裂。不能用512px图认证每个被遮挡的针叶接点内部拓扑。
- `top.png` / `bottom.png` 保持围绕主轴的侧枝和细喷束；俯仰图与侧图的覆盖差异符合薄叶方向性。底图未见新增宽叶壳或脱离主体的大组件。
- `clayalt.png` 改变主光后仍保留枝根形态和羽状分枝，没有量化引入的大片暗斑、突兀法线接缝或不合理明暗翻转。匹配 hero/灰模对比图肉眼未见实质退化；这个感知结论不等于像素完全相同。
- 原生128px四个hero和四个水平向仍能识别轻透针叶树、主干与侧枝层级，细针大量消退为点线。该尺度不适合承诺逐针细节。线条的运动闪烁、双面叶的视角稳定性和抗锯齿行为，必须由目标 GPU 任务补测。
- cross-asset family / 同场材质一致性不由孤立诊断图证明，留给实际场景。

## 几何与法线：独立数值

三 primitive 的 POSITION 有效字节、POSITION accessor、index 有效字节、index accessor及三角次序全部精确相同；asset/materials/nodes/scenes/scene/meshes JSON 逐项相等。没有位置量化、改变拓扑、材质或变换来换取字节节省。

NORMAL 从 FLOAT32 改为 `componentType=5122`、`type=VEC3`、`normalized=true`；每元素 stride8，起点符合4字节对齐，三流合计29,882法线。

| 独立法线误差 | 结果 |
|---|---:|
| 最大方向角误差 | 0.001443161840° |
| 平均方向角误差 | 0.000660944827° |
| p99（nearest rank） | 0.001227486402° |
| 最大分量绝对差 | 0.000015258560 |
| 解码向量最大单位长度偏差 | 0.000024205792 |

角误差使用向量叉积长度和点积的 atan2 计算，避免极小角度 acos 的数值敏感性。结果与 maker 报告一致。**法线有精度损失，完整文件不能称数学无损。**

## 实际像素差异

独立重新计算16组匹配图的 RGB 差异，与 maker 披露一致。这里只对有匹配 r19 对照的16组作数值比较；新增全角度图经过目视审查，不声称有53组像素相等证明。

| 图像 | 改变像素 | 最大8位通道差 | 结论 |
|---|---:|---:|---|
| native128 silhouette | 0 | 0 | 实际 RGB 像素完全相同，PNG 文件 hash 不同 |
| 四个512px hero | 每张162–206（0.0618–0.0786%） | 3 | 微差，非全像素相等 |
| 512px color detail | 1,125（0.4292%） | 6 | mean abs 0.003512/255 |
| 512px gray detail | 1,177（0.4490%） | 9 | mean abs 0.005535/255，RMSE 0.095143/255 |
| 512px whole clay | 195 | 3 | 微差 |
| 其他八张128px彩图 | 每张5–12 | 2–5 | 微差 |

几何完全相同不推出所有着色像素相同。CPU图差也不能当作其他GPU/光照/阴影设置下的最大差界限。

## glTF 扩展、加载器与技术声明

实际 GLB 同时在 `extensionsUsed`、`extensionsRequired` 声明 `KHR_mesh_quantization`。这是必须支持的扩展，没有 FLOAT 法线回退；不能保证任意 glTF 客户端兼容。

[Khronos KHR_mesh_quantization 规范](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_mesh_quantization/README.md) 的类型表允许归一化 SHORT VEC3 NORMAL，要求顶点元素的4字节对齐，并要求光照计算前归一化向量。此次编码符合已检查的要求。不是 Draco/Meshopt，不新增外部解码器。

独立实际执行结果：

- Khronos `gltf-validator`：**0 errors、0 warnings、0 infos、0 hints**，报告 `validator-independent.json`。
- 固定 Three.js **0.180.0** GLTFLoader：成功 parse，3 mesh primitive；每流都是 normalized、interleaved `Int16Array`，逐元素读取后的XYZ均有限值；没有配置外部解码器。报告 `parse-independent.json`。[固定 r180 loader 源码](https://github.com/mrdoob/three.js/blob/r180/examples/jsm/loaders/GLTFLoader.js) 与实际解析路径一致。
- 实际 parse bounds：min `[-2.3983466625,0,-2.7512788773]`，max `[2.2636053562,7.0421104431,2.4159319401]`；总19,052三角形、29,882 POSITION vertices、3 materials / primitives、0 textures。没有把3 primitives写成 GPU 实测 draw calls。
- 已存独立进程 rebuild 的最终 GLB 与 r20 字节相同；其 canonical FLOAT GLB 与 r19 字节相同。此次仅核对这些已有输出及冻结绑定，**没有重新执行生成器**；source/export 和生成过程仍按已有报告的证据范围采纳，不伪称此次独立 Blender 复跑。

## 成本与收益

r19 834,840 B → r20 **715,500 B**，节省 **119,340 B（14.295%）**；三角形和顶点数量完全不降。这项储存优化保持 A 形态，误差已验证，具有合理收益，可以保留。

独立 buffer审计：POSITION 358,584 B不变；NORMAL含stride从358,584 B降为239,056 B；index114,312 B不变。两文件均无未使用顶点、精确重复的完整position+normal顶点，或 bufferView 未覆盖的BIN字节。故不能假定还有大量无损垃圾可删。此处没有重跑所有 r12/r15分解、Brotli/gzip计时或确认实际 hosting 配置；参考成本报告中相关数字仍是其报告值。

相对原始2,382三角形 /145,732 B，r20约8.00倍三角形、4.91倍字节。512px羽状细节和更合理的木质次级结构有实质收益；128px针叶细节利用率低，是选定A表现的成本取舍，不能再通过无限加叶追求密冠。是否适用于重复场景仍待实测。NORMAL16更小不保证GPU属性分配或帧时同比改善；双面叶、细线闪烁、阴影和多pass仍有成本。

## 门禁和下一步

| 门禁 | 本次结论 |
|---|---|
| 当前冻结完整性、精度比较、格式合法性 | pass（独立执行范围见上） |
| 当前全角度CPU图片中的用户A视觉 | pass；无造型返工要求 |
| 固定Three.js parser / normalized属性路径 | pass；无GPU含义 |
| 既有byte rebuild/canonical输出一致性 | pass（字节核对）；此次未重新生成 |
| 全部source/export/build technical子项 | 已有maker证据；此次未独立逐项复跑 |
| factual全门禁 | 此次未完成全面源核查；保持艺术概念/现代类比标签，不宣称古代物种复原通过 |
| specification最终验收 | 未闭合；不能忽略GPU与scene必需项 |
| gpu / scene | **unknown / 未通过**，由协调的独立运行任务补；本报告不填写测量值 |
| accepted_for_brief / publication | **未通过 / 未执行** |

下一步无需再改叶型或为密度加面。由独立运行任务使用这个精确GLB完成Three.js真实渲染器/设备、运动检查、错误记录，以及1/16/32 independent-clone组合场景的尺度/接地/材质和采样帧时/提交工作量证据；软件fallback须如实区分。GPU实例化测试不能替代声明的clone基线。任何后续修改位置、法线、材质或导出物均应重新绑定受影响证据。
