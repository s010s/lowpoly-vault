# batch-05 — next-round maker task; not yet dispatched

**当前状态：线上67已确认（main ccf48bb446dd4d0a710ab14dfc05d6fbf7064cdb，PR9/Pages/public Chromium均PASS）；13–15全模型QA PASS、67→79发布容量失败待恢复，不影响已完成67；16–17候选完成/QA运行无结论，18独占制作。以最新state和父任务派发证明覆盖下方历史空claim/未派发/旧线上数量。**

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

Only inventory IDs: goniophyllum, halysites, marrella, proteroctopus.

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
| `goniophyllum` | Goniophyllum（四盖珊瑚） / Goniophyllum four-lidded coral | 方锥体和四片三角盖形成与Calceola不同的有盖单体珊瑚。 方形渐细杯锥与四片三角盖的基本关系；保留四盖可读轮廓，精确隔壁与软体不用复原。不是Calceola换色或盖子数量随意变体。 | `items/goniophyllum/` |
| `halysites` | Halysites（链珊瑚） / Halysites chain coral | 开放环链式直立管壁形成通透礁体，区别于Favosites实心蜂巢群体。 相连直立管壁形成开放曲折环链，主要孔隙用真实结构表达；链路可经济简化，不用大贴图伪造空隙。 | `items/halysites/` |
| `marrella` | Marrella（叉棘节肢动物） / Marrella fork-spined arthropod | 头盾双组长棘和细分节躯干形成新的小型底栖轮廓。 头盾的成组长棘与分节躯干相连；有负空间，不用随机插针代替结构。肢节/刚毛可经济简化。 | `items/marrella/` |
| `proteroctopus` | Proteroctopus（有鳍八腕动物） / Proteroctopus finned octopod | 柔软外套膜、成对鳍和八腕补充海生软体动物，避免全是硬甲。 紧凑外套膜、成对鳍和八条渐细腕；腕根过渡柔和。现有参考是 Coleoidea 类群页，不能把所有本属细节说成已证实；泛化为受 Proteroctopus 启发的有鳍八腕教学道具即可，若添加属级特定特征应另找真实支持。 | `items/proteroctopus/` |
