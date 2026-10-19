# 两件自然观感校准候选

仅供用户看过前后图后选择基准。**未批准为新基准，未替换线上、merge、发布或恢复生产。** 当前生产基准 `de413ef720463a2999516faf92c606bcdf9ab1b7`，175件。PR20未修改。作者 Leon Made This <8357465+s010s@users.noreply.github.com>；云端 Blender 4.3.2，GPT-6.1 Sol medium。没有使用 Mac、Drive、生成式图片或第三方模型。

| 模型 | Before tri / GLB B | After tri / GLB B | 变更 |
|---|---:|---:|---|
| cross-bedded-sandstone | 588 / 34,128 | 2,276 / 133,172 | 不对称碎块外轮廓、后部收缩断面；保留三组不等厚截切与清楚露面；层间距变化，取消每三层周期凸起；连续中尺度露面折面 |
| hydrothermal-chimney | 4,032 / 150,088 | 5,760 / 213,240 | 保留宽窄、偏移轴线、开口和连续内壁；沉积区域沿高度和周向漂移、局部隆起与矿物色区，不再完整等厚环带 |

成本也包括primitive：砂岩从2增至15，烟囱从3增至4（精确计数以comparison-metrics.json为准）；不把文件体积当作全部运行成本。砂岩以三个可编辑层组保留语义，未为最少draw call破坏源编辑结构。

两件均为原创风格化环境概念，不是特定地点或严格科学复原。名义尺度与原版接近，砂岩宽0.81m、高0.515m，烟囱高约0.87m；这是近似美术尺度。两边没有按各自包围盒归一化。均无纹理；没有突破原14k tri / 1,000,000B硬帽，没有改任何全库门禁、Skill或旧批准记录。

## 文件与观看

每个模型文件夹提供同名 `.blend`、`.glb`，`comparison.jpg` 为手机友好的 hero 左右图，`all-views.jpg` 为全视图左右图。`views/` 保留原始真实渲染：hero/front/back/clay/top/side/reversehero、240px单件和三件摆放缩略场景。Before实际导入生产GLB，After实际导入新GLB；没有用源场景或生成式图片代替导出结果。

主对比由同一脚本建立固定相机、正交尺度、目标点、面积灯和地面，Standard/None、曝光0、Cycles CPU 32 samples、无降噪。每一对使用相同物理比例和设置。棚景与240px场景摆放不进入资产GLB；三件小景的左右陪衬实例使用相同0.65显示缩放，不改变交付GLB尺度。`render-manifest.json` 和 `scene-render-manifest.json` 记录实际来源hash与相机；`evidence-integrity.json` 绑定图片hash。全图中的缩略图以原生240px显示，不放大冒充细节。

`runtime/` 是 Three.js r180 + Chromium 154 / ANGLE SwiftShader 的真实新GLB功能渲染，含9件重复小景和计数。它独立于棚景对比，不能当成完全匹配的前后相机，也不能当作真实手机GPU或性能证明。

## 已做验证与尚未完成

两件均通过源几何及GLB审计（烟囱内壁有意平滑，源检查提示的style warning由制作者保留说明）、Khronos官方 glTF Validator（零错误、零警告），两次重建的GLB逐字节相同。新GLB经Three.js实际加载和软件WebGL渲染，未见加载错误或GL错误。指标与精确hash见 `comparison-metrics.json`，格式报告见各文件夹 `qa.json` 和 `gltf-validator.report.json`。源顶点、导出POSITION顶点、tri、primitive分别记录；不会把它们统称面数。

**实物参考像素阻塞：** 已读NPS页面正文并取得NPS、GEOMAR图片地址，也尝试NOAA。云端urllib/curl（含一次提升网络执行）均遭代理403；禁用代理则DNS失败。网页图片通道只返回`ImageDisplayed`文字占位，没有可供此执行者查看的像素。因此本执行者没有实际看过参考实物照片，不能声称满足该义务。原会话看图不等于本执行者看图。来源、署名和访问事实见 `references.json`；未把第三方照片打包为原创资产。该项保持unknown，独立QA与用户基准决定也保持pending。

自检只形成一次候选：砂岩首先出现非平面多边形层界暗缝，已局部改为连续折面并重新出图。可见收益和剩余局限由 `maker-self-check.json` 记录，不能替代父会话安排的独立QA。自然露面仍有明显的风格化切面，烟囱仍有低模色区边缘；是否达到用户希望的自然程度由看图决定。

## 复现

仓库根运行：

```sh
npm ci --ignore-scripts --cache /tmp/lowpoly-calibration-npm
blender -b -t 2 --python experiments/geology-calibration-20261019/build.py
python experiments/geology-calibration-20261019/rebuild.py
node scripts/validate_gltf.cjs experiments/geology-calibration-20261019
blender -b -t 2 --python experiments/geology-calibration-20261019/render_compare.py
blender -b -t 2 --python experiments/geology-calibration-20261019/render_compare.py -- --scene-only
python experiments/geology-calibration-20261019/compose.py
python experiments/geology-calibration-20261019/freeze.py
node experiments/geology-calibration-20261019/runtime.mjs experiments/geology-calibration-20261019/cross-bedded-sandstone/cross-bedded-sandstone.glb experiments/geology-calibration-20261019/cross-bedded-sandstone/runtime
node experiments/geology-calibration-20261019/runtime.mjs experiments/geology-calibration-20261019/hydrothermal-chimney/hydrothermal-chimney.glb experiments/geology-calibration-20261019/hydrothermal-chimney/runtime
```

生成器seed20261019，参数在build.py中显式保存；输出名、候选范围与上限在各 `brief.json`，旧brief/config/references原样副本附于各文件夹。依赖hash见 `dependency-hashes.json`。脚本MIT，模型、图像、说明CC-BY-4.0，署名Leon Made This / s010s。

读过的研究：非生物全审 `f0a43c6f806c78f5564d62059ea489dc8e1190e6` 的 `reviews/natural-appearance-nonbiota-20261019/report.md`；基准研究 `321f4b4bbaf69cd4c080ddaaab594ae7327f53bc` 的 `docs/research/production-baseline-20261019/README.zh-CN.md`。它们是依据与提案，不是更改生产规则的授权。
