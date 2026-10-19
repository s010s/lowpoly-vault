# 砂岩第二候选：连续石体与原创细层理纹理

状态：**用户授权的单件实验候选，待看图；不是生产批准或新基准。** 本次只新增此目录，原线上资产、上一砂岩候选、烟囱和既有证据均保留。未merge、发布或恢复批量制作。制作：GPT-6.1 Sol medium；云端Blender 4.3.2；作者Leon Made This <8357465+s010s@users.noreply.github.com>。

## 参考实际看到了什么

已通过父会话提供的Drive文件内联字节取得NPS Scotts Bluff照片，解码为1600×900、464,502B，并实际打开像素。照片SHA256为 `4f06545d408e2d00a80c555cac5bd9ea59c71b7864ec7c86b4c5d9da50be3e86`；公开来源、署名和观察记录见 `references.json`。此前Library签名传输失败的事实不改写；本次成功取得图片是新的证据。没有把参考照片或私有Drive链接放进资产，生成器从不读取参考照片。

照片中局部薄层成组延伸，主斜层与上覆/侵蚀界面相截；厚薄、可见长度与强弱有变化，较大的破损、浅凹和侵蚀断面打断层理。细密粗糙表面可见，但不能据照片可靠量测单颗砂粒。此次借鉴这些组织关系，不复制照片轮廓或纹理，不声称特定地点或精确地层复原。

## 本版分工

几何：一件连接、封闭的石体网格；斜断面、左侧断裂、两处较大的抗蚀层起伏与局部浅凹。没有逐层挤出、等距台阶、密集裂缝或全顶点随机噪声。断面平面着色、风化侧部平滑着色，混合使用以免全部磨成圆块。

贴图：一张原创512×512 RGB PNG底色，按原创三维颜色场烘焙到带padding的六面UV图集。细层理有不同组倾角、非等距相位、厚薄/强弱及局部消退，细颗粒是克制的原创颜色扰动。组内平行可保留，不为了打乱平行而画随机线。照片没有参与采样。材质粗糙度恒定0.91；**没有法线、位移或粗糙度贴图**，所以细颗粒主要是颜色，不等于照片中完整的表面微起伏。灰模不要求呈现所有薄层。

自检初稿曾因全平滑法线显得偏圆整，已做一次针对性修正：斜断面和左侧断裂保留平面、适度增加局部大起伏及薄层可读性。最终仍是简化的风格化石体；不宣称自然观感已经获用户或独立评审通过，不再自动继续美学修模。

## 实际成本

| 版本 | tri | GLB B | 材质 | primitive | 图像 |
|---|---:|---:|---:|---:|---|
| 原生产版 | 588 | 34,128 | 2 | 2 | 0 |
| 上一候选 | 2,276 | 133,172 | 5 | 15 | 0 |
| 本候选R002 | 3,840 | 423,928 | 1 | 1 | 1×512px RGB PNG |

本版源顶点1,922，导出POSITION流3,859；差异来自UV接缝和断面法线拆分。源网格boundary/nonmanifold边均为0。PNG编码275,532B，已嵌入独立GLB；GLB余下部分约148KB。按RGBA8完整mip粗略估计解码图像约1.40MB，此数不是实际GPU内存测量。512px与纹理成本是这次单件用户授权的实验参数，没有改旧brief、批准记录或全库门禁。GLB保持原14k tri／1,000,000B上限以内。

本版约0.80m宽；厚度比上一版增加，这是整体石形的改动。三版相机按同一米制、同一正交尺度或同一透视位置渲染，**没有分别按包围盒缩放成一样大**。

## 看图

- `comparison-side.jpg`：主要层理露面与窄侧面，三列分别是原生产、上一候选、本候选；侧面无遮挡。
- `comparison-hero.jpg`：相同四分之三角度。
- `comparison-scene-240.jpg`：普通视线高度的透视小景，240px原生渲染，不埋土、不放大冒充细节。
- `comparison-clay.jpg`：同灰模，检验大形与断面；薄层不靠沟槽表达。
- `views/`：15张原始实际GLB渲染，固定光照、Standard/None、曝光0、Cycles CPU 64 samples，无降噪。相机与来源hash见render-manifest.json。

实际看图：宽色带和板条台阶已换成更细、较弱且有分组消退的纹理；整体仍有圆整区和较概括的顶断面。240px时细层理与颗粒大多淡出，这次纹理投入主要改善近看，不应拿它冒充远景识别能力。

这些图用于观察细层理是否脱离板材感、石体是否可信，以及在240px时哪些纹理会淡出。它们不自动证明材质质感达到实物或用户基准。原生产与上一候选没有改模型或材质来配合新版。

## 导出、验证与交付

可编辑、贴图已打包的Blend和独立GLB在 `cross-bedded-sandstone/`；原创PNG和生成器在本目录。官方glTF Validator零错误、零警告，源/导出三角形与边界回读一致；两次重建GLB逐字节相同。源检查保留“平滑面需美术审查”提示，对风化侧面有意使用平滑、断面使用平面着色。Three.js r180 / Chromium ANGLE SwiftShader已实际加载新GLB；这是软件WebGL功能证据，不代表手机硬件性能。

不写入生产/profile通过；独立QA及用户风格选择仍待进行。PNG为原创，模型/渲染/文档CC-BY-4.0，代码MIT。

仓库根复现：

```sh
blender -b -t 2 --python experiments/geology-calibration-20261019/sandstone-r002-textured/build.py
node scripts/validate_gltf.cjs experiments/geology-calibration-20261019/sandstone-r002-textured/cross-bedded-sandstone
blender -b -t 2 --python experiments/geology-calibration-20261019/sandstone-r002-textured/render.py
python experiments/geology-calibration-20261019/sandstone-r002-textured/compose.py
```

生成器seed20261019；纹理及参数均在源代码与build-parameters.json显式保存。场景灯光、地面和相机不进入资产。独立证据完整性见integrity.json与checksums.sha256。
