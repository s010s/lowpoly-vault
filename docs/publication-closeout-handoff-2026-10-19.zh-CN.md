# 发布任务收尾与后续队列交接

最后更新：2026-10-19 UTC。用户要求结束持续领取批次：本任务只完成已经启动的 PR #17（31–33 批，139 → 151）及其 CI、Pages 和真实线上验证，随后结束。不得从本队列自动领取下一批，不再重复 CI 优化。后续批量发布由独立任务承接。

## 已完成的原始工作

- 初始 main 已核实为 `0d22f06124a8dbac40ca7e0e4570aa44659dc3d2`。
- CI 精简已在 PR #2 合并，main `643534830397824dfd46990485bd16ad66ecf9ce`；当时 PR/主线常规构建实测 98/102 秒。构建、交付完整性、关键交互及缩略图到真实 3D 烟测保留；完整模型、语言/主题/视口矩阵、精确重渲染按相关变更或手动运行。未修改仓库保护或权限，未通过删除失败断言掩盖问题。
- 已认可的三模型 v002 在 PR #3 合并发布，main `12550349a9678398b9360e97d7908bc42667c42c`。Diplomystus/Burgessomedusa/Kalligramma GLB 分别 93752/122504/150456 字节，实际线上 6/6 验收通过。
- PR #1 动画改动说明和现有录屏见 [动画说明](animation-pr1-changes.zh-CN.md)，没有为说明新增动效。

## 当前收尾边界

已确认生产：**139 模型**，main `a82524f654035556bb938419c843ada481713027`，PR #16。PR/主线构建实测 **438/453 秒**，完整审查25/25通过，实际线上24/24与24条双语详情路由通过，部署清单精确匹配该 SHA，错误为0。

线上证据：[139 实际 Pages Chromium 验收](https://github.com/s010s/lowpoly-vault/actions/runs/39182435069/artifacts/12157490367)。

当前已启动、须完成后停止： [PR #17](https://github.com/s010s/lowpoly-vault/pull/17)，分支 `capture/small-life-round11-20261018`，头 `7b69ca4c587251a39785782330e0207183e39425`，目标151。1,320项声明哈希与875个来源/QA文件已核验，旧139保持一致。新增门禁38项、本地15套强制发布检查共518项、24个桌面/触屏用例与308条静态路由均通过。软件 WebGL 场景83,632三角形与预期一致，GL错误0。相关CI审查16/16已通过；保存本文件时常规CI已进入构建，尚未合并/部署/验收151，不能把本地浏览器结果称为线上验收。

PR CI：常规发布 `39183925160`；资产管线 `39183925201`；相关审查 `39183925207`。正式图捕获 `39183556383`，Chromium141.0.7390.37，源图哈希/字节均核验；新增12图精确复现零差异。旧139图此前在生产main完成全量复现并且本轮字节不变。

## 精确来源与 QA 清单

| 批次 | 状态 | 来源分支与精确提交 | 独立 QA 分支与精确提交 |
|---|---|---|---|
|31|已启动，属于PR17收尾；勿重复发布|`candidate/small-life-batch31-20261018` @ `b94453827c90ed71df0087017a48701477944f35`|`qa/independent-small-life-batch31-20261018` @ `ba33ae2cbd93fc65e423f76ec252f6e66883ce67`|
|32|已启动，属于PR17收尾；勿重复发布|`handoff/batch32-20261018` @ `5d2cfac309a28b05a1f213d69f79938081c8bbdc`|`qa/independent-batch32-20261019` @ `bf753fe39eb630759ff6596488117fed8f9e1a20`|
|33|已启动，属于PR17收尾；勿重复发布|`candidate/small-life-batch33-20261018` @ `1156d5a59362fbc191f217fdacf0dd051b58f95c`|`qa/independent-batch33-20261019` @ `f8559b952c68bcadccdac3a6b4596033a2dd7f07`|
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
