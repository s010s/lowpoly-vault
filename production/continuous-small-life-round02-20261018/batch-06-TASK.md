# batch-06 — next-round maker task; not yet dispatched

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

Only inventory IDs: aulopora, thamnopora, hallucigenia, fenestella.

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
| `aulopora` | Aulopora（喇叭网珊瑚） / Aulopora trumpet-network coral | 低矮附生管网与上翘喇叭口丰富岩面覆盖层，不是大块礁体缩放版。 沿基底低矮分枝的管网与向上喇叭口；基底若为展示用必须与可复用珊瑚主体分开。支路数量/颜色可以风格化。 | `items/aulopora/` |
| `thamnopora` | Thamnopora（孔枝珊瑚） / Thamnopora porous branch coral | 粗指状分枝和向外孔口增加海底竖向层次，区别于低矮管网和链状/块状珊瑚。 粗而自然衔接的指状分枝与若干向外孔口；用少量可读开口表达，不堆微孔。原清单needs-specific-reference且来源是床板珊瑚类群页：可靠基础枝状/孔口参考支持即可做inspired-by教学造型，不冒充属级微观验证；没有依据的新属级特征不添加。 | `items/thamnopora/` |
| `hallucigenia` | Hallucigenia（背棘叶足动物） / Hallucigenia spiny lobopodian | 细长体、背棘和软足形成低位行走生物，与硬壳蟹和海星不同。 背面成对高棘与腹侧柔软弯腿方向正确，前后体连续；不采用历史倒置复原，微爪、口器和逐节计数可简化。 | `items/hallucigenia/` |
| `fenestella` | Fenestella（窗格扇苔藓动物） / Fenestella windowed fan bryozoan | 开窗网格扇形增加海底竖向背景，区别于海绵盘和分枝腕动物；是苔藓动物而非植物。 薄扇形分枝与横条构成可见开窗；窗口数量可压缩，孔隙不能全靠大贴图画出。现有来源支持 fenestrate 类群形态，不声称属级微观鉴别已经核实。 | `items/fenestella/` |
