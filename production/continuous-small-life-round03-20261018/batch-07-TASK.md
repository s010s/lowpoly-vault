# batch-07 — 仅计划，尚未派发

**当前状态：线上67已确认（main ccf48bb446dd4d0a710ab14dfc05d6fbf7064cdb，PR9/Pages/public Chromium均PASS）；13–15全模型QA PASS、67→79发布容量失败待恢复，不影响已完成67；16–17候选完成/QA运行无结论，18独占制作。以最新state和父任务派发证明覆盖下方历史空claim/未派发/旧线上数量。**

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。Bosworthia/Buthograptus保持标本/藻体片段浅浮雕，不能做未知整株、根系或海底植被；Halimeda是完整藻体概念但不指定无依据现代种。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `syringopora` | Syringopora organ-pipe coral / Syringopora（管风琴珊瑚） | `items/syringopora/` | 分离直立细管与稀疏横桥提供通透管风琴群体，不重复蜂巢块或开放链壁。 以独立竖管和间断横连为主要结构；管口少量可读、连接有生长逻辑。区别于Halysites连续链壁，不能只是换密度。 |
| `vauxia` | Vauxia branching fibrous sponge / Vauxia（分枝纤维海绵） | `items/vauxia/` | 反复分枝的细管海绵提供灌丛式立体空间，区别于扁盘Choia。 自然粗细递变的多次分枝、若干开口尖端和克制纤维节奏；这是海绵不是植物或珊瑚，不用机械等宽管拼接。 |
| `halimeda` | Halimeda articulated calcified thallus / Halimeda 仙掌藻类 | `items/halimeda/` | 关节相连扁平节片链，补充活体概念的钙化海藻形态，与管状/丝状藻不同。 少量自然分枝扁平节片链与窄连接；以来源支持的基础节片形态为界。不指派现代种，不把白垩纪外观相似性当种级证据，不加陆生根叶。 |
| `isoxys` | Isoxys double-spined swimmer / Isoxys（双棘甲游泳动物） | `items/isoxys/` | 双瓣凸甲、前后相对长棘及突眼，丰富水层小型游泳动物。 两片凸甲、前后长棘、可读眼位与内部躯体有连贯关系；区别于已做Canadaspis/Waptia。未保存小肢与软组织可经济简化，不作游泳机制或动画就绪承诺。 |
