# 一手来源与证据边界

研究日期：2026-10-16。只把 Blender 官方文档、艺术家本人的站点与本人发布的教程用作依据。未下载任何第三方模型、纹理、色板或 .blend 文件。本文建议是综合后的原创美术工作方法，不是对某位艺术家的逐字复述，也不声称已经看完视频。

## Blender 官方资料

1. [Decimate Modifier](https://docs.blender.org/manual/en/3.3/modeling/modifiers/generate/decimate.html)
   - 官方可检索正文说明：Decimate 以尽量少改变形状的方式减少顶点/面；对已经精心、经济地建模的网格通常不是必需步骤；更适合复杂建模、雕刻或细分结果的简化。
   - 用在本项目：反对把减面当作低多边形美术设计的替代；雕刻后减面可以使用，但必须重新验收。
   - 证据边界：读取到的是官方索引中的 3.3 版正文；直接页面抓取返回 402。概念参考可用；不据此断言当前安装版本的 UI 或 Python API。

2. [Triangulate Modifier](https://docs.blender.org/manual/en/5.3/modeling/modifiers/generate/triangulate.html)
   - 官方可检索正文说明：可把四边面和多边形变成三角面；四边面支持不同对角线策略，n-gon 有不同分割方式。
   - 用在本项目：主动检查最终分割方向，尤其非共面四边面；三角化不是制造所有可见面纹理的理由。
   - 证据边界：索引返回 5.3 文档，不能由此推断生产环境版本或该版本的发行状态；直接抓取返回 402。执行时使用实际安装版本帮助。

3. [Mesh Structure / Shading](https://docs.staging.blender.org/manual/en/latest/modeling/meshes/structure.html)
   - 官方索引说明 flat 与 smooth shading 的法线插值差异，并支持按对象或按面配置。
   - 用在本项目：棱面通过几何与法线共同表达；允许有意的混合着色，不把所有低多边形资产强制成同一种表面。
   - 证据边界：仅官方检索正文可用；直接抓取返回 403，不继续尝试绕过。没有依据该页操作任何账户或下载。

4. [Mesh Clean Up](https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/cleanup.html)
   - 官方索引列出 Delete Loose、Degenerate Dissolve、Make Planar Faces、Split Non-Planar Faces、Split Concave Faces 和 Merge by Distance。
   - 用在本项目：把不共面大面和退化几何纳入显式检查；不能把这些工具全选一遍当作自动美术验收。
   - 证据边界：检索正文可用，直接抓取返回 402；工具名称和概念参考不代替版本内的操作验证。

5. [Blender 4.0 Color Management Release Notes](https://developer.blender.org/docs/release_notes/4.0/color_management/)
   - 一手文档确认 AgX 在 4.0 新文件中替代 Filmic 成为默认视图变换，并改变高亮区域的色彩处理。
   - 用在本项目：固定并记录视图变换与曝光，不能用不同版本默认值比较色板。

## 艺术家本人资料

6. [Polygon Runway: Become a 3D Illustrator](https://polygonrunway.com/p/become-a-3d-illustrator)
   - Roman Klčo 本人的课程纲要把建模、灯光、纹理绘制、构图和环境光组合为连续的创作流程；森林与古代遗迹都是相关案例。
   - 用在本项目：独立资产需要同时在隔离视图与场景组合中检查；成图质感不只来自面数。
   - 证据边界：读取的是公开课程纲要，没有访问付费内容或下载示例场景。

7. [Polygon Runway: Enchanted Forest](https://www.youtube.com/watch?v=stdVW3kmMbw)
   - 艺术家本人发布的教程公开描述包含地块、树桩、蘑菇、草与石块，并说明可用于等距插画或游戏资产。
   - 用在本项目：作为环境类别的组合案例与后续人工学习入口，不复制其资产或场景。
   - 证据边界：已读公开简介，未取得完整视频逐帧内容；不把具体操作步骤归因于视频。

8. [Polygon Runway: Better Blender Low Poly with a Simple Trick](https://www.blendernation.com/2024/12/11/better-blender-low-poly-with-a-simple-trick/)
   - 文章署名为 polygonrunway，说明教程针对低多边形模型的平面保持与异常渲染。
   - 对应本人视频链接：[YouTube](https://www.youtube.com/watch?v=ahhLRwTxtPk)。
   - 用在本项目：把非共面面片作为常见外观故障检查。
   - 证据边界：只读取署名文章说明；视频读取失败，没有声称观看到具体技巧。

9. [Grant Abbitt Course Library](https://www.gabbitt.co.uk/courses)
   - 本人站点描述了通过简单雕刻流程制作低面数岩石的方法，并直接链接其 [Realistic Low Poly Game Assets — Rocks](https://www.youtube.com/watch?v=WQHBSgRQ50o)。
   - 用在本项目：低面数模型可从不同建模路径得到，不能把“原创手工”误解为禁止雕刻或程序辅助；最终形体仍要有设计。
   - 证据边界：课程目录与视频标题可验证；未取得完整教程内容，不照抄其岩石。

10. [Imphenzia: PixPal Palette Texture](https://imphenzia.com/imphenzia-pixpal)
    - 创作者本人说明了以小型共享色板纹理和共享材质给整场景配色的方案，以及 UV 选择颜色和材质参数的思路。
    - 用在本项目：借鉴共享色板工作流的概念；自行设计全部色值、纹理与材质。没有下载该资产包。一个材质也不能脱离目标引擎条件保证固定 draw call 数量。

11. [Andrew Price: Lighting Mastery Series](https://www.blenderguru.com/posts/2019/lighting-mastery)
    - 本人教程公开页面按方向、光源大小、颜色、可读性、强调五部分组织；明确讨论阴影软硬、曝光、填充光与主体分离。
    - 用在本项目：测试灯光首先用于检查体积、接触与可读性；展示灯光再负责气氛，避免强效果遮掩结构问题。

12. [Andrew Price: Understanding Composition](https://www.blenderguru.com/posts/understanding-composition)
    - 本人文章指出构图并非仅有三分法，关联结构、焦点与平衡的学习。
    - 用在本项目：环境为动物展品提供空间和视线引导；所有资产都争当最亮最艳焦点会使全场失去层级。

## 本研究原创综合，不能冒充来源原话

以下是面向本项目的设计决策：128 像素剪影测试、五项评分及 16/20 门槛、三件先行样件、三角数档、60/30/10 起始形体关系、十四色色板和具体反模式修法。它们是可调整的工作约定，不是任何文档或教程给出的通用标准。最终十类资产名单由项目确定，美术构形建议由本研究补充。

## 尚需专项研究

- 博物馆实际展陈年代、地区、目标动物与植被共存关系。
- 具体植物的叶序、枝形、比例和是否应使用现代属种名称。
- 巢穴、蛋、足迹的真实形制、尺寸、数量、排列与证据来源。
- 目标运行时、最小可见尺寸、目标设备、碰撞和 LOD 要求。

在这些问题未明确前，资产可作为明确标注的风格化环境道具制作，不能声称“准确复原某时代生态”。
