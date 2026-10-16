# 博物馆环境研究与科学边界

[English](museum-research.md) · 简体中文补充

检查日期：2026-10-16。博物馆源码快照：[`dbdb0a3`](https://github.com/s010s/prehistoric-animal-museum/commit/dbdb0a3fc1ec82c586f8aaa45667aac76c424669)（2026-10-07）。这是原创总结及来源链接，不包含第三方模型、参考图片或下载的源码全文。

## 当前项目需要什么

- 项目主要面向2–6岁儿童与陪伴家长，强调平静观察，已有艺术复原免责声明。因此环境宜温和、可辨认，卵窝/倒木不必附加危险叙事。[README](https://github.com/s010s/prehistoric-animal-museum/blob/dbdb0a3fc1ec82c586f8aaa45667aac76c424669/README.zh-CN.md)
- 当前生产世界由远景全景图、PBR地表及真实世界坐标的地形、河岸、水体、植被/道具构成，并非统一lowpoly。新包应先独立展示；正式接入另验风格、尺度、遮挡与性能。此判断来自源码，未对线上页面逐屏视觉验收。[环境说明](https://github.com/s010s/prehistoric-animal-museum/blob/dbdb0a3fc1ec82c586f8aaa45667aac76c424669/src/scale-encounter/environments/land-biomes/README.md)
- 遗留主题ID gobi 表示Iren Dabasu有植被的河漫平原、辫状河道与暂时水塘；不要按今日戈壁画空沙丘。双冠龙使用Kayenta季节河谷；另有独立石炭纪煤沼、冰期草原、海洋及天空主题。[注册表](https://github.com/s010s/prehistoric-animal-museum/blob/dbdb0a3fc1ec82c586f8aaa45667aac76c424669/src/scale-encounter/environment-theme-registry.ts)
- 猛犸象已有约4.5万年前东阿尔卑斯区域教学综合复原锚点：无冰河谷、少量季节残雪、远处高地冰体。本包没有冰期专用植被，不能用中生代植物凑配。[科学锚点](https://github.com/s010s/prehistoric-animal-museum/blob/dbdb0a3fc1ec82c586f8aaa45667aac76c424669/src/scale-encounter/environments/glacier/scientific-anchor.ts)

## 首包十类

详细形态、用途、尺寸建议、禁用误导与证据ID见[asset-briefs.json](asset-briefs.json)。

| 资产 | 必须保留的辨识结构 | 允许表达 |
|---|---|---|
| 层理岩崖 | 连贯层理、软硬层错退、厚实体 | 跨时代沉积岩概念 |
| 天然石拱 | 贯穿拱孔、非对称支脚、厚拱顶 | 跨时代侵蚀地貌概念 |
| 针叶乔木 | 通直主干、分层侧枝与冠隙 | 侏罗纪—白垩纪概念森林 |
| 苏铁形植株 | 矮粗干、刚性羽状放射叶冠 | 中生代植物形态概念 |
| 地被蕨丛 | 近地弧形叶轴、羽片、少量卷叶 | 中生代蕨类形态概念 |
| 木贼群落 | 分节茎、节点、轮生细侧枝 | 中生代湿润边缘概念 |
| 连根倒木 | 横向断干、根盘、自然折裂 | 中生代种子植物死木概念 |
| 恐龙卵窝 | 低地窝、卵群、中央空隙 | 晚白垩世窃蛋龙类形式启发的教学示意 |
| 三趾足迹泥板 | 凹痕、挤压边、错步方向 | 中生代行迹教学示意，不指定属种 |
| 石炭纪鳞木 | 柱状干、菱形叶枕、顶部二歧分枝 | 晚石炭世煤沼，单独主题 |

十件通过结构和用途区分，不按换色/缩放计新类别。岩崖是实心层理体，石拱以贯穿负空间组织几何；针叶树和鳞木采用不同的分枝语法。画廊可并列展示，但应标“跨时期资产目录”，不能声称它们同地同时共存。

## 六条科学边界

1. **古老类群不等于不变的现代种。** 现代蕨、苏铁和针叶树可作形态参考；不能因此命名为某现代种在中生代的原样复刻。[NHM恐龙花园](https://www.nhm.ac.uk/discover/how-to-grow-a-dinosaur-garden.html)、[NHM蕨类](https://www.nhm.ac.uk/discover/ferns.html)
2. **相似叶冠不是同一植物。** 苏铁不是棕榈，也不能把苏铁与本内苏铁繁殖器官随意混装；小型木贼整体放大不等于石炭纪芦木。[Smithsonian苏铁](https://qrius.si.edu/taxonomy/term/11978)、[NHM木贼](https://www.nhm.ac.uk/discover/jurassic-scavenger-hunt.html)
3. **鳞木需要自己的结构。** 菱形纹理是叶枕，二歧分枝区别于针叶树侧枝；连根倒木的现代根盘结构不应套给鳞木。[PRI叶结构](https://www.digitalatlasofancientlife.org/learn/embryophytes/tracheophytes/leaves/)、[PRI分枝](https://www.digitalatlasofancientlife.org/learn/embryophytes/tracheophytes/branching/)、[Smithsonian煤沼研究](https://repository.si.edu/bitstreams/27b279ae-6030-4d71-93ba-1b0a713e7399/download)
4. **岩石年龄不等于地貌年龄。** Kayenta沉积记录支持河流和洪泛环境，不证明当时已有今天的峡谷。天然石拱可由后期节理和侵蚀形成，不绑定博物馆化石地点。[NPS Kayenta](https://www.nps.gov/zion/learn/nature/kayenta.htm)、[NPS石拱](https://www.nps.gov/articles/nps-geodiversity-atlas-arches-national-park-utah.htm)
5. **卵窝不能靠邻居认主人。** 本包不命名“巨盗龙的巢”，不宣称所有恐龙卵型、排列和巢材一致；完整平静的卵窝是教学设计。[AMNH恐龙卵](https://www.amnh.org/dinosaurs/dinosaur-eggs)、[AMNH关联标本](https://www.amnh.org/research/paleontology/vertebrate/fossil-preparation/follow-the-specimen)
6. **三趾足迹不等于某个属的签名。** 默认是新鲜泥面凹印；不做凸起脚趾，不凭形状指定双冠龙，也不从艺术步长推算速度。化石版须区别真足迹、底层变形与天然铸模。[NPS足迹](https://www.nps.gov/zion/learn/nature/fossil-footprints.htm)

## 资产声明与待验证事项

建议声明：“有科学资料参考的原创风格化模型。形态经过简化，颜色与部分细节为艺术设计；不代表某个物种、地点或时刻的精确复原。”

颜色、数量、磨损、精确尺寸和布局均属艺术选择。升级为科学复原需要具体分类、层位、地点、尺度证据及对缺失部分的明确推断。博物馆/大学科普能支持概念包，不能独自替代完整证据链。

首包尚不覆盖海洋生态道具、天空/海岸专用物体、冰期植被或完整生态群落。发布时按本仓LICENSE/ATTRIBUTION标注原创资产；参考机构不因此成为模型作者或背书者。模型导出成功也不等于已通过博物馆生产集成验收。

