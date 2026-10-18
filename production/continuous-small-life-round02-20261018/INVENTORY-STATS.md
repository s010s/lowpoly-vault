# 实际1000清单：珊瑚与主分类统计

直接重新计数 `research/prehistoric-1000-v1/inventory.json` 的 `assets[]`，与 `counts.json.category` / `counts.json.total` 逐项核对。本报告不改原inventory，不把研究概念数说成已完成模型数。

## 真正珊瑚：17项

抓取的main（`643534830397824dfd46990485bd16ad66ecf9ce`）assets树未找到这17个ID的GLB；因此这里是17项待制作概念，不能回答成已有17个可下载珊瑚模型。未推送/未公开工作不在观察范围。

全部是 `category=animals` / `subcategory=cnidarian`，但该子类22项还包括5项其他刺胞动物/近缘候选，不能把22全算珊瑚。下表原名取自 `name.en` / `name.zh`，形态差异取自 `distinctness.zh`。三组标题为便于理解的珊瑚类群归纳，原schema没有单独珊瑚子类。

| 精确ID | English name | 清单中文名 | 形态差异 | 原制作门槛 |
|---|---|---|---|---|
| `heliophyllum` | Heliophyllum ribbed horn coral | Heliophyllum（肋角珊瑚） | 弯角状珊瑚骨骼具深圆杯及强放射隔壁 | `needs-specific-reference` |
| `calceola` | Calceola slipper coral | Calceola（拖鞋珊瑚） | 扁拖鞋形角杯由铰接半圆盖封闭 | `reference-ready` |
| `goniophyllum` | Goniophyllum four-lidded coral | Goniophyllum（四盖珊瑚） | 方形渐细锥体，开口周围有四片三角盖 | `reference-ready` |
| `cystiphyllum` | Cystiphyllum blister-cup coral | Cystiphyllum（泡杯珊瑚） | 膨大弯曲单体杯，顶部宽浅且内部起伏如泡 | `needs-specific-reference` |
| `acrocyathus` | Acrocyathus clustered rugose coral | Acrocyathus（簇生四射珊瑚） | 厚群体由紧排长多边杯组成，杯内有放射壁 | `needs-specific-reference` |
| `favosites` | Favosites honeycomb tabulate coral | Favosites（蜂巢床板珊瑚） | 圆群体由紧排直多边形管组成 | `reference-ready` |
| `halysites` | Halysites chain coral | Halysites（链珊瑚） | 直立相连管壁形成开放环链 | `reference-ready` |
| `syringopora` | Syringopora organ-pipe coral | Syringopora（管风琴珊瑚） | 分离直立细管由小横连管间断连接 | `needs-specific-reference` |
| `aulopora` | Aulopora trumpet-network coral | Aulopora（喇叭网珊瑚） | 低矮附生分枝管网末端为上翘喇叭口 | `reference-ready` |
| `pleurodictyum` | Pleurodictyum low cup-disc coral | Pleurodictyum（低杯盘珊瑚） | 小穹盘由数个较大相邻多边杯组成 | `needs-specific-reference` |
| `thamnopora` | Thamnopora porous branch coral | Thamnopora（孔枝珊瑚） | 粗分枝指体表面布斜向外的珊瑚孔口 | `needs-specific-reference` |
| `isastraea` | Isastraea polygon-cup reef coral | Isastraea（多边杯造礁珊瑚） | 低块状群体由相接大多边星隔杯组成 | `needs-specific-reference` |
| `thecosmilia` | Thecosmilia branch-tube reef coral | Thecosmilia（枝管造礁珊瑚） | 直立厚管枝末端为分离深隔壁杯 | `needs-specific-reference` |
| `montlivaltia` | Montlivaltia stalked solitary coral | Montlivaltia（有柄单体珊瑚） | 宽外张单体杯自窄柄升起，杯内放射隔壁密排 | `needs-specific-reference` |
| `micrabacia` | Micrabacia radial-disc coral | Micrabacia（放射盘珊瑚） | 自由小扁盘具强放射肋和低中央杯 | `needs-specific-reference` |
| `flabellum` | Flabellum fan-wedge coral | Flabellum（扇楔珊瑚） | 侧扁楔形单体杯，顶部开口宽如刀片 | `needs-specific-reference` |
| `meandrina` | Meandrina maze-ridge coral | Meandrina（迷宫脊珊瑚） | 圆骨骼丘由连续蜿蜒沟谷及双侧壁分隔 | `needs-specific-reference` |

便于阅读的归纳：四射珊瑚5项（角杯/有盖杯/簇生杯等）、床板珊瑚6项（蜂巢/链/管网/指枝等）、六射珊瑚6项（星隔杯/枝管/柄杯/盘/楔/迷宫脊等），合计17。原表中5项reference-ready、12项needs-specific-reference；这表示规划参考状态，不是完成资产、源许可或模型QA认证。

其他5项 `cnidarian`：`conularia`, `mackenzia`, `burgessomedusa`, `rhizostomites`, `sphenothallus`。保留原有近缘/不确定性措辞，不额外宣布它们的精确分类已定。

明确排除：`fenestella` 的 `subcategory=bryozoan` / `taxon_group=Bryozoa`，是苔藓动物；`choia` 的 `subcategory=sponge`，是海绵；`richthofenia` 的 `subcategory=brachiopod` / `taxon_group=Brachiopoda`，即使英文名含 coral-cone、中文含珊瑚锥形，也仍是腕足动物。三者不是珊瑚。

## 七个主要物体分类

中文直接采用 `registry.json.categories[].name.zh`，并非另创分类。

| category字段 | English / 中文类名 | 数量 |
|---|---|---:|
| `animals` | Animals / 动物 | 700 |
| `plants` | Plants / 植物与藻类 | 101 |
| `terrain` | Terrain / 地形 | 89 |
| `geology` | Geology / 地质体 | 65 |
| `traces` | Traces / 遗迹与生态构造 | 40 |
| `fungi` | Fungi / 真菌 | 4 |
| `wood` | Wood / 木质环境物 | 1 |
| **合计** | | **1000** |

700 + 101 + 89 + 65 + 40 + 4 + 1 = 1000。研究清单最初的status口径为10 existing-candidate + 990 planned；后来的发布进度看release描述符，不擅自把静态inventory历史状态改写成实时发布统计。`plants`包含藻类形态的实用归档，`wood`在本清单只有一项枯木。主分类与子类共有56种category/subcategory组合；不是56个主分类。

动物700项的子类实数（本表仍是实用资产分类，不是系统演化树）：

| subcategory字段 | 数量 |
|---|---:|
| `dinosaur` | 110 |
| `arthropod` | 99 |
| `mollusk` | 71 |
| `fish` | 70 |
| `mammal` | 65 |
| `marine-reptile` | 35 |
| `echinoderm` | 35 |
| `reptile` | 28 |
| `pterosaur` | 25 |
| `amphibian` | 25 |
| `bird` | 25 |
| `cnidarian` | 22 |
| `early-metazoan` | 21 |
| `synapsid` | 17 |
| `sponge` | 17 |
| `brachiopod` | 12 |
| `worm` | 7 |
| `bryozoan` | 6 |
| `graptolite` | 5 |
| `other-invertebrate` | 4 |
| `ctenophore` | 1 |

## 世界、pack与物体分类是独立轴

- `worlds[]`回答“属于哪个世界主题”：本次1000项全部是`prehistoric`，registry中文为史前世界；没有把动物、植物当作两个world。
- `packs[]`回答“编入哪些专题素材包”：实际34个不同pack ID，registry也登记34个。一个条目可属于多个包；pack成员数不能相加当成资产总数，包本身也不增加1000条记录。
- `category` / `subcategory`回答“是什么形态/用途的物体”：例如动物→刺胞动物、海绵、苔藓动物。这是本次七主类统计的键；`taxon_group`另存生物类群，分类不是严格系统树。
- `eras[]`、`biomes[]`和tags也是单独维度，空数组是未指定，不代表到处都适用；相同pack不等于同地点同时代共存。

真实例子：`favosites` 和 `fenestella` 都是 `worlds=[prehistoric]`、`packs=[fossil-reef-and-seafloor-forms]`、`category=animals`；前者`subcategory=cnidarian`且是珊瑚，后者`subcategory=bryozoan`不是珊瑚。共同“古礁与海底形态”包不能改变其物体类别。

来源定位：`inventory.json`的assets逐项字段和顶层counts；`counts.json`第13行category及第63行total；`registry.json`第4行worlds、第13行categories、第975行packs、第2524行axis_notes；原`README.md`的Shared information architecture / Evidence and production gates同样解释这些边界。机器可读重计数结果见同目录 `INVENTORY-STATS.json`。
