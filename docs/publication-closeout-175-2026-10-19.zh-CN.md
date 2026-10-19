# 37–39 批发布收尾：175 模型

本任务已完成并停止。仅发布 batches 37–39，163 → 175；不领取第 40 批或任何后续批次。

生产 main：`de413ef720463a2999516faf92c606bcdf9ab1b7`。PR #19，最终 PR 头：`c0cc3e6726b62076cd4d16d37f9bc0b107520b8b`。普通合并与普通推送，作者和提交者均为 `Leon Made This <8357465+s010s@users.noreply.github.com>`；无强推、远端删除或权限变更，未使用 Drive 或用户 Mac。

该精确 main 的工作流全部成功：

- [资产管线](https://github.com/s010s/lowpoly-vault/actions/runs/39192836357)：17 套发布拒绝回归及发布清单通过。
- [相关审查](https://github.com/s010s/lowpoly-vault/actions/runs/39192836340)：18/18。
- [构建、Pages 与真实公网](https://github.com/s010s/lowpoly-vault/actions/runs/39192836362)：构建、部署、实际公网验收全部通过。
- [实际公网验收证据](https://github.com/s010s/lowpoly-vault/actions/runs/39192836362/artifacts/12161600281)：24/24 用例、24 条双语详情路由、浏览器和资源错误均为 0；公网 payload 精确匹配 175 件，20 份硬件限制声明保留。

实际公网报告和索引持久化于本交接分支：`qa/publication175-closeout-20261019/actual-public-report.json` 与 `evidence-index.json`。交接分支不触发部署；生产 main 保持上述精确提交。

最终 PR 构建作业 767 秒；main 构建作业 774 秒、资产管线作业 576 秒、Pages 部署 15 秒、真实公网验收 108 秒。整体收尾约 50 分钟，包含准备、既有门禁等待与一次作业超时修复。

## 精确冻结来源

|批次|最终来源|最终独立 QA|
|---|---|---|
|37|`4642f57de8be861e2e9ecc44f05167424e7e7973`|`8b0963c5a8b2f40b8824d31ff338384e6f673fab`|
|38|`70abb5ec41aadd31d56ac9f0d1890ad708afc6da`|`e3cacea1e54a57b665b0d0ea3c7f966f0e4b690a`|
|39|`aac9a3c9085136469f816862b0c2a4139fc4eb3c`|`bcbd042dd325d209133c3726e71e6f7a588c7090`|

aa-lava-front 使用 r002 候选 `1a65d88bd1fe81d0df3211b61235a150d71caa8d`，GLB SHA-256 `7960936e5ee17c46db8cd3d5658705ef04643a665ebfe5305e16a2bdefeb243c`。最终差异 QA 解除 B39-AA-01，其他三件原决定不变。独立模型 QA 沿用已有证据，没有再做完整模型验收。

438 项交接哈希核对无差异，1752 个来源及 QA 文件冻结。旧 163 条模型记录与 652 份旧 GLB／Blend／预览／正式海报文件字节不变。12 张新图由锁定 Chromium 141 捕获，CI 精确复现零差异；12 模型软件 WebGL 场景绘制 62336 三角形，与预期一致，GL 错误 0。未改 UI 行为。

正式 profile 保持 `static-stylized-v1` / `2026-10-18.1`，采用单独用户授权的网站发布政策；所有候选原审批为 false，formal/hardware acceptance 继续 BLOCKED。SwiftShader 只证明软件 WebGL 功能，未做实体 GPU 或设备性能验证。科学范围、参考访问限制、旧 checker 失败与不确定性原样保留。

必要 CI 修复仅把资产管线作业时限 10 → 20 分钟：原作业到 10 分钟时在最后 round13 回归被取消，之前回归均通过。未删除测试或断言。捕获早期缺少被 gitignore 忽略的冻结日志，已普通提交补齐；完整来源门禁随后通过。main 首次普通推送认证失败，普通重试成功，未使用强推。

最终无在途生产部署。停止本任务，不继续队列。
