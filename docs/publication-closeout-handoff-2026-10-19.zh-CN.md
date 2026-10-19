# 发布任务收尾与后续队列交接

最后更新：2026-10-19 UTC。用户要求结束持续领取批次：本任务只完成已经启动的 PR #17（31–33 批，139 → 151）及其 CI、Pages 和真实线上验证，随后结束。不得从本队列自动领取下一批，不再重复 CI 优化。后续批量发布由独立任务承接。

## 已完成的原始工作

- 初始 main 已核实为 `0d22f06124a8dbac40ca7e0e4570aa44659dc3d2`。
- CI 精简已在 PR #2 合并，main `643534830397824dfd46990485bd16ad66ecf9ce`；当时 PR/主线常规构建实测 98/102 秒。构建、交付完整性、关键交互及缩略图到真实 3D 烟测保留；完整模型、语言/主题/视口矩阵、精确重渲染按相关变更或手动运行。未修改仓库保护或权限，未通过删除失败断言掩盖问题。
- 已认可的三模型 v002 在 PR #3 合并发布，main `12550349a9678398b9360e97d7908bc42667c42c`。Diplomystus/Burgessomedusa/Kalligramma GLB 分别 93752/122504/150456 字节，实际线上 6/6 验收通过。
- PR #1 动画改动说明和现有录屏见 [动画说明](animation-pr1-changes.zh-CN.md)，没有为说明新增动效。

## 最终结果：本任务已经结束

**151 模型已正式上线并完成真实线上验收。** 最终 main `2f0a90f833e2607963ec33e5fd4647a8506e1bee`，PR #17，PR头 `7b69ca4c587251a39785782330e0207183e39425`。远端与本地提交一致，署名为 `Leon Made This <8357465+s010s@users.noreply.github.com>`。

- PR常规构建589秒，主线构建412秒。PR分阶段耗时见证据目录；其中约388秒属于15套强制发布拒绝回归，与早期串行浏览器审查并非同一耗时来源。
- 主线三套工作流全部成功：资产管线 `39184763524`、Pages `39184763555`、相关审查 `39184763563`（16/16）。这些是在收尾要求前已启动的工作流；恢复后没有追加完整模型验收或重新运行已完成步骤。
- 实际网站Chromium验收24/24用例和24条双语详情路由通过，部署清单精确匹配最终SHA。目录、独立详情、GLB/Blend/ZIP下载、署名与预览通过，浏览器/资源错误均为0。
- [实际Pages验收证据](https://github.com/s010s/lowpoly-vault/actions/runs/39184763555/artifacts/12158255336)；完整报告已保存为 `qa/publication-closeout-20261019/151-actual-public-report.json`。
- 四项旧硬件限制继续为 `formal_profile_acceptance: BLOCKED`、`hardware_gpu_verified: false`，没有实体GPU性能声明。
- 本轮版本绑定核验1,320项声明哈希、875个来源/独立QA文件；旧139资产及正式图字节保持不变。既有独立QA均通过，无必修项；未改写原始审批状态或科学/来源范围。
- 本轮此前已完成的本地证据：15套发布回归518项，24个桌面/触屏用例、308静态路由，12模型软件WebGL场景83,632三角形与预期一致，GL错误0。正式图锁定Chromium141捕获，新12图复现零差异；旧139此前已经完成全量复现且本轮未变。这些本地结果与实际线上结果明确分开。

**停止边界：不再领取34–36，不再重复CI优化。** 后续批量发布由独立任务承接。最新用户明确已有独立QA，后续恢复只做版本绑定和必要上线检查，不因本交接文件自动追加父任务/发布者的完整模型验收。

先前139生产版本为 `a82524f654035556bb938419c843ada481713027`，PR16，构建438/453秒，实际线上24/24通过：[139证据](https://github.com/s010s/lowpoly-vault/actions/runs/39182435069/artifacts/12157490367)。31–33已包含在151，勿重复发布。

持久化证据：[证据索引](../qa/publication-closeout-20261019/evidence-index.json)、[待发布队列JSON](../qa/publication-closeout-20261019/pending-batches.json)。本地已经生成的40份最终批次截图/报告及PR分阶段耗时已推送保存；没有未推送的已跟踪代码改动。历史无关生成目录仍保留原工作区，未清理或误提交。

## 精确来源与 QA 清单

| 批次 | 状态 | 来源分支与精确提交 | 独立 QA 分支与精确提交 |
|---|---|---|---|
|31|已发布并验收，属于151；勿重复发布|`candidate/small-life-batch31-20261018` @ `b94453827c90ed71df0087017a48701477944f35`|`qa/independent-small-life-batch31-20261018` @ `ba33ae2cbd93fc65e423f76ec252f6e66883ce67`|
|32|已发布并验收，属于151；勿重复发布|`handoff/batch32-20261018` @ `5d2cfac309a28b05a1f213d69f79938081c8bbdc`|`qa/independent-batch32-20261019` @ `bf753fe39eb630759ff6596488117fed8f9e1a20`|
|33|已发布并验收，属于151；勿重复发布|`candidate/small-life-batch33-20261018` @ `1156d5a59362fbc191f217fdacf0dd051b58f95c`|`qa/independent-batch33-20261019` @ `f8559b952c68bcadccdac3a6b4596033a2dd7f07`|
|34|仅登记，四件PASS无必修，未启动整合|`handoff/batch34-20261018` @ `5284d5574d5088a8f6ee887b391fa4988cbd9bf1`|`qa/batch34-independent-review-20261019` @ `e04430b0a8c4056040169410f7787a5da1cb2434`|
|35|仅登记，四件PASS无必修，未启动整合|`candidate/small-life-batch35-20261018` @ `9a64871c3fda8f791f84c8ed3d66c181aca87e20`|`qa/independent-batch35-20261019` @ `56fd3af8bb727a980384f05c687217403d0f47cc`|
|36|尚未齐备，未启动整合|制作模型容量失败，按原配置重试；尚无可交接的最终来源SHA，不能猜测|尚未提供最终QA分支/SHA|

31模型：asaphus、hazelia、sea-cave、cruziana-crawling-furrow。32：ctenocystis、baculites、estuary-basin、cross-bedded-sandstone。33：mucrospirifer、wave-cut-platform、flute-cast-slab、paleodictyon-mesh-trace。

34认证失败已普通重试成功。34/35的远端SHA与并非仅本地产物，由父任务核实并通知；本发布者只登记，未导入它们的模型。34–36须后续独立任务在齐备后重新核对来源及QA范围，勿自动从本文件触发发布。

## 必须保留的证据边界与操作约束

- 只导入最终模型与相关冻结证据，不合并候选分支的无关实现。
- 候选审批仍为false；独立QA通过不改写原始阶段、阻塞、旧验证失败或来源限制。采用既有 `static-stylized-v1` / `2026-10-18.1` 与单独授权的网站发布政策；不降低规则或放宽断言。
- 软件SwiftShader WebGL证明功能，不证明实体GPU或设备性能。旧27批的 sollasina、ottoia、eocladus、limestone-pavement 必须继续 `formal_profile_acceptance: BLOCKED` 且 `hardware_gpu_verified: false`；线上验收检查完整四份声明。
- 风格化启发教学美术不等于严格科学标本复原。参考访问限制、needs-specific-reference、非同域共存及非实际博物馆集成范围原样保留。
- 正式缩略图须由锁定的Playwright Chromium生成。云端只能运行本地Chromium154，不能冒充141的规范生成；已有 `publication-poster-capture.yml` 是只读捕获入口，不是部署或门禁绕过。日志分块传输须核验源GLB、浏览器版本、长度与SHA；新图最后仍需精确复现。
- 署名：`Leon Made This <8357465+s010s@users.noreply.github.com>`。仅普通推送，禁止强推、删除远端分支或修改仓库保护/权限。不要上传Google Drive。
- 收尾后不再领取34–36，不再以本任务继续无限发布。当前工作区仍保留历史和本轮生成QA文件；不要清理或误提交无关生成目录。
