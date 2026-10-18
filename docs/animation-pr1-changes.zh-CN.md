# PR #1 动画改动：代码对应的前后变化

- 筛选卡片：原 `GalleryMotion` 每次筛选/排序会等待 100ms 退场，再做 460ms 入场（最多 240ms 错峰）或 280ms 重排。现在移除这些高频列表动效，数据到达立即更新，保留“最新查询胜出”。
- 点击反馈：原来全局 click 会播放 180ms 的 1 → .96 → 1 回弹，键盘触发也会播放。现在只在真实指针按下时设置 `data-pointer-pressed`，CSS 压至 .97；松开、取消或失焦清除，键盘不回弹。
- 筛选面板：原生 details 原来即时开关；现在支持 `::details-content` 的浏览器从触发点右上角以 160ms opacity/transform 过渡，可从当前状态反向。关闭立即 inert，Escape 恢复焦点；键盘、减少动态效果与不支持增强的浏览器保持即时原生操作。
- 复制反馈：原来成功只替换按钮文字。现在仅在 clipboard 写入成功后显示文字与 160ms 小勾，重复复制复用同一节点；失败会清除成功状态并播报不可用。键盘和减少动态效果即时反馈。
- 慢帧交接：原来两条独立 WAAPI 淡变可能在主线程卡顿后直接到终点，跳过可见中间混合。现在 `startHandoffDissolve` 用同一 160ms 时钟控制互补权重；即使首帧延迟 1000ms，也先留一次 .5/.5 的真实绘制机会，再追上墙钟终点。取消、隐藏、减少动态效果会清理或立即完成，避免滞留遮罩。

代码：`site/main.js`、`site/motion.js`、`site/style.css`、`site/handoff-dissolve.js`。现有约 14 秒真实浏览器录屏：[animation-walkthrough.mp4](../qa/animation-refinements/selected/animation-walkthrough.mp4)；没有为本说明新增动效。旧 Chromium154 触摸诊断失败仍保留，未通过删除断言掩盖。
