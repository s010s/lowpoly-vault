<div align="center">

# Lowpoly Vault

**原创 low-poly 资产，构建更多世界。**

使用 Blender 制作 · 可编辑、可复用、可再创作

[浏览资产](#浏览资产) · [格式与流程](#格式与流程) · [许可](#许可与署名) · [English](README.md)

</div>

Lowpoly Vault 是 **Leon Made This / [s010s](https://github.com/s010s)** 持续创作的风格化 3D 资产库。从日常物件、自然景观，到未来、幻想与外星世界，不受单一主题限制。

> **制作中。** 资产、导出文件与浏览体验正在建设。以下展示预期组织方式；完整资产版本与在线展厅尚未开放。

## 格式与流程

| 编辑 | 使用 | 浏览 |
| :--- | :--- | :--- |
| 可编辑的 **Blender** 源文件 | 通用 **GLB** 导出文件 | **PNG** 预览图与分类 **Web 3D** 展厅 |
| 修改几何、材质与构图 | 导入实时场景 | 按主题与类别寻找资产 |

可重现脚本与可复用 Skills 将记录从建模到导出的制作过程。展厅计划使用 GitHub Pages 托管，部署验证后再补充链接。

**选择主题 → 寻找资产 → 编辑或导入 → 标注署名。**

## 浏览资产

每个主题的说明与资产文件放在一起，各主题可独立扩展，共用统一的组织方式。

| 主题 | 范围 | 状态 |
| :--- | :--- | :--- |
| [史前环境](assets/prehistoric/README.zh-CN.md) | 地形、植物与环境细节 | 制作中 |

新的主题会随着制作进展加入这里。

## 目录结构

资产按**主题 → 粗分类 → 资产标识**组织。以下为目标结构，不代表所有文件已经发布：

```text
assets/
├── manifest.json                 # 所有主题共用的总目录
└── <theme>/
    ├── README.md                 # 主题范围与说明
    ├── README.zh-CN.md
    └── <category>/
        └── <slug>/
            ├── <slug>.blend      # 可编辑 Blender 源文件
            ├── <slug>.glb        # 实时模型
            └── preview-hero.png       # 预览图
```

总资产目录统一放在 `assets/manifest.json`。相关资产按粗分类归置，主题背景与使用边界写在各主题自己的 README 中。

## 许可与署名

不同内容适用不同许可：

- **[CC BY 4.0](LICENSES/CC-BY-4.0.txt)**：原创模型、渲染、图片、资产元数据、文档与 Skills 说明文字
- **[MIT](LICENSES/MIT.txt)**：原创建模与导出脚本、网页代码、工作流、配置代码、Skills 可执行脚本及文档中的代码示例
- **第三方内容**：保留各自许可证

分享 CC BY 4.0 内容时，请署名 **Leon Made This / s010s**，链接到来源与许可，并说明修改。分发 MIT 代码时须保留版权与许可声明。详细范围见 [LICENSE](LICENSE)，资产署名示例见 [ATTRIBUTION.md](ATTRIBUTION.md)。

## 图库改版预览

改版分支保留十个原创候选模型，尚未作为正式版本发布或通过最终验收。世界主题、多对多组合包与跨世界分类已分开；现有模型 ID 和文件路径保持兼容。全局检索默认使用紧凑网格，地图只用于选中的真实小组合包（最多 30 个模型）。规划中的资产不会进入线上数量或搜索建议。

英文 `/models/<id>/` 与中文 `/zh-CN/models/<id>/` 是实际生成的静态 HTML 页面。即使 JavaScript 不可用，也可阅读描述、预览、署名和下载。列表普通点击增强为弹窗，保留搜索、筛选、排序、分页与返回状态。ZIP 下载包含 GLB、Blender 源文件和 CREDITS.txt；文件大小来自实际字节数。

测试：`npm run test:redesign`。预览构建：`SITE_BASE=/lowpoly-vault/ node site/prepare-review.mjs`。浏览器验收：`node site/redesign-browser-test.mjs`。发布复制器只按获批 manifest 的明确文件清单工作；没有获批 manifest 时，不复制模型二进制文件到正式输出。详见[构建说明](docs/static-catalog-build-v2.md)、[架构合同](docs/catalog-schema-v2.md)和[改版清单](docs/redesign-v2-checklist.md)。

[三模型预览实验](experiments/preview-turntable-v3/README.md)保留原始几何与尺度。当前实测支持静态卡片加按需 GLB，暂不集成 16 帧 sprite。CPU 解码代理、云浏览器降级截图与真实 WebGL、触摸设备验收分别记录，不互相替代。
