# 第二轮：12项可恢复规划，批次04–06

**只规划，尚未派发/领取。** 父任务确认 CI 完成于 main `643534830397824dfd46990485bd16ad66ecf9ce`；首轮批次01–03已由父任务独占派发。CI完成不等于授权本planning会话开始制作；本目录12项需父任务显式领取和派发，当前state没有owner/attempt/QA结果。

计划分支沿用 `planning/recoverable-small-life-12-20261018`，不合并main。独立轮次目录避免改写首轮12项冻结输入或碰撞首轮制作输出。

## 条目与分工

下表是原1000清单的已有稳定ID，不新增研究概念。完整原始中英名称、选择理由、尺度、预算和目录在queue.json；每项下有brief/config/references/inventory-record/freeze。

| 批次任务 | inventory ID | 精确原名 | 选择理由 | 计划目录 |
|---|---|---|---|---|
| [batch-04](batch-04-TASK.md) | `opabinia` | Opabinia five-eyed swimmer / Opabinia（五眼古生动物） | 五眼、单根长吻和侧叶形成游泳主体；区别于已有鱼、蟹、双瓣甲动物。 | `items/opabinia/` |
| [batch-04](batch-04-TASK.md) | `choia` | Choia radial-disc sponge / Choia（放射盘状海绵） | 扁盘与放射骨针丰富海底低矮层，不是海胆的球壳长刺变种。 | `items/choia/` |
| [batch-04](batch-04-TASK.md) | `meganeura` | Meganeura griffinfly / Meganeura（巨脉蜓类） | 四翼长腹部丰富飞行昆虫层，区别于宽翅蝶蛉和悬蝇；不是小型恐龙替代品。 | `items/meganeura/` |
| [batch-04](batch-04-TASK.md) | `cooksonia` | Cooksonia sporangial shoots / Cooksonia 裸轴植物 | 末端囊与简单叉枝形成稀疏低矮植物，区别于首轮根茎拱与叶丛。 | `items/cooksonia/` |
| [batch-05](batch-05-TASK.md) | `marrella` | Marrella fork-spined arthropod / Marrella（叉棘节肢动物） | 头盾双组长棘和细分节躯干形成新的小型底栖轮廓。 | `items/marrella/` |
| [batch-05](batch-05-TASK.md) | `proteroctopus` | Proteroctopus finned octopod / Proteroctopus（有鳍八腕动物） | 柔软外套膜、成对鳍和八腕补充海生软体动物，避免全是硬甲。 | `items/proteroctopus/` |
| [batch-05](batch-05-TASK.md) | `mongolarachne` | Mongolarachne Jurassic long-legged spider / Mongolarachne（侏罗纪长足蜘蛛） | 双体节和八条长足补充陆地蛛形纲，不能标成昆虫或六足虫。 | `items/mongolarachne/` |
| [batch-05](batch-05-TASK.md) | `salvinia` | Salvinia paired floats and submerged leaf / Salvinia 槐叶萍类水蕨 | 成对浮叶和水下沉叶丰富水面；结构上区别于首轮有根羽状 Hydropteris。 | `items/salvinia/` |
| [batch-06](batch-06-TASK.md) | `hallucigenia` | Hallucigenia spiny lobopodian / Hallucigenia（背棘叶足动物） | 细长体、背棘和软足形成低位行走生物，与硬壳蟹和海星不同。 | `items/hallucigenia/` |
| [batch-06](batch-06-TASK.md) | `fenestella` | Fenestella windowed fan bryozoan / Fenestella（窗格扇苔藓动物） | 开窗网格扇形增加海底竖向背景，区别于海绵盘和分枝腕动物；是苔藓动物而非植物。 | `items/fenestella/` |
| [batch-06](batch-06-TASK.md) | `leclercqia` | Leclercqia divided-leaf shoot / Leclercqia 裂叶石松类植物 | 裂叶单元和弯曲中央叶尖补充小型叶生石松层，不重复裸轴植物或大树冠。 | `items/leclercqia/` |
| [batch-06](batch-06-TASK.md) | `montsechia` | Montsechia flexible fine-leaf shoots / Montsechia 水生早期被子植物 | 柔软细叶水生枝与成对果实丰富水下层，区别于浮生水蕨。 | `items/montsechia/` |

输出为 `assets/candidates/continuous-small-life-round02-20261018/<batch>/<ID>/r001/`；脚本/执行记录为本目录 `work/<batch>/<ID>/r001/`；通过QA后由父任务整合到 `assets/additions/<ID>/continuous-small-life-v1/`。各任务文件列出完整本批条目与约束，可直接派发。

四种植物分别是末端囊裸轴、成对浮叶/沉水叶、分裂叶石松枝和细叶带果水生枝，结构不同，不以冠密度或色彩变体凑数量。蜘蛛属于蛛形纲，Fenestella属于苔藓动物，不错误归为昆虫或植物。Meganeura名义翼展是0.65m的美术起点；不把“巨脉”标签或尺寸当成新的化石测量。批次为制作分工，不声明同地点同时代共存；海底/水面/水下/陆地/飞行层分场景使用。

## 去重与参考边界

`dedup-snapshot.json` 保存本次所有抓取分支SHA、所选ID模型/生成器路径扫描和已提交发布描述符哈希。首轮12项全部排除，并记录父任务实际制作线程；已发布十六项、鱼蟹候选Dapedium/Callichimaera、获准发布的Diplomystus/Burgessomedusa/Kalligramma也排除。当前main除CI变更外发布描述符保持原有范围；不宣称线上部署重新验收。所有选中ID都在真实inventory中为reference-ready/direct，但此规划不是新来源核验或模型QA。

远端没有发现本轮ID的.blend/.glb或按ID命名的生成器；共享生成器函数、未推送工作和其他实时会话仍须父任务领取前统一核对。路径扫描不是全局任务锁，不可自发认领。

参考按inventory原字段逐字保留在inventory-record.json，来源入口、支持范围和历史访问方式列入references.json。本轮没有重新打开外部页面，不把继承的opened/search-result说成这次新核验。可靠基础参考能支撑辨识形态、模型/贴图原创或有实际授权，即可在领取后继续，不要求精确微观、物种/产地/共存、软组织或运动机制复原。不得伪造来源或事实PASS。

两项特别注意：Proteroctopus现有来源仅承诺Coleoidea类群/所述标本，适合支撑基本有鳍八腕教学造型，不证明全部属级形态；Fenestella来源支持开窗群体形态，不证明属级微观鉴别。使用受其启发的描述性标签，若要新增属级精确断言才补对应真实证据；不因此开启严格复原研究循环。Salvinia下垂结构称沉水叶而非真根；Montsechia无支持不加根；Hallucigenia不采用历史倒置朝向。以上是待执行的美术/标签约束，不是本轮重新验证的事实结论。

查阅参考并原创建模不涉及复制图片/扫描的再分发权。consulted-only不是开放许可；不打包来源媒体、扫描或第三方网格，确需收录先记录真实使用授权。保留来源URL、访问方式、支持范围、署名及不确定性。

## 同一制作和QA标准

制作必须 **GPT-6.1 Sol medium**；独立QA由父任务新任务派 **GPT-6 Luna xhigh**，制作自查不能替代。沿用已认可v002提交 `c8514b8c348777c9a2d81c6c0bbd9cf02cdb5184` 的自然精致、可信比例、柔和衔接风格；适度卡通、儿童场景正常与中近距离可看，不以面数论质量。

- 每项14,000三角形、1,000,000GLB bytes为硬上限而非目标；通常约100–500KB，更小同样可。只为可见轮廓/比例/衔接收益增加面数，超过通常区间但在硬上限内记录具体收益即可。
- ≤6材质、≤30 primitives；最多一张≤256px原创贴图，总编码≤65,536 bytes、解码预算≤524,288 bytes，不用大贴图凑精细。源顶点/求值顶点/导出POSITION-stream顶点、三角形、GLB字节、解码估算和场景实例分别报告；不凭面数承诺性能。
- 可编辑Blend、独立GLB、确定性生成脚本/参数/依赖哈希、中英metadata和出处/许可/署名、透明封面；八个固定QA视图及实际GLB多角度运行时证据；零转台序列，有实际问题才加针对性视图。
- 源重开、两次语义重建、Khronos/project检查、目标loader、功能渲染和简化多实例场景记录均绑定精确GLB哈希。软件图形运行时不冒充真实设备性能，模型不得标为动画就绪。
- 一次汇总独立QA、至多一次计划内外观修复；真实必需缺陷未解决交父任务决定，不为不确定的微观复原反复返工。修改模型的新hash使旧受影响verdict失效。

父任务已授权通过QA后分批直接推送/合并，无需逐模型审批；整合发布由父任务串行协调。本planner不生产、不发布、不合main、不上传Google Drive、不改权限、不强推，提交署名Leon Made This <8357465+s010s@users.noreply.github.com>。

## 恢复与领取

运行 `python3 production/continuous-small-life-round02-20261018/verify_plan.py` 只检查规划一致性。完整恢复/不可变attempt/runner契约见[首轮流程](../continuous-small-life-20261018/README.md)和仓库[队列契约](../../skills/blender-lowpoly-pipeline/references/parallel-queue.md)。队列不是可执行runner manifest，不含虚构的generator路径。

父任务先fetch最新main/候选/制作分支、检查实时claim，再把实际thread、owner、分支、基准SHA、领取时间（未知则只记观察时间）写入本轮state并追加events，然后派发04–06。没有owner不等于任何maker可以抢占。state/events为动态真相，queue为初始快照；父任务串行合并状态，正常push冲突就fetch/reconcile，禁止force。未完成attempt/缺文件/不同输入工具配置或输出hash不能复用为成功。

实际制作从届时最新main独立worktree/branch起步，仅携带本目录和必要依赖，避免整体挑入旧分支的站点/CI/release变更。build/preview/render分lane，默认共享协调池1worker×2threads；资源额度经父任务分配，三批不能各自占满主机。实际generator出现后才生成含全部语义inputs、必需outputs、timeout等的runner manifest，用--resume验证完整输出hash后复用。

规划输入由freeze和checksums锁定；若改brief/config/reference/policy，提升版本、重算freeze/checksums再提交。动态state/events单独由Git追踪，不混入静态哈希。保留失败日志，新的attempt/revision隔离输出。
