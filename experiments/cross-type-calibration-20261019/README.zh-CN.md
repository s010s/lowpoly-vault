# 砾岩与木贼：两件最小改动对照

**仅实验候选供用户选择，未获生产批准。** 源版本固定在175件main `de413ef720463a2999516faf92c606bcdf9ab1b7`。本次只修改本实验目录，不改原资产、Skills、门禁、批准或线上，不merge、deploy或恢复批量制作。云端Blender4.3.2，GPT-6.1 Sol medium；作者Leon Made This <8357465+s010s@users.noreply.github.com>。

## 为什么这样试

33项重筛报告已通过官方Library完整读取：report.zh-CN.md `libfile_38d99fa743ac81919ed56719fa55198d`、provenance.json `libfile_a35339c6f8008191a8217ee4392c6bc8`。报告是保留22、可选7、待核实3、砂岩个案1，**0项新确认硬性改模问题**；不能把33项当成缺陷单。两件相关条目与准确原版/证据hash见rescreen-relevant-entries.json。木贼四视及砾岩六视的实际像素均已查看，与报告hash对应。

另已实际查看父会话提供的四张实物照片：NPS Florissant露头、NPS Yellowstone砾岩近照、NC State木贼分枝与全株照。原照片没有进入Git、贴图或Library交付截图。来源与访问事实见references.json。Florissant照片较远且受遮挡，不能作粒径量测；Yellowstone近照可看出不同形状与暴露比例的砾屑嵌在连续细基质中。

木贼现代照片只辅助属级形态：节处径向轮生细枝、方向与长短有变化，不是平面蕨叶。不同现代物种及其营养/生殖茎关系不能强套到这个史前风格概念中。原版已具有七根高低不一分节茎、轮生枝，以及两根少枝顶穗茎；没有已证实结构缺陷。

## 两件各自的最少动作

- **砾岩**：原版已建连续基质、砾屑剖切面与半嵌入外缘。只选六颗外缘砾屑，沿原基质表面法向再沉入约5.6–13.7mm，其中三颗尺度稍缩小。保留完整基质、教学破裂面和其余砾屑。目的只是比较“圆凸点装饰感”是否减弱，不全面重建，不套砂岩纹理。
- **木贼**：只选不同茎上的三条下层枝梢，保持着生根部，长度变化约−12%／+8%／−6%、方位变化−8°／+6°／+10°，并作5–8mm末梢高差。茎、节鞘、轮数、其余69条侧枝以及两根少枝顶穗茎均保留；没有给分枝茎添加锥体，没有变成特定现代物种。它是可选姿态对照，不是修复判定。

精确组件、中心、下沉量和枝梢参数见modifications.json。生成器从两件冻结原版Blend读取并只写candidates目录，便于复现。没有新纹理、加面、重新配色或隐蔽删除结构。

## 真实成本

| 资产 | 原版tri / GLB B | 候选tri / GLB B | 材质 / primitive | 纹理 |
|---|---:|---:|---:|---:|
| conglomerate-outcrop | 7,840 / 174,328 | 7,840 / 174,328 | 4 / 4，两版相同 | 0 |
| horsetail-cluster | 1,838 / 107,256 | 1,838 / 107,256 | 4 / 5，两版相同 | 0 |

同字节数并不代表同模型：两个候选GLB哈希均已改变，只有指定顶点位置改变，没有填满预算。源/导出顶点和bounds见各qa.json；完整前后指标与hash见comparison-metrics.json。

## 图证和验证

每件`*-comparison.jpg`为原版/候选并排主视，砾岩强调曲面背侧，木贼强调整体轮生轮廓；`*-all-views.jpg`含hero、背3/4、正面、侧面、顶面、灰模及原生240px正常透视小景。原始实际GLB渲染在evidence目录。每对相机、灯光、米制尺寸一致，不独立归一化、不埋土、不加遮挡。Standard/None、曝光0、Cycles CPU32samples，无降噪；相机和源hash见render-manifest.json。

两件基础源/导出检查与官方glTF Validator均通过（官方零错误零警告）；保留原版有意使用平滑面的风格提示。两次重建得到逐字节相同GLB。原版Blend/GLB均与冻结main精确核对，并未被写入。本轮没有宣称独立视觉/事实QA通过或手机硬件性能达标。

制作后只做一次有界自检，具体有效/无效收益和保留建议见maker-observations.json。木贼可以选择保留原版；不能因做过试验就要求替换，更不能把此结果推广为全库加纹理或加面规则。

## 复现与交付

候选可编辑Blend、GLB、metadata与基础报告位于candidates各自目录。代码MIT，模型、渲染与文档CC-BY-4.0，署名Leon Made This / s010s。四张对比截图已准备，但此云端官方Library上传流程在上传前连接失败，未创建Library文件；待父环境完成Library交付。具体失败与文件名见library-delivery.json，不将其标作成功。

```sh
blender -b -t 2 --python experiments/cross-type-calibration-20261019/build.py
node scripts/validate_gltf.cjs experiments/cross-type-calibration-20261019/candidates
blender -b -t 2 --python experiments/cross-type-calibration-20261019/render.py
python experiments/cross-type-calibration-20261019/compose.py
```

本轮不更新Skill，后续是否采纳及是否继续其他对象由用户选择。
