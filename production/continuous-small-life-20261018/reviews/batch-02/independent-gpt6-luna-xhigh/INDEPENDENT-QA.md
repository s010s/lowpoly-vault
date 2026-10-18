# Batch 02 独立 QA

**结论：四项均 PASS；无必须返工项。** 该结论针对冻结 brief 中的 *stylized-inspired* 低模候选标准，不代表严格的古生物复原认证。

- 审核源提交：`29b0ceb97ae74d77846f7576cf9552fe178accb9`
- 源分支：`candidate/small-life-batch-02-20261018`
- 审核分支：`qa/s010s/small-life-batch-02-20261018`
- 审核模型：GPT-6 Luna xhigh；日期：2026-10-18 UTC
- 报告及联系表：本目录；联系表见 [contact-sheet.jpg](contact-sheet.jpg)，SHA-256 `e734813df22a69b6db05c986210b979ef90513bde7db62912b41ccd0049520ee`

## 独立核验摘要

我把 handoff 作为线索，而非 PASS 结论的依据。对四个 bundle 的 `checksums.sha256`（每项 37 个文件）、evidence manifest、candidate record、GLB、blend、16 张 manifest 图像及 Khronos 报告逐项复算。四个 GLB SHA 与精确源提交、manifest、runtime 报告及批次结果一致；每张 manifest 图像的字节数和 SHA 均一致。随附 Khronos 报告均为 0 errors / 0 warnings，报告中的 GLB digest 与实际文件相符。尺寸小于 100 KB 不作为缺陷。

我用 Blender 4.3.2 分别打开源 blend 并导入同一 bundle 的 GLB，重新计算三角数、包围尺寸、位置集合、三角面积和边界边。源与 GLB 的三角数、以 `1e-7 m` 坐标精度比较的唯一位置集合及包围尺寸相符；四项均无零面积三角形，且没有任何三角形低于私有 checker 的 `1e-14 m²` 面积阈值。实际最小 GLB 三角面积为：longipteryx `4.28717e-8 m²`、urasterella `7.34646e-10 m²`、alienopterus `1.68380e-10 m²`、aglaophyton `2.41147e-8 m²`。我也用原共享阈值复核：每项最小源面积都高于原 `1e-10 m²` 阈值；最小 GLB 叉积平方是 `1.134e-19 m⁴`（alienopterus），仍高于原 `1e-20 m⁴` 阈值。也就是说，阈值从 `1e-10/1e-20` 调到 `1e-14/1e-28` 没有改变任何一项的退化面判定；这些最小值也远高于本地阈值，没有迹象表明这次 PASS 是靠放宽阈值取得。

urasterella 的 GLB 有 3,962 个 POSITION 顶点，而源 mesh 有 3,122 个唯一位置。独立导入确认这是法线/顶点拆分：以 `1e-8 m` 焊合位置后，恢复 3,122 个位置且边界/非流形边均为 0；源 mesh 本身也为 0。该现象不构成可见裂缝或缺面，且 Khronos 报告无警告。

视觉检查直接查看了每项 8 张原始 source PNG、多角度 exact-GLB runtime 联系图，以及 GLB `small80.png`（80px）、`normal.png`（240px）、`near.png`（360px）、顶视图和九件同屏 `scene.png`。80px 目标下鸟、海星、昆虫、分叉植物仍各自可辨；适度近看未发现明显穿插、缺面或断裂。九件场景中各实例的屏幕投影约为 longipteryx `52–53×54–56px`、urasterella `74–75×32–34px`、alienopterus `62–66×37–38px`、aglaophyton 多数约 `73×70–71px`。runtime 证据由 Three.js r180 / SwiftShader 提供；这证明静态解析与软件渲染，不代表实体 GPU 或目标设备性能。

审查了小尺度预览改动：Alienopterus 与 Aglaophyton 的相机最小正交跨度由共享 helper 的 `0.05 m` 改成 `0.00001 m`；Longipteryx 与 Urasterella 仍用 `0.05 m`。这只改变 source 预览相机。四个 exact-GLB 在 80/240/360px 及多角度 runtime 中另行检查；相机调整没有藏住可见的接点、薄片或轮廓问题。Aglaophyton 的最大尺寸超过 0.05 m，因此对它的预览取景实际上没有影响。

## 逐项判定

### longipteryx — PASS

- **资产绑定：** candidate JSON SHA-256 `66b3a8dae527298b1589dbc8d1cb091a9b8671e25f0992f8b7006befc9fc038b`；GLB 47,420 B / 2,228 triangles，SHA-256 `787b7859332aebf4c8135bd2c1af4723d90ef86b5f9f9e00f2b2f8fdff4f8953`；blend SHA-256 `a6897d5915649dfd919a780ec82e0c02f572ef72df653370df4aafeb132eb012`。
- **视觉：** 长而窄的喙、鸟形躯干、折叠翼/短尾羽、双腿与脚趾在原始视图和 GLB 视图中都连贯；正侧顶及反向视图没有明显破面或比例断层。九件同屏中单只约 `52×55px`，脚趾细节会自然收缩，但鸟形及长喙轮廓仍读得出。
- **必须问题：** 无。
- **非阻塞建议：** 无需改模；保持目前已接受的自然低模处理。近期羽毛描述称已知 Longipteryx 标本没有尾羽痕迹；此处短尾扇应视为艺术化造型，不要在标签中当作该属特征。[Clark et al., Journal of Paleontology (2026)](https://www.cambridge.org/core/journals/journal-of-paleontology/article/plumage-of-longipteryx-aves-enantiornithes/86992F399FDADC4CA0E218EDF578DF55)
- 证据：[bundle](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/longipteryx/)、[source 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/longipteryx/contact-sheet.jpg)、[exact GLB 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/longipteryx/runtime/contact-sheet.jpg)。

### urasterella — PASS

- **资产绑定：** candidate JSON SHA-256 `3ea5d55c786ed88295fa650424c035654ae3ce94aebc14f35ac7705575749c30`；GLB 135,700 B / 6,240 triangles，SHA-256 `c15c786fbf9cb626385b10ea2a806a6203219ad8a2b1786475d625cfd2ac2d50`；blend SHA-256 `4f957143bbdd5530668f9e49489f65d1d8f40eaab637ba56668fac16cb269ab0`。
- **视觉：** 顶视能辨出中央盘与五条分离、渐尖的腕；背面、正面及极薄侧视连续。整体厚度约为腕展的 4.1%，但这符合 brief 的低剖面方向；在正常与近看尺寸均未发现缺臂、断接或破洞。
- **必须问题：** 无。
- **非阻塞建议：** 无需改模。表面放射纹在 360px 近看较明显，属于当前风格选择，不影响五腕轮廓。Digital Atlas 的页面确认所列 PRI 76788 是泥盆纪 Urasterella 海星标本，但嵌入 Sketchfab 视图返回 403；因此五腕、板片节律只按 brief 中的 stylized-inspired 造型要求评估，不宣称逐项复原该标本。
- 证据：[bundle](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/urasterella/)、[source 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/urasterella/contact-sheet.jpg)、[exact GLB 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/urasterella/runtime/contact-sheet.jpg)。

### alienopterus — PASS

- **资产绑定：** candidate JSON SHA-256 `ee712f3ad7fbb94bbd1425a82787aa2ddc3485c60628e58267d674469f71c400`；GLB 32,340 B / 1,428 triangles，SHA-256 `1463670dda905a4c3107b5216d7e57736789da2b6548d8b5cbda49b991946a98`；blend SHA-256 `d76e20ff419a353cf427b544273d29c9978a72080b97d11717ffcb40bbdd53c5`。
- **视觉：** 头、分节躯干、六条腿、短前翅盖与长后翅在顶、正、侧、背及反向视图里都能区分；各部件根部连续，无明显穿插或缺面。九件同屏中单只约 `62–66×37–38px`，腿会变细，但昆虫轮廓仍清楚。
- **必须问题：** 无。
- **非阻塞建议：** 无需改模。
- 证据：[bundle](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/alienopterus/)、[source 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/alienopterus/contact-sheet.jpg)、[exact GLB 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/alienopterus/runtime/contact-sheet.jpg)。

### aglaophyton — PASS

- **资产绑定：** candidate JSON SHA-256 `f15454c70a53f70bbf7e0b0c36be0a27c419e56d1b9f59c101be213f4bb0c591`；GLB 66,016 B / 3,412 triangles，SHA-256 `428d646967dcb99ef11dc093f6df7c58ed1d288d318f607ba91f139df0a35ef1`；blend SHA-256 `60e4ffc9f3deba5b189131a016171a07aac96ed423d419763abb3cc1356734c7`。
- **视觉：** 匍匐基部、向上分叉的裸轴和终端纺锤形孢子囊在原始及运行时视图中都可读；分枝衔接连续，顶视没有异常扭转，未见叶片/花状误读或缺面。
- **必须问题：** 无。
- **非阻塞建议：** 模型无需修改。九件同屏图里少数分枝投影靠近相邻实例；若以后将该图用作展示构图，可稍微增加实例间距。
- 证据：[bundle](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/aglaophyton/)、[source 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/aglaophyton/contact-sheet.jpg)、[exact GLB 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/aglaophyton/runtime/contact-sheet.jpg)。

## 事实范围与局限

四项 brief 均限定为 *stylized-inspired*。handoff 的 `actual-reference-access.json` 说明部分外部化石图像/Sketchfab 视图因 403 未能下载；我没有把这些文件当作已查看。另行核对可访问的文字来源后，只按 brief 声明的基本形态与轮廓判定：五腕海星、具长喙的鸟、短前翅盖/较长后翅昆虫、无叶分叉轴与终端孢子囊。Longipteryx 的长吻、喙端齿与无尾羽证据见 Clark et al. (2026) 的新标本描述；[2024 年饮食论文](https://www.cell.com/current-biology/fulltext/S0960-9822%2824%2901124-2)报告标本腹腔内有种子，后者不支持捕食场景。[Clark et al. (2026), *Journal of Paleontology*](https://www.cambridge.org/core/journals/journal-of-paleontology/article/plumage-of-longipteryx-aves-enantiornithes/86992F399FDADC4CA0E218EDF578DF55)。Urasterella 来源页确认数字档案中的 PRI 76788 是泥盆纪海星标本，但五腕数量及板片细节并没有通过不可访问的 Sketchfab 图像独立确认；周围岩石尺寸没有当作动物尺寸。[Digital Atlas of Ancient Life: Asteroidea](https://www.digitalatlasofancientlife.org/vc/echinodermata/asteroidea/)。Alienopterus 的短前翅与发达后翅见 Bai et al. (2016) 原始描述的摘要（DOI `10.1016/j.gr.2016.02.002`）。Aglaophyton 的下伏/匍匐轴、二歧分枝与植株重建见 Edwards (1986) 原始描述的摘要；顶生纺锤形孢子囊见 Kerp et al. (2017) 对 Rhynie chert 植物器官的综述。[Edwards (1986), *Botanical Journal of the Linnean Society*](https://doi.org/10.1111/j.1095-8339.1986.tb01020.x)；[Kerp et al. (2017)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5745331/)。我没有据此宣称完全复原、精确尺寸、颜色、局部共存或行为；软组织、羽毛/翅面细节和数量比例仍属艺术选择。

## 阈值与旧验收器说明

历史共享 helper 使用 source area `<1e-10 m²` 和 GLB cross-product-squared `<1e-20 m⁴`；bundle 内冻结 checker 使用 `<1e-14 m²` 与 `<1e-28 m⁴`。上述源/GLB实测最小面均高于旧阈值，因此旧阈值下也都是零个被标为退化的三角形。零面积、非有限坐标、拓扑闭合与官方 Khronos 报告均另行核对；降阈值没有让一个原本会被拒绝的模型通过。

`validate_candidate.py` 是另一套历史 record contract。本次只读执行对 Longipteryx 返回 `maker: expected object`，未触及 brief；源码还要求 turntable 至少 2 帧且 production 视图包含 9 项，而本批 frozen brief 明确是 8 张固定图、0 帧 turntable。该 gate 与 `practical-fixed-eight-v1` record/brief 不兼容，不能把它的旧 schema 错误说成几何或视觉失败，也不能用伪造 turntable 让它通过。`verify_batch02.py` 的 PASS 仅代表交付完整性与 maker 技术报告一致；本独立视觉/事实结论另行完成。该旧 gate 的集成处理交由父任务。

## 实际执行命令

```sh
git fetch origin 29b0ceb97ae74d77846f7576cf9552fe178accb9
git worktree add -b qa/s010s/small-life-batch-02-20261018 /tmp/batch02-qa 29b0ceb97ae74d77846f7576cf9552fe178accb9

# 在 /tmp/batch02-qa 仓库根目录执行
python production/continuous-small-life-20261018/work/batch-02/verify_batch02.py
python3 production/continuous-small-life-20261018/reviews/batch-02/independent-gpt6-luna-xhigh/audit_hashes.py --repo .
blender -b --python production/continuous-small-life-20261018/reviews/batch-02/independent-gpt6-luna-xhigh/audit_meshes.py -- assets/candidates/continuous-small-life-20261018/batch-02/r001
python3 production/continuous-small-life-20261018/work/batch-02/lib/qa_glb.py assets/candidates/continuous-small-life-20261018/batch-02/r001/longipteryx/longipteryx.glb --max-triangles 14000 --max-materials 6 --max-primitives 30
python3 production/continuous-small-life-20261018/work/batch-02/lib/qa_glb.py assets/candidates/continuous-small-life-20261018/batch-02/r001/urasterella/urasterella.glb --max-triangles 14000 --max-materials 6 --max-primitives 30
python3 production/continuous-small-life-20261018/work/batch-02/lib/qa_glb.py assets/candidates/continuous-small-life-20261018/batch-02/r001/alienopterus/alienopterus.glb --max-triangles 14000 --max-materials 6 --max-primitives 30
python3 production/continuous-small-life-20261018/work/batch-02/lib/qa_glb.py assets/candidates/continuous-small-life-20261018/batch-02/r001/aglaophyton/aglaophyton.glb --max-triangles 14000 --max-materials 6 --max-primitives 30
python3 production/continuous-small-life-20261018/reviews/batch-02/independent-gpt6-luna-xhigh/prepare_80_runtime.py
node production/continuous-small-life-20261018/reviews/batch-02/independent-gpt6-luna-xhigh/runtime80.mjs longipteryx urasterella alienopterus aglaophyton
python3 production/continuous-small-life-20261018/reviews/batch-02/independent-gpt6-luna-xhigh/build_contact_sheet.py
python3 scripts/validate_candidate.py assets/candidates/continuous-small-life-20261018/batch-02/r001/longipteryx/candidate.json --root . --json
```

哈希审计每项输出 `PASS`，校验 37/37 bundle checksum 与 16/16 manifest 图像；Blender 审计每项输出 `PASS`；80px exact-GLB report 均绑定相应 GLB digest、无 GL error，Three.js r180 渲染 PASS。Three.js `0.180.0` 与 Playwright `1.56.1` 安装在 `/tmp/batch02-deps`；运行时仅在仓库根临时添加并移除 `node_modules` 符号链接。候选 bundle 没有被改写。历史 validator 按预期输出 `maker: expected object`。机器日志留在 `hash-audit.txt`、`mesh-audit.txt` 和 `runtime80/`。
