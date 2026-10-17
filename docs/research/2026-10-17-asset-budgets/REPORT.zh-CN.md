# lowpoly-vault：低多边形资产预算研究

研究日：2026-10-17。基线：main `e4019e28354f058cd11efaf5e4529af1e957855a`，Three.js `0.180.0`。本报告是独立研究分支上的提案，**没有修改生产默认预算**。

## 执行摘要

1. **按“用途 × 屏幕大小 × 同屏数量 × 设备档位”分配预算。** 不应为全部现代、史前、奇幻资产设同一个 MB 或三角面上限。glTF 规范规定格式，不提供保证流畅的统一预算。[glTF 2.0.1](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)、[Khronos Asset Auditor](https://www.khronos.org/blog/khronos-gltf-asset-auditor)
2. **默认候选采用比例/轮廓优先、轻量配色、按需增加细节。** 本项目 14,432 三角面的三角龙已做到 471,784 B，单张 512 JPEG、1 材质/primitive。用户接受了该具体候选的体积和风格。这是一个可复用的取舍样例，不是全库 500 KB 标准。
3. **下载大小、解码与驻留、每帧成本必须分账。** 同面数三张 2K 纹理版本约 7.70 MB、RGBA8+mip 估算 64 MiB；轻量颜色层约 0.472 MB、1.33 MiB。三角面、调用、透明叠加、阴影、动画、画布物理像素都要独立核算。[Three.js textures](https://threejs.org/manual/pages/textures.html)、[Three.js shadows](https://threejs.org/manual/pages/shadows.html)
4. **1,000/10,000 件库不等于同时加载 1,000/10,000 件。** 目录用海报/轻量转台，展厅按房间加载，近景增强和 Blender 源档按需下载，资源缓存按字节和共享引用计数。
5. **先校准真实设备，再冻结 profile。** 下表数字是项目试验起点，不是行业标准或已测性能。本次完成的是官方资料、文件结构和现有视觉证据研究，未完成真实手机/笔记本 GPU 的 FPS、解码耗时或总内存测试。

配套：[英文规则](proposals/BUDGET_POLICY.md)、[机器可读规划表](proposals/budget-profiles.proposed.json)、[记录 Schema](proposals/asset-budget-record.schema.json)、[测量计划](MEASUREMENT_PLAN.md)、[37 条一手来源](SOURCES.md)。

## 1. 标准、建议、观察和提案必须分开

| 层级 | 本次证据 | 正确用法 |
|---|---|---|
| 规范 | glTF 2.0.1、已批准的 Draco/Meshopt/量化/BasisU 扩展 | 校验格式、扩展和解码契约，不推导统一 FPS/MB |
| 厂商建议 | Khronos、Three.js、Unity、Unreal、PlayCanvas、model-viewer | 理解机制，保留设备/版本/场景背景 |
| 项目观察 | 精确 GLB 哈希/字节、匹配视角 A/B、官方样例元数据 | 只支持该资产和该比较条件 |
| 本项目提案 | 用途、屏幕与场景分档 | 校准后才可写入冻结 brief |

常见“100k 面、最好 <5 MB”来自 2020 年 Khronos 电商资产发布建议，不能当成现代博物馆全场景标准。标为 2025 年 8 月的 2.0 创建指南在所查仓库快照中仍有多个展开章节是 WIP，不能把未完成的 publishing/performance 章节说成新的已定数字规范。[Khronos 2020 creation guidelines](https://www.khronos.org/assets/uploads/apis/3DCommerce-Realtime-sset-Creation-Guidelines_Jul20.pdf)、[Khronos Asset Creation Guidelines 2.0](https://github.com/KhronosGroup/3DC-Asset-Creation/blob/3ba6cf7045f0b3bc7d845bc518ccdbd1356a3b93/asset-creation-guidelines/RealtimeAssetCreationGuidelines.md)

Unreal 5.6 文档的 500k 三角面/700 调用文字仍关联旧 iPad 4/Air 约 30 FPS；PlayCanvas 的 100–200 调用明确是低端移动端的粗略建议。均只能作上下文证据。[Unreal mobile performance](https://dev.epicgames.com/documentation/en-us/unreal-engine/performance-guidelines-for-mobile-devices-in-unreal-engine?application_version=5.6)、[PlayCanvas optimization](https://developer.playcanvas.com/user-manual/optimization/guidelines/)

## 2. 本项目的实际成本证据

文件 MB=1,000,000 B；内存 MiB=1,048,576 B。下表纹理内存是假定每张图各一次 RGBA8/SRGB8_ALPHA8 上传并带完整 mip 的估算，不含几何、CPU 图像副本、渲染目标、环境图和驱动开销。

### 三角龙：采用公平基线

| 版本 | GLB 字节 | 三角面 | 材质/primitive | 纹理 | 纹理驻留估算 |
|---|---:|---:|---:|---|---:|
| 首次交付 canonical V1 | 573,640 | 8,256 | 见清单 | 无 | 0 |
| 精修研究原始纯色 | 596,068 | 14,432 | 9/9 | 无；仍留 tangent | 0 |
| 公平轻量纯色 | 428,496 | 14,432 | 9/9 | 无；删除无用 tangent | 0 |
| **用户接受的轻量颜色候选** | **471,784** | **14,432** | **1/1** | **512 JPEG 颜色，58,887 B** | **1.33 MiB** |
| 1K 三图 | 2,689,404 | 14,432 | 1/1 | 颜色/normal/ORM | 16 MiB |
| 2K 三图 | 7,695,292 | 14,432 | 1/1 | 颜色/normal/ORM | 64 MiB |

轻量颜色层比公平纯色只多 **43,288 B（10.10%）**，同时由 9 个 primitive 变为 1 个。不要拿保留无用 tangent 的旧纯色证明“纹理没有代价”。纯色和合并后颜色版 POSITION accessor 分别为 10,392 与 10,141 顶点；同为 14,432 三角面，不代表顶点缓冲逐字节相同。

匹配 hero/detail GLB 渲染与独立评审：保留配色层次，精细鳞片起伏基本消失，不能说与 2K 近景层等价。用户接受该版本的体积和风格，支持日常浏览采用轻量颜色层；既有形体/解剖与 GPU hold 不自动消失。相关固定案例：[实验案例](https://github.com/s010s/lowpoly-vault/blob/888c139b651692dd4e4481669403c35493b63063/docs/case-studies/lightweight-triceratops.md)。

精确文件/图片哈希、导出顶点与 bufferView 字节见 [local-sample-inventory.json](data/local-sample-inventory.json)。轻量候选 SHA-256 为 `d9396f37f1d8453fa68916de8e4d6671f20b89cc96bf4687b60652006d9c2b9c`。

### 环境资产：少量几何也会被贴图主导

| 资产/变体 | GLB 字节 | 三角面 | 材质 | 基础提交估算 | 纹理估算 |
|---|---:|---:|---:|---:|---:|
| 岩拱原始 | 40,656 | 672 | 3 | 6 | 0 |
| 岩拱 full | 1,669,400 | 672 | 1 | 4 | 12 MiB |
| 岩拱 half | 366,184 | 672 | 1 | 4 | 3 MiB |
| 岩拱 512 颜色层 | 69,912 | 672 | 1 | 4 | 1.33 MiB |
| 蕨类原始 | 186,208 | 2,418 | 3 | 11 | 0 |
| 蕨类 512 颜色层 | 303,916 | 2,418 | 1 | 11 | 1.33 MiB |
| 松柏 v2 原始 | 964,328 | 14,118 | 6 | 15 | 0 |
| 松柏 v2 512 颜色层 | 1,258,428 | 14,118 | 1 | 8 | 1.33 MiB |

full 实际为 1K 颜色 + 1K normal + 512 ORM；half 为 512+512+256，不能记成三个同尺寸图。颜色层保留部分主要视觉提示，但独立评审仍发现岩拱塑模感、蕨叶形态、松针/枝条组织等问题。这些变体仍是实验，不是合格替代资产。贴图节省无法解决形体问题。

一个材质也没有把蕨类变成一次调用：多个 mesh/primitive 实例仍需提交。表格只提供结构估算，实际还受剔除、批处理、透明和额外 pass 影响。

外部博物馆三角龙参考为 3,178,460 B、12,560 面，三张 1024 WebP 占文件约 96.77%；RGBA8+mip 估算仍为 16 MiB。即使 Meshopt/量化已处理几何，纹理仍可主导；WebP 不是 GPU 原生块压缩。

### 官方开源 Web3D 样例：可复现，不当速度测试

| 样例 | 官方固定提交元数据 | 启发 |
|---|---|---|
| Fox | GLB 162,852 B；576 面；24 关节；3 clip | 风格化动画资产可以很轻，不是恐龙准确性基准 |
| DamagedHelmet | GLB 3,773,916 B；15,452 面；5 张图约 3.21 MB | 材质细节常支配文件，面数不能预测 MB |
| FlightHelmet | 完整 glTF 目录 48,392,569 B，KTX 目录 33,959,955 B；均 94,722 面 | 此例存储约降 29.8%，仍非轻量默认；GPU 收益另测 |

只读元数据、每文件大小/Git blob SHA 和目录口径见 [official-sample-metadata.json](data/official-sample-metadata.json)。外置 glTF 必须统计所有依赖，不能只看 JSON。模型许可逐资产核对；没有重发这些样例的二进制。[Khronos official sample assets](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/edc7c9e67c639d230715049ee31f9a96a6babbbe)

## 3. 五本账

| 账本 | 必记内容 | 常见误判 |
|---|---|---|
| 分发/网络 | GLB+外部依赖、实际 HTTP 传输、冷 decoder/transcoder、缓存和首个有用画面 | 磁盘大小=传输；忽略首次解码器下载 |
| CPU/加载 | 解析、解码、转码、临时缓冲、图像副本、动画更新 | worker 没阻塞主线程=无成本 |
| GPU 驻留估算 | 唯一几何/纹理/动画、实际格式/mip、共享关系；渲染目标另算 | JPEG 字节=显存；纹理计数=字节 |
| 每帧渲染 | 全 pass 调用/提交面数、CPU/GPU 时间、物理像素、alpha/阴影/shader | 一材质=一调用；实例化消除实例三角面 |
| 编辑维护 | .blend/原图/脚本、版本、许可、派生哈希 | 为网页目标破坏源档；源档塞进首包 |

Three r180 的 `memory.textures/geometries` 是数量；三角面统计乘以 instanceCount。该 renderer 默认在阴影渲染**之后**重置 info，直接读取一次 render 后的数字会漏掉阴影工作。完整计数要 `autoReset=false`，整个应用帧开始前 reset 一次，全部 pass 后再取数。[Three.js renderer source](https://github.com/mrdoob/three.js/blob/r180/src/renderers/WebGLRenderer.js)、[Three.js counter source](https://github.com/mrdoob/three.js/blob/r180/src/renderers/webgl/WebGLInfo.js)

### 纹理容量

| 单张方图 | RGBA8+完整 mip | 三张同尺寸 |
|---|---:|---:|
| 256 | 0.333 MiB | 1 MiB |
| 512 | 1.333 MiB | 4 MiB |
| 1024 | 5.333 MiB | 16 MiB |
| 2048 | 21.333 MiB | 64 MiB |
| 4096 | 85.333 MiB | 256 MiB |

逐级累加 mip 像素×4，近似基础层的 4/3。原生块压缩应按实际格式/块舍入计算；1K 的 4bpp/8bpp+mip 约 0.67/1.33 MiB，但设备回退 RGBA 时可恢复到 5.33 MiB。不能承诺所有设备都“省 8 倍”。WebGL 无可靠可移植的剩余显存查询，应保守分配、留余量、实机验证。[Three.js textures](https://threejs.org/manual/pages/textures.html)、[MDN WebGL best practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices)、[KHR_texture_basisu](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Khronos/KHR_texture_basisu/README.md)

## 4. 资产分档提案

**所有数字都是待校准项目起点，不是规范、最低质量要求或已采用门禁。** 越低且满足 brief 越好；超范围需要用途审议，不自动降面。范围重叠是有意的。

| 用途 | LOD0 面数起点 | 便携 GLB 规划 | 材质/基础 primitive 目标 | 贴图起点 | 同屏重复 |
|---|---:|---:|---:|---|---:|
| 微小重复物 | 20–300 | 5–75 KB | 1/1 | 无/顶点色/共享 128–512 图集 | 20–500 |
| 小道具/草簇/石 | 300–2k | 25–250 KB | 1/1 | 有收益才用 256–512 颜色 | 5–100 |
| 环境/树/建筑模块 | 1k–6k | 100–750 KB | 2/2 | 512 颜色或生物群系共享图集 | 3–50 |
| 特色生物/重点展品 | 6k–20k | 250 KB–1 MB | 2/2 | 512–1K 颜色，数据图单独论证 | 1–8 |
| 近看主展品 | 15k–60k | 0.5–2 MB | 3/4 | 1K 颜色/normal、512 ORM 按需；2K 需例外 | 1–2 |

471,784 B 三角龙只证明“特色生物”档里有一个真实可用取舍，不证明边界已正确，也不要求所有恐龙 14k 面。复杂羽毛/翼/角的轮廓需求可以获例外。

同时预算导出顶点：硬法线、平面着色和 UV 接缝会拆点。浮点 position/normal/UV/tangent 常见布局为 48 B/顶点，量化布局示例约 20 B；无用 tangent 的 16 B/顶点可先清除，避免盲目损坏形体。[Blender glTF exporter](https://github.com/KhronosGroup/glTF-Blender-IO/blob/main/docs/blender_docs/scene_gltf2.rst)、[KHR_mesh_quantization](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Khronos/KHR_mesh_quantization/README.md)

### 屏幕占用与距离

使用物理 drawing-buffer 的投影最长边，不用 CSS 像素直接替代。

| 观察状态 | 投影最长边 | 可试 LOD 比例 | 材质 |
|---|---:|---:|---|
| 仔细检查 | ≥512 px | 70–100% | 可按需增强 |
| 近景 | 256–512 px | 40–70% | 颜色优先，保可见数据图 |
| 中景 | 64–256 px | 10–35% | 共享/简化表面 |
| 远景 | <64 px | 1–10% 或已验证 impostor | 保识别轮廓 |

比例是第一轮试验，不是硬要求；保留角、趾、尾和叶缘等识别点，检查多视角跳变并加滞回。很小的网格或固定视角可能无需增加 LOD，避免额外文件/内存。[Unity mobile art optimization](https://unity.com/how-to/mobile-game-optimization-tips-part-1)、[Three.js LOD](https://threejs.org/docs/pages/LOD.html)

距离示例：1 m 垂直物体、720 px 高画布、垂直 FOV 50°、正对相机时，投影高度约 `H × viewportHeight / (2 × distance × tan(FOV/2))`。512/256/64 px 分别约为 1.51/3.02/12.06 m。不同大小/FOV 不能共用这组米数，实际应测投影包围盒/屏幕误差。

LOD 需要按需文件才能减少初始传输；把所有 LOD 装进首个 GLB 只减少渲染复杂度。材质/阴影也应随 LOD 简化。

### 生物群系与重复数

| 情境 | 策略 | 重点风险 |
|---|---|---|
| 50–500 草/石/小蕨 | 少数共享网格/图集、空间分块实例化、远景低 LOD | alpha 叠加，实例化不消除提交三角面 |
| 10–100 树 | 树种资源复用、形态变体、按屏幕 LOD、限制阴影范围 | 全森林面数/阴影 |
| 1–8 生物 | 按识别度/屏幕占用分配，增强只给当前目标 | 蒙皮、动画和材质差异 |
| 多展柜 | 简化版保持可读，选中才增强 | 全体最大纹理同时驻留 |

算术例：100 棵 14,118 面、8 基础提交的现有松柏，约 141 万面/800 调用。实例化同空间块可将基础提交降到约 8，但面数仍约 141 万；换 1,000 面 LOD 才降到约 10 万。巨型单批也会降低剔除粒度。此例不是帧率测试。[EXT_mesh_gpu_instancing](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Vendor/EXT_mesh_gpu_instancing/README.md)、[Three.js InstancedMesh](https://threejs.org/docs/pages/InstancedMesh.html)、[Three.js many objects](https://threejs.org/manual/pages/optimize-lots-of-objects.html)

## 5. 场景分档提案

下表均为校准试验分配。驻留资产只含唯一几何/纹理/动画估算，深度/MSAA/阴影/PMREM/后处理/CPU 副本/解码峰值另外记账并留余量。

| 档位 | FPS 目标 | 画布高/DPR 上限起点 | 主/全 pass 三角面 | 主/全 pass 调用 | 驻留资产估算 | 首房间 3D 资源 |
|---|---|---|---:|---:|---:|---:|
| 移动保守 | 30 | 720 / 1 | 100k/200k | 75/125 | 64 MiB | 2 MB |
| 移动均衡 | 60，显式 30 回退 | 最高 1080 / 1.5；弱机先 720 | 250k/500k | 120/200 | 128 MiB | 4 MB |
| 桌面均衡 | 60 | 1080 / 1.5 | 750k/1.5m | 300/500 | 256 MiB | 8 MB |

画布高与 DPR 是同时约束的上限，不再相乘出额外像素。以指定最低设备的质量/帧时间曲线批准档位；达不到目标先找瓶颈，分辨率、alpha、阴影或提交可能比面数更重要。

假设房间：14,432 面主展品 + 6×5k 次展品 + 40×1.5k 树 + 160×200 地被 + 40×500 石 + 30k 房间 = **186,432 主 pass 面**。低于规划 250k 只代表账面余量，不证明 60 FPS。

透明双面材质可能前后两次 pass，层叠造成大量片元工作；实体叶簇、alpha mask、blend 要实测比较。`forceSinglePass` 不是无条件无损开关。点光阴影可额外渲染六个方向。[Three.js Material](https://threejs.org/docs/pages/Material.html)、[Three.js shadows](https://threejs.org/manual/pages/shadows.html)

动画另记关节、每顶点权重、活跃 rig/clip 数、关键帧和 morph。10k 顶点×10 morph×position+normal 各三个 float，未压缩约 2.4 MB，只是算术例。静态博物馆变体可移除不需要的 clips；24 关节 Fox 不证明大量蒙皮角色便宜。

## 6. 压缩、材质、图集和源文件

### 三层交付

- 编辑源：.blend、原图、生成脚本、单位/轴向、出处/许可。允许较大，按需下载，不为了网络预算不可逆覆盖源。
- 便携 GLB：依赖最少；471,784 B 例不需 Meshopt/Draco/WebP 解码器。
- Web 优化变体：经消费者和冷启动验证再用量化/Meshopt/KTX2；声明扩展、解码器版本、哈希和回退。

| 手段 | 主要节省 | 不自动解决 | 前提 |
|---|---|---|---|
| 清除无用属性/常量图 | 下载/解码/驻留 | 错误形体 | 证明未用，导出 A/B |
| JPEG/WebP 与降尺寸 | 下载；降尺寸也省驻留 | 仅换编码不省 RGBA 上传 | 色彩空间、alpha、细纹 QA |
| 量化 | 顶点存储/带宽 | 面数/调用 | 精度/薄结构/UV/loader |
| Meshopt | bufferView 传输，可含动画 | 相同拓扑面数/调用 | 冷启动+解码实测 |
| Draco | mesh primitive 几何传输 | 纹理/任意动画/LOD | 同质量条件比较 |
| KTX2/BasisU | GPU 原生压缩，常兼顾下载 | 相同设备格式/零转码 | 实际目标格式/回退/质量 |

不作 Meshopt/Draco 总是更小或更快的结论。小模型节约可能被首次 decoder/transcoder 下载抵消，多模型共享后才摊薄。[EXT_meshopt_compression](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Vendor/EXT_meshopt_compression/README.md)、[KHR_draco_mesh_compression](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Khronos/KHR_draco_mesh_compression/README.md)、[model-viewer loading](https://modelviewer.dev/examples/loading/)

KTX2 颜色图比较 ETC1S/UASTC；normal/ORM 更重质量和实际设备格式。KHR_texture_basisu 范围是 ETC1S/UASTC，不能因最新 Basis 工具新增模式便假定 loader 支持。非颜色 UASTC 在缺合适格式时可能需要 RGBA 回退，不能把原生压缩比例当跨设备保证。[KHR_texture_basisu](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Khronos/KHR_texture_basisu/README.md)、[Basis Universal](https://github.com/BinomialLLC/basis_universal/tree/1706f948a2f0992d7a6dc2a909f35690b508571c)、[Three.js KTX2Loader](https://threejs.org/docs/pages/KTX2Loader.html)

Three r180 的已核对支持是 EXT_meshopt。新 KHR_meshopt 在检索快照中仍为 Release Candidate，不能直接改扩展名替代。[KHR_meshopt_compression](https://github.com/KhronosGroup/glTF/blob/521a91d491f02bb7db7d445b35f591d09d2a64ce/extensions/2.0/Khronos/KHR_meshopt_compression/README.md)、[Three.js GLTFLoader](https://github.com/mrdoob/three.js/blob/r180/examples/jsm/loaders/GLTFLoader.js)

一个 1K 图集的 texel 数约等于 16 张 256 图，padding/mip 前容量相当。收益在复用/绑定/批处理，代价在 UV、gutter、mip 渗色、空白与为了小件载入整图。4K RGBA+mip 约 85.3 MiB，不宜全库必载。按生物群系/材质家族分片，以 512–2K 作试验起点；动物脸部斑纹可能更适合独立 UV。自包含 GLB 和跨资产外置共享纹理是不同分发契约，统计不能同时无条件享受两者好处。

## 7. 优化顺序

1. 冻结 brief：物种/时代/尺寸、最近观察、同屏数、动画、设备；先过比例/轮廓/事实。
2. 盘点精确导出：哈希、三角面/顶点、材质/primitive、图片字节与尺寸、动画/扩展，找最大成本。
3. 低风险清理：无用属性/贴图/材质/片段、常量 roughness/metalness；去重时保交互语义和剔除粒度。
4. 按可见收益减图：颜色层起步，normal/ORM 逐个匹配 A/B，独立尺寸。
5. 按轮廓/重复减几何：先碎面/不可见面/导出拆点，再 LOD；不让贴图掩盖形体。
6. 量化/缓存/编码：固定版本参数，计冷解码器；广泛 optimize 可能改层级/材质/动画，验证输出。
7. 放进真房间：多实例、动画、阴影、透明、切房间、峰值与释放。
8. 记录资产专属合同和例外，发布结论绑定确切 hash/场景/设备/距离。

工具的作用是可控转换，不是质量判定。[glTF Transform CLI](https://gltf-transform.dev/cli)、[glTF Transform textureCompress](https://gltf-transform.dev/modules/functions/functions/textureCompress)、[meshoptimizer](https://github.com/zeux/meshoptimizer/tree/f0a684f11ead064e176775c9b796f82a55910e92)、[gltfpack](https://meshoptimizer.org/gltf/)

## 8. 千件/万件库

500 KB×10,000≈5 GB 存储，2 MB×10,000≈20 GB；源档/版本/海报另计，不能等同于一次下载或内存。

目录分页/筛选、视口海报、受限并发、字节 LRU。基线已部署的三组 24 帧 320px 转台包为 47,868/85,854/111,402 B，十张海报合计 30,248 B；单卡只解码当前+两邻帧约 1,228,800 B，加 canvas 409,600 B。这是图像 UI 账，不是 GPU 帧率证据。

出版任务另报告待发布 768px/q90 修订：十组 24 帧加海报共 250 文件、3,993,538 B，海报 164,604 B；三帧 RGBA+canvas 约 9 MiB，序列 197,584–626,534 B。该修订截至本报告证据截止仍在上传/CI，不能当成已部署基线；更高预览分辨率会显著增加解码内存。

展厅只加载当前房间和必要邻区；选中才增强。离开时释放未引用几何/纹理/bitmap，引用计数保护共享资源；静态画面按需渲染。model-viewer 按模型数的 cache 不能替代本库字节预算。[Three.js disposal](https://threejs.org/manual/pages/how-to-dispose-of-objects.html)、[Three.js on-demand rendering](https://threejs.org/manual/pages/rendering-on-demand.html)、[model-viewer API](https://modelviewer.dev/docs/index.html)

## 9. 验收、例外和下一步

分别记录技术、形体/美学、事实、运行时、场景五道 gate，绑定输出 hash。用户体积/风格接受单列范围。必需证据 unknown 就 hold，不补为 pass。

例外必须写：超出的字段/新上限、不可删的视觉/语义原因、设备/场景实测、轻量回退、批准者/有效条件、确切版本/hash。主展品例外不能授权无限复制或变成全库默认。

现有静态检查器对压缩/蒙皮/动画仍 fail-closed；采用前补正反 fixture、解码器和运行时检验，不绕过 gate。Validator 不能证明审美/科学正确/帧率。[glTF Validator](https://github.com/KhronosGroup/glTF-Validator)

下一步最有价值的工作：
1. 保留用户接受的颜色层锚点与公平纯色，不为任意整数继续改造。
2. 选择小石、密叶植物、重复树、建筑、静态生物、带骨骼生物、近景主展品；先修形体，再对比编码。
3. 固定最低 Android、iPhone/Safari、集显笔记本及浏览器版本，测冷/暖启动与实际纹理格式。
4. 固定博物馆压力房间，逐档找质量/成本拐点，批准后才冻结数值。
5. 将英文规则和记录 Schema 与当前流水线协调，所有未知实机数据保留为未完成。

详细协议见 [MEASUREMENT_PLAN.md](MEASUREMENT_PLAN.md)。本研究的完成条件是可审阅的证据与可执行提案；真实设备校准是清楚列出的后续要求，不是已经完成的测试。
