# Batch 02 独立 QA

**结论：四项均 PASS；无必须返工项。** 该结论针对冻结 brief 中的 *stylized-inspired* 低模候选标准，不代表严格的古生物复原认证。

- 审核源提交：`29b0ceb97ae74d77846f7576cf9552fe178accb9`
- 源分支：`candidate/small-life-batch-02-20261018`
- 审核分支：`qa/s010s/small-life-batch-02-20261018`
- 审核模型：GPT-6 Luna xhigh；日期：2026-10-18 UTC
- 报告及联系表：本目录；联系表见 [contact-sheet.jpg](contact-sheet.jpg)，SHA-256 `772e46c361471c104ed4eff185944e12b6e43ab614fd0f350d6b35cc88a48625`

## 独立核验摘要

我把 handoff 作为线索，而非 PASS 结论的依据。对四个 bundle 的 `checksums.sha256`（每项 37 个文件）、evidence manifest、candidate record、GLB、blend、16 张 manifest 图像及 Khronos 报告逐项复算。四个 GLB SHA 与精确源提交、manifest、runtime 报告及批次结果一致；每张 manifest 图像的字节数和 SHA 均一致。随附 Khronos 报告均为 0 errors / 0 warnings，报告中的 GLB digest 与实际文件相符。尺寸小于 100 KB 不作为缺陷。

我用 Blender 4.3.2 分别打开源 blend 并导入同一 bundle 的 GLB，重新计算三角数、包围尺寸、位置集合、三角面积和边界边。源与 GLB 的三角数、以 `1e-7 m` 坐标精度比较的唯一位置集合及包围尺寸相符；四项均无零面积三角形，且没有任何三角形低于私有 checker 的 `1e-14 m²` 面积阈值。实际最小面积为：longipteryx `4.28717e-8 m²`、urasterella `7.34646e-10 m²`、alienopterus `1.68380e-10 m²`、aglaophyton `2.41147e-8 m²`。这些最小值分别约为该阈值的 4.29M、73.5K、16.8K 和 2.41M 倍；因此这批几何没有显示出阈值放宽掩盖退化面的迹象。GLB 叉积平方阈值 `1e-28 m⁴` 也远低于实测最小面的量级。

urasterella 的 GLB 有 3,962 个 POSITION 顶点，而源 mesh 有 3,122 个唯一位置。独立导入确认这是法线/顶点拆分：以 `1e-8 m` 焊合位置后，恢复 3,122 个位置且边界/非流形边均为 0；源 mesh 本身也为 0。该现象不构成可见裂缝或缺面，且 Khronos 报告无警告。

视觉检查直接查看了每项 8 张原始 source PNG、多角度 exact-GLB runtime 联系图，以及 GLB `normal`（240px target）、`near`（360px target）和九件同屏 `scene.png`。九件场景中各实例的屏幕投影约为 longipteryx `52–53×54–56px`、urasterella `74–75×32–34px`、alienopterus `62–66×37–38px`、aglaophyton 多数约 `73×70–71px`。缩小时轮廓仍可辨，适度近看未发现明显穿插、缺面或断裂。runtime 证据由 Three.js r180 / SwiftShader 提供；这证明静态解析与软件渲染，不代表实体 GPU 或目标设备性能。

## 逐项判定

### longipteryx — PASS

- **资产绑定：** GLB 47,420 B / 2,228 triangles；GLB SHA-256 `787b7859332aebf4c8135bd2c1af4723d90ef86b5f9f9e00f2b2f8fdff4f8953`；blend SHA-256 `a6897d5915649dfd919a780ec82e0c02f572ef72df653370df4aafeb132eb012`。
- **视觉：** 长而窄的喙、鸟形躯干、折叠翼/短尾羽、双腿与脚趾在原始视图和 GLB 视图中都连贯；正侧顶及反向视图没有明显破面或比例断层。九件同屏中单只约 `52×55px`，脚趾细节会自然收缩，但鸟形及长喙轮廓仍读得出。
- **必须问题：** 无。
- **非阻塞建议：** 无需改模；保持目前已接受的自然低模处理。
- 证据：[bundle](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/longipteryx/)、[source 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/longipteryx/contact-sheet.jpg)、[exact GLB 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/longipteryx/runtime/contact-sheet.jpg)。

### urasterella — PASS

- **资产绑定：** GLB 135,700 B / 6,240 triangles；GLB SHA-256 `c15c786fbf9cb626385b10ea2a806a6203219ad8a2b1786475d625cfd2ac2d50`；blend SHA-256 `4f957143bbdd5530668f9e49489f65d1d8f40eaab637ba56668fac16cb269ab0`。
- **视觉：** 顶视能辨出中央盘与五条分离、渐尖的腕；背面、正面及极薄侧视连续。整体厚度约为腕展的 4.1%，但这符合 brief 的低剖面方向；在正常与近看尺寸均未发现缺臂、断接或破洞。
- **必须问题：** 无。
- **非阻塞建议：** 无需改模。表面放射纹在 360px 近看较明显，属于当前风格选择，不影响五腕轮廓。
- 证据：[bundle](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/urasterella/)、[source 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/urasterella/contact-sheet.jpg)、[exact GLB 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/urasterella/runtime/contact-sheet.jpg)。

### alienopterus — PASS

- **资产绑定：** GLB 32,340 B / 1,428 triangles；GLB SHA-256 `1463670dda905a4c3107b5216d7e57736789da2b6548d8b5cbda49b991946a98`；blend SHA-256 `d76e20ff419a353cf427b544273d29c9978a72080b97d11717ffcb40bbdd53c5`。
- **视觉：** 头、分节躯干、六条腿、短前翅盖与长后翅在顶、正、侧、背及反向视图里都能区分；各部件根部连续，无明显穿插或缺面。九件同屏中单只约 `62–66×37–38px`，腿会变细，但昆虫轮廓仍清楚。
- **必须问题：** 无。
- **非阻塞建议：** 无需改模。
- 证据：[bundle](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/alienopterus/)、[source 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/alienopterus/contact-sheet.jpg)、[exact GLB 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/alienopterus/runtime/contact-sheet.jpg)。

### aglaophyton — PASS

- **资产绑定：** GLB 66,016 B / 3,412 triangles；GLB SHA-256 `428d646967dcb99ef11dc093f6df7c58ed1d288d318f607ba91f139df0a35ef1`；blend SHA-256 `60e4ffc9f3deba5b189131a016171a07aac96ed423d419763abb3cc1356734c7`。
- **视觉：** 匍匐基部、向上分叉的裸轴和终端纺锤形孢子囊在原始及运行时视图中都可读；分枝衔接连续，顶视没有异常扭转，未见叶片/花状误读或缺面。
- **必须问题：** 无。
- **非阻塞建议：** 模型无需修改。九件同屏图里少数分枝投影靠近相邻实例；若以后将该图用作展示构图，可稍微增加实例间距。
- 证据：[bundle](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/aglaophyton/)、[source 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/aglaophyton/contact-sheet.jpg)、[exact GLB 多角度](../../../../../assets/candidates/continuous-small-life-20261018/batch-02/r001/aglaophyton/runtime/contact-sheet.jpg)。

## 事实范围与局限

四项 brief 均限定为 *stylized-inspired*。handoff 的 `actual-reference-access.json` 说明部分外部化石图像/Sketchfab 视图因 403 未能下载；我没有把这些文件当作已查看，也没有据此要求推测性细节。此次只核对 brief 规定的基本形态和可见造型：五腕海星、长喙鸟、六足双翅昆虫、无叶分叉轴与终端孢子囊。颜色、软组织、精确比例/姿势/数量及严格物种学精度不在本次 PASS 声明内。

## 实际执行命令

```sh
git fetch origin 29b0ceb97ae74d77846f7576cf9552fe178accb9
git worktree add -b qa/s010s/small-life-batch-02-20261018 /tmp/batch02-qa 29b0ceb97ae74d77846f7576cf9552fe178accb9

# 在 /tmp/batch02-qa 仓库根目录执行
python3 production/continuous-small-life-20261018/reviews/batch-02/independent-gpt6-luna-xhigh/audit_hashes.py --repo .
blender -b --python production/continuous-small-life-20261018/reviews/batch-02/independent-gpt6-luna-xhigh/audit_meshes.py -- assets/candidates/continuous-small-life-20261018/batch-02/r001
```

哈希审计每项输出 `PASS`，校验 37/37 bundle checksum 与 16/16 manifest 图像；Blender 审计每项输出 `PASS`。两个脚本只读取候选，不会重写模型或证据文件。
