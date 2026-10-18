# batch-04 — next-round maker task; not yet dispatched

**当前状态：线上79已确认（main eb9153eab06f7e95235eac30611b731c8178ffb7）；16/18旧错批QA无效，16新线程01a150f1-ab04-71eb-af42-0a2fc9450036、18新线程01a150f5-9dfe-77e0-bd27-6cbc89942035审正确source；17模型QA PASS；19新QA运行、20模型QA PASS、21制作中。错批报告不计PASS，最新state/派发证明覆盖历史描述。**

**当前状态：线上67已确认（main ccf48bb446dd4d0a710ab14dfc05d6fbf7064cdb，PR9/Pages/public Chromium均PASS）；13–15全模型QA PASS、67→79发布容量失败待恢复，不影响已完成67；16–17候选完成/QA运行无结论，18独占制作。以最新state和父任务派发证明覆盖下方历史空claim/未派发/旧线上数量。**

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

Only inventory IDs: calceola, favosites, opabinia, choia.

CI 已由父任务确认完成于 main `643534830397824dfd46990485bd16ad66ecf9ce`；这不等于本轮已派发。先由父任务统一更新本目录 state.json 的独占 claim 和实际 task/thread ID，才能开始。本 planner 不生产、不创建制作会话、不合并 main。

制作必须 GPT-6.1 Sol medium，授权云环境。读 README.md、queue.json、reference-policy.json、state.json 及每项冻结的 brief/config/references。延续 v002 自然精致、可信比例、柔和衔接和适度卡通；80–240px 普通观看，约480px 中近距离，不要求显微科考。

每项上限 14,000 三角形 / 1,000,000 GLB bytes，不是目标。通常争取约100–500KB，更小同样可；增加面数须有轮廓、比例或衔接的明显收益，记录收益即可，不为了软目标破坏造型。≤6 materials / ≤30 primitives；最多1张≤256px原创贴图，编码总计≤65,536 bytes、解码预算≤524,288 bytes，不以大贴图凑精细。

可靠基础参考支持可辨识形态即可合理风格化继续。来源访问是继承历史，不冒充本轮已重读；仅查阅不赋予复制媒体权利。模型/贴图原创，不搬运外部网格或图片。微观解剖、精确齿/板/羽/分枝数量、未保存软组织、实际尺寸和运动机制不是门槛。真实基本身份矛盾、无来源的属级强断言或无权使用的第三方素材需修正；优先缩窄 inspired-by 标签，不进行无限研究。

使用届时最新 main 的独立 branch/worktree，携带本规划目录及必要当前 helpers；不整体挑入旧制作分支，不改CI/无关站点代码。所有制作、重建、预览与QA证据按本批/ID/revision/attempt隔离。默认协调池1 worker×2 threads，三个批次不能各自抢占全机。

每项交付：可编辑Blend、独立GLB、确定性generator/config及依赖哈希、中英metadata与来源/不确定性/许可/署名、可选原创贴图、透明封面、hero/reversehero/front/side/rear/top/clay/silhouette八个固定QA视图，以及实际GLB多角度loader/功能渲染/多实例场景证据。零转台序列；有问题才加针对性视角。记录source reopen、两次语义重建、Khronos/project checks、顶点/三角形/材料/primitive/字节/贴图/场景实例计量；软件渲染不冒充物理设备性能。

冻结精确commit与GLB/brief/reference/evidence哈希，正常push本批分支，回报父任务所有路径。独立QA必须由父任务新派GPT-6 Luna xhigh，制作自查不能替代。一次汇总QA、最多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节反复返工。修复新revision/attempt，旧verdict标stale。

通过全部必需QA后用户已授权直接推送/合并，无需逐模型审批；父任务串行整合发布。这里不自行合并main，不上传Google Drive、不改权限、不强推。

| ID | 原始中英名称 | 选择理由 / 基本形态 | 计划目录 |
|---|---|---|---|
| `calceola` | Calceola（拖鞋珊瑚） / Calceola slipper coral | 单体拖鞋杯与单盖提供低矮有盖珊瑚，区别于块状和枝状群体。 扁拖鞋形杯体与一个半圆盖的基本关系；盖缝留可读层次。开合姿态和软组织是美术选择，不作活动机制精确复原。 | `items/calceola/` |
| `favosites` | Favosites（蜂巢床板珊瑚） / Favosites honeycomb tabulate coral | 蜂巢状紧排多边管群体，提供厚实圆块礁体，与链状珊瑚不同。 圆块群体和紧邻多边管口形成蜂巢节奏；选择少量足够可读的管口，不填满微小孔阵列。宏观蜂巢形态足够，具体种级管壁微孔不必复原。 | `items/favosites/` |
| `opabinia` | Opabinia（五眼古生动物） / Opabinia five-eyed swimmer | 五眼、单根长吻和侧叶形成游泳主体；区别于已有鱼、蟹、双瓣甲动物。 五个眼部突起、单根末端抓握式长吻、低矮侧叶体要清楚；精确节数、腹侧细肢和软组织可简化。 | `items/opabinia/` |
| `choia` | Choia（放射盘状海绵） / Choia radial-disc sponge | 扁盘与放射骨针丰富海底低矮层，不是海胆的球壳长刺变种。 低扁椭圆中心与伸出式放射骨针轮廓；有秩序疏密，微观骨针计数/骨架截面不作为门槛。 | `items/choia/` |
