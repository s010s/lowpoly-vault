# r15 独立图片 QA — 阻塞，修复后复审

审查日期：2026-10-17。审查对象固定 Git commit `1f3cc24b32ddad01d5a84636b80e083e92f7e821`，候选 `candidate-r15/`。GLB SHA-256：`2ad0baa9c4b54be1a3a5ebd2298eb612ca9d9cb4b4b3a09a2eddd16ae38eca8d`。

本报告为独立只读图片审查；未参与制作，未修改候选、源脚本、已有证据、Git 分支或发布记录。未运行 Blender、浏览器、GPU 测试或重建；未使用用户 Chrome/Safari。只新增本 QA 目录。初始 HEAD 与指定 commit 相同，工作区干净。

## 结论

**visual = fail；整体阻塞。** r15 确实消除了 r12 的绿色粗管/香肠形叶簇，木质结构也明显优于原始树。可是叶扇从可见面转为侧面时大面积变成细刃，近景是尖菱形硬片，远景树冠则成为稀薄的分层枝架。它没有达到可近看、可多方向查看、低模形态统一的精修样本要求。不能因 479,320 B 小于上限，或把“风格化”解释得更窄而放行。

造型失败与 GPU/组合场景缺失是两件事。即使修复造型，仍须补足固定新导出物的目标运行时与 1/16/32 独立 clone 场景证据，不能把 Node parse 或 Blender PNG 当作 GPU/场景通过。

## 实际打开的图片

共 **53 张现有 PNG**，逐项由 `view_image` 打开；未只读文字、文件名或联系表。以下路径均相对 `candidate-r15/`。独立 `inspection-manifest.json` 记录每张的 SHA-256、尺寸和字节数。

- `comparisons/` 全部 9 张：`original-r12-r15-hero.png`、`original-r12-r15-detail.png`、`original-r12-r15-detailclay.png`、`original-r12-r15-hero128.png`、`original-r12-r15-silhouette128.png`、`r12-vs-r15-hero.png`、`r12-vs-r15-detail.png`、`r12-vs-r15-detailclay.png`、`full-angle256-contact-sheet.png`。
- `evidence/detail512/`：`hero.png`、`detail.png`、`detailclay.png`。
- `evidence/native128/`：`hero.png`、`front.png`、`rear.png`、`left.png`、`right.png`、`silhouette.png`，原生 128px。
- `evidence/full-angle256/`：`turntable-000.png` 至 `turntable-023.png` 共 24 张全部逐张打开；另打开 `hero.png`、`reversehero.png`、`front.png`、`rear.png`、`left.png`、`right.png`、`top.png`、`bottom.png`、`clay.png`、`clayalt.png`、`wire.png` 共 11 张。

未以 `pilot512` / `pilot128` 代替最终证据。打开过联系表，也独立打开了所有对应原始帧。

## 像素缺陷与通过部分

下述近景位置使用单张 512×512 原图坐标，左上为原点；范围是目视定位，不是假定测量结果。

| 项目 | 判定 | 具体证据与影响 |
|---|---|---|
| r12 粗绿色管状问题 | pass（仅此缺陷） | 匹配 `r12-vs-r15-detail.png` 左格是圆截面、钝端的粗绿色手指；右格已改为薄的成对表面。不能说 r15 仍是同一种香肠叶簇。 |
| 叶扇侧刃、多方向稳定性 | **fail，主要阻塞** | `detail512/detail.png` 左上 x0–220/y40–200 与左下 x0–215/y310–455 出现大量极细水平/斜线，少量菱片像悬在丝线上；相邻右侧却是密集宽叶面。`detailclay.png` 保留同样的线/片突变，说明换绿色不能解决。`hero.png` x130–250/y220–375 一侧明显虚薄，x280–370 的另一侧密集。完整转台 000–005、008–010、014–020 等反复出现薄侧与较密侧，反向 hero 也不消失。这里只确认像素缺陷，未推断一定是法线、背面剔除、光照或几何中的哪一个原因。 |
| 近景叶形、柔软针叶组身份 | **fail，主要阻塞** | `detail.png` x330–500/y70–415 和底部右侧叶组是宽中段、两端急收的尖菱形/箭片；叶片成串呈硬折线和锯齿，夹杂细长直尖。`detailclay.png` 同处仍像硬片，不能靠颜色把它解释为柔软羽状针叶扇。它不是原始大叶壳，但仍没有形成稳定、自然的针叶组读法。没有要求每根针叶按真实尺寸建模。 |
| 树冠与负空间 | **fail，主要阻塞** | `native128/front.png`、`rear.png`、`left.png`、`right.png` 可辨主干及数层横向枝叶，但上半冠尤其疏薄，中下部层间大面积空白；叶组细节在 128px 消失为碎点/细线。`full-angle256/front.png` 与 `rear.png` 的层状枝架感尤其强。`top.png` / `bottom.png` 却呈相当完整的放射叶扇覆盖，说明不能只拿俯视密度证明水平视角冠层成立。保留局部自然天窗是合理的，当前问题是多层整体过薄。 |
| 主干—主枝层级及圆润连接 | pass（图片可见范围） | 近景主干连续、逐渐收细，主枝有弧度，枝基由较宽的根部并入主干；clay 可读出同样结构。比原始直板式枝根和粗叶壳有实质改善。未看到要求重做全部木质结构的证据。密集叶片中的每个连接未能凭 256px 全景认证。 |
| 低模形态统一与节奏 | **fail** | 木质大平面与弯曲主枝清楚，但表面可见的尖菱形叶片、极薄线条、重叠叶串混在同一冠层，产生“枝架 + 硬片碎屑”的尺度突变。`clayalt.png` 换主光后仍有左右密度与线片差异；单纯换材质或调曝光不足以修复。无同场其他资产证据，跨资产 family consistency 仍 unknown。 |
| 类别识别 | pass（最低门槛） | 原生 silhouette 和各向彩图仍能辨认锥形针叶树轮廓、主轴和侧枝。可识别不等于视觉精修通过。 |

## 几何成本与可见收益

独立读取固定 GLB 的 JSON/accessor：16,450 exported triangles、15,718 POSITION-stream vertices、3 materials、3 primitives、0 textures、479,320 B；与 maker 数值一致。本审查没有重跑官方 validator、Three.js loader 或 Blender 重建。

原始 2,382 triangles / 145,732 B 对比：r15 约 **6.91 倍三角形、3.29 倍文件字节**。合理收益在于弯曲的主枝、较好的枝根、可读的次级分枝，以及取消巨型阔叶壳。这些收益确实存在；但在 128px，新增叶片的大部分只剩细噪点，近景又带来尖硬片和侧刃问题。因此目前不足以把 6.91 倍几何开销批准为成功的精修收益。也不能反推它 GPU 性能一定差；性能仍须实测。

## 门禁分开记录

| 门禁 | 状态 | 范围 |
|---|---|---|
| 冻结文件完整性 | pass | 独立对 `freeze.json` 所列 119 文件逐一计算 SHA-256，0 mismatch；确认当前 GLB hash。不是画质证明。 |
| 静态基本计数 | pass | 独立 GLB accessor/header 读取结果见上；不是完整格式验证。 |
| technical / runtime_parse / reproducibility 全门禁 | unknown（本审查未独立执行） | 已读 maker 声明，不能把声明改写成此次独立通过。现有技术报告可以由父任务按范围采纳。 |
| visual-acceptance | **fail** | 上表三个主要像素阻塞。 |
| crown-hierarchy / distributed-foliage | **fail** | 木质层级可读，冠层与叶扇在水平和近景范围未成立。 |
| round-organic-joins | pass（可见图片层面） | 不代表几何内部拓扑或所有遮挡连接均已检查。 |
| honest-concept | pass（标签范围） | brief 与 maker 保持无命名灭绝种、约 7m 艺术尺度、现代类比、不等于古植物复原的边界。 |
| factual-acceptance 全门禁 | unknown / 未批准 | 已核对部分现代类比来源；未完成 HK、NHM 等完整逐项源核查。来源支持针叶组类比，不支持目前硬菱片画质，更不证明古代物种、冠层密度或尺寸。 |
| specification-acceptance | **fail / 未批准** | 必需视觉义务未满足，且 GPU、scene 必需项未闭合；数字上限合规不够。 |
| gpu-acceptance | unknown，独立剩余门禁 | 无 exact Three.js 0.180.0 实际 GPU 画面、设备/渲染器及测量。 |
| scene-acceptance | unknown，独立剩余门禁 | 无预定 1/16/32 independent-clone 组合场景的尺度、接地、材质一致性与工作量/帧时证据。 |
| publication | 未授权、未执行 | 本报告不改变任何批准或发布状态。 |

## 有限、最小可操作修复

不要求推翻 r12 木质骨架，不要求增加预算，不要求逐针建模，也不要求无休止迭代。建议只修复叶扇层，两项为同一次受限修复：

1. **改变可见针叶组的轮廓。** 把最大宽度集中于中部的双尖菱片，改为较窄、有一段稳定宽度再缓收的叶组，短而较柔和的端部，加轻微弯曲/下垂。保留成对、沿轴组织及长短递减关系，避免统一锯齿。优先验证当前右半近景几个代表叶扇；不靠增加细针数量掩盖。
2. **让叶扇成为有深度的枝叶组，而非整片只绕轴滚转。** 在现有叶组内分配少数不同俯仰/弯曲，针对目前水平视角消失的组调整有效叶面覆盖；必要时重新分配已有叶面面积和重叠，保持几处大天窗。不要把全树均匀加密或简单加厚成圆管。先对 front/rear/left/right、hero/opposite hero 的 128px 及当前近景灰模小样验证；全部恢复枝叶体量后才生成新候选完整转台。

复审通过标准：相同光照/相机下，近景能读成沿枝排列的渐尖叶扇，不再是硬菱片和细刃混杂；四个水平角和反向 hero 没有大半冠层消失，128px 保留明确的中尺度叶簇而非仅细线横层；主干/枝根、自然负空间及已消除的粗管问题不回退。若这一轮仍不成立，应与父任务决定表示尺度取舍，而不是继续放宽 brief 或反复只调随机种子。

## 使用的要求与来源

已读 `maker-observations.md`、原始 study `brief.json` 与 r15 brief、`references.json`，以及仓库 `lowpoly-art-direction/SKILL.md`、`asset-factual-review/SKILL.md`、`blender-lowpoly-pipeline/SKILL.md`，并读 visual-acceptance、asset-budgeting、standardized-pipeline 参考要求。没有用分数覆盖失败门禁。

2026-10-17 在线核对：[NC State Leaves / identification](https://plants.ces.ncsu.edu/plants/metasequoia-glyptostroboides/) 描述柔软、线形、对生及羽状针叶；[C.J. Earle Description](https://www.conifers.org/cu/Metasequoia.php) 描述扁平线形、可略弯、端部钝或短尖的叶。这仅支持现代叶组类比；当前尖菱片视觉是否可接受，是结合候选实际像素作出的失败判断，并非声称艺术聚合叶组必须复刻真实每叶尺寸。[Digital Atlas Monopodial growth](https://www.digitalatlasofancientlife.org/learn/embryophytes/tracheophytes/branching/) 支持主轴和侧枝的一般结构关系，不批准该模型的精修质量。
