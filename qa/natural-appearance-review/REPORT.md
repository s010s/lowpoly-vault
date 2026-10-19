# 自然观感审查：lowpoly-vault 生物与木材资产

**审查日期：2026-10-19。范围锚点：冻结发布基线 `main` / `de413ef720463a2999516faf92c606bcdf9ab1b7`。本报告及证据只写入独立审查分支，不改资产模型、门禁、网站或 CI。**

## 结论与覆盖

- 冻结基线有 175 件模型；审查范围内有 125 件已发布动物、植物、木材相关资产（另含木材蛀蚀铸型），全部核对了实际模型像素。范围内未找到真菌资产。
- batches 40–50 最新相关候选范围：26 件实际生成的模型/痕迹/用户指定地貌样本完成像素检查；另有 1 件 Tempskya 只有准备文件，未生成模型，标为未检查。
- 总覆盖表为 152 行：151 行有图像检查，1 行待图像证据。发布资产的 GLB 与 Blend SHA256 均与冻结清单匹配（125/125）；候选按实际文件独立计算哈希，含 Belosaepia、Joffrea r002、Diania、Czekanowskia、Lockeia 和自然堤。
- 逐件分类：118 可用、17 建议小幅调整、9 教学标本/剖面呈现、7 遗迹教学模型、1 待证据。分类是自然观感筛查，不是发布验收。
- Batch49 和 batch50 均为暂停/未完成；本审查没有把它们写成已验收，也不把 maker self-check 当视觉通过。

逐件覆盖和准确源文件/版本/哈希/查看图路径：[CSV](coverage.csv)、[JSON](coverage.json)；多视图和缩略图联系表索引：[证据索引](evidence/INDEX.md)；最新 handoff 快照：[JSON](handoff-snapshot.json)。

分类含义：**可用**表示当前缩略图与多视图尺度下自然、可辨，无须为过度细节返工；**建议小幅调整**表示重复、比例或主体结构辨识有具体可改善处；**教学标本/剖面**及**遗迹教学模型**保留其孤立标本或剖面展示语境；**待证据**表示没有可查看模型像素，不能判通过。

## 范围来源与候选批次状态

已发布模型来源为冻结 `origin/main` 基线 `de413ef720463a2999516faf92c606bcdf9ab1b7` 的 `assets/manifest.json` 与文件树；按动物、植物、木材筛出，并把 Teredolites wood-boring cast 作为直接相关木材铸型纳入。候选来源为下表每批最新有效 candidate/handoff ref；实际模型身份同时用逐项源提交、GLB/Blend SHA 和文件路径锁定。用户明确指定 batch49 natural-levee attempt-02，因此虽属地貌仍纳入。Batch50 的 Tempskya 虽未生成，也保留待证据行。该十一个批次没有其他范围内真菌条目。

| 批次 | 最新 ref / commit | 本范围候选 | 当前 handoff 状态 |
|---|---|---|---|
| 40 | `origin/candidate/small-life-batch40-20261018` / `af92e43e0b191f024c72232a40f0fe0f42996fa1` | sidneyia, botrychium, diplocraterion-spreite-burrow | 4 maker candidates delivered; one parent independent QA pending. |
| 41 | `origin/handoff/batch41-20261018` / `a6fabaa18df480e5f73d505162199a51282d25c1` | dicroidium, selkirkia | Maker handoff; independent QA pending. |
| 42 | `origin/candidate/small-life-batch42-20261018` / `658fc5bc4a6e1c7823655ef6388c4bfbe067b67e` | conularia, ophiomorpha-pellet-lined-burrow | 4 maker candidates delivered; parent independent QA pending. |
| 43 | `origin/candidate/small-life-batch43-20261018` / `5163f72e8d32fc4a8eefd2f191dc46d9956feeb7` | kootenayscolex, dillhoffia, phycodes-palmate-burrow | 4 maker candidates delivered; independent acceptance pending. |
| 44 | `origin/handoff/batch44-20261018` / `49b1d6cddd807c89884935974ee2de1bc27bd0fb` | joffrea, yochelcionella | Targeted Joffrea r002 handoff; no second full-batch QA or independent r002 acceptance. Original r001 QA identified Joffrea as the sole MUST FIX; other three item verdicts remain tied to unchanged hashes. |
| 45 | `origin/candidate/small-life-batch45-20261018` / `2ef6f5bca0f63b753dbfa7fa0192f925fb2785c3` | tokummia, protovirgularia-chevron-trail | 4 maker candidates delivered; independent acceptance pending. |
| 46 | `origin/candidate/small-life-batch46-20261018` / `1e100d5b274a40fa264a2aad7c7df884e4381ca5` | eiffelia, pseudofrenelopsis, diplichnites-paired-trackway | 4 maker candidates delivered; independent acceptance pending. |
| 47 | `origin/handoff/batch47-20261018` / `4c9a811685c6fa32d67c8157dccc03c41460c135` | ecphora, pteleoidea | Maker handoff; independent QA pending. |
| 48 | `origin/candidate/small-life-batch48-20261018` / `04a4bee524379fa0022bbfc7133fa9640bfa6fdc` | facivermis, treptichnus-serial-probe-burrow | 4 maker candidates delivered; independent acceptance pending. |
| 49 | `origin/candidate/small-life-batch49-20261018` / `85671289a3f01b89f0be33e13512be736f5a11d7` | diania, czekanowskia, natural-levee, lockeia-resting-trace | Paused awaiting the revised appearance standard; four generated models exist, with no independent QA. This batch is incomplete. |
| 50 | `origin/handoff/batch50-20261018` / `396d9d1fa72fb3b9d1dfb564cec8d760d5401b38` | belosaepia, tempskya | Paused recovery handoff; only Belosaepia reached model generation, no independent review. This batch is incomplete. |

Candidate 几何以独立 source refs 为准；尤其 Joffrea 使用 `origin/candidate/batch44-joffrea-r002-20261019` @ `ed8e178b94fcbbec0a151f44f77113c4f9699c28`，handoff 为 `origin/handoff/batch44-20261018` @ `49b1d6cddd807c89884935974ee2de1bc27bd0fb`。只看 r002，没有复述 r001 已解决项。Batch49 四件是 Diania、Czekanowskia、natural-levee attempt-02、Lockeia resting trace；Batch50 仅 Belosaepia 有模型，其 GLB hash `889bfac2d29dc7887fcad1fea4fa4bf1828ca193f9d2eb267198e1e2c8370d03` 是本审查独立按文件计算。

## 需要优先处理的自然观感项

以下是实际查看图像后筛出的 17 项有限调整建议。它们多是低到中优先级的轮廓/器官辨识改进，不建议无限增加微观细节。每项附确切模型源版本、完整 source commit、单件四视图证据图与最小建议。

### `horsetail-cluster` — frozen-main

- 精确来源：`origin/main` @ `de413ef720463a2999516faf92c606bcdf9ab1b7`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-horsetail-cluster.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-horsetail-cluster.jpg)；常规尺寸缩略图源：`assets/prehistoric/plants/horsetail-cluster/preview-hero.png`。
- 观感：茎节和轮生枝层层等距，整体节奏过于像重复的环状积木。
- 最小改进：保留清晰节轮，只改变少数轮生枝长度、角度和层间距，茎体略向上收细即可。
- 呈现语境 / 优先级：whole organism / watch。

### `favosites` — small-life-round02-20261018 @ abc24f3289df

- 精确来源：`origin/main` @ `abc24f3289df8ccce4ef6fd29c1edb1eeec8253a`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-favosites.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-favosites.jpg)；常规尺寸缩略图源：`assets/additions/favosites/small-life-round02-20261018/preview.webp`。
- 观感：群体由过于一致、蜂窝般重复的管孔构成，远看更像规则拼装的蜂巢块；管孔开口和群体外缘变化不足。
- 最小改进：保留群体轮廓，只让少量管孔直径、倾角和边缘完整度有轻微变化，并柔化最规整的外缘。
- 呈现语境 / 优先级：colony / teaching specimen / targeted。

### `halysites` — small-life-round02-20261018 @ e968fab0544c

- 精确来源：`origin/main` @ `e968fab0544ce2dc41814c057b1f9dca43a2b22d`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-halysites.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-halysites.jpg)；常规尺寸缩略图源：`assets/additions/halysites/small-life-round02-20261018/preview.webp`。
- 观感：链状珊瑚的单元大小和转弯节奏过于均匀，环状管孔有串珠或模块链的机械感。
- 最小改进：不增加微小纹理；仅轻微改变链宽、弯曲半径和局部管孔开口，使链条有自然生长的松紧变化。
- 呈现语境 / 优先级：colony / teaching specimen / targeted。

### `syringopora` — small-life-round03-20261018 @ d0894b30b0fb

- 精确来源：`origin/main` @ `d0894b30b0fbeedb4d946d0d976a4e98abeb5aff`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-syringopora.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-syringopora.jpg)；常规尺寸缩略图源：`assets/additions/syringopora/small-life-round03-20261018/preview.webp`。
- 观感：成束的长管大多平行且间距、粗细近似，重复管件感明显。
- 最小改进：保持可辨识的管状群体，少量改变管径、倾斜角和间距，并加入一两处自然偏转或分叉。
- 呈现语境 / 优先级：colony / teaching specimen / targeted。

### `halimeda` — small-life-round03-20261018 @ 5ea23624b9e5

- 精确来源：`origin/main` @ `5ea23624b9e56ccfc4b6700ef9b54774bc5acd6c`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-halimeda.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-halimeda.jpg)；常规尺寸缩略图源：`assets/additions/halimeda/small-life-round03-20261018/preview.webp`。
- 观感：分段近乎相同大小并按固定节奏排列，低角度下容易像串珠或拼接圆片。
- 最小改进：沿枝条只调整几处节片的宽厚与夹角，并让分枝长度有轻微差别；保留其分节藻体的简洁读法。
- 呈现语境 / 优先级：whole organism / watch。

### `pirania` — small-life-round03-20261018 @ 7327e3cb1022

- 精确来源：`origin/main` @ `7327e3cb1022028ca488ee8afe23c9b221a7628a`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-pirania.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-pirania.jpg)；常规尺寸缩略图源：`assets/additions/pirania/small-life-round03-20261018/preview.webp`。
- 观感：直立管状构件几乎同粗、平行排列，整体更像管束而非有机的海绵群体。
- 最小改进：用不规则但克制的群体基部连接管体，稍变管径、弯曲度和开口高度，保留当前易读的纵向形态。
- 呈现语境 / 优先级：colony / teaching specimen / targeted。

### `leptomitus` — small-life-round03-20261018 @ 18af552039cc

- 精确来源：`origin/main` @ `18af552039cc1573d676601a531ae4c2728cbabb`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-leptomitus.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-leptomitus.jpg)；常规尺寸缩略图源：`assets/additions/leptomitus/small-life-round03-20261018/preview.webp`。
- 观感：单根笔直、等粗、光滑的中空长管在常规视角下像吸管，海绵主体与开口/出水孔的层次不够明确。
- 最小改进：将主体稍微扩成柔和的海绵体轮廓并轻微收尖，加入少量尺寸不同的开口；不需要密集细孔。
- 呈现语境 / 优先级：whole organism / targeted。

### `isastraea` — small-life-round06-20261018 @ fa28e9b97437

- 精确来源：`origin/main` @ `fa28e9b9743702e64170f646884a035e44c9ff88`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-isastraea.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-isastraea.jpg)；常规尺寸缩略图源：`assets/additions/isastraea/small-life-round06-20261018/preview.webp`。
- 观感：珊瑚表面近似统一大小的三角拼片，边界与间距过于规则，带有几何铺砖感。
- 最小改进：保留珊瑚杯/群体结构，仅让少量珊瑚杯尺寸和多边形边界有轻微不规则，避免添加高密度纹理。
- 呈现语境 / 优先级：colony / teaching specimen / watch。

### `odontogriphus` — small-life-round06-20261018 @ 2b897228411e

- 精确来源：`origin/main` @ `2b897228411ee19af3fe9ee830e7bfc45735af46`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-odontogriphus.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-odontogriphus.jpg)；常规尺寸缩略图源：`assets/additions/odontogriphus/small-life-round06-20261018/preview.webp`。
- 观感：整体像一块薄而平的椭圆片，前后端和身体主要区域的起伏差异很弱，动物轮廓容易被读成一片垫片。
- 最小改进：保持扁平保存感；仅加强头端、身体边缘和腹足/躯干部位的浅层轮廓差异，不必加写实小器官。
- 呈现语境 / 优先级：whole organism / flattened fossil / watch。

### `dollocaris` — small-life-round07-20261018 @ 76872051f731

- 精确来源：`origin/main` @ `76872051f73176326d40df9ac4dafbc0dcc9583c`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-dollocaris.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-dollocaris.jpg)；常规尺寸缩略图源：`assets/additions/dollocaris/small-life-round07-20261018/preview.webp`。
- 观感：眼部相对头胸和躯干显得过分突出，第一眼视觉重量集中于两个球形眼点。
- 最小改进：保留大眼的识别特征，略收眼球尺寸或降低高光/凸出度，同时加强头胸外缘的轮廓。
- 呈现语境 / 优先级：whole organism / watch。

### `nordenskioldia` — small-life-round08-20261018 @ 00710386584b

- 精确来源：`origin/main` @ `00710386584b58bdb844e9ea8db5b2c2b0de0920`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-nordenskioldia.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-nordenskioldia.jpg)；常规尺寸缩略图源：`assets/additions/nordenskioldia/small-life-round08-20261018/preview.webp`。
- 观感：枝端叶片呈过分齐整的放射/轮生节奏，叶片轮廓和展开角度重复。
- 最小改进：只让少数叶片尺寸和角度错开，并把枝端中心与叶柄连接做得更自然。
- 呈现语境 / 优先级：whole organism / watch。

### `ctenorhabdotus` — small-life-round08-20261018 @ 15ebe8c0420b

- 精确来源：`origin/main` @ `15ebe8c0420bcb128f5c9496c7c77f96787ab736`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-ctenorhabdotus.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-ctenorhabdotus.jpg)；常规尺寸缩略图源：`assets/additions/ctenorhabdotus/small-life-round08-20261018/preview.webp`。
- 观感：背部板片重复尺度和间距过于相同，轮廓读起来有连续硬壳/装甲块的拼装感。
- 最小改进：只需使数片板的宽度、边缘和覆盖间距有轻微节奏变化，并让头部与躯干轮廓过渡更顺。
- 呈现语境 / 优先级：whole organism / watch。

### `jimaodanus` — small-life-round09-20261018 @ 2c97b832c116

- 精确来源：`origin/main` @ `2c97b832c116ea6aff320ebef9489ec3d4c567ac`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-jimaodanus.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-jimaodanus.jpg)；常规尺寸缩略图源：`assets/additions/jimaodanus/small-life-round09-20261018/preview.webp`。
- 观感：叶簇围绕枝轴的大小和间隔很均匀，个别枝端显得像规则的扇形模块。
- 最小改进：在现有叶簇中加入轻微长短、角度和稀疏度变化，不需增加小叶脉。
- 呈现语境 / 优先级：whole organism / watch。

### `odaraia` — small-life-round10-20261018 @ ad5f8d9a17a0

- 精确来源：`origin/main` @ `ad5f8d9a17a0e1c1afa36ceb92dc2d349e6ee9e4`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-odaraia.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-odaraia.jpg)；常规尺寸缩略图源：`assets/additions/odaraia/small-life-round10-20261018/preview.webp`。
- 观感：躯干过于光滑、等粗的长筒在部分视角中像管子，头胸与尾部的节奏对比不足。
- 最小改进：稍微收窄后躯并让分节/侧叶在少数位置显现，强化头部与身体的连接层次，避免额外密集小节。
- 呈现语境 / 优先级：whole organism / watch。

### `peltaspermum` — small-life-round10-20261018 @ e49e64e8c3ad

- 精确来源：`origin/main` @ `e49e64e8c3ad92eb7a4c962466648a90f6badccd`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/published/pub-peltaspermum.jpg](qa/natural-appearance-review/evidence/multiview/published/pub-peltaspermum.jpg)；常规尺寸缩略图源：`assets/additions/peltaspermum/small-life-round10-20261018/preview.webp`。
- 观感：叶面上的孔洞看起来边缘整齐、尺寸相近，像被打孔的薄片；叶片层次辨识弱于孔洞。
- 最小改进：保留叶片和生殖结构的教学表达；缩减或弱化过于整齐的穿孔，先建立完整叶片外缘及有节奏的叶片分区。
- 呈现语境 / 优先级：whole organism / fossil plant / watch。

### `diania` — r001/attempt-01

- 精确来源：`origin/candidate/small-life-batch49-20261018` @ `85671289a3f01b89f0be33e13512be736f5a11d7`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/candidates/cand-b49-diania.jpg](qa/natural-appearance-review/evidence/multiview/candidates/cand-b49-diania.jpg)；常规尺寸缩略图源：`assets/candidates/continuous-small-life-round17-20261018/batch-49/diania/r001/attempt-01/diania/preview-hero.png`。
- 观感：躯干上的叶足几乎等长、等距且平行，背板也以固定节奏重复，显得像等规格的机械排布。
- 最小改进：仅对少数叶足改变长度、角度和前后节奏，轻微收细身体两端；保留分节和板片的主要特征。
- 呈现语境 / 优先级：whole organism / targeted。

### `natural-levee` — r001/attempt-02

- 精确来源：`origin/candidate/small-life-batch49-20261018` @ `85671289a3f01b89f0be33e13512be736f5a11d7`。
- 查看图：[qa/natural-appearance-review/evidence/multiview/candidates/cand-b49-natural-levee.jpg](qa/natural-appearance-review/evidence/multiview/candidates/cand-b49-natural-levee.jpg)；常规尺寸缩略图源：`assets/candidates/continuous-small-life-round17-20261018/batch-49/natural-levee/r001/attempt-02/natural-levee/preview-hero.png`。
- 观感：r001/attempt-02 的四视图显示一块浅矩形地表上有两道近乎平行、平滑的隆脊/沟槽；像压褶薄片，河岸高地的偏侧性和渐变不明显。
- 最小改进：保留教学用地形小样，只让一侧形成不对称的低堤脊并向泛滥平原缓慢变低；沟槽弯曲和脊线高度稍作自然变化。
- 呈现语境 / 优先级：geomorphology / teaching profile / targeted。

## 教学标本、剖面与遗迹的处理

教学习惯性单体标本、骨骼/壳体或保存剖面不因缺少完整活体、平面展示或切面就自动判错。9 件教学标本/剖面为 Calceola、Goniophyllum、Heliophyllum、Flabellum、Micrabacia、Cystiphyllum、Montlivaltia、Teredolites wood-boring cast、Belosaepia；其中 Belosaepia 的内壳表面偏光滑，作为单体标本保留，并仅建议浅显提示内壳中轴/腔室。7 件 candidate traces（Diplocraterion、Ophiomorpha、Phycodes、Protovirgularia、Diplichnites、Treptichnus、Lockeia）单独归为遗迹教学模型，底板和切面属于展示方式。

## 图像方法与界限

对 151 件有模型的项目，先看常规尺寸缩略图，再看每件四视图联系表；旧资产缺少等效来源多视图时，从其 GLB 渲染四视图并保存证据。逐件 `coverage.json` 记录 source ref、完整提交、模型路径、独立 SHA256、缩略图路径、四视图路径和图片哈希。多视图总览图让每件四个角度可一起比较；天然堤和 Joffrea r002 的单件大图也被直接打开检查。

此次只评自然轮廓、比例、主要层理/器官结构、重复规律、材质与光影造成的观感。低模和儿童 3D 世界允许的艺术化、非写实配色、简化结构均不作为扣分；没有以缺少微鳞片或微纹理判差。体积大小本身不构成优劣：小模型不会因小而自动加分，大模型也不会因大而自动扣分。此次未验证科学复原准确性、网格/材质技术质量、性能或 QA 门禁结果；batch40–48 的 maker handoff 状态依原始 handoff 保留，batch49–50 仍未完成。

## 交付文件

- `coverage.csv` / `coverage.json`：152 个范围条目的逐件结果。
- `handoff-snapshot.json`：40–50 候选/handoff refs、commit、范围 ID 与状态。
- `evidence/INDEX.md`：全部普通尺寸缩略图总览和四视图证据总览。
- `evidence/multiview/{published,candidates}/`：每件独立四视图图像；`evidence/thumbnail-overviews/`：常规尺寸页面。
