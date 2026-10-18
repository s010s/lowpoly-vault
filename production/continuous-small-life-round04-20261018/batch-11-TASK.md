# batch-11 — 仅计划，尚未派发

**当前状态：线上79已确认（main eb9153eab06f7e95235eac30611b731c8178ffb7）；16/18旧错批QA无效，16新线程01a150f1-ab04-71eb-af42-0a2fc9450036、18新线程01a150f5-9dfe-77e0-bd27-6cbc89942035审正确source；17模型QA PASS；19新QA运行、20模型QA PASS、21制作中。错批报告不计PASS，最新state/派发证明覆盖历史描述。**

**当前状态：线上67已确认（main ccf48bb446dd4d0a710ab14dfc05d6fbf7064cdb，PR9/Pages/public Chromium均PASS）；13–15全模型QA PASS、67→79发布容量失败待恢复，不影响已完成67；16–17候选完成/QA运行无结论，18独占制作。以最新state和父任务派发证明覆盖下方历史空claim/未派发/旧线上数量。**

**当前状态：最后确认live43；07–09模型QA PASS、发布适配CI中；10–12模型QA全PASS、release排队；13–14候选完成/独立QA运行，14当前turn未知留空；15独占制作。最新state与父任务派发证明覆盖下方历史空claim/未派发描述；不由QA PASS推断发布。**

以最新state和父任务明确派发证明为准，历史queue/config/工作副本空claim不得阻塞已被父任务独占派发的worker。本轮目前确实尚未派发，planner不得自行启动。

制作必须 GPT-6.1 Sol medium；独立QA由父任务新派 GPT-6 Luna xhigh，制作会话自检不能替代。读本目录README、queue/state/reference-policy和每项freeze/brief/config/references。

14,000三角形、1,000,000 GLB bytes是上限而非目标；通常约100–500KB，更小亦可，只为轮廓/比例/柔和衔接的可见收益增加面数，不以大贴图凑精细。≤6材质/≤30 primitives；最多一张≤256px原创贴图，编码总计≤65,536bytes、解码预算≤524,288bytes。自然精致、可信比例、适度卡通；通常80–240px、约480px中近景，非显微科考。

可靠基础形态来源和原创/实际授权素材足够即可合理风格化继续。既有source访问记录是继承历史，本轮没有重新读网页；不得伪造参考或把类群页当属级精确证明。未保存软组织、微观计数、颜色、真实尺寸和运动机制不需要反复研究返工。本轮Limnobiophyllum只作淡水岸边植物；波痕、贝壳灰岩和泥裂是地表/岩体过程概念，不伪称精确史前地点；珊瑚只需可靠基础辨识，不强加显微复原。

父任务正式派发后从届时最新main独立branch/worktree起步，隔离本批ID/revision/attempt，不能复制旧分支CI/site/release改动。脚本/work和候选目录见queue。默认协调池1worker×2threads；共享容量由父任务分配，三批不得各自占满主机。实际generator就绪后才生成完整inputs/outputs的runner manifest；本queue不是可执行manifest。

交付可编辑Blend、独立GLB、确定性generator/config与依赖哈希、中英metadata/事实标签/来源/许可/署名、可选原创贴图、透明封面、八固定QA视图(hero/reversehero/front/side/rear/top/clay/silhouette)及实际GLB多角度loader/功能渲染/多实例场景证据。零转台；真正问题才加针对性视图。源重开、两次语义重建、Khronos/project、预算与实际计量绑定精确GLB hash；软件渲染不冒充物理设备性能。

一次汇总独立QA、至多一次计划内外观修复；真正必需缺陷未解决交父任务裁决，不为不确定复原细节开无限循环。修复新revision/hash使旧受影响verdict失效。用户已授权QA通过分批push/merge无需逐模型审批，但仅父任务协调唯一release执行；本任务不自行发布、不上传Google Drive、不改权限、不强推。

| 精确ID | 原始中英名 | 目录 | 选择理由与基本形态 |
|---|---|---|---|
| `micrabacia` | Micrabacia radial-disc coral / Micrabacia（放射盘珊瑚） | `items/micrabacia/` | 自由扁盘与放射肋带来低平珊瑚轮廓，区别于丘状迷宫和深角杯。 小扁盘、明显放射肋和低中央杯有几何层次；不复制Choia长刺或海胆轮廓。肋数、微孔和软组织可简化。 |
| `sengelia` | Sengelia K-branching ground plant / Sengelia 匍匐早期植物 | `items/sengelia/` | 连续K形匍匐节点补充贴地早期植物，区别于直立轴丛和蕨类叶冠。 贴地连续K形分枝节点与少数抬高枝条方向可读；保持根生枝的基本关系。细根和重复节数可简化，不能只把旧裸轴植物旋转放倒。 |
| `coquina-outcrop` | Coquina outcrop / 贝壳灰岩露头 | `items/coquina-outcrop/` | 可见贝壳碎片构成多孔固结岩，增加岸边材质与结构差异，不重复层理崖或自然拱。 贝壳碎片嵌在连续固结岩基体中，孔隙有整体逻辑；选择几处可读断壳截面，不堆满松散完整贝壳或随机亮点。不是活动贝群、不命名碎壳物种。 |
| `naraoia` | Naraoia two-shield arthropod / Naraoia（双甲节肢动物） | `items/naraoia/` | 两块背甲下藏细足的小型底栖轮廓，区别于前轮封闭双瓣甲泳体。 前后两块平缓背甲与下方步足连贯，轮廓是背面双盾而非左右双瓣；足排少量可读，不把它做成现代蟹。细肢节数和软组织可经济简化。 |

新候选采用最新main的显式 `static-stylized-v1` profile（规则2026-10-18.1），机器字段 `publication_authority: separate`；用户批量发布授权另pin到profile-policy.json的policy。实际candidate生成后再用scripts/candidate_profile.py生成绑定真实hash的sidecar；不得预填假hash或称profile PASS。保留legacy错误，blockers用结构对象、criterion IDs与brief一致；模型QA PASS、candidate/profile PASS和发布状态分别记录。
