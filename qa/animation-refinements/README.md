# 动画改进交付 / 2026-10-18

后续确切 CI 发现并修复了中文 opening dissolve 慢帧回归。原始记录保留；最新技术说明、独立审查与短录屏请看 [CI 修复说明](ci-regression.md)、[独立 review](independent-review.md)、[约 14 秒操作录屏](selected/animation-walkthrough.mp4)。新提交的 CI 必须按其确切 head 检查，不能把下方旧版本本地通过结果当作 CI 全绿。

云端 `/workspace/lowpoly-vault` 完成；未使用用户 Mac。同步后 main 为 `77720858d73fcb8f6b8845576851762dcba078ef`。独立分支 `codex/animation-refinements-20261018`，实现提交 `ebce4e7f0155982d49f87b41d2792061fd9a4690`。实际发布清单为 16 个模型，原有模型与 GLB/Blend/海报字节未改变。

已按官方 find-animation-opportunities → animate → review-animations 完成三个阶段，读取各自 SKILL.md、RECIPES.md 与 STANDARDS.md。固定官方版本 `2d228630ba1446365f614a108cb8252f1feda202`，原文与 MIT 许可保存在 `.agents/skills/emil-animation/`，第三方声明已补充。

移除重复筛选的 460ms 入场、最多 240ms 错峰、100ms 等待式退场、280ms 重排，以及全局点击的 180ms 重复回弹。列表随数据立即更新，保留最新查询胜出。所有现有 CSS hover 都区分精细指针，焦点与选中样式保留。新动画仅为 Refine 原生 details 的 160ms 轻量出现/消失、成功复制后的小勾反馈；CSS 过渡可打断，键盘和 reduced motion 即时。原有单实例 Three.js、140ms hover reveal、弹窗/返回/历史中断连续性保留；没有恢复序列帧或添加第二渲染器。Related 保持原样。

## 验证结果

| 检查 | 结果 | 证据 |
| --- | --- | --- |
| `SITE_BASE=/lowpoly-vault/ npm run build` | 通过；415 项发布白名单，16 组模型、源文件和 ZIP 字节一致 | selected/build.txt |
| `npm test` | 通过；manifest、catalog、theme、Python 管线、资源生命周期、return/hover 等 | selected/unit.txt |
| `npm run test:redesign`、`npm run test:publication` | 通过 | selected/unit.txt |
| 新增 `npm run test:interaction:browser` | 8/8 通过：Refine 快速反转、键盘/指针区分、快速筛选排序搜索、剪贴板成功/重复/失败、reduced motion、移动无黏滞 hover、中文深色主题/动态 reduced motion、原生降级 | selected/interaction-report.json |
| `npm run test:hover:browser` | 4/4 通过：冷/热加载、离开重进/快速切换、reduced motion、失败海报 | selected/hover-report.json |
| `npm run test:modal:browser` | 8/8 通过：中英文、桌面/移动、键盘/reduced motion、打开关闭中断、Back/Forward、直接路由 | selected/modal-summary.json |
| `GALLERY_DIR=dist npm run test:redesign:browser` | 通过；16 个真实模型、38 个静态路由、一万条元数据、417 页、24 张卡 DOM 上限、一次渲染器创建、单 GLB 通道 | selected/redesign-report.json |
| `npm run test:handoff:browser` | 10/10 通过；真实像素、透明度、几何/海报连续性、不同分辨率/主题/移动/reduced motion、中断和 WebGL 恢复 | selected/handoff-summary.json |
| `npm run test:preview:browser` | **16/17 通过，整体失败**：原 `trusted-touch-swipe-and-tap` 的手势后快速缩放没有收到 click | selected/shared-report.json |
| 同一触摸失败基线复现 | **未修改 main 也失败**；禁用新增按压效果仍失败。另允许手势间隔 400ms 的诊断通过全部相机/返回/后续手势断言 | selected/touch-*-report.json、diagnostics/ |

弹窗测试沿用仓库既有的返回时延 advisory 例外，原 120/180ms 目标及超时测量保留，没有修改测试或放宽阈值。8/8 功能通过不等于所有名义时延达标。

首轮新增移动测试错误地要求触屏隐藏静态箭头，失败记录在 diagnostics/initial-mobile-affordance-assertion.json；改为检查 hover 前后静态可见度不变后通过，没有为通过测试隐藏移动操作提示。改版浏览器首次因默认 review 构建目录不存在而未启动，设置 GALLERY_DIR=dist 后完整通过。安装首次因 npm 默认缓存目录不可写而失败，改用可写 `/workspace/.npm-cache`，只安装锁文件依赖并禁用 lifecycle scripts；无全局安装、无绕过权限审批。录屏复用现有 `/usr/bin/ffmpeg`，无额外下载。

## 环境与复现

Chromium **154.0.8037.57**、Linux、ANGLE SwiftShader 软件 WebGL，Node **24.19.0**、npm **11.9.0**。这些是实际浏览器渲染/输入和仿真移动视口，不是物理手机性能或生产网络测量。Safari、Firefox、真实 iOS/Android 和独立人工视觉签核**未跑**。原触摸快速缩放失败仍需后续处理，未修改产品代码掩盖它。

```sh
npm ci --ignore-scripts --cache /workspace/.npm-cache
SITE_BASE=/lowpoly-vault/ npm run build
npm test
npm run test:redesign
npm run test:publication
CHROMIUM_PATH=/usr/bin/chromium npm run test:interaction:browser
CHROMIUM_PATH=/usr/bin/chromium npm run test:hover:browser
CHROMIUM_PATH=/usr/bin/chromium PLAYWRIGHT_BROWSERS_PATH=/workspace/playwright-browsers npm run test:preview:browser
CHROMIUM_PATH=/usr/bin/chromium PLAYWRIGHT_BROWSERS_PATH=/workspace/playwright-browsers npm run test:modal:browser
CHROMIUM_PATH=/usr/bin/chromium PLAYWRIGHT_BROWSERS_PATH=/workspace/playwright-browsers npm run test:handoff:browser
CHROMIUM_PATH=/usr/bin/chromium GALLERY_DIR=dist npm run test:redesign:browser
```

此云端 Playwright 录屏使用 `/workspace/playwright-browsers/ffmpeg-1011/ffmpeg-linux` 指向已安装的 `/usr/bin/ffmpeg`；其他环境应使用其已经批准安装的 Playwright 录屏依赖。

## 证据与恢复

`selected/` 包含可直接审查的原始报告、8 张新增交互截图、基线与连续性截图、3 段真实录屏和测试日志。`source-sha256.json` 将测试树绑定到实现提交；部分原测试没有提供 commit 环境变量，原始报告按原样保留，由校验值文件补充来源。完整 raw JSON、全部截图/录屏和失败诊断将包含在恢复归档中。请勿把本地目录视作已完成外部备份；外部备份链接和校验在最终交付中单独给出。

恢复归档提供 main 前置提交以上的 Git bundle、逐提交 patch、分支树 tar 和测试说明。bundle 是增量，需从仓库取得上述 main 基线；source tree tar 可在没有 Git 历史时直接恢复文件。阶段提交均使用 `Leon Made This <8357465+s010s@users.noreply.github.com>`，无强推、删远端、合并或部署。PR 只创建 draft。
