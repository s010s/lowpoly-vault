# Batch 87：两件尺寸语义澄清与几何优先返修建议

状态：独立、只读、有界规格研究；不是 full QA，不接受旧候选。spatter-cone r004 和 travertine-terrace-pools r002 的原 specification BLOCKED 原样保留。没有新模型、重渲染、Blender 作业、源文件修改、提交或发布。

## 结论先行

1. 两件原 art target 都应先用真实几何去达到，不建议把目标改成现在的尺寸，也不建议事后补 ±15% 一类美术容差。几何可行性未见用户设计上的冲突。
2. Travertine 最小修复是上表面整体升高约 0.63550396 m，底面仍在 z=0，连接侧壁真实加厚；XY 包络分别收至 10、18 m。这样五级之间的 0.7 m 高差及既有局部唇口高度不变，不是全局 Z 缩放。其外观仍须新视图验证，不能自动把更厚底座当通过。
3. Spatter 必须局部修正高处叠加起伏、保护 vent floor 和名义 rim，不能全局压扁。2.5 m 名义环口与 2.8 m 总高可共存：不规则 crest 的均值 2.5 m，最高点 2.8 m；但“均值”是建议明确的新版测量定义，不是原文已写的事实。
4. 真实内部语义冲突只有硬解读才会产生：若 outer_radius=3.7 m 指最终最大半径，则任意 X 宽度最多 7.4 m，不可能达到 7.8 m。原文没有说最大半径，且同时要求不对称形态，合理澄清是 3.7 m 为变形前的名义径向构造值，实际最终 envelope 仍达到 7.8×7.4×2.8 m。不能因此宣称旧 r004 合格。
5. 没有本次提供的用户消息或原文件证明用户指定过精确真实场地尺度。数字来自 maker 的冻结 brief/config；冻结仍应尊重，不能伪称科学测量，也不应就内部术语反复打断用户。下一步需要内部明确测量口径、几何返修、新 exact proof 和 fresh QA，不需要当前用户设计选择。若以后发现用户确实另有“最大半径 3.7”之类明确要求，应停止冲突部分并向用户呈现真正二选一。

## 证据与不可变锚点

- 只读 source HEAD：14f14a9e0ab6c5bacab7c746d27186a8ea4de2f0，工作区起止均干净。
- 原 QA：/workspace/shared/lowpoly-batch87-independent-qa-20261020/independent-qa.report.json，SHA-256 913ddcec6eb6e8d3c72d9d277948301363f71487375834e77732a720ceb80246。
- 原 QA handoff SHA-256：cfb135f08148188e1725978de5fbbec84bf1a8664bd1d96b9dbfd80d49d3375f。
- Spatter 原 r001 brief：4a9bdc49e33fafb7fb7810734bce6397936d4aa2e784c08d366665f74b7a487f；config：fd84521ebe0b37f92f292bba75835269c0a77855e7d35beadddd29483dcffa42。
- Travertine 原 r001 brief：d7162b92d9382923a8d5db28ac3be641029741e68aacabd0d7fcc58f3b8002b0；config：e8a9a9ca9f3f694eb1c483a78ac4d6d4a4c5e00f3d34865fcfd73f6f6a990a29。
- 原候选 GLB：spatter f03be9c18ee9c9e2f2e7bba6017536efc82067b218c72d1b7aed426c48a34ff2；travertine b98d97ae9575d6bb5e3848338aa2dae36a9dbe75118ebd1ab83bd6f94766f46d。
- 全部 44 个所用本地输入及 hashes 见 input-manifest.json；未把 lean commit b45f2ded… 当作新几何或另一次 QA。

本研究独立读了两个原 brief、原 config、reference ledger、两个 generator、现有 source measurements 与其测量代码，并用 Python 标准库重新解码两个 GLB 的 POSITION 二进制。节点无 transform，按 glTF(x,y,z)→Blender(x,-z,y) 量出 bounds，与原独审精确吻合。独立结果见 independent-readonly-measurements.json。没有开 Blender 或另导出文件。原协调分析在独立阅读后仅用于核对；本报告新增的半径不可兼容证明、未消费 config、profile station/segment 差异及局部测量限制均直接来自原文件。

## Primary 与视觉证据能证明什么

- NPS Spatter Cones：https://www.nps.gov/places/spatter-cones.htm 。本次打开原 primary 文字；其形成机制支持中心小喷口附近熔融喷溅物黏合成凝聚墙体。独立查看原 Jacob W Frank 照片像素，看到宽底、粗糙不均匀上壁与起伏口沿。照片无本资产的精确比例尺，不支持 2.5、2.8、3.7 或 0.65 m 的科学精度。
- NPS Travertine Terraces：https://www.nps.gov/yell/learn/nature/hydrothermal-features.htm 的 Travertine Terraces 段。本次重新打开文字；碳酸钙沉积支持连通的浅阶地形态。独立查看实际 travertine.jpg，不是 geyser 图：宽、浅、细薄弯曲边缘与多级连通层架。没有测量尺度，不能从照片推出五级、0.7 或 0.18 m。
- 两张概念图的全部面板已看；spatter 概念有高直沟槽，travertine 概念有厚圆筒式阶梯。原 brief 明确要求纠正这些点，不能为了尺寸而回退到概念的错误形态。
- 两件最终无损 contact-sheet 的八个面板及各自 bottom 原图已看。现候选有可识别开口与凝聚起伏、五个浅池及连续侧壁。这里只用来判断返修风险，不重新授予 visual PASS；未逐张重做整套验收。

## 原字段、实际值、含义分层

共通：原 scale.accuracy 明写“illustrative, not measured specimen/site”。art_target_bounds 是目标，不是已定义 hard maximum；没有容差。units、轴向、bottom contact at z0、静态不透明无贴图、禁止概念当科学证据等是明确条件。max_triangles=14000、max_materials=6、max_primitives=30、max_glb_bytes=1000000 和零贴图是明确硬上限。两件没有类似 leaf_length_range 的尺寸 hard range；这不等于无须达到目标，也不等于可私设容差。

### Spatter r004

- bbox 目标 XYZ = [7.8,7.4,2.8] m；实际 [7.924457311630249,7.465818405151367,3.1593129634857178] m；偏差 [+1.5956%,+0.8894%,+12.8326%]。
- outer_radius_m=3.7：source 外侧基准 profile r=3.70，之后乘角向 anisotropy、加焊接起伏，再 voxel remesh/decimate。实际围绕现 origin 的最大半径 4.288108883559628 m。原文未定义最大、平均或在哪一圈测；不能把此参数自动当 hard radial maximum。
- vent_radius_m=0.65：原 generator 没有读取该值；邻近 profile 是 (r,z)=(0.64,0.32)、(0.69,1.0)，crest 附近为 (1.03,2.47)。原文也未定义测量高度、平面、面积等效半径或均值。现有 QA 没有真正测出“实际 vent_radius=0.65”，不可补造该结论。
- rim_height_m=2.5：原 profile 峰值基准 2.47，非 2.5，且叠加角向起伏、lumps 与焊接 packet。现独审的 rim_height_range=[1.801505804,3.159312963] 只是 r∈(0.6,1.7)、z>1.8 的空间筛选，包含墙体，不能当真正 crest 环的最低/最高或均值。
- vent_floor_m=0.18：原前两圈 nominal z=0.18，但同样受高度扰动、remesh 和 grounding 影响。现独审 r<0.4 且 z>0.02 的点集 z=[0.156257197,0.255279034]，不是已识别平坦 floor 的严格标志。原 brief 没定义允许粗糙度或均值，建议新几何直接保护可测 floor datum=0.18。
- angular_segments=64：原构造 64 rays，属于构造拓扑值，不要求 remesh 后仍为 64 最终顶点。
- radial_profile_segments=14：原 prof 恰有 14 stations，但只有 13 相邻径向 strip intervals。字段名与实现计数不一致，原 QA 未解决。建议下一版保守按 14 intervals 实现 15 stations（新增一个插值 station），而不是把原 13 偷换成 14；新澄清文明确计数法。若保持 14 stations，则必须明确这是更名澄清且不可宣称满足 14 intervals。
- welded_lobe_groups=9：原 centers 列表确有 9 个角向组；每组 2 层 analytic relief、3 个实体 packets，最终联合成一体，不是必须只剩 9 个可见球。
- 重要实现问题：两个 spatter 函数没有从 c['parameters'] 读取这些几何尺寸或计数；当前 config 并非尺寸控制器。只更新 JSON 无效。

### Travertine r002

- bbox 目标 XYZ=[10,18,4.7] m；实际 [10.105728149414062,18.59927749633789,4.064496040344238] m；偏差 [+1.0573%,+3.3293%,-13.5214%]。
- width_m=10、length_m=18：现 source 总 nominal run 为 18；实际宽度函数、中心线摆动和 y scallop 扩大外包络。没有独立定义 nominal 与 final width/length 的差别。新几何可以直接令 final envelope 达到两者，无须放宽。
- terrace_levels=5：实际五个主要平底为 [0.85,1.55,2.25,2.95,3.65] m，四段高差都是 0.7 m；不是五段 rise。GLB floor-material 高度 histogram 独立重算吻合。边缘微带 0.005195 m 不是额外楼层。
- pool_rim_relief_m=0.18：source 横向 lip 的基准 dz=.18；overflow Gaussian 下凹最大幅值 .15，side rim 额外 .20 及 ±.035 扰动叠加。横向中心截面实际 relief 约 .171443/.177992，受 saddle 尾部影响。不能写“每个口沿顶点严格高于 floor 0.18”；原 QA 已按名义主 lip、排除 saddle 解读。这一名义局部参数不等于总高，也不等于每处侧缘最大高度。
- cross_segments=28：每 row 29 vertices，即 28 横向 intervals，构造匹配。
- 任意五个平底仅约束相对高差 4×0.7=2.8 m，并未冻结最低 floor 对底面的高度。原 floor=3.65-level*.7、side rim .20、扰动 .035 是实现常数，不是用户或原 brief 冻结的数字。
- 重要实现问题：travertine 函数同样没有读取 c['parameters']；width、length、levels、rise、lip、cross count 全靠硬编码。下一版必须绑定配置而非在文档中假装已参数化。

## 可直接实施的最小几何返修

### T1：推荐的最小 travertine 路径

1. 新 revision 与专用 generator 读取全部原参数，保留 5 个不等长浅池、28 横向段、同样材质与 scallop/overflow 表达；不改原 r001/r002 文件。
2. 在构造 top rows 后、solid_grid 生成底面/侧壁前，用 H=4.7-max(top_z) 给每个 top vertex 加 H；底面仍由 solid_grid 落在 z=0。现几何 H=0.6355039596557619 m，是算例，重建时应从实际新 top extrema 重算，不能固定照搬。
3. 当前算例新平底为 [1.48550396,2.18550396,2.88550396,3.58550396,4.28550396] m。四段 rise 与所有原有局部 relief 均不变，总高实为 4.7；原 3.65 并不是冻结条件。真实侧壁延长，不能单把整物体上移并留悬空底面。
4. 完成所有 XY scallop 后，按实际 envelope 做 XY-only 归一化与中心平移，使范围 X=[-5,5]、Y=[-9,9]。当前因子为 .98953779996346、.9677795281856575。Z 不缩放，所以 .7、.18 不受影响。底面与侧壁共用顶点映射，不引入重叠壳。
5. 独立看 side/rear/reversehero：必须仍是浅而宽的池面与连续斜坡，不能变成厚高 parapet、孤立堆碗或概念图的圆筒。

T1 是几何可行性方案，不是新的美术通过。若 reviewer 认为现有 side-corner .18+.20 叠加不能符合“thin rims”，可走更严格 T2：侧缘/横唇相接处用 max 而非相加，所有非-saddle rim relief 统一不超过 .18；最高 floor=4.52、最低 floor=1.72、四差 .7。随后重算每个相接处和 envelope。这会比 T1 多改局部侧缘，不是现在必需，更不能偷称原文已有 .18 hard maximum。

禁止用全局 Z 比例 1.15635492 拉高：会把 rise 变 .80944845 m、lip 变 .20814389 m。视觉相近也不合原数值。

### S1：推荐 spatter 路径，限局部与包络

1. 新 revision/专用 generator 绑定配置：64 angular rays、14 radial intervals（15 stations）、9 角向 lobe groups。新增 station 仅插值细分现 profile，不复制一颗物体来凑组数。维持凝聚一体、不透明、单个窄开口。
2. 先明确语义 append-only 后再生成：3.7 为无变形参考径向 foot；.65 为新设计开口 crest 内缘的 nominal 平均水平半径（现原文件没有指定测量高度，这个定义须写出）；2.5 为 64 等角截面 crest 高度均值；.18 为中央 floor datum。它们不是 primary 测得的自然尺度。
3. 为 crest 设零均值不规则高度函数 q(a)，令 z_crest(a)=2.5+q(a)，最高 q=.3，即最高 2.8。保留起伏而非把每点截平在2.8；最大峰设在 crest 上，不靠一个隐藏顶点凑 bbox。构造 floor 平区 z=.18 并保护它；开口的平均半径 .65、向下收拢至 floor 的内壁保持非自交。若更新开口尺寸相较旧版变小，必须在 top/clay 检查其仍清楚可辨。
4. 只调整过高 crest/upper-wall 的起伏振幅与 packet Z 支撑；9 组焊接形态与外侧宽 foot 尽量保留。限制外侧起伏不超过最高 crest，并用平滑连接避免裁平平台。不要把 entire Z 乘 .88626864，否则 nominal rim→2.21567160、floor→.15952836。
5. outer-radius 不当最终最大半径：参考 foot r=3.7 后做有界方向变形，达到最终 X=7.8、Y=7.4。可在 r=3.7 的参考形上设 X 轴基础伸长 7.8/7.4，再把不对称变化绑定到固定轴向 envelope；内开口保持其独立 .65 半径，不给它同乘全局 XY 因子。将外圈与内圈用连续径向权重过渡，不变更曲面连通性。现旧版 XY 只超约1.6%/0.9%，因此不需要大改整体轮廓。
6. 若保留 voxel union，remesh 会扰动 floor、crest 和 bbox。优先保护 datum/landmark 或改为不会扰动这些边界的连续单一表面构造。不能 remesh 后仅以“生成前恰好等于”交差。最终由实际新 Blend/GLB 反量并迭代真实顶点；不动 camera、scale metadata 或 tolerance 掩盖误差。

S1 是明确可实现的数值构造示例，未生成、未证明可见质量/预算已过。其不确定性在施工与后处理保真，不在用户需要选择一个真实场地尺寸。至少 .65 的测量高度和 crest 统计量须先记录，不能由每次 reviewer 临时选最有利点集。

## 建议的透明澄清文本（草案，未采纳，未改原 freeze）

新建同目录外/新 revision 下的 specification-clarification-v002，parent 指向以上原 brief hash、原 QA hash。内容建议：

“原 original-v001、全部原候选及失败/阻塞记录保留不变。本文件只规定后续返修候选的可执行量法，不追认 r004/r002。所有尺寸为艺术构造单位，不是实测 specimen/site。最终 geometry 的 Blender XYZ 包络以原 art_target 数值作为修复目标；不新增百分比艺术容差。以实际 source/GLB 顶点测量，允许的数值比较 epsilon 应预先记录并限于坐标序列化舍入（建议 absolute 1e-5 m，理由是本资产量级 float32 精度；这不是 ±1e-5 m 的自然测量准确度）。minZ=0，XY footprint 的 bbox 中点为 origin。明确预算、形态、材质、视图、复建和独审条件保持原样。”

“Spatter：outer_radius_m 是不对称造型前的参考径向构造值，不是最终最大半径。否则与原7.8 m X包络数学矛盾。rim_height_m 指以64等角截面取得的实际 crest 高度算术均值；峰值与最终总高另测。vent_radius_m 指这同一 crest 开口内缘的等角水平半径算术均值。vent_floor_m 指中央水平 floor datum。为便于复核，生成器须记录语义区域对应与测量路径，独审从最终几何重建截面，不接受只读该记录即通过。radial_profile_segments=14 按相邻环间 interval 计数，使用15个profile stations；其他闭合封底面不充数。所有维度在后处理后的新几何中证明。”

“Travertine：terrace_levels=5 表示五个主要平底，rise_per_level_m=.7 表示相邻平底四个差。pool_rim_relief_m=.18 是横向主唇的名义 offset，overflow saddle 与侧缘连接位置必须单列实测，不伪称所有 rim 点都为 .18。floor 对模块底面的 offset 未冻结，可通过连续实体 substrate 调整总高，而不改变四段 rise 和局部唇口。width_m、length_m 与本修复 final XY envelope 一致。counter/accepted 状态不得因这份文本变化。”

选择依据：保留原数值并消除测量欠定义；对 radius 明确记录数学冲突；对 rim 的名义含义同时受“uneven rim / small overflow saddles”原文字约束；对未冻结 substrate offset 利用真实自由度，不更改局部尺寸。它不是从旧输出反推一个可容纳旧输出的阈值。若不愿采纳某项名义解释，先用更严格真实几何满足数字，而不是扩大 tolerance 或把旧文件改绿。

## 后续最小执行与停止条件

1. 返修 worker 先读本报告及原 brief，以新 append-only clarification 固定所选量法；不得修改 original-v001、原 source revision 或原 QA。
2. 按 T1/S1 做新几何，两个新 revision 各自记录新 generator/config/Blend/GLB SHA 与 parent。全局重作业仍排队 flock /tmp/lowpoly-production-blender.lock 且 Blender --threads 2。当前不需要重跑旧 fullQA。
3. 先做小范围 exact proof：全部XYZ bounds/minZ/footprint中心；spatter crest语义截面、开口radius、floor、64/14/9构造计数；travertine五平底/四rise、按区域分开的lip/saddle/side-relief、28横向段。既测source，也独立解码最终GLB，输出 max residual、测量位置、方法，而不是只写PASS。
4. 数值与连通性先满足后再做新的完整交付：新exact九视图、预算/格式/原点/非流形等检查、source重开、两个真正的语义复建及runtime parse。新独立 reviewer 以已固定的新bytes和原freeze+clarification作 fresh QA。旧技术/视觉/事实/runtime PASS不能继承为新几何的PASS。
5. GPU和scene仍未做；不能拿CPU图或Node parse替代。没有用户/发布批准，也不把这两件计入通过、发布或1000计数。
6. 若新几何仍失败，保留失败并做局部修复。只有发现真实用户要求彼此冲突，或返修必然损失已明确的设计意图，才需要用户选项；一般内部名义参数无需用户动作。任何上传/提交/PR/合并/上线按父任务与平台审批执行，本报告不授予这些操作。
